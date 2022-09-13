import csv
import FetchData
import os_convert

from shortest_detour import getBottlenecks

way_infos = FetchData.get_ways_from_file(
    filtered_highways=["motorway", "service", "primary"],
)

# fyi way_infos can have duplicates in

bottlenecks = getBottlenecks(way_infos)

min_detour = 0.5

print("Bottlenecks")

with open(f"detours_min_{int(min_detour*10)}.csv", "w+") as fh:
    csv_writer = csv.writer(fh)
    for bottleneck in bottlenecks:
        (node1, node2, weight), detour_weight = bottleneck
        if detour_weight < min_detour:
            break
        print(
            f"  {os_convert.latlon2grid(node1, 3)} to {os_convert.latlon2grid(node2, 3)} detour {round(detour_weight)}"
        )

        csv_writer.writerow([node1.lat, node1.lon, node2.lat, node2.lon, detour_weight])
