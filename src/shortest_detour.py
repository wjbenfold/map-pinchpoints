from typing import List
import networkx as nx
from my_types import WayInfo
import numpy as np

# WayInfo(name: str, type: str, segments: List[Segment])
# Segment(start_node: LatLon, end_node: LatLon)
# LatLon(lat: float, lon: float)


def getWeight(segment):
    (lat1, lon1), (lat2, lon2) = segment
    rlat1 = np.radians(lat1)
    rlon1 = np.radians(lon1)
    rlat2 = np.radians(lat2)
    rlon2 = np.radians(lon2)
    return (
        np.arccos(
            np.sin(rlat1) * np.sin(rlat2)
            + np.cos(rlat1) * np.cos(rlat2) * np.cos(rlon2 - rlon1)  # noqa: W503
        )
        * 6371  # noqa: W503
    )


def graphFromWayInfos(way_infos):
    G = nx.Graph()

    def segmentGen(way_infos):
        for way_info in way_infos:
            for segment in way_info.segments:
                weight = getWeight(segment)
                yield *segment, {"weight": weight}

    G.add_edges_from(segmentGen(way_infos))

    return G


def getBottlenecks(way_infos: List[WayInfo], *args, **kwargs):

    G = graphFromWayInfos(way_infos)

    while True:
        unary_nodes = [*map(lambda y: y[0], filter(lambda x: x[1] == 1, G.degree()))]
        if not unary_nodes:
            break
        G.remove_nodes_from(unary_nodes)

    binary_nodes = [*map(lambda y: y[0], filter(lambda x: x[1] == 2, G.degree()))]

    for b_node in binary_nodes:
        try:
            neighbour1, neighbour2 = nx.neighbors(G, b_node)
            new_weight = (
                G[neighbour1][b_node]["weight"] + G[neighbour2][b_node]["weight"]
            )
        except ValueError:
            # print("loop including", b_node)
            continue
        if G.has_edge(neighbour1, neighbour2):
            pass  # Because our new edge would wipe out this one
        else:
            G.add_edge(neighbour1, neighbour2, weight=new_weight)
            G.remove_node(b_node)

    while True:
        unary_nodes = [*map(lambda y: y[0], filter(lambda x: x[1] == 1, G.degree()))]
        if not unary_nodes:
            break
        G.remove_nodes_from(unary_nodes)

    detour_weights = []

    for node1, node2, edge_data in [*G.edges(data=True)]:

        G.remove_edge(node1, node2)

        try:
            detour_weight = (
                nx.dijkstra_path_length(G, node1, node2) - edge_data["weight"]
            )
        except nx.NetworkXNoPath:
            G.add_edge(node1, node2, **edge_data)
            continue

        G.add_edge(node1, node2, **edge_data)

        detour_weights.append(((node1, node2, edge_data["weight"]), detour_weight))

    for detour_weight in sorted(detour_weights, key=lambda x: x[1], reverse=True):
        yield detour_weight
