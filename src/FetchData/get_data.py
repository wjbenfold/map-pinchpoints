import overpy
from my_types import LatLon, Segment, WayInfo
import overpass_query


def get_ways(maps, filtered_highways):

    result: overpy.Result = overpass_query.get_highways_from_maps(maps)

    return waysFromResult(result, filtered_highways)


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
                        LatLon(
                            float(way.nodes[ii + 1].lat), float(way.nodes[ii + 1].lon)
                        ),
                    )
                    for ii in range(len(way.nodes) - 1)
                ],
            )
        )

    return usable_way_infos
