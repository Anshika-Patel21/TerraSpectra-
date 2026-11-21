
from pathlib import Path

import pandas as pd

from inference import GrapevineDiseasePredictor


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"

CLASS_NAMES = [
    "Black rot",
    "Esca",
    "Healthy",
    "Leaf blight"
]

train_df = pd.read_csv(
    SPLIT_DIR / "train.csv"
)


def resolve_image_path(value):

    path = Path(str(value).replace("\\", "/"))

    if path.is_absolute():
        return path

    parts = list(path.parts)

    if parts and parts[0] == "..":
        parts = parts[1:]

    return PROJECT_ROOT.joinpath(*parts)


predictor = GrapevineDiseasePredictor()

print("\nTERRASPECTRA INFERENCE TEST\n")

for class_name in CLASS_NAMES:

    sample = train_df[
        train_df["label"].astype(str).str.strip().str.lower()
        == class_name.lower()
    ].iloc[0]

    image_path = resolve_image_path(
        sample["image_path"]
    )

    result = predictor.predict(image_path)

    print("\nActual:", class_name)
    print("Predicted:", result["predicted_disease"])
    print("Confidence:", result["confidence"])

    print("Probabilities:")

    for disease, score in result["probabilities"].items():
        print(f"{disease}: {score}")
