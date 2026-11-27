
from pathlib import Path
import json
import random
import time

import numpy as np
import pandas as pd
import torch  # pyright: ignore[reportMissingImports]
from torch import nn
from torch.utils.data import Dataset, DataLoader
from PIL import Image

from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight

import matplotlib.pyplot as plt


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"

MODEL_NAME = "facebook/deit-tiny-patch16-224"

MODEL_DIR = PROJECT_ROOT / "models" / "terraspectra_deit_tiny_best"

REPORT_DIR = PROJECT_ROOT / "reports"

TRAIN_CSV = SPLIT_DIR / "train.csv"
VAL_CSV = SPLIT_DIR / "validation.csv"

SEED = 42
BATCH_SIZE = 8
EPOCHS = 12
LEARNING_RATE = 5e-4
PATIENCE = 3

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]

LABEL_TO_ID = {
    "black rot": 0,
    "esca": 1,
    "healthy": 2,
    "leaf blight": 3
}

ID_TO_LABEL = {
    index: name for index, name in enumerate(CLASS_NAMES)
}


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

def set_seed(seed=42):

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(SEED)

REPORT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("TERRASPECTRA - DEIT TINY RGB CLASSIFICATION")
print("=" * 60)

print("PyTorch version:", torch.__version__)
print("Device:", DEVICE)
print("Model:", MODEL_NAME)


# ============================================================
# 3. LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)

required_columns = {"image_path", "label"}

for name, dataframe in [
    ("Training", train_df),
    ("Validation", val_df)
]:
    missing = required_columns - set(dataframe.columns)

    if missing:
        raise ValueError(
            f"{name} CSV is missing columns: {missing}"
        )


def normalize_label(label):

    label = str(label).strip().lower()

    if label not in LABEL_TO_ID:
        raise ValueError(f"Unknown class label: {label}")

    return LABEL_TO_ID[label]


train_df["label_id"] = train_df["label"].apply(normalize_label)
val_df["label_id"] = val_df["label"].apply(normalize_label)

print("\nTraining images:", len(train_df))
print("Validation images:", len(val_df))

print("\nTraining class distribution:")
print(train_df["label"].value_counts())


# Verify paths
for dataframe in [train_df, val_df]:

    missing_paths = [
        path for path in dataframe["image_path"]
        if not Path(path).is_file()
    ]

    if missing_paths:
        raise FileNotFoundError(
            f"Missing image files. Examples: {missing_paths[:5]}"
        )


# ============================================================
# 4. LOAD PRETRAINED IMAGE PROCESSOR
# ============================================================

print("\nLoading pretrained image processor...")

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

print("Image processor loaded.")


# ============================================================
# 5. DATASET
# ============================================================

class GrapevineDataset(Dataset):

    def __init__(self, dataframe, image_processor):

        self.dataframe = dataframe.reset_index(drop=True)
        self.processor = image_processor

    def __len__(self):

        return len(self.dataframe)

    def __getitem__(self, index):

        row = self.dataframe.iloc[index]

        image_path = Path(row["image_path"])
        label = int(row["label_id"])

        with Image.open(image_path) as image:

            image = image.convert("RGB")

            processed = self.processor(
                images=image,
                return_tensors="pt"
            )

        pixel_values = processed["pixel_values"].squeeze(0)

        return {
            "pixel_values": pixel_values,
            "labels": torch.tensor(label, dtype=torch.long)
        }


train_dataset = GrapevineDataset(train_df, processor)
val_dataset = GrapevineDataset(val_df, processor)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ============================================================
# 6. LOAD PRETRAINED DEIT-TINY MODEL
# ============================================================

print("\nLoading pretrained DeiT-Tiny model...")

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(CLASS_NAMES),
    id2label=ID_TO_LABEL,
    label2id=LABEL_TO_ID,
    ignore_mismatched_sizes=True
)

model.to(DEVICE)

print("DeiT-Tiny model loaded.")


# ============================================================
# 7. FREEZE BACKBONE
# ============================================================

# Freeze all pretrained parameters.
for parameter in model.parameters():
    parameter.requires_grad = False


# Train only the new classification head.
for parameter in model.classifier.parameters():
    parameter.requires_grad = True


trainable_parameters = [
    parameter for parameter in model.parameters()
    if parameter.requires_grad
]

trainable_count = sum(
    parameter.numel()
    for parameter in trainable_parameters
)

total_count = sum(
    parameter.numel()
    for parameter in model.parameters()
)

print("\nTotal parameters:", f"{total_count:,}")
print("Trainable parameters:", f"{trainable_count:,}")

print("Training strategy: Frozen backbone / Linear probing")


# ============================================================
# 8. CLASS-WEIGHTED LOSS
# ============================================================

class_ids = np.arange(len(CLASS_NAMES))

weights = compute_class_weight(
    class_weight="balanced",
    classes=class_ids,
    y=train_df["label_id"].values
)

class_weights = torch.tensor(
    weights,
    dtype=torch.float32,
    device=DEVICE
)

print("\nClass weights:")

for name, weight in zip(CLASS_NAMES, weights):
    print(f"{name}: {weight:.4f}")


criterion = nn.CrossEntropyLoss(weight=class_weights)

optimizer = torch.optim.AdamW(
    trainable_parameters,
    lr=LEARNING_RATE,
    weight_decay=0.01
)


# ============================================================
# 9. TRAINING FUNCTION
# ============================================================

def train_one_epoch():

    model.train()

    running_loss = 0.0
    all_predictions = []
    all_labels = []

    for batch in train_loader:

        pixel_values = batch["pixel_values"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        optimizer.zero_grad()

        outputs = model(pixel_values=pixel_values)

        loss = criterion(outputs.logits, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        predictions = torch.argmax(
            outputs.logits,
            dim=1
        )

        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / len(train_loader)

    epoch_accuracy = accuracy_score(
        all_labels,
        all_predictions
    )

    return epoch_loss, epoch_accuracy


# ============================================================
# 10. VALIDATION FUNCTION
# ============================================================

def validate():

    model.eval()

    running_loss = 0.0
    all_predictions = []
    all_labels = []

    with torch.no_grad():

        for batch in val_loader:

            pixel_values = batch["pixel_values"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)

            outputs = model(pixel_values=pixel_values)

            loss = criterion(outputs.logits, labels)

            running_loss += loss.item()

            predictions = torch.argmax(
                outputs.logits,
                dim=1
            )

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    val_loss = running_loss / len(val_loader)

    val_accuracy = accuracy_score(
        all_labels,
        all_predictions
    )

    macro_precision, macro_recall, macro_f1, _ = (
        precision_recall_fscore_support(
            all_labels,
            all_predictions,
            average="macro",
            zero_division=0
        )
    )

    return {
        "loss": val_loss,
        "accuracy": val_accuracy,
        "precision": macro_precision,
        "recall": macro_recall,
        "f1": macro_f1
    }


# ============================================================
# 11. TRAINING LOOP
# ============================================================

history = []

best_val_loss = float("inf")
best_epoch = 0
epochs_without_improvement = 0

print("\nStarting training...")
print("=" * 60)

start_time = time.time()

for epoch in range(EPOCHS):

    epoch_start = time.time()

    train_loss, train_accuracy = train_one_epoch()

    val_metrics = validate()

    epoch_time = time.time() - epoch_start

    record = {
        "epoch": epoch + 1,
        "train_loss": train_loss,
        "train_accuracy": train_accuracy,
        "val_loss": val_metrics["loss"],
        "val_accuracy": val_metrics["accuracy"],
        "val_precision": val_metrics["precision"],
        "val_recall": val_metrics["recall"],
        "val_f1": val_metrics["f1"]
    }

    history.append(record)

    print(f"\nEpoch {epoch + 1}/{EPOCHS}")

    print(
        f"Train Loss: {train_loss:.4f} | "
        f"Train Accuracy: {train_accuracy:.4f}"
    )

    print(
        f"Val Loss: {val_metrics['loss']:.4f} | "
        f"Val Accuracy: {val_metrics['accuracy']:.4f}"
    )

    print(
        f"Val Precision: {val_metrics['precision']:.4f} | "
        f"Val Recall: {val_metrics['recall']:.4f} | "
        f"Val F1: {val_metrics['f1']:.4f}"
    )

    print(f"Epoch time: {epoch_time:.1f} seconds")

    # Save best model using validation loss.
    if val_metrics["loss"] < best_val_loss:

        best_val_loss = val_metrics["loss"]
        best_epoch = epoch + 1
        epochs_without_improvement = 0

        model.save_pretrained(
            MODEL_DIR,
            safe_serialization=True
        )

        processor.save_pretrained(MODEL_DIR)

        print("Best model checkpoint saved.")

    else:

        epochs_without_improvement += 1

    # Early stopping
    if epochs_without_improvement >= PATIENCE:

        print("\nEarly stopping triggered.")
        break


total_time = time.time() - start_time


# ============================================================
# 12. SAVE TRAINING HISTORY
# ============================================================

history_df = pd.DataFrame(history)

history_path = REPORT_DIR / "deit_tiny_training_history.csv"

history_df.to_csv(history_path, index=False)

print("\nTraining history saved:", history_path)


# ============================================================
# 13. LOAD BEST MODEL
# ============================================================

print("\nLoading best checkpoint for validation evaluation...")

model = AutoModelForImageClassification.from_pretrained(
    MODEL_DIR
)

model.to(DEVICE)
model.eval()


# ============================================================
# 14. FINAL VALIDATION PREDICTIONS
# ============================================================

all_predictions = []
all_labels = []
all_probabilities = []

with torch.no_grad():

    for batch in val_loader:

        pixel_values = batch["pixel_values"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        outputs = model(pixel_values=pixel_values)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        predictions = torch.argmax(
            probabilities,
            dim=1
        )

        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_probabilities.extend(probabilities.cpu().numpy())


# ============================================================
# 15. CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    all_labels,
    all_predictions,
    labels=class_ids,
    target_names=CLASS_NAMES,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report).transpose()

report_path = REPORT_DIR / "deit_tiny_validation_report.csv"

report_df.to_csv(report_path)

print("\nValidation classification report:")
print(
    classification_report(
        all_labels,
        all_predictions,
        labels=class_ids,
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# ============================================================
# 16. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=class_ids
)

plt.figure(figsize=(8, 6))

plt.imshow(cm, interpolation="nearest")

plt.title("DeiT-Tiny Validation Confusion Matrix")
plt.colorbar()

ticks = np.arange(len(CLASS_NAMES))

plt.xticks(ticks, CLASS_NAMES, rotation=30, ha="right")
plt.yticks(ticks, CLASS_NAMES)

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")

for i in range(cm.shape[0]):

    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.tight_layout()

cm_path = REPORT_DIR / "deit_tiny_validation_confusion_matrix.png"

plt.savefig(cm_path, dpi=300)
plt.close()


# ============================================================
# 17. SAVE METRICS
# ============================================================

precision, recall, macro_f1, _ = precision_recall_fscore_support(
    all_labels,
    all_predictions,
    average="macro",
    zero_division=0
)

weighted_f1 = precision_recall_fscore_support(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)[2]

metrics = {
    "model": MODEL_NAME,
    "experiment": "DeiT-Tiny RGB Linear Probing",
    "device": str(DEVICE),
    "best_epoch": best_epoch,
    "total_epochs": len(history),
    "best_validation_loss": float(best_val_loss),
    "validation_accuracy": float(
        accuracy_score(all_labels, all_predictions)
    ),
    "macro_precision": float(precision),
    "macro_recall": float(recall),
    "macro_f1": float(macro_f1),
    "weighted_f1": float(weighted_f1),
    "validation_images": len(all_labels),
    "class_names": CLASS_NAMES,
    "training_seconds": round(total_time, 2),
    "input_type": "RGB",
    "pretrained_weights": MODEL_NAME,
    "training_strategy": "Frozen backbone; classifier head only"
}

metrics_path = REPORT_DIR / "deit_tiny_validation_metrics.json"

with open(metrics_path, "w", encoding="utf-8") as file:

    json.dump(metrics, file, indent=4)


# ============================================================
# 18. COMPLETION
# ============================================================

print("\n" + "=" * 60)
print("DEIT-TINY TRAINING COMPLETED")
print("=" * 60)

print("Best epoch:", best_epoch)
print("Best validation loss:", round(best_val_loss, 4))

print(
    "Validation accuracy:",
    round(metrics["validation_accuracy"] * 100, 2),
    "%"
)

print("Macro F1:", round(macro_f1, 4))
print("Weighted F1:", round(weighted_f1, 4))

print("\nSaved model:", MODEL_DIR)
print("Training history:", history_path)
print("Classification report:", report_path)
print("Confusion matrix:", cm_path)
print("Metrics:", metrics_path)

print("\nTest split has NOT been evaluated in this script.")
