import OSGridConverter as osgc
from typing import Tuple, Union

from my_types import LatLon


def grid2latlon(grid: str) -> LatLon:
    ll = osgc.grid2latlong(grid, tag="WGS84")
    return LatLon(float(ll.latitude), float(ll.longitude))


def latlon2grid(latlon: LatLon) -> str:
    return osgc.latlon2grid(*latlon)


def split_grid(grid: str) -> Tuple[str, int, int]:
    letters, xx, yy = grid.split(" ")
    return letters, int(xx), int(yy)


def join_grid(
    letters: str, xx: Union[int, str], yy: Union[int, str]
) -> str:
    return " ".join([letters, str(xx), str(yy)])
