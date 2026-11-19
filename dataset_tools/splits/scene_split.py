"""Deduplicate a manifest by image hash, then split it by scene (no leakage)."""
import random


def dedupe(records):
    """Keep the first record for each sha256. Returns (kept, dropped_ids)."""
    seen = set()
    kept, dropped = [], []
    for r in records:
        if r["sha256"] in seen:
            dropped.append(r["image_id"])
        else:
            seen.add(r["sha256"])
            kept.append(r)
    return kept, dropped


def split_by_scene(records, fractions=(0.6, 0.2, 0.2), seed=0):
    """Assign each record a 'split' of train/val/test, keeping scenes whole."""
    scenes = sorted({r["scene_id"] for r in records})
    random.Random(seed).shuffle(scenes)

    n = len(scenes)
    n_train = max(1, round(n * fractions[0]))
    n_val = max(1, round(n * fractions[1]))
    scene_to_split = {}
    for i, s in enumerate(scenes):
        if i < n_train:
            scene_to_split[s] = "train"
        elif i < n_train + n_val:
            scene_to_split[s] = "val"
        else:
            scene_to_split[s] = "test"

    for r in records:
        r["split"] = scene_to_split[r["scene_id"]]
    return records


def check_no_leakage(records):
    """Return a list of scenes that appear in more than one split."""
    splits_by_scene = {}
    for r in records:
        splits_by_scene.setdefault(r["scene_id"], set()).add(r["split"])
    return [s for s, sp in splits_by_scene.items() if len(sp) > 1]
