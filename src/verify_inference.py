
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

from inference import GrapevineDiseasePredictor


# --------------------------------------------------
# 1. PROJECT PATHS AND CLASS MAPPING
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]

class_to_index = {
    "black rot": 0,
    "esca": 1,
    "healthy": 2,
    "leaf blight": 3
}


# --------------------------------------------------
# 2. LOAD TEST DATA
# --------------------------------------------------

test_csv = SPLIT_DIR / "test.csv"

if not test_csv.exists():
    raise FileNotFoundError(f"Test CSV not found: {test_csv}")

test_df = pd.read_csv(test_csv)

print("Test dataset loaded successfully!")
print("Total test images:", len(test_df))


# --------------------------------------------------
# 3. RESOLVE IMAGE PATHS
# --------------------------------------------------

def resolve_image_path(value):

    path = Path(str(value).replace("\\", "/"))

    if path.is_absolute():
        return path

    parts = list(path.parts)

    if parts and parts[0] == "..":
        parts = parts[1:]

    return PROJECT_ROOT.joinpath(*parts)


# --------------------------------------------------
# 4. LOAD TRAINED MODEL
# --------------------------------------------------

predictor = GrapevineDiseasePredictor()


# --------------------------------------------------
# 5. RUN STANDALONE INFERENCE
# --------------------------------------------------

actual = []
predicted = []

print("\nRunning predictions on test images...")

for index, row in test_df.iterrows():

    image_path = resolve_image_path(row["image_path"])

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    result = predictor.predict(image_path)

    actual_label = str(row["label"]).strip().lower()

    predicted_label = (
        result["predicted_disease"].strip().lower()
    )

    if actual_label not in class_to_index:
        raise ValueError(f"Unknown actual label: {actual_label}")

    if predicted_label not in class_to_index:
        raise ValueError(f"Unknown predicted label: {predicted_label}")

    actual.append(class_to_index[actual_label])

    predicted.append(class_to_index[predicted_label])

    if (index + 1) % 50 == 0:
        print(f"Processed {index + 1}/{len(test_df)} images")


# --------------------------------------------------
# 6. EVALUATE MODEL
# --------------------------------------------------

accuracy = accuracy_score(actual, predicted)

macro_f1 = f1_score(
    actual,
    predicted,
    average="macro",
    zero_division=0
)

weighted_f1 = f1_score(
    actual,
    predicted,
    average="weighted",
    zero_division=0
)

print("\n" + "=" * 50)
print("STANDALONE INFERENCE TEST")
print("=" * 50)

print("Images tested:", len(actual))

print("Inference accuracy:", round(accuracy, 4))

print("Inference macro F1:", round(macro_f1, 4))

print("Inference weighted F1:", round(weighted_f1, 4))


# --------------------------------------------------
# 7. CLASSIFICATION REPORT
# --------------------------------------------------

print("\nCLASSIFICATION REPORT\n")

print(
    classification_report(
        actual,
        predicted,
        labels=[0, 1, 2, 3],
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# --------------------------------------------------
# 8. SAVE STANDALONE PREDICTIONS
# --------------------------------------------------

output_df = test_df.copy()

output_df["actual_index"] = actual

output_df["predicted_index"] = predicted

output_df["predicted_disease"] = [
    CLASS_NAMES[index] for index in predicted
]

output_path = PROJECT_ROOT / "reports" / "standalone_test_predictions.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)

output_df.to_csv(output_path, index=False)

print("Predictions saved to:", output_path)

print("\nStandalone inference verification completed!")
