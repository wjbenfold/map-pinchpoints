import csv
import functools
import itertools
from typing import List, Tuple
import shapely.geometry as sg
import networkx as nx

import get_data
from my_types import LatLon, WayInfo
import os_convert
from shortest_detour import graphFromWayInfos


def load_csv(csv_filename):
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


def generate_wkt(config):
    unfiltered_way_infos = get_data.get_ways_from_file(
        config["download"]["output_filename_xml"],
        filtered_highways=config["pinchpoints"]["filtered_highways"],
    )

    min_lon = config["outputs"]["wkt"]["min_lon"]
    max_lon = config["outputs"]["wkt"]["max_lon"]
    min_lat = config["outputs"]["wkt"]["min_lat"]
    max_lat = config["outputs"]["wkt"]["max_lat"]

    wayinfo_filter = get_wayinfo_filter(min_lon, max_lon, min_lat, max_lat)
    way_infos = filter(wayinfo_filter, unfiltered_way_infos)
    G = graphFromWayInfos(way_infos)

    pinchpoint_filter = get_pinchpoint_filter(
        min_lon, max_lon, min_lat, max_lat, config["outputs"]["wkt"]["min_detour"]
    )
    unfiltered_data = load_csv(config["pinchpoints"]["output_filename_csv"])
    pinchpoint_list = filter(pinchpoint_filter, unfiltered_data)

    with open(config["outputs"]["wkt"]["output_filename_csv"], "w+") as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow(["WKT", "detourLength", "gridRefs"])
        for node1, node2, detour_weight in pinchpoint_list:
            shortest_path = nx.dijkstra_path(G, node1, node2, "weight")
            csv_writer.writerow(
                [
                    pathToWkt(shortest_path),
                    round(detour_weight, 2),
                    f"{os_convert.latlon2grid(node1, 3)} to {os_convert.latlon2grid(node2, 3)}",
                ]
            )


def generate_phone_csv(config):

    pinchpoint_list = load_csv(config["pinchpoints"]["output_filename_csv"])

    with open(config["outputs"]["phone_csv"]["output_filename_csv"], "w+") as fh:
        csv_writer = csv.writer(fh)
        for node1, node2, detour_weight in pinchpoint_list:
            if detour_weight < config["outputs"]["phone_csv"]["min_detour"]:
                break
            csv_writer.writerow(
                [
                    node1.lat,
                    node1.lon,
                    node2.lat,
                    node2.lon,
                    os_convert.latlon2grid(node1, 3),
                    os_convert.latlon2grid(node2, 3),
                    round(detour_weight, 2),
                ]
            )
