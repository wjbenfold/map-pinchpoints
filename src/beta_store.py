import FetchData
import os_convert

from shortest_detour import getBottlenecks

way_infos = FetchData.get_ways_from_file(
    filtered_highways=["motorway", "service", "primary"],
)

# fyi way_infos can have duplicates in

bottlenecks = getBottlenecks(way_infos)

print("Bottlenecks")
for bottleneck in bottlenecks:
    (node1, node2, weight), detour_weight = bottleneck
    if detour_weight < 10:
        break
    print(f"  {os_convert.latlon2grid(node1, 3)} to {os_convert.latlon2grid(node2, 3)} detour {round(detour_weight)}")
    # input()
