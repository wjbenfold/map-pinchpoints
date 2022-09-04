from typing import List, Optional
from .horizontal_remoteness import getBottlenecks as hrGetBottlenecks
from my_types import LatLon, WayInfo
from .shortest_detour import getBottlenecks as sdGetBottlenecks

methods = {
    "horizontal_remoteness": hrGetBottlenecks,
    "shortest_detour": sdGetBottlenecks,
}


def getBottlenecks(
    method="shortest_detour",
    way_infos: List[WayInfo] = [],
    start_loc: Optional[LatLon] = None,
    end_loc: Optional[LatLon] = None,
):
    return methods[method](way_infos=way_infos, start_loc=start_loc, end_loc=end_loc)


__all__ = ["methods", "getBottlenecks"]
