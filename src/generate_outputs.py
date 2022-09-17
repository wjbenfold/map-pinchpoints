import csv
import functools
import itertools
from typing import List, Tuple
import shapely.geometry as sg
import networkx as nx

import FetchData
from my_types import LatLon, WayInfo
import os_convert
from shortest_detour import graphFromWayInfos

csv_filename = "detours_min_5.csv"
google_csv_filename = "google_wkts.csv"
phone_csv_filename = "phone_data.csv"


def load_csv():
    pinchpoint_list: List[Tuple[LatLon, LatLon, float]] = []
    with open(csv_filename, "r") as fh:
        reader = csv.DictReader(
            fh, fieldnames=["lat1", "lon1", "lat2", "lon2", "detour"]
        )
        for row in reader:
            pinchpoint_list.append(
                (
                    LatLon(float(row["lat1"]), float(row["lon1"])),
                    LatLon(float(row["lat2"]), float(row["lon2"])),
                    float(row["detour"]),
                )
            )
    return pinchpoint_list


def get_latlon_filter(min_lon, max_lon, min_lat, max_lat):
    def latlon_filter(latlon):
        lat, lon = latlon
        return (
            lat > min_lat
            and lat < max_lat  # noqa: W503
            and lon > min_lon  # noqa: W503
            and lon < max_lon  # noqa: W503
        )

    return latlon_filter


def get_wayinfo_filter(min_lon, max_lon, min_lat, max_lat):
    def wayinfo_filter(wayinfo: WayInfo):
        return functools.reduce(
            lambda x, y: x and y, itertools.chain(*wayinfo.segments)
        )

    return wayinfo_filter


def get_pinchpoint_filter(min_lon, max_lon, min_lat, max_lat, min_detour):
    def pinchpoint_filter(pinchpoint):
        node1, node2, detour = pinchpoint
        latlon_filter = get_latlon_filter(min_lon, max_lon, min_lat, max_lat)
        return latlon_filter(node1) and latlon_filter(node2) and detour > min_detour

    return pinchpoint_filter


def pathToWkt(path):
    path = map(lambda x: (x[1], x[0]), path)
    shapely_line = sg.LineString(path)
    return shapely_line.wkt


def generate_wkt(min_lon, max_lon, min_lat, max_lat, min_detour):
    unfiltered_way_infos = FetchData.get_ways_from_file(
        filtered_highways=["motorway", "service", "primary"],
    )
    wayinfo_filter = get_wayinfo_filter(min_lon, max_lon, min_lat, max_lat)
    way_infos = filter(wayinfo_filter, unfiltered_way_infos)
    G = graphFromWayInfos(way_infos)

    pinchpoint_filter = get_pinchpoint_filter(
        min_lon, max_lon, min_lat, max_lat, min_detour
    )
    unfiltered_data = load_csv()
    pinchpoint_list = filter(pinchpoint_filter, unfiltered_data)

    with open(google_csv_filename, "w+") as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow(["WKT", "description"])
        for node1, node2, detour_weight in pinchpoint_list:
            shortest_path = nx.dijkstra_path(G, node1, node2, "weight")
            csv_writer.writerow([pathToWkt(shortest_path), round(detour_weight, 2)])


def generate_phone_csv(min_detour):

    pinchpoint_list = load_csv()

    with open(phone_csv_filename, "w+") as fh:
        csv_writer = csv.writer(fh)
        for node1, node2, detour_weight in pinchpoint_list:
            if detour_weight < min_detour:
                break
            csv_writer.writerow(
                [
                    node1.lat,
                    node1.lon,
                    node2.lat,
                    node2.lon,
                    os_convert.latlon2grid(node1),
                    os_convert.latlon2grid(node2),
                    round(detour_weight, 2),
                ]
            )


if __name__ == "__main__":
    # generate_wkt(-0.26237, 0.96858, 51.77382, 52.23979, 3)

    generate_phone_csv(3)
