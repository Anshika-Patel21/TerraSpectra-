
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits_final"

files = ["train.csv", "validation.csv", "test.csv"]
total = 0

for filename in files:
    csv_path = SPLIT_DIR / filename
    df = pd.read_csv(csv_path)

    missing = []

    for image_path in df["image_path"]:
        path = Path(str(image_path).replace("\\", "/"))

        if not path.is_absolute():
            parts = list(path.parts)

            # CSV paths may be relative to notebooks/
            if parts and parts[0] == "..":
                parts = parts[1:]

            path = PROJECT_ROOT.joinpath(*parts)

        if not path.exists():
            missing.append(str(image_path))

    print(f"\n{filename}")
    print("Rows:", len(df))
    print("Missing images:", len(missing))

    if missing:
        print("First missing paths:", missing[:5])

    total += len(df)

print("\nTOTAL IMAGES:", total)
