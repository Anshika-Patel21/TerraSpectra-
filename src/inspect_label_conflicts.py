
from pathlib import Path
from PIL import Image, ImageDraw

RAW_ROOT = Path("data/raw/GVLiD/DATASET")
OUTPUT_DIR = Path("reports")
OUTPUT_DIR.mkdir(exist_ok=True)

examples = [
    {
        "title": "Conflict 1",
        "black_rot": RAW_ROOT / "Black rot" / "black rot793.jpg",
        "esca": RAW_ROOT / "esca" / "esca002.jpg",
    },
    {
        "title": "Conflict 2",
        "black_rot": RAW_ROOT / "Black rot" / "black rot801.jpg",
        "esca": RAW_ROOT / "esca" / "esca248.jpg",
    },
]

canvas = Image.new("RGB", (1200, 1350), "white")
draw = ImageDraw.Draw(canvas)

for i, item in enumerate(examples):
    y = i * 660

    draw.text((30, y + 10), item["title"], fill="black")

    for j, label in enumerate(["black_rot", "esca"]):
        image = Image.open(item[label]).convert("RGB")
        image.thumbnail((520, 560))

        x = 40 + j * 580

        canvas.paste(image, (x, y + 60))
        draw.text(
            (x, y + 35),
            label.replace("_", " ").upper(),
            fill="black"
        )

output_path = OUTPUT_DIR / "label_conflict_visual_review.png"
canvas.save(output_path)

print("Comparison image saved:", output_path.resolve())
