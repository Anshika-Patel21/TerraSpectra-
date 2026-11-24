
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data/processed/audit/duplicate_group_manifest.csv"
OUTPUT = ROOT / "data/processed/splits_clean"

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

# 1. Check original vineyard separation
vineyard_splits = df.groupby("vineyard_id")["split"].nunique()

if (vineyard_splits > 1).any():
    raise ValueError(
        "Original splits contain vineyard overlap. Stop and investigate."
    )

print("Original vineyard separation: PASSED")

# 2. Identify and exclude conflicting-label image hashes
label_counts = df.groupby("sha256")["label"].nunique()

conflicting_hashes = set(
    label_counts[label_counts > 1].index
)

print("Conflicting image groups:", len(conflicting_hashes))

df = df[~df["sha256"].isin(conflicting_hashes)].copy()

# 3. Keep one copy of each exact image globally.
# Prefer test, then validation, then train.
priority = {
    "test": 0,
    "validation": 1,
    "train": 2
}

df["priority"] = df["split"].map(priority)

df = df.sort_values(
    ["priority", "sha256", "filename"]
)

clean = df.drop_duplicates(
    subset="sha256",
    keep="first"
).copy()

clean = clean.drop(columns="priority")

# 4. Save corrected split CSV files
for split in ["train", "validation", "test"]:
    split_df = clean[clean["split"] == split].copy()

    split_df.to_csv(
        OUTPUT / f"{split}.csv",
        index=False
    )

    print(f"{split}: {len(split_df)} images saved")

# 5. Verify no duplicate hashes across splits
hash_overlap = {}

for a, b in [
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test")
]:
    hashes_a = set(clean.loc[clean["split"] == a, "sha256"])
    hashes_b = set(clean.loc[clean["split"] == b, "sha256"])

    hash_overlap[f"{a}-{b}"] = len(hashes_a & hashes_b)

# 6. Verify vineyard separation remains intact
vineyard_check = clean.groupby("vineyard_id")["split"].nunique()

print("\n========== FINAL VERIFICATION ==========")
print("Remaining images:", len(clean))
print("Unique hashes:", clean["sha256"].nunique())
print("Duplicate hash overlap:", hash_overlap)
print(
    "Vineyard overlap:",
    int((vineyard_check > 1).sum())
)

assert all(value == 0 for value in hash_overlap.values())
assert (vineyard_check <= 1).all()
assert clean["sha256"].is_unique

print("\nSUCCESS: Clean splits created and verified.")
print("Output folder:", OUTPUT)
