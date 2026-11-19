from dataset_tools.exporters.yolo_detect import bbox_to_yolo, export_yolo_detect
from dataset_tools.make_fixture import make_fixture
from dataset_tools.importers.fixture_importer import import_fixture
from dataset_tools.splits.scene_split import split_by_scene


def test_bbox_conversion():
    cx, cy, w, h = bbox_to_yolo([5, 33, 44, 46], 128, 128)
    assert round(cx, 4) == 0.2109
    assert round(cy, 4) == 0.4375
    assert round(w, 4) == 0.3438
    assert round(h, 4) == 0.3594


def test_export_skips_records_without_box(tmp_path):
    make_fixture(out_dir=tmp_path / "fx")
    recs = import_fixture(tmp_path / "fx", tmp_path / "m.json")["records"]
    recs = split_by_scene(recs)
    recs[0]["instances"][0]["bbox_xywh"] = None  # no label for this one
    n, skipped = export_yolo_detect(recs, tmp_path / "fx", tmp_path / "out")
    assert skipped == [recs[0]["image_id"]]
    assert n == 39
    assert (tmp_path / "out" / "dataset.yaml").exists()
