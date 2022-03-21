from mapa_streamlit.verification import _get_area, _selected_bbox_too_large


def test__selected_bbox_too_large() -> None:
    geometry = {
        "type": "Polygon",
        "coordinates": [
            [
                [6.767578, 43.644026],
                [6.767578, 47.754098],
                [19.248047, 47.754098],
                [19.248047, 43.644026],
                [6.767578, 43.644026],
            ]
        ],
    }
    area = _get_area(geometry["coordinates"][0])
    assert area == 51.3
    assert _selected_bbox_too_large(geometry=geometry, threshold=50) is True
    assert _selected_bbox_too_large(geometry=geometry, threshold=60) is False


def test__get_area() -> None:
    bbox = [[1, 1], [1, 3], [3, 1], [3, 3]]
    area = _get_area(bbox=bbox)
    assert area == 5.66
