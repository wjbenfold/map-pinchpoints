from typing import List
import networkx as nx
from my_types import WayInfo
import numpy as np

# WayInfo(name: str, type: str, segments: List[Segment])
# Segment(start_node: LatLon, end_node: LatLon)
# LatLon(lat: float, lon: float)


def getWeight(segment):
    (lat1, lon1), (lat2, lon2) = segment
    return (
        np.arccos(
            np.sin(lat1) * np.sin(lat2)
            + np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1)
        )
        * 6371000
    )


def getBottlenecks(way_infos: List[WayInfo], *args, **kwargs):

    G = nx.Graph()

    def segmentGen(way_infos):
        for way_info in way_infos:
            for segment in way_info.segments:
                weight = getWeight(segment)
                yield *segment, {"weight": weight}

    G.add_edges_from(segmentGen(way_infos))

    print(G.number_of_nodes())
    print(G.number_of_edges())

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
            print("loop including", b_node)
            continue
        G.add_edge(neighbour1, neighbour2, weight=new_weight)
        G.remove_node(b_node)

    while True:
        unary_nodes = [*map(lambda y: y[0], filter(lambda x: x[1] == 1, G.degree()))]
        if not unary_nodes:
            break
        G.remove_nodes_from(unary_nodes)

    print(G.number_of_nodes())
    print(G.number_of_edges())

    detour_weights = []

    for node1, node2, edge_data in [*G.edges(data=True)]:

        G.remove_edge(node1, node2)

        try:
            detour_weight = nx.dijkstra_path_length(G, node1, node2)
        except nx.NetworkXNoPath:
            G.add_edge(node1, node2, **edge_data)
            continue

        G.add_edge(node1, node2, **edge_data)

        detour_weights.append(((node1, node2, edge_data), detour_weight))

    return [*map(
        lambda x: x[0][0], sorted(detour_weights, key=lambda x: x[1], reverse=True)[:10]
    )]
