"""One command: import fixture -> validate -> dedupe -> split -> export YOLO Detect."""
from dataset_tools.make_fixture import make_fixture
from dataset_tools.importers.fixture_importer import import_fixture
from dataset_tools.validators.manifest_validator import validate_manifest
from dataset_tools.splits.scene_split import dedupe, split_by_scene, check_no_leakage
from dataset_tools.exporters.yolo_detect import export_yolo_detect


def main():
    make_fixture("data/fixture")
    manifest = import_fixture("data/fixture", "data/manifest.json")

    problems = validate_manifest(manifest)
    if problems:
        raise SystemExit("Validation failed:\n" + "\n".join(problems))

    records, dropped = dedupe(manifest["records"])
    records = split_by_scene(records, seed=0)
    assert check_no_leakage(records) == [], "scene leakage detected"

    n, skipped = export_yolo_detect(records, "data/fixture", "data/yolo_detect")
    print(f"Dropped duplicates: {len(dropped)}")
    print(f"Exported {n} images, skipped {len(skipped)} (no usable label)")


if __name__ == "__main__":
    main()
