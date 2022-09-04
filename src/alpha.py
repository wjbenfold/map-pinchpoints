import overpass_query
import overpy
import os_convert
from my_types import WayInfo, Segment, LatLon
import plot

# from PinchpointAlgos.horizontal_remoteness import getBottlenecks
from PinchpointAlgos.shortest_detour import getBottlenecks

grid_corner1 = "SX 999 960"
grid_corner2 = "SS 95 01"

start_loc = LatLon(*os_convert.grid2latlon("SX 997 962"))
end_loc = LatLon(*os_convert.grid2latlon("SS 951 003"))

lat_corner1, lon_corner1 = os_convert.grid2latlon(grid_corner1)
lat_corner2, lon_corner2 = os_convert.grid2latlon(grid_corner2)

min_x, max_x = sorted((lon_corner1, lon_corner2))
min_y, max_y = sorted((lat_corner1, lat_corner2))


result: overpy.Result = overpass_query.get_highways_from_maps(
    [(grid_corner1, grid_corner2)]
)


def waysFromResult(result, filtered_highways):
    def way_filter(way: overpy.Way) -> bool:
        if way.tags.get("highway") in filtered_highways:
            return False
        return True

    usable_ways = filter(way_filter, result.ways)

    usable_way_infos = []

    for way in usable_ways:
        usable_way_infos.append(
            WayInfo(
                way.tags.get("name", "n/a"),
                way.tags.get("highway", "n/a"),
                [
                    Segment(
                        LatLon(float(way.nodes[ii].lat), float(way.nodes[ii].lon)),
                        LatLon(float(way.nodes[ii + 1].lat), float(way.nodes[ii + 1].lon)),
                    )
                    for ii in range(len(way.nodes) - 1)
                ],
            )
        )

    return usable_way_infos


usable_way_infos = waysFromResult(result, ["motorway", "service", "primary"])


bottlenecks = getBottlenecks(usable_way_infos, start_loc, end_loc)

print("Bottlenecks")
for bottleneck in bottlenecks:
    print(f"  {bottleneck}")

plot.plot_latlons(start_loc, end_loc, bottlenecks, min_x, max_x, min_y, max_y)
