from mapa_streamlit.verification import _get_area, selected_bbox_out_of_bounds, selected_bbox_too_large


def test__selected_bbox_too_large() -> None:
    bbox = [
        [
            [6.767578, 43.644026],
            [6.767578, 47.754098],
            [19.248047, 47.754098],
            [19.248047, 43.644026],
            [6.767578, 43.644026],
        ]
    ]
    area = _get_area(bbox)
    assert area == 51.3
    assert selected_bbox_too_large(bbox=bbox, threshold=50) is True
    assert selected_bbox_too_large(bbox=bbox, threshold=60) is False


def test__get_area() -> None:
    bbox = [[1, 1], [1, 3], [3, 1], [3, 3]]
    area = _get_area(bbox=bbox)
    assert area == 5.66


def test_selected_bbox_out_of_bounds() -> None:
    bbox = [
        [
            [-316.683655, 60.233335],
            [-316.683655, 60.239811],
            [108.28125, 60.239811],
            [108.28125, 60.233335],
            [-316.683655, 60.233335],
        ]
    ]

    assert selected_bbox_out_of_bounds(bbox) is False
