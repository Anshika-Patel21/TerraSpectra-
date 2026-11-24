
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parents[1]

MANIFEST = ROOT / "data/processed/audit/duplicate_group_manifest.csv"
OUTPUT = ROOT / "data/processed/splits_final"

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(MANIFEST)

# Remove the two unresolved conflicting-label image groups
label_counts = df.groupby("sha256")["label"].nunique()
bad_hashes = set(label_counts[label_counts > 1].index)

df = df[~df["sha256"].isin(bad_hashes)].copy()

# Keep one representative for every exact image
df = df.drop_duplicates("sha256").reset_index(drop=True)

X = np.zeros((len(df), 1))
y = df["label"].values
groups = df["vineyard_id"].values

classes = sorted(df["label"].unique())
target_ratios = {
    "train": 5 / 7,
    "validation": 1 / 7,
    "test": 1 / 7
}

best_score = float("inf")
best_splits = None
best_seed = None

# Search for a good stratified group assignment
for seed in range(200):
    sgkf = StratifiedGroupKFold(
        n_splits=7,
        shuffle=True,
        random_state=seed
    )

    folds = [
        test_idx
        for _, test_idx in sgkf.split(X, y, groups)
    ]

    candidate = {
        "train": np.concatenate(folds[2:]),
        "validation": folds[0],
        "test": folds[1]
    }

    valid = True
    score = 0

    for name, indices in candidate.items():
        part = df.iloc[indices]

        # Every class must occur in every split
        if set(part["label"].unique()) != set(classes):
            valid = False
            break

        actual = part["label"].value_counts(normalize=True)

        for label in classes:
            score += abs(
                actual.get(label, 0)
                - df["label"].value_counts(normalize=True)[label]
            )

        actual_size = len(part) / len(df)
        score += 2 * abs(actual_size - target_ratios[name])

    if valid and score < best_score:
        best_score = score
        best_splits = candidate
        best_seed = seed

if best_splits is None:
    raise RuntimeError(
        "No valid split found. Do not use an unverified split."
    )

print("Selected seed:", best_seed)

final_parts = {}

for name, indices in best_splits.items():
    part = df.iloc[indices].copy()

    # Save only the columns needed by the training pipeline
    final_parts[name] = part

    part.to_csv(
        OUTPUT / f"{name}.csv",
        index=False
    )

    print(f"\n{name.upper()}: {len(part)} images")
    print(part["label"].value_counts().to_string())

# Final verification
for a, b in [
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test")
]:
    hashes_a = set(final_parts[a]["sha256"])
    hashes_b = set(final_parts[b]["sha256"])

    vineyards_a = set(final_parts[a]["vineyard_id"])
    vineyards_b = set(final_parts[b]["vineyard_id"])

    assert not hashes_a.intersection(hashes_b)
    assert not vineyards_a.intersection(vineyards_b)

print("\nAll checks passed:")
print("- No duplicate hashes across splits")
print("- No vineyard overlap")
print("- All four classes represented in every split")
print("\nSaved to:", OUTPUT)
