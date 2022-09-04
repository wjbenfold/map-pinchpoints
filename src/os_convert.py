import OSGridConverter as osgc
from typing import Tuple, Union


def grid2latlon(grid: str) -> Tuple[float, float]:
    ll = osgc.grid2latlong(grid, tag="WGS84")
    return float(ll.latitude), float(ll.longitude)


def latlon2grid(lat: float, lon: float) -> str:
    return osgc.latlon2grid(lat, lon)


def split_grid(grid: str) -> Tuple[str, int, int]:
    letters, xx, yy = grid.split(" ")
    return letters, int(xx), int(yy)


def join_grid(
    letters: str, xx: Union[int, str], yy: Union[int, str]
) -> Tuple[str, int, int]:
    return " ".join([letters, str(xx), str(yy)])
