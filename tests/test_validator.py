import copy
import json

from dataset_tools.make_fixture import make_fixture
from dataset_tools.importers.fixture_importer import import_fixture
from dataset_tools.validators.manifest_validator import validate_manifest


def _good_manifest(tmp_path):
    make_fixture(out_dir=tmp_path / "fx")
    return import_fixture(tmp_path / "fx", tmp_path / "manifest.json")


def test_clean_manifest_has_no_problems(tmp_path):
    assert validate_manifest(_good_manifest(tmp_path)) == []


def test_box_outside_image_is_caught(tmp_path):
    m = _good_manifest(tmp_path)
    m["records"][0]["instances"][0]["bbox_xywh"] = [100, 100, 60, 60]  # sticks out
    problems = validate_manifest(m)
    assert any("outside image bounds" in p for p in problems)


def test_bad_source_type_is_caught(tmp_path):
    m = _good_manifest(tmp_path)
    m["records"][0]["source_type"] = "banana"
    problems = validate_manifest(m)
    assert any("bad source_type" in p for p in problems)


def test_missing_field_is_caught(tmp_path):
    m = _good_manifest(tmp_path)
    del m["records"][0]["sha256"]
    problems = validate_manifest(m)
    assert any("missing field 'sha256'" in p for p in problems)


def test_duplicate_image_id_is_caught(tmp_path):
    m = _good_manifest(tmp_path)
    m["records"][1] = copy.deepcopy(m["records"][0])
    problems = validate_manifest(m)
    assert any("duplicate image_id" in p for p in problems)
