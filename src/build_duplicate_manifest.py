
import hashlib
from pathlib import Path
import pandas as pd

# Resolve project root independently of terminal location
PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "audit"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

split_files = {
    "train": SPLIT_DIR / "train.csv",
    "validation": SPLIT_DIR / "validation.csv",
    "test": SPLIT_DIR / "test.csv",
}

def resolve_image_path(value):
    path = Path(str(value).replace("\\", "/"))

    if path.is_absolute():
        return path

    parts = list(path.parts)

    # CSV paths were originally relative to notebooks/
    if parts and parts[0] == "..":
        parts = parts[1:]

    return PROJECT_ROOT.joinpath(*parts)

records = []
missing = []

for split, csv_path in split_files.items():
    print(f"Processing {split}...")

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        image_path = resolve_image_path(row["image_path"])

        if not image_path.exists():
            missing.append(str(image_path))
            continue

        file_hash = hashlib.sha256(
            image_path.read_bytes()
        ).hexdigest()

        records.append({
            "sha256": file_hash,
            "split": split,
            "filename": row["filename"],
            "label": row["label"],
            "vineyard_id": row["vineyard_id"],
            "image_path": str(image_path),
        })

print("\nMissing images:", len(missing))

if missing:
    print("\nFirst missing paths:")
    for path in missing[:10]:
        print(path)
    raise SystemExit("Fix missing paths before continuing.")

if not records:
    raise SystemExit("No images were processed. Check the CSV paths.")

manifest = pd.DataFrame(records)

manifest["duplicate_group_id"] = (
    manifest.groupby("sha256").ngroup()
    .map(lambda x: f"DG_{x:04d}")
)

manifest.to_csv(
    OUTPUT_DIR / "duplicate_group_manifest.csv",
    index=False
)

summary = (
    manifest.groupby("duplicate_group_id")
    .agg(
        copies=("filename", "count"),
        labels=("label", "nunique"),
        splits=("split", "nunique"),
        vineyards=("vineyard_id", "nunique"),
    )
)

print("\n========== MANIFEST SUMMARY ==========")
print("Total images:", len(manifest))
print("Unique image groups:", len(summary))
print("Duplicate groups:", (summary["copies"] > 1).sum())
print("Conflicting-label groups:", (summary["labels"] > 1).sum())
print("Groups crossing splits:", (summary["splits"] > 1).sum())
print("\nManifest saved:", OUTPUT_DIR / "duplicate_group_manifest.csv")
