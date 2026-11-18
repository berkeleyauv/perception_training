from dataset_tools.schema_constants import SOURCE_TYPES, SCHEMA_VERSION

def test_source_types():
    assert SOURCE_TYPES == {"real", "synthetic"}

def test_version_is_draft():
    assert "draft" in SCHEMA_VERSION
