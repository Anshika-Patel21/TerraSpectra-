
from pathlib import Path
from collections import defaultdict
import hashlib

DATA_DIR = Path("data/processed/GVLiD_224")

hash_groups = defaultdict(list)

for image_path in DATA_DIR.rglob("*"):
    if image_path.is_file():
        file_hash = hashlib.sha256(
            image_path.read_bytes()
        ).hexdigest()

        hash_groups[file_hash].append(image_path)

duplicate_groups = [
    files for files in hash_groups.values()
    if len(files) > 1
]

print("DUPLICATE IMAGE REPORT")
print("-" * 50)

class_counts = defaultdict(int)

for group in duplicate_groups:
    classes = sorted({p.parent.name for p in group})

    for class_name in classes:
        class_counts[class_name] += len(group)

    print("\nDuplicate group:")
    for image in group:
        print(f"  {image}")

print("\nSUMMARY")
print("-" * 50)
print("Total duplicate groups:", len(duplicate_groups))
print("Total files involved:", sum(map(len, duplicate_groups)))

for class_name, count in sorted(class_counts.items()):
    print(f"{class_name}: {count} files involved")
