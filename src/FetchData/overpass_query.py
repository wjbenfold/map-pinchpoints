import pickle
from typing import List, Tuple
import overpy
import os_convert
from my_types import LatLon
import sys
from pathlib import Path

pickle_path = "cache.p"
source_file = "map.xml"


def get_highways(lat_min=None, lon_min=None, lat_max=None, lon_max=None, from_file: bool = False):

    api = overpy.Overpass()

    if from_file:

        with open(source_file, "r+") as fh:

            result = api.parse_xml(fh.read())

    else:

        if None in [lat_min, lon_min, lat_max, lon_max]:
            raise Exception("Full supply of latlons or file must be provided")

        retries = 3

        while True:
            try:
                result = api.query(
                    f"""
                    way({lat_min},{lon_min},{lat_max},{lon_max}) ["highway"];
                    (._;>;);
                    out body;
                    """
                )
            except Exception:
                if retries > 0:
                    retries -= 1
                    continue
                raise
            break

    return result


def get_highways_by_corners(corner1: LatLon, corner2: LatLon) -> overpy.Result:
    if Path(pickle_path).exists():
        with open(pickle_path, "rb") as fh:
            cached_data = pickle.load(fh)
    else:
        cached_data = {}

    map_key = (corner1, corner2)

    if "--use-cache" in sys.argv and map_key in cached_data:
        return cached_data[map_key]

    lat1, lon1 = corner1
    lat2, lon2 = corner2
    return_val = get_highways(
        min(lat1, lat2),
        min(lon1, lon2),
        max(lat1, lat2),
        max(lon1, lon2),
    )

    cached_data[map_key] = return_val

    with open(pickle_path, "wb") as fh:
        print("Updating cache")
        pickle.dump(cached_data, fh)

    return return_val


def get_highways_from_maps(maps: List[Tuple[str, str]]) -> List[overpy.Result]:
    results = []
    for corner1, corner2 in maps:

        results.append(
            get_highways_by_corners(
                os_convert.grid2latlon(corner1),
                os_convert.grid2latlon(corner2),
            )
        )

    return results


def get_highways_from_map(map: Tuple[str, str]):

    return get_highways_from_maps([map])
