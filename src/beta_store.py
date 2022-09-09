import itertools
import FetchData
import os_convert
import plot

from PinchpointAlgos import getBottlenecks

way_infos = FetchData.get_ways_from_file(
    filtered_highways=["motorway", "service", "primary"],
)

# fyi way_infos can have duplicates in

bottlenecks = getBottlenecks("shortest_detour", way_infos, None, None)

print("Bottlenecks")
for bottleneck in bottlenecks:
    print(f"  {os_convert.latlon2grid(bottleneck)}")
