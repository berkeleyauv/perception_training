import copy

from dataset_tools.make_fixture import make_fixture
from dataset_tools.importers.fixture_importer import import_fixture
from dataset_tools.splits.scene_split import dedupe, split_by_scene, check_no_leakage


def _records(tmp_path):
    make_fixture(out_dir=tmp_path / "fx")
    return import_fixture(tmp_path / "fx", tmp_path / "m.json")["records"]


def test_dedupe_drops_duplicate_hash(tmp_path):
    recs = _records(tmp_path)
    dup = copy.deepcopy(recs[0])
    dup["image_id"] = "img_copy"
    kept, dropped = dedupe(recs + [dup])
    assert dropped == ["img_copy"]
    assert len(kept) == 40


def test_split_keeps_scenes_whole(tmp_path):
    recs = split_by_scene(_records(tmp_path))
    assert check_no_leakage(recs) == []
    assert {r["split"] for r in recs} == {"train", "val", "test"}


def test_split_is_reproducible(tmp_path):
    a = split_by_scene(_records(tmp_path), seed=1)
    b = split_by_scene(_records(tmp_path), seed=1)
    assert [r["split"] for r in a] == [r["split"] for r in b]
