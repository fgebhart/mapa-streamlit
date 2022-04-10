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


def selected_bbox_too_large(geometry: dict, threshold: float) -> bool:
    bbox = geometry["coordinates"][0]
    area = _get_area(bbox=bbox)
    log.info(f"📏  area with size: {area} was selected, threshold is: {threshold}")
    return area > threshold


class CoordinateBoundaries:
    lon_min: int = -180
    lat_min: int = -90
    lon_max: int = 180
    lat_max: int = 90


def selected_bbox_in_boundary(geometry: dict, boundary: CoordinateBoundaries = CoordinateBoundaries) -> bool:
    bbox = geometry["coordinates"][0]
    for coordinate in bbox:
        lon = coordinate[0]
        lat = coordinate[1]
        if lon < boundary.lon_min or lon > boundary.lon_max:
            return False
        elif lat < boundary.lat_min or lat > boundary.lat_max:
            return False
    return True
