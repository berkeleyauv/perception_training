from dataset_tools.make_fixture import make_fixture, WIDTH, HEIGHT


def test_fixture_boxes_inside_image(tmp_path):
    records = make_fixture(out_dir=tmp_path)
    assert len(records) == 40
    for r in records:
        x, y, w, h = r["bbox_xywh"]
        assert x >= 0 and y >= 0
        assert x + w <= WIDTH and y + h <= HEIGHT
