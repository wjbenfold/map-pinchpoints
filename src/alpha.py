# Known bugs
#   - The algorithm drops half of loops because the network can't distinguish
#     them
#   - No route around something should make it a pinchpoint (at least in small
#     networks)
#
# Additional features:
#   - Location input
#   - Portablility
#   - Multiple maps
#   - Draw the whole pinchpoint segment
#   - Cache sections of map
#   - YAML config?

import FetchData
import os_convert
import plot

from PinchpointAlgos import getBottlenecks

grid_corner1 = "SX 999 960"
grid_corner2 = "SS 95 01"

ll_corner1 = os_convert.grid2latlon(grid_corner1)
ll_corner2 = os_convert.grid2latlon(grid_corner2)

start_loc = os_convert.grid2latlon("SX 997 962")
end_loc = os_convert.grid2latlon("SS 951 003")

lat_corner1, lon_corner1 = ll_corner1
lat_corner2, lon_corner2 = ll_corner2

min_x, max_x = sorted((lon_corner1, lon_corner2))
min_y, max_y = sorted((lat_corner1, lat_corner2))


way_infos = FetchData.get_ways(
    maps=[(ll_corner1, ll_corner2)],
    filtered_highways=["motorway", "service", "primary"],
)

bottlenecks = getBottlenecks("shortest_detour", way_infos, start_loc, end_loc)

print("Bottlenecks")
for bottleneck in bottlenecks:
    print(f"  {bottleneck}")

plot.plot_latlons(start_loc, end_loc, bottlenecks, min_x, max_x, min_y, max_y)
