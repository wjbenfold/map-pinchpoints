from typing import Set
import FetchData
from my_types import LatLon
import os_convert
import plot

grid_corner1 = "SX 999 960"
grid_corner2 = "SS 95 01"

ll_corner1 = os_convert.grid2latlon(grid_corner1)
ll_corner2 = os_convert.grid2latlon(grid_corner2)

lat_corner1, lon_corner1 = ll_corner1
lat_corner2, lon_corner2 = ll_corner2

min_x, max_x = sorted((lon_corner1, lon_corner2))
min_y, max_y = sorted((lat_corner1, lat_corner2))

way_infos = FetchData.get_ways(
    maps=[(ll_corner1, ll_corner2)],
    filtered_highways=[],
)

all_lat_lons: Set[LatLon] = set()

for way_info in way_infos:
    for segment in way_info.segments:
        all_lat_lons.add(segment.start_node)
        all_lat_lons.add(segment.end_node)

node_one = all_lat_lons.pop()
node_two = all_lat_lons.pop()

plot.plot_latlons(node_one, node_two, list(all_lat_lons), min_x, max_x, min_y, max_y)
