
from pathlib import Path
import json

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image

import matplotlib.pyplot as plt
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


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"

MODEL_DIR = PROJECT_ROOT / "models" / "terraspectra_deit_tiny_best"

REPORT_DIR = PROJECT_ROOT / "reports"

TEST_CSV = SPLIT_DIR / "test.csv"

BATCH_SIZE = 8

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

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
    index: name
    for index, name in enumerate(CLASS_NAMES)
}

NUM_CLASSES = len(CLASS_NAMES)

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD TEST DATA
# ============================================================

print("=" * 60)
print("TERRASPECTRA - DEIT TINY TEST EVALUATION")
print("=" * 60)

print("Device:", DEVICE)

test_df = pd.read_csv(TEST_CSV)

required_columns = {"image_path", "label"}

if not required_columns.issubset(test_df.columns):
    raise ValueError("Test CSV is missing required columns.")

test_df["label_id"] = (
    test_df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(LABEL_TO_ID)
)

if test_df["label_id"].isna().any():
    raise ValueError("Unknown labels found in test CSV.")

test_df["label_id"] = test_df["label_id"].astype(int)

print("\nTest images:", len(test_df))

print("\nTest class distribution:")
print(test_df["label"].value_counts())


# Verify image paths
missing_paths = [
    path
    for path in test_df["image_path"]
    if not Path(path).is_file()
]

if missing_paths:
    raise FileNotFoundError(
        f"Missing test images: {missing_paths[:5]}"
    )


# ============================================================
# 3. LOAD PROCESSOR AND MODEL
# ============================================================

print("\nLoading saved DeiT-Tiny checkpoint...")

processor = AutoImageProcessor.from_pretrained(
    MODEL_DIR
)

model = AutoModelForImageClassification.from_pretrained(
    MODEL_DIR
)

model.to(DEVICE)
model.eval()

print("Model loaded successfully.")
print("Model input:", model.config.image_size)
print("Number of classes:", model.config.num_labels)


# ============================================================
# 4. TEST DATASET
# ============================================================

class GrapevineTestDataset(Dataset):

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


test_dataset = GrapevineTestDataset(
    test_df,
    processor
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ============================================================
# 5. PREDICTION
# ============================================================

print("\nRunning test evaluation...")

all_predictions = []
all_labels = []
all_probabilities = []

with torch.no_grad():

    for batch_index, batch in enumerate(test_loader):

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

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.cpu().numpy()
        )

        all_probabilities.extend(
            probabilities.cpu().numpy()
        )

        print(
            f"Completed batch "
            f"{batch_index + 1}/{len(test_loader)}"
        )


all_predictions = np.array(all_predictions)
all_labels = np.array(all_labels)
all_probabilities = np.array(all_probabilities)


# ============================================================
# 6. CALCULATE METRICS
# ============================================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

macro_precision, macro_recall, macro_f1, _ = (
    precision_recall_fscore_support(
        all_labels,
        all_predictions,
        labels=list(range(NUM_CLASSES)),
        average="macro",
        zero_division=0
    )
)

weighted_precision, weighted_recall, weighted_f1, _ = (
    precision_recall_fscore_support(
        all_labels,
        all_predictions,
        labels=list(range(NUM_CLASSES)),
        average="weighted",
        zero_division=0
    )
)


# ============================================================
# 7. CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    all_labels,
    all_predictions,
    labels=list(range(NUM_CLASSES)),
    target_names=CLASS_NAMES,
    output_dict=True,
    zero_division=0
)

report_df = pd.DataFrame(report).transpose()

report_path = (
    REPORT_DIR /
    "deit_tiny_test_classification_report.csv"
)

report_df.to_csv(report_path)

print("\nTEST CLASSIFICATION REPORT")

print(
    classification_report(
        all_labels,
        all_predictions,
        labels=list(range(NUM_CLASSES)),
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# ============================================================
# 8. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(NUM_CLASSES))
)

plt.figure(figsize=(8, 6))

plt.imshow(cm, interpolation="nearest")

plt.title("DeiT-Tiny Test Confusion Matrix")

plt.colorbar()

ticks = np.arange(NUM_CLASSES)

plt.xticks(
    ticks,
    CLASS_NAMES,
    rotation=30,
    ha="right"
)

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

cm_path = (
    REPORT_DIR /
    "deit_tiny_test_confusion_matrix.png"
)

plt.savefig(cm_path, dpi=300)
plt.close()


# ============================================================
# 9. SAVE INDIVIDUAL PREDICTIONS
# ============================================================

prediction_df = test_df[
    ["filename", "image_path", "label"]
].copy()

prediction_df["actual_class"] = [
    ID_TO_LABEL[int(label)]
    for label in all_labels
]

prediction_df["predicted_class"] = [
    ID_TO_LABEL[int(prediction)]
    for prediction in all_predictions
]

prediction_df["confidence"] = np.max(
    all_probabilities,
    axis=1
)

prediction_df["correct_prediction"] = (
    all_predictions == all_labels
)

for class_id, class_name in enumerate(CLASS_NAMES):

    column_name = (
        "probability_" +
        class_name.lower().replace(" ", "_")
    )

    prediction_df[column_name] = (
        all_probabilities[:, class_id]
    )

predictions_path = (
    REPORT_DIR /
    "deit_tiny_test_predictions.csv"
)

prediction_df.to_csv(
    predictions_path,
    index=False
)


# ============================================================
# 10. SAVE METRICS JSON
# ============================================================

metrics = {
    "model": "facebook/deit-tiny-patch16-224",
    "experiment": "DeiT-Tiny RGB Linear Probing",
    "device": str(DEVICE),
    "test_images": int(len(all_labels)),
    "correct_predictions": int(
        np.sum(all_predictions == all_labels)
    ),
    "incorrect_predictions": int(
        np.sum(all_predictions != all_labels)
    ),
    "accuracy": float(accuracy),
    "macro_precision": float(macro_precision),
    "macro_recall": float(macro_recall),
    "macro_f1": float(macro_f1),
    "weighted_precision": float(weighted_precision),
    "weighted_recall": float(weighted_recall),
    "weighted_f1": float(weighted_f1),
    "class_names": CLASS_NAMES,
    "input_type": "RGB",
    "training_strategy": "Frozen pretrained backbone"
}

metrics_path = (
    REPORT_DIR /
    "deit_tiny_test_metrics.json"
)

with open(
    metrics_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(metrics, file, indent=4)


# ============================================================
# 11. FINAL RESULTS
# ============================================================

print("\n" + "=" * 60)
print("DEIT-TINY TEST EVALUATION COMPLETED")
print("=" * 60)

print("Test images:", len(all_labels))

print(
    "Correct predictions:",
    metrics["correct_predictions"]
)

print(
    "Incorrect predictions:",
    metrics["incorrect_predictions"]
)

print(f"Accuracy: {accuracy * 100:.2f}%")

print(f"Macro Precision: {macro_precision:.4f}")
print(f"Macro Recall: {macro_recall:.4f}")
print(f"Macro F1: {macro_f1:.4f}")

print(f"Weighted F1: {weighted_f1:.4f}")

print("\nSaved files:")
print(metrics_path)
print(report_path)
print(cm_path)
print(predictions_path)

print("\nTest evaluation finished.")
