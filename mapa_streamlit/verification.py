import logging
from math import sqrt
from typing import List

log = logging.getLogger(__name__)


def _get_distance(c1: List[float], c2: List[float]) -> float:
    return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def _get_area(bbox: List[List[float]]) -> float:
    width = _get_distance(c1=bbox[0], c2=bbox[1])
    height = _get_distance(c1=bbox[1], c2=bbox[2])
    return round(abs(width * height), 2)


def selected_bbox_too_large(bbox: List[List[float]], threshold: float) -> bool:
    area = _get_area(bbox=bbox)
    log.info(f"area with size: {area} was selected, threshold is: {threshold}")
    return area > threshold


def selected_bbox_out_of_bounds(bbox: List[List[float]]) -> bool:
    out_of_bounds = False
    # TODO refactor this function
    for coordinate in bbox:
        # check first coordinate
        if -180 < coordinate[0] < 180:
            out_of_bounds = False
        else:
            out_of_bounds = True
        # check second coordinate
        if -90 < coordinate[1] < 90:
            out_of_bounds = False
        else:
            out_of_bounds = True
    return out_of_bounds
