import pickle
import overpy
import os_convert
import sys
from pathlib import Path

pickle_path = "cache.p"


def get_highways(lat_min, lon_min, lat_max, lon_max):

    # print("get_highways args", lat_min, lon_min, lat_max, lon_max)

    api = overpy.Overpass()

    result = api.query(
        f"""
        way({lat_min},{lon_min},{lat_max},{lon_max}) ["highway"];
        (._;>;);
        out body;
        """
    )

    return result


def get_highways_by_corners(corner1, corner2):
    if "--use-cache" in sys.argv and Path(pickle_path).exists():
        with open(pickle_path, "rb") as fh:
            return pickle.load(fh)
    lat1, lon1 = os_convert.grid2latlon(corner1)
    lat2, lon2 = os_convert.grid2latlon(corner2)
    return_val = get_highways(
        min(lat1, lat2), min(lon1, lon2), max(lat1, lat2), max(lon1, lon2)
    )
    with open(pickle_path, "wb") as fh:
        print("Updating cache")
        pickle.dump(return_val, fh)
    return return_val


def get_highways_from_maps(maps):
    try:
        (corners,) = maps
        corner1, corner2 = corners
    except ValueError:
        raise NotImplementedError(
            "get_highways_from_maps only supports a single map specified by two corners currently"
        )

    return get_highways_by_corners(corner1, corner2)
