import itertools
from typing import List, Tuple
import overpy
from my_types import LatLon, Segment, WayInfo
import overpass_query


def get_ways_from_api(
    maps: List[Tuple[str, str]], filtered_highways: List[str]
) -> List[WayInfo]:

    results: List[overpy.Result] = overpass_query.get_highways_from_maps(maps)

    return waysFromResults(results, filtered_highways)


def get_ways_from_file(filename: str, filtered_highways: List[str]) -> List[WayInfo]:

    result: List[overpy.Result] = overpass_query.get_highways(source_file=filename)

    return waysFromResults([result], filtered_highways)


def waysFromResults(
    results: List[overpy.Result], filtered_highways: List[str]
) -> List[WayInfo]:
    def way_filter(way: overpy.Way) -> bool:
        if way.tags.get("highway") in filtered_highways:
            return False
        return True

    all_ways = itertools.chain(*[result.ways for result in results])

    usable_ways = filter(way_filter, all_ways)

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
