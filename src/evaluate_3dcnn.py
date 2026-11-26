
"""
TerraSpectra - Independent RGB 3D-CNN Evaluation

Loads the saved RGB 3D-CNN model and evaluates it on the
existing test dataset. This script does not train the model.

Run from the project root:
    python -u src/evaluate_3dcnn.py
"""

from pathlib import Path
import json

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "splits_final"
    / "test.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "terraspectra_rgb_3dcnn_best.keras"
)

REPORT_DIR = PROJECT_ROOT / "reports"

IMAGE_SIZE = 64
BATCH_SIZE = 4
NUM_CLASSES = 4

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]

LABEL_MAP = {
    "black rot": 0,
    "black_rot": 0,
    "black-rot": 0,
    "esca": 1,
    "healthy": 2,
    "leaf blight": 3,
    "leaf_blight": 3,
    "leaf-blight": 3
}


# ============================================================
# 2. FIND CSV COLUMNS
# ============================================================

def find_column(dataframe, candidates, description):

    columns = {
        str(column).strip().lower(): column
        for column in dataframe.columns
    }

    for candidate in candidates:

        if candidate in columns:
            return columns[candidate]

    raise ValueError(
        f"Cannot find {description} column.\n"
        f"Available columns: {list(dataframe.columns)}"
    )


# ============================================================
# 3. IMAGE PATH RESOLUTION
# ============================================================

def resolve_image_path(value):

    path = Path(str(value))

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    return path.resolve()


# ============================================================
# 4. LABEL CONVERSION
# ============================================================

def convert_label(value):

    if pd.isna(value):
        raise ValueError("Missing label found in test CSV.")

    if isinstance(value, (int, np.integer)):
        label = int(value)

    elif isinstance(value, (float, np.floating)):
        if not float(value).is_integer():
            raise ValueError(f"Invalid numeric label: {value}")

        label = int(value)

    else:
        text = str(value).strip().lower()

        if text in LABEL_MAP:
            label = LABEL_MAP[text]

        else:
            try:
                label = int(text)

            except ValueError:
                raise ValueError(
                    f"Unknown label: {value}"
                )

    if label < 0 or label >= NUM_CLASSES:
        raise ValueError(
            f"Invalid label index: {label}"
        )

    return label


# ============================================================
# 5. LOAD TEST DATAFRAME
# ============================================================

def load_test_dataframe():

    print("\n[1/6] Loading test dataset...", flush=True)

    if not TEST_CSV.exists():
        raise FileNotFoundError(
            f"Test CSV not found: {TEST_CSV}"
        )

    dataframe = pd.read_csv(TEST_CSV)

    print(
        "CSV columns:",
        list(dataframe.columns),
        flush=True
    )

    path_column = find_column(
        dataframe,
        [
            "image_path",
            "filepath",
            "file_path",
            "path",
            "filename",
            "image"
        ],
        "image path"
    )

    label_column = find_column(
        dataframe,
        [
            "label",
            "class",
            "disease",
            "category",
            "target"
        ],
        "label"
    )

    dataframe = dataframe.copy()

    dataframe["resolved_image_path"] = (
        dataframe[path_column].apply(resolve_image_path)
    )

    dataframe["label_index"] = (
        dataframe[label_column].apply(convert_label)
    )

    missing_files = dataframe[
        ~dataframe["resolved_image_path"].apply(
            lambda path: path.exists()
        )
    ]

    if not missing_files.empty:

        raise FileNotFoundError(
            f"{len(missing_files)} image files are missing.\n"
            f"Examples:\n"
            f"{missing_files['resolved_image_path'].head().tolist()}"
        )

    print(
        f"Test images loaded: {len(dataframe)}",
        flush=True
    )

    return dataframe


# ============================================================
# 6. IMAGE PREPROCESSING
# Must match train_3dcnn.py
# ============================================================

def load_rgb_volume(image_path, label):

    image_bytes = tf.io.read_file(image_path)

    image = tf.io.decode_jpeg(
        image_bytes,
        channels=3
    )

    image = tf.image.resize(
        image,
        [IMAGE_SIZE, IMAGE_SIZE]
    )

    image = tf.cast(
        image,
        tf.float32
    ) / 255.0

    # Original shape: (64, 64, 3)
    # Transposed shape: (3, 64, 64)
    image = tf.transpose(
        image,
        perm=[2, 0, 1]
    )

    # Final shape: (3, 64, 64, 1)
    image = tf.expand_dims(
        image,
        axis=-1
    )

    return image, label


# ============================================================
# 7. CREATE TEST DATASET
# ============================================================

def create_test_dataset(dataframe):

    paths = (
        dataframe["resolved_image_path"]
        .astype(str)
        .to_numpy()
    )

    labels = (
        dataframe["label_index"]
        .to_numpy(dtype=np.int32)
    )

    dataset = tf.data.Dataset.from_tensor_slices(
        (paths, labels)
    )

    dataset = dataset.map(
        load_rgb_volume,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    dataset = dataset.batch(BATCH_SIZE)

    dataset = dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return dataset


# ============================================================
# 8. SAVE CONFUSION MATRIX
# ============================================================

def save_confusion_matrix(matrix):

    print(
        "\n[5/6] Generating confusion matrix...",
        flush=True
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    image = ax.imshow(
        matrix,
        interpolation="nearest"
    )

    fig.colorbar(image, ax=ax)

    ax.set(
        xticks=np.arange(NUM_CLASSES),
        yticks=np.arange(NUM_CLASSES),
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        xlabel="Predicted Label",
        ylabel="Actual Label",
        title="TerraSpectra RGB 3D-CNN Confusion Matrix"
    )

    plt.setp(
        ax.get_xticklabels(),
        rotation=25,
        ha="right"
    )

    threshold = matrix.max() / 2.0

    for row in range(NUM_CLASSES):

        for column in range(NUM_CLASSES):

            ax.text(
                column,
                row,
                str(matrix[row, column]),
                ha="center",
                va="center",
                color=(
                    "white"
                    if matrix[row, column] > threshold
                    else "black"
                )
            )

    fig.tight_layout()

    output_path = (
        REPORT_DIR
        / "rgb_3dcnn_independent_confusion_matrix.png"
    )

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(
        f"Confusion matrix saved: {output_path}",
        flush=True
    )


# ============================================================
# 9. MAIN EVALUATION FUNCTION
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("TERRASPECTRA RGB 3D-CNN EVALUATION")
    print("=" * 60, flush=True)

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"TensorFlow version: {tf.__version__}",
        flush=True
    )

    print(
        f"Available GPUs: {tf.config.list_physical_devices('GPU')}",
        flush=True
    )

    # Load test data
    test_df = load_test_dataframe()

    y_true = test_df[
        "label_index"
    ].to_numpy(dtype=np.int32)

    # Display class distribution
    print("\nTest class distribution:")

    for index, class_name in enumerate(CLASS_NAMES):

        count = int(
            np.sum(y_true == index)
        )

        print(
            f"{class_name}: {count}"
        )

    # Load saved model
    print(
        "\n[2/6] Loading saved 3D-CNN model...",
        flush=True
    )

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model checkpoint not found: {MODEL_PATH}"
        )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Model loaded successfully.",
        flush=True
    )

    print(
        "Model input shape:",
        model.input_shape
    )

    # Create test dataset
    print(
        "\n[3/6] Preparing test dataset...",
        flush=True
    )

    test_dataset = create_test_dataset(
        test_df
    )

    # Predict
    print(
        "\n[4/6] Running model predictions...",
        flush=True
    )

    probabilities = model.predict(
        test_dataset,
        verbose=1
    )

    if probabilities.shape != (
        len(y_true),
        NUM_CLASSES
    ):

        raise ValueError(
            f"Unexpected prediction shape: {probabilities.shape}"
        )

    y_pred = np.argmax(
        probabilities,
        axis=1
    )

    confidence = np.max(
        probabilities,
        axis=1
    )

    # Calculate metrics
    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    macro_precision = precision_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    macro_recall = recall_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    weighted_f1 = f1_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    report = classification_report(
        y_true,
        y_pred,
        labels=list(range(NUM_CLASSES)),
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0
    )

    print("\n" + "=" * 45)
    print("FINAL TEST RESULTS")
    print("=" * 45)

    print(f"Accuracy:         {accuracy:.4f}")
    print(f"Macro Precision:  {macro_precision:.4f}")
    print(f"Macro Recall:     {macro_recall:.4f}")
    print(f"Macro F1:         {macro_f1:.4f}")
    print(f"Weighted F1:      {weighted_f1:.4f}")

    print("\nPER-CLASS CLASSIFICATION REPORT")

    print(
        classification_report(
            y_true,
            y_pred,
            labels=list(range(NUM_CLASSES)),
            target_names=CLASS_NAMES,
            zero_division=0
        )
    )

    # Confusion matrix
    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=list(range(NUM_CLASSES))
    )

    save_confusion_matrix(matrix)

    # Save JSON metrics
    print(
        "\n[6/6] Saving evaluation reports...",
        flush=True
    )

    metrics = {
        "experiment": "RGB 3D-CNN",
        "test_samples": int(len(y_true)),
        "class_names": CLASS_NAMES,
        "input_shape": [3, IMAGE_SIZE, IMAGE_SIZE, 1],
        "accuracy": float(accuracy),
        "macro_precision": float(macro_precision),
        "macro_recall": float(macro_recall),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "per_class": report,
        "limitation": (
            "RGB channels are used as the depth dimension. "
            "This is not a hyperspectral model."
        )
    }

    metrics_path = (
        REPORT_DIR
        / "rgb_3dcnn_independent_metrics.json"
    )

    with open(
        metrics_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )

    # Save per-class CSV
    class_rows = []

    for class_name in CLASS_NAMES:

        values = report[class_name]

        class_rows.append({
            "class": class_name,
            "precision": values["precision"],
            "recall": values["recall"],
            "f1_score": values["f1-score"],
            "support": int(values["support"])
        })

    class_report_path = (
        REPORT_DIR
        / "rgb_3dcnn_independent_classification_report.csv"
    )

    pd.DataFrame(
        class_rows
    ).to_csv(
        class_report_path,
        index=False
    )

    # Save individual predictions
    predictions_df = pd.DataFrame({
        "image_path": test_df[
            "resolved_image_path"
        ].astype(str),

        "actual_class": [
            CLASS_NAMES[index]
            for index in y_true
        ],

        "predicted_class": [
            CLASS_NAMES[index]
            for index in y_pred
        ],

        "confidence": confidence,

        "correct_prediction": (
            y_true == y_pred
        )
    })

    for index, class_name in enumerate(CLASS_NAMES):

        column_name = (
            "probability_"
            + class_name.lower().replace(" ", "_")
        )

        predictions_df[column_name] = (
            probabilities[:, index]
        )

    predictions_path = (
        REPORT_DIR
        / "rgb_3dcnn_test_predictions.csv"
    )

    predictions_df.to_csv(
        predictions_path,
        index=False
    )

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nGenerated files:")

    print(metrics_path)
    print(class_report_path)

    print(
        REPORT_DIR
        / "rgb_3dcnn_independent_confusion_matrix.png"
    )

    print(predictions_path)


# ============================================================
# 10. SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as error:

        print("\nEVALUATION FAILED")
        print(f"Error: {error}")

        raise
