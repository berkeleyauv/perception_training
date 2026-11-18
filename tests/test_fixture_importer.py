from dataset_tools.make_fixture import make_fixture
from dataset_tools.importers.fixture_importer import import_fixture
from dataset_tools.schema_constants import SOURCE_TYPES, ANNOTATION_PROVENANCE


def test_import_fixture(tmp_path):
    make_fixture(out_dir=tmp_path / "fx")
    manifest = import_fixture(tmp_path / "fx", tmp_path / "manifest.json")

    assert len(manifest["records"]) == 40
    for r in manifest["records"]:
        assert r["source_type"] in SOURCE_TYPES
        assert len(r["sha256"]) == 64
        assert r["instances"][0]["annotation_provenance"] in ANNOTATION_PROVENANCE
        assert r["instances"][0]["keypoints"] is None
