"""Import the fixture dataset into the common manifest format.

Reads:  <fixture_dir>/annotations.json and <fixture_dir>/images/*.png
Writes: <out_path> (manifest.json), one record per image.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image

from dataset_tools.schema_constants import SCHEMA_VERSION


def sha256_of_file(path):
    """Fingerprint of a file's bytes. Identical images give identical hashes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def import_fixture(fixture_dir="data/fixture", out_path="data/manifest.json"):
    fixture = Path(fixture_dir)
    raw = json.loads((fixture / "annotations.json").read_text())

    records = []
    for entry in raw:
        img_path = fixture / "images" / entry["file"]
        with Image.open(img_path) as img:
            width, height = img.size

        records.append({
            "image_id": Path(entry["file"]).stem,
            "image_path": f"images/{entry['file']}",   # relative, not absolute
            "sha256": sha256_of_file(img_path),
            "width": width,
            "height": height,
            "source_type": "synthetic",
            "scene_id": entry["scene_id"],
            "camera_id": None,
            "timestamp": None,
            "calibration_ref": None,
            "review_status": None,
            "instances": [
                {
                    "class_name": "gate",
                    "bbox_xywh": entry["bbox_xywh"],
                    "mask": None,
                    "keypoints": None,
                    "annotation_provenance": "rendered_gt",
                }
            ],
        })

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "source": str(fixture_dir),
        "records": records,
    }
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    m = import_fixture()
    print(f"Wrote manifest with {len(m['records'])} records")
