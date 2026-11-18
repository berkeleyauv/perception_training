"""Validate a manifest and return a list of readable problems.

An empty list means the manifest passed every check.
"""
from dataset_tools.schema_constants import (
    SOURCE_TYPES,
    ANNOTATION_PROVENANCE,
)

REQUIRED_RECORD_FIELDS = [
    "image_id", "image_path", "sha256", "width", "height",
    "source_type", "scene_id", "instances",
]
REQUIRED_INSTANCE_FIELDS = ["class_name", "bbox_xywh", "annotation_provenance"]


def validate_record(record):
    """Return a list of problem strings for one record."""
    problems = []
    rid = record.get("image_id", "<no image_id>")

    # 1. Required fields present
    for field in REQUIRED_RECORD_FIELDS:
        if field not in record:
            problems.append(f"{rid}: missing field '{field}'")
    if problems:
        return problems  # can't check further without the basics

    # 2. Allowed values
    if record["source_type"] not in SOURCE_TYPES:
        problems.append(f"{rid}: bad source_type '{record['source_type']}'")

    # 3. Instances
    for i, inst in enumerate(record["instances"]):
        for field in REQUIRED_INSTANCE_FIELDS:
            if field not in inst:
                problems.append(f"{rid} instance {i}: missing field '{field}'")
                continue

        prov = inst.get("annotation_provenance")
        if prov not in ANNOTATION_PROVENANCE:
            problems.append(f"{rid} instance {i}: bad provenance '{prov}'")

        bbox = inst.get("bbox_xywh")
        if bbox is not None:
            x, y, w, h = bbox
            if w <= 0 or h <= 0:
                problems.append(f"{rid} instance {i}: box has non-positive size")
            if x < 0 or y < 0 or x + w > record["width"] or y + h > record["height"]:
                problems.append(f"{rid} instance {i}: box outside image bounds")

    return problems


def validate_manifest(manifest):
    """Return a list of problems for the whole manifest."""
    problems = []

    # Duplicate image ids
    seen = set()
    for record in manifest["records"]:
        rid = record.get("image_id")
        if rid in seen:
            problems.append(f"{rid}: duplicate image_id")
        seen.add(rid)

        problems.extend(validate_record(record))

    return problems


if __name__ == "__main__":
    import json

    manifest = json.load(open("data/manifest.json"))
    problems = validate_manifest(manifest)
    if problems:
        print(f"{len(problems)} problem(s) found:")
        for p in problems:
            print(" -", p)
    else:
        print("Manifest is valid: 0 problems")
