
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

# =====================================================
# 1. CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

IMAGE_SIZE = 64
BATCH_SIZE = 4
EPOCHS = 15
SEED = 42
NUM_CLASSES = 4

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]

CLASS_TO_INDEX = {
    "black rot": 0,
    "esca": 1,
    "healthy": 2,
    "leaf blight": 3
}

tf.keras.utils.set_random_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

print("TensorFlow:", tf.__version__)
print("GPU:", tf.config.list_physical_devices("GPU"))


# =====================================================
# 2. LOAD DATASET SPLITS
# =====================================================

train_df = pd.read_csv(SPLIT_DIR / "train.csv")
val_df = pd.read_csv(SPLIT_DIR / "validation.csv")
test_df = pd.read_csv(SPLIT_DIR / "test.csv")


def encode_labels(df):
    labels = (
        df["label"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(CLASS_TO_INDEX)
    )

    if labels.isna().any():
        raise ValueError("Unknown class labels found.")

    return labels.to_numpy(dtype=np.int32)


def resolve_image_path(value):
    path = Path(str(value).replace("\\", "/"))

    if path.is_absolute():
        return str(path)

    parts = list(path.parts)

    if parts and parts[0] == "..":
        parts = parts[1:]

    return str(PROJECT_ROOT.joinpath(*parts))


def prepare_split(df, split_name):
    paths = df["image_path"].apply(
        resolve_image_path
    ).to_numpy()

    labels = encode_labels(df)

    missing = [p for p in paths if not Path(p).is_file()]

    print(
        f"{split_name}: {len(paths)} images | "
        f"Missing: {len(missing)}"
    )

    if missing:
        raise FileNotFoundError(missing[:5])

    return paths, labels


train_paths, train_labels = prepare_split(
    train_df, "Training"
)

val_paths, val_labels = prepare_split(
    val_df, "Validation"
)

test_paths, test_labels = prepare_split(
    test_df, "Testing"
)


# =====================================================
# 3. RGB IMAGE PREPROCESSING
# =====================================================

def load_rgb_volume(image_path, label):

    image = tf.io.read_file(image_path)

    image = tf.io.decode_jpeg(
        image,
        channels=3
    )

    image = tf.image.resize(
        image,
        [IMAGE_SIZE, IMAGE_SIZE]
    )

    image = tf.cast(image, tf.float32) / 255.0

    # RGB: H x W x 3
    # Convert to: 3 x H x W x 1
    image = tf.transpose(image, [2, 0, 1])

    image = tf.expand_dims(image, axis=-1)

    image.set_shape([
        3,
        IMAGE_SIZE,
        IMAGE_SIZE,
        1
    ])

    return image, label


def create_dataset(paths, labels, training=False):

    dataset = tf.data.Dataset.from_tensor_slices(
        (paths, labels)
    )

    if training:
        dataset = dataset.shuffle(
            len(paths),
            seed=SEED,
            reshuffle_each_iteration=True
        )

    dataset = dataset.map(
        load_rgb_volume,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(1)

    return dataset


train_ds = create_dataset(
    train_paths, train_labels, training=True
)

val_ds = create_dataset(
    val_paths, val_labels
)

test_ds = create_dataset(
    test_paths, test_labels
)

print("\nDataset pipelines created successfully.")


# =====================================================
# 4. BUILD 3D CNN MODEL
# =====================================================

def build_3dcnn():

    inputs = tf.keras.Input(
        shape=(3, IMAGE_SIZE, IMAGE_SIZE, 1)
    )

    x = tf.keras.layers.Conv3D(
        8,
        kernel_size=(3, 3, 3),
        padding="same",
        activation="relu"
    )(inputs)

    x = tf.keras.layers.MaxPooling3D(
        pool_size=(1, 2, 2)
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.Conv3D(
        16,
        kernel_size=(3, 3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.MaxPooling3D(
        pool_size=(1, 2, 2)
    )(x)

    x = tf.keras.layers.BatchNormalization()(x)

    x = tf.keras.layers.Conv3D(
        32,
        kernel_size=(3, 3, 3),
        padding="same",
        activation="relu"
    )(x)

    x = tf.keras.layers.GlobalAveragePooling3D()(x)

    x = tf.keras.layers.Dropout(0.35)(x)

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax"
    )(x)

    model = tf.keras.Model(
        inputs,
        outputs,
        name="TerraSpectra_RGB_3D_CNN"
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


model = build_3dcnn()

model.summary()


# =====================================================
# 5. VERIFY INPUT SHAPE
# =====================================================

sample_images, sample_labels = next(iter(train_ds))

print("\nInput batch shape:", sample_images.shape)
print("Output shape:", model(sample_images).shape)

print(
    "Pixel range:",
    float(tf.reduce_min(sample_images)),
    float(tf.reduce_max(sample_images))
)


# =====================================================
# 6. TRAIN MODEL
# =====================================================

checkpoint_path = (
    MODEL_DIR / "terraspectra_rgb_3dcnn_best.keras"
)

callbacks = [

    tf.keras.callbacks.ModelCheckpoint(
        filepath=str(checkpoint_path),
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    ),

    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        verbose=1
    )
]

print("\nStarting RGB 3D-CNN training...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks,
    shuffle=False
)

pd.DataFrame(history.history).to_csv(
    REPORT_DIR / "rgb_3dcnn_training_history.csv",
    index=False
)


# =====================================================
# 7. LOAD BEST MODEL
# =====================================================

best_model = tf.keras.models.load_model(
    checkpoint_path
)

print("\nBest checkpoint loaded successfully.")


# =====================================================
# 8. TEST EVALUATION
# =====================================================

probabilities = best_model.predict(
    test_ds,
    verbose=1
)

predictions = np.argmax(
    probabilities,
    axis=1
)

accuracy = accuracy_score(
    test_labels,
    predictions
)

precision, recall, macro_f1, _ = (
    precision_recall_fscore_support(
        test_labels,
        predictions,
        average="macro",
        zero_division=0
    )
)

weighted_precision, weighted_recall, weighted_f1, _ = (
    precision_recall_fscore_support(
        test_labels,
        predictions,
        average="weighted",
        zero_division=0
    )
)

print("\n========== TEST RESULTS ==========")

print(f"Accuracy: {accuracy:.4f}")
print(f"Macro Precision: {precision:.4f}")
print(f"Macro Recall: {recall:.4f}")
print(f"Macro F1: {macro_f1:.4f}")
print(f"Weighted F1: {weighted_f1:.4f}")


# =====================================================
# 9. CLASSIFICATION REPORT
# =====================================================

report = classification_report(
    test_labels,
    predictions,
    labels=list(range(NUM_CLASSES)),
    target_names=CLASS_NAMES,
    output_dict=True,
    zero_division=0
)

pd.DataFrame(report).transpose().to_csv(
    REPORT_DIR / "rgb_3dcnn_classification_report.csv"
)

print(
    classification_report(
        test_labels,
        predictions,
        labels=list(range(NUM_CLASSES)),
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# =====================================================
# 10. CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(
    test_labels,
    predictions,
    labels=list(range(NUM_CLASSES))
)

plt.figure(figsize=(8, 6))

plt.imshow(cm, cmap="Blues")

plt.title("TerraSpectra RGB 3D-CNN")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.xticks(
    range(NUM_CLASSES),
    CLASS_NAMES,
    rotation=25
)

plt.yticks(
    range(NUM_CLASSES),
    CLASS_NAMES
)

plt.colorbar()

for i in range(NUM_CLASSES):
    for j in range(NUM_CLASSES):
        plt.text(
            j, i, str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "rgb_3dcnn_confusion_matrix.png",
    dpi=200
)

plt.close()


# =====================================================
# 11. SAVE METRICS AND METADATA
# =====================================================

metadata = {

    "model": "TerraSpectra RGB 3D-CNN",

    "dataset": "GVLiD",

    "model_type": "RGB experimental 3D-CNN",

    "input_shape": [
        3, IMAGE_SIZE, IMAGE_SIZE, 1
    ],

    "class_names": CLASS_NAMES,

    "normalization": "RGB values divided by 255",

    "training_images": len(train_labels),

    "validation_images": len(val_labels),

    "test_images": len(test_labels),

    "seed": SEED,

    "epochs": len(history.history["loss"]),

    "batch_size": BATCH_SIZE,

    "test_accuracy": float(accuracy),

    "macro_precision": float(precision),

    "macro_recall": float(recall),

    "macro_f1": float(macro_f1),

    "weighted_precision": float(weighted_precision),

    "weighted_recall": float(weighted_recall),

    "weighted_f1": float(weighted_f1),

    "checkpoint": str(checkpoint_path.relative_to(PROJECT_ROOT)),

    "limitation": (
        "This model uses RGB channels as a depth dimension. "
        "It is not a hyperspectral model and does not contain "
        "independent wavelength bands."
    )
}

with open(
    REPORT_DIR / "rgb_3dcnn_metrics.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print("\n===================================")
print("RGB 3D-CNN EXPERIMENT COMPLETED")
print("===================================")

print("Model:", checkpoint_path)
print("Reports:", REPORT_DIR)
