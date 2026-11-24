
from pathlib import Path
from collections import defaultdict
import hashlib

DATA_DIR = Path("data/raw/GVLiD/DATASET")

hash_groups = defaultdict(list)

class_counts = {}

for class_folder in DATA_DIR.iterdir():
    if not class_folder.is_dir():
        continue

    files = [
        f for f in class_folder.iterdir()
        if f.is_file()
    ]

    class_counts[class_folder.name] = len(files)

    for file_path in files:
        try:
            file_hash = hashlib.sha256(
                file_path.read_bytes()
            ).hexdigest()

            hash_groups[file_hash].append({
                "class": class_folder.name,
                "filename": file_path.name
            })

        except Exception as error:
            print("Could not read:", file_path, error)

duplicate_groups = [
    group for group in hash_groups.values()
    if len(group) > 1
]

cross_class_groups = [
    group for group in duplicate_groups
    if len(set(item["class"] for item in group)) > 1
]

print("\nORIGINAL DATASET SUMMARY")
print("------------------------")

for class_name, count in class_counts.items():
    print(f"{class_name}: {count}")

print("\nTotal original images:", sum(class_counts.values()))
print("Unique image hashes:", len(hash_groups))
print("Duplicate groups:", len(duplicate_groups))

print(
    "Files involved in duplicates:",
    sum(len(group) for group in duplicate_groups)
)

print("Cross-class duplicate groups:", len(cross_class_groups))

print("\nFIRST 10 DUPLICATE GROUPS")

for index, group in enumerate(duplicate_groups[:10], start=1):
    print(f"\nGroup {index}:")

    for item in group:
        print(f"  {item['class']} / {item['filename']}")

print("\nFIRST 10 CROSS-CLASS GROUPS")

for index, group in enumerate(cross_class_groups[:10], start=1):
    print(f"\nGroup {index}:")

    for item in group:
        print(f"  {item['class']} / {item['filename']}")
