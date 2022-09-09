import itertools
import FetchData
import os_convert
import plot

from PinchpointAlgos import getBottlenecks

grid_corner1 = "SX 999 960"
grid_corner2 = "SS 950 010"
grid_corner3 = "SX 970 990"
grid_corner4 = "SX 980 980"

maps = [(grid_corner1, grid_corner3), (grid_corner4, grid_corner2)]

start_loc = os_convert.grid2latlon("SX 997 962")
end_loc = os_convert.grid2latlon("SS 951 003")

way_infos = FetchData.get_ways_from_api(
    maps=maps,
    filtered_highways=["motorway", "service", "primary"],
)

# fyi way_infos can have duplicates in

bottlenecks = getBottlenecks("shortest_detour", way_infos, start_loc, end_loc)

print("Bottlenecks")
for bottleneck in bottlenecks:
    print(f"  {os_convert.latlon2grid(bottleneck)}")

grid_corner_lats, grid_corner_lons = zip(
    *map(os_convert.grid2latlon, itertools.chain(*maps))
)

sorted_lons = sorted([*grid_corner_lons])
sorted_lats = sorted([*grid_corner_lats])
min_x, max_x = sorted_lons[0], sorted_lons[-1]
min_y, max_y = sorted_lats[0], sorted_lats[-1]

plot.plot_latlons(start_loc, end_loc, bottlenecks, min_x, max_x, min_y, max_y)
