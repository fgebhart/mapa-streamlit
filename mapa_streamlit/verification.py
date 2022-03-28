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


def _selected_bbox_too_large(geometry: dict, threshold: float) -> bool:
    bbox = geometry["coordinates"][0]
    area = _get_area(bbox=bbox)
    log.info(f"📏  area with size: {area} was selected, threshold is: {threshold}")
    return area > threshold
