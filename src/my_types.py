from typing import NamedTuple, List


class LatLon(NamedTuple):
    lat: float
    lon: float


class Segment(NamedTuple):
    start_node: LatLon
    end_node: LatLon


class WayInfo(NamedTuple):
    name: str
    type: str
    segments: List[Segment]
