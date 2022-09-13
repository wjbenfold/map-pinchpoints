import OSGridConverter as osgc
from typing import Union

from my_types import LatLon


def grid2latlon(grid: str) -> LatLon:
    ll = osgc.grid2latlong(grid, tag="WGS84")
    return LatLon(float(ll.latitude), float(ll.longitude))


def latlon2grid(latlon: LatLon, precision: Union[None, int] = None) -> str:
    full_precision = osgc.latlong2grid(*latlon)
    if precision is None:
        return full_precision
    else:
        letters, first_num, second_num = str(full_precision).split(" ")
        return f"{letters} {first_num[:precision]} {second_num[:precision]}"
