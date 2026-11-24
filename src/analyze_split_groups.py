
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

manifest_path = (
    ROOT / "data/processed/audit/duplicate_group_manifest.csv"
)

df = pd.read_csv(manifest_path)

# Union-Find implementation
parent = list(range(len(df)))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

# Keep all images from the same vineyard together
for _, indices in df.groupby("vineyard_id").groups.items():
    indices = list(indices)
    for i in indices[1:]:
        union(indices[0], i)

# Keep all exact duplicates together
for _, indices in df.groupby("sha256").groups.items():
    indices = list(indices)
    for i in indices[1:]:
        union(indices[0], i)

df["component_id"] = [
    find(i) for i in range(len(df))
]

components = (
    df.groupby("component_id")
    .agg(
        images=("filename", "count"),
        vineyards=("vineyard_id", "nunique"),
        duplicate_groups=("sha256", "nunique"),
        labels=("label", "nunique"),
    )
    .sort_values("images", ascending=False)
)

print("\n========== GROUPING ANALYSIS ==========")
print("Total images:", len(df))
print("Independent components:", len(components))
print("Largest component:", components["images"].max())
print("Components containing multiple vineyards:",
      (components["vineyards"] > 1).sum())

print("\nTop 15 largest components:")
print(components.head(15).to_string())

print("\nComponents with conflicting labels:",
      (components["labels"] > 1).sum())
