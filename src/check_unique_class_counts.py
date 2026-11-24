
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/audit/duplicate_group_manifest.csv"
)

# Exclude duplicate groups with conflicting labels
conflicts = df.groupby("sha256")["label"].nunique()
bad_hashes = set(conflicts[conflicts > 1].index)

df = df[~df["sha256"].isin(bad_hashes)].copy()

# Count one representative per unique image
unique_df = df.drop_duplicates("sha256")

print("\nUNIQUE IMAGE CLASS COUNTS")
print(unique_df["label"].value_counts().to_string())

print("\nUNIQUE IMAGE VINEYARD COUNTS")
print("Vineyards:", unique_df["vineyard_id"].nunique())

print("\nCLASS DISTRIBUTION BY VINEYARD")
print(pd.crosstab(
    unique_df["vineyard_id"],
    unique_df["label"]
).to_string())
