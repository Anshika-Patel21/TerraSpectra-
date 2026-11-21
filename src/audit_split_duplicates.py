
from pathlib import Path
from collections import defaultdict
import hashlib
import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SPLIT_DIR = PROJECT_ROOT / "data" / "processed" / "splits"
IMAGE_ROOT = PROJECT_ROOT / "data" / "processed" / "GVLiD_224"


# --------------------------------------------------
# 2. CLASS FOLDER MAPPING
# --------------------------------------------------

# CSV labels are normalized to lowercase before lookup.

CLASS_FOLDERS = {
    "black rot": "Black rot",
    "esca": "esca",
    "healthy": "healthy",
    "leaf blight": "leaf blight"
}


# --------------------------------------------------
# 3. DATASET SPLIT FILES
# --------------------------------------------------

split_files = {
    "train": SPLIT_DIR / "train.csv",
    "validation": SPLIT_DIR / "validation.csv",
    "test": SPLIT_DIR / "test.csv"
}


# --------------------------------------------------
# 4. CALCULATE IMAGE HASHES
# --------------------------------------------------

hash_records = []

missing_images = []

for split_name, csv_path in split_files.items():

    print(f"\nProcessing {split_name} split...")

    if not csv_path.exists():
        raise FileNotFoundError(f"Split CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():

        label = str(row["label"]).strip().lower()

        if label not in CLASS_FOLDERS:
            print("Unknown class label:", row["label"])
            continue

        folder = CLASS_FOLDERS[label]

        image_path = IMAGE_ROOT / folder / str(row["filename"])

        if not image_path.exists():
            missing_images.append(str(image_path))
            continue

        try:
            image_hash = hashlib.sha256(
                image_path.read_bytes()
            ).hexdigest()

            hash_records.append({
                "hash": image_hash,
                "split": split_name,
                "label": label,
                "filename": row["filename"],
                "vineyard_id": row["vineyard_id"],
                "image_path": str(image_path)
            })

        except Exception as error:
            print("Error reading:", image_path, error)


# --------------------------------------------------
# 5. CREATE AUDIT DATAFRAME
# --------------------------------------------------

records_df = pd.DataFrame(hash_records)

if records_df.empty:
    raise RuntimeError("No images were successfully checked.")


print("\n======================================")
print("       DUPLICATE SPLIT AUDIT")
print("======================================")

print("Total images checked:", len(records_df))
print("Unique image hashes:", records_df["hash"].nunique())

print("Missing images:", len(missing_images))

if missing_images:
    print("\nFirst 10 missing images:")
    for path in missing_images[:10]:
        print(path)


# ======================================
# TEST SET DUPLICATE LEAKAGE SUMMARY
# ======================================

split_counts = (
    records_df.groupby("hash")["split"]
    .agg(lambda x: sorted(set(x)))
    .reset_index(name="splits")
)

cross_split = split_counts[
    split_counts["splits"].apply(len) > 1
]

test_hashes = set(
    records_df.loc[records_df["split"] == "test", "hash"]
)

train_hashes = set(
    records_df.loc[records_df["split"] == "train", "hash"]
)

val_hashes = set(
    records_df.loc[records_df["split"] == "validation", "hash"]
)

test_train_overlap = test_hashes & train_hashes
test_val_overlap = test_hashes & val_hashes

print("\n======================================")
print("       TEST SET LEAKAGE SUMMARY")
print("======================================")

print("Unique test images:", len(test_hashes))
print("Test hashes also in train:", len(test_train_overlap))
print("Test hashes also in validation:", len(test_val_overlap))
print("Test hashes overlapping either split:",
      len(test_train_overlap | test_val_overlap))

print("\nCross-split group combinations:")
print(
    cross_split["splits"]
    .value_counts()
    .to_string()
)

# --------------------------------------------------
# 6. DUPLICATES WITHIN AND ACROSS SPLITS
# --------------------------------------------------

duplicate_groups = []

for image_hash, group in records_df.groupby("hash"):

    if len(group) > 1:
        duplicate_groups.append(group)


cross_split_groups = []

for image_hash, group in records_df.groupby("hash"):

    if group["split"].nunique() > 1:
        cross_split_groups.append(group)


print("\nDuplicate groups within all splits:",
      len(duplicate_groups))

print("Duplicate groups crossing splits:",
      len(cross_split_groups))


# --------------------------------------------------
# 7. DISPLAY CROSS-SPLIT DUPLICATES
# --------------------------------------------------

if cross_split_groups:

    leakage_df = pd.concat(cross_split_groups)

    print("\nCROSS-SPLIT DUPLICATE DETAILS")
    print("-----------------------------")

    print(
        leakage_df.sort_values(
            ["hash", "split"]
        )[
            ["split", "label", "filename", "vineyard_id"]
        ].to_string(index=False)
    )

    leakage_path = PROJECT_ROOT / "duplicate_split_leakage.csv"

    leakage_df.to_csv(leakage_path, index=False)

    print("\nLeakage report saved to:", leakage_path)

else:

    print("\nNo exact duplicate images found across splits.")


# --------------------------------------------------
# 8. CHECK CONFLICTING LABELS
# --------------------------------------------------

conflicts = []

for image_hash, group in records_df.groupby("hash"):

    if group["label"].nunique() > 1:
        conflicts.append(group)


print("\nDuplicate groups with conflicting labels:",
      len(conflicts))


if conflicts:

    conflict_df = pd.concat(conflicts)

    print("\nCONFLICTING LABEL DETAILS")
    print("-------------------------")

    print(
        conflict_df.sort_values(
            ["hash", "split"]
        )[
            ["split", "label", "filename", "vineyard_id"]
        ].to_string(index=False)
    )

    conflict_path = PROJECT_ROOT / "duplicate_label_conflicts.csv"

    conflict_df.to_csv(conflict_path, index=False)

    print("\nLabel conflict report saved to:", conflict_path)

else:

    print("\nNo conflicting labels found within the checked splits.")


# --------------------------------------------------
# 9. FINAL SUMMARY
# --------------------------------------------------

print("\n======================================")
print("             FINAL SUMMARY")
print("======================================")

print("Images checked:", len(records_df))
print("Unique images:", records_df["hash"].nunique())
print("Duplicate groups:", len(duplicate_groups))
print("Cross-split duplicate groups:", len(cross_split_groups))
print("Conflicting-label groups:", len(conflicts))
print("Missing images:", len(missing_images))

print("\nAudit completed successfully.")



# ======================================
# TEST SET LEAKAGE SUMMARY
# ======================================

split_counts = (
    records_df.groupby("hash")["split"]
    .agg(lambda x: sorted(set(x)))
    .reset_index(name="splits")
)

test_hashes = set(
    records_df.loc[records_df["split"] == "test", "hash"]
)

train_hashes = set(
    records_df.loc[records_df["split"] == "train", "hash"]
)

val_hashes = set(
    records_df.loc[records_df["split"] == "validation", "hash"]
)

test_train_overlap = test_hashes & train_hashes
test_val_overlap = test_hashes & val_hashes

print("\n========== TEST LEAKAGE SUMMARY ==========")
print("Unique test images:", len(test_hashes))
print("Test images also in train:", len(test_train_overlap))
print("Test images also in validation:", len(test_val_overlap))
print(
    "Test images overlapping either:",
    len(test_train_overlap | test_val_overlap)
)