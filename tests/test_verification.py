from mapa_streamlit.verification import _get_area, selected_bbox_in_boundary, selected_bbox_too_large


def test_selected_bbox_too_large() -> None:
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
    assert selected_bbox_too_large(geometry=geometry, threshold=50) is True
    assert selected_bbox_too_large(geometry=geometry, threshold=60) is False


def test__get_area() -> None:
    bbox = [[1, 1], [1, 3], [3, 1], [3, 3]]
    area = _get_area(bbox=bbox)
    assert area == 5.66


def test_selected_bbox_in_boundary() -> None:
    valid_bbox = {
        "type": "Polygon",
        "coordinates": [
            [
                [8.076906, 48.098505],
                [8.076906, 48.115011],
                [8.107111, 48.115011],
                [8.107111, 48.098505],
                [8.076906, 48.098505],
            ]
        ],
    }
    assert selected_bbox_in_boundary(valid_bbox) is True

    # longitude too small
    invalid_bbox = valid_bbox.copy()
    invalid_bbox["coordinates"][0][0] = [-200.0, 50.0]
    assert selected_bbox_in_boundary(invalid_bbox) is False

    # longitude too large
    invalid_bbox = valid_bbox.copy()
    invalid_bbox["coordinates"][0][0] = [200.0, 50.0]
    assert selected_bbox_in_boundary(invalid_bbox) is False

    # latitude too small
    invalid_bbox = valid_bbox.copy()
    invalid_bbox["coordinates"][0][0] = [50.0, -100.0]
    assert selected_bbox_in_boundary(invalid_bbox) is False

    # latitude too large
    invalid_bbox = valid_bbox.copy()
    invalid_bbox["coordinates"][0][0] = [50.0, 100.0]
    assert selected_bbox_in_boundary(invalid_bbox) is False
