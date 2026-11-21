
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPLIT_DIR = ROOT / "data/processed/splits_clean"

files = {
    "Train": "train.csv",
    "Validation": "validation.csv",
    "Test": "test.csv"
}

frames = {}

for name, filename in files.items():
    df = pd.read_csv(SPLIT_DIR / filename)
    frames[name] = df

    print(f"\n{name}: {len(df)} images")

    print(
        df["label"]
        .value_counts()
        .sort_index()
        .to_string()
    )

distribution = pd.DataFrame({
    name: df["label"].value_counts()
    for name, df in frames.items()
}).fillna(0).astype(int)

print("\n========== CLASS DISTRIBUTION ==========")
print(distribution.to_string())

print("\n========== IMAGE PATH CHECK ==========")

for name, df in frames.items():
    missing = sum(
        not Path(p).exists()
        for p in df["image_path"]
    )
    print(f"{name} missing paths: {missing}")
