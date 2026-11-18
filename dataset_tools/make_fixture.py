"""Generating a fake dataset with known bounding boxes.

Output (under data/fixture/):
    images/img_000.png ...
    annotations.json   one entry per image with its true box and a fake scene id
"""
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw

WIDTH, HEIGHT = 128, 128
NUM_IMAGES = 40
NUM_SCENES = 8


def make_fixture(out_dir="data/fixture", seed=0):
    rng = random.Random(seed)  # fixed seed: same output every run
    out = Path(out_dir)
    (out / "images").mkdir(parents=True, exist_ok=True)

    records = []
    for i in range(NUM_IMAGES):
        # Random box: at least 20px wide/tall, fully inside the image
        w = rng.randint(20, 60)
        h = rng.randint(20, 60)
        x = rng.randint(0, WIDTH - w)
        y = rng.randint(0, HEIGHT - h)

        # Background color depends on the scene, so images in a scene look alike
        scene = i % NUM_SCENES
        bg = (20 * scene, 40, 80)
        img = Image.new("RGB", (WIDTH, HEIGHT), bg)
        ImageDraw.Draw(img).rectangle([x, y, x + w, y + h], fill=(255, 200, 0))

        name = f"img_{i:03d}.png"
        img.save(out / "images" / name)

        records.append({
            "file": name,
            "scene_id": f"scene_{scene:02d}",
            "bbox_xywh": [x, y, w, h],  # pixels: top-left x, y, width, height
        })

    (out / "annotations.json").write_text(json.dumps(records, indent=2))
    return records


if __name__ == "__main__":
    make_fixture()
    print("Fixture written to data/fixture/")
