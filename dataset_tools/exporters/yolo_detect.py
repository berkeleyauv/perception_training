"""Export a split manifest to the YOLO Detect dataset layout."""
import shutil
from pathlib import Path

CLASS_NAMES = ["gate"]  # class id = index in this list


def bbox_to_yolo(bbox_xywh, width, height):
    """Pixel top-left x,y,w,h -> normalized center x,y,w,h."""
    x, y, w, h = bbox_xywh
    return (
        (x + w / 2) / width,
        (y + h / 2) / height,
        w / width,
        h / height,
    )


def export_yolo_detect(records, image_root, out_dir="data/yolo_detect"):
    """Write images, labels, and dataset.yaml. Returns (n_exported, skipped_ids)."""
    out = Path(out_dir)
    image_root = Path(image_root)
    exported, skipped = 0, []

    for split in ("train", "val", "test"):
        (out / "images" / split).mkdir(parents=True, exist_ok=True)
        (out / "labels" / split).mkdir(parents=True, exist_ok=True)

    for r in records:
        # Keep only instances that have a box and a known class
        lines = []
        for inst in r["instances"]:
            if inst["bbox_xywh"] is None or inst["class_name"] not in CLASS_NAMES:
                continue
            cx, cy, w, h = bbox_to_yolo(inst["bbox_xywh"], r["width"], r["height"])
            cls = CLASS_NAMES.index(inst["class_name"])
            lines.append(f"{cls} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

        if not lines:
            skipped.append(r["image_id"])  # no usable label: exclude, don't invent
            continue

        split = r["split"]
        src = image_root / r["image_path"]
        shutil.copy(src, out / "images" / split / src.name)
        (out / "labels" / split / f"{r['image_id']}.txt").write_text("\n".join(lines) + "\n")
        exported += 1

    yaml_text = (
        f"path: {out.resolve()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "names:\n"
        + "".join(f"  {i}: {n}\n" for i, n in enumerate(CLASS_NAMES))
    )
    (out / "dataset.yaml").write_text(yaml_text)
    return exported, skipped
