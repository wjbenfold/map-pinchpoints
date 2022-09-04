import numpy as np
import galilean_transform
from my_types import LatLon, Segment


def getBottlenecks(way_infos, start_loc, end_loc):
    def getTransformers(start_loc, end_loc):
        x0 = start_loc.lon
        y0 = start_loc.lat
        theta = -np.arctan(
            (end_loc.lon - start_loc.lon) / (end_loc.lat - start_loc.lat)
        )

        to_line_space_transformer = galilean_transform.getTransformer(x0, y0, theta)

        y0_prime, x0_prime = to_line_space_transformer(LatLon(0, 0))

        from_line_space_transformer = galilean_transform.getTransformer(
            x0_prime, y0_prime, -theta
        )

        return to_line_space_transformer, from_line_space_transformer

    transformer, transformer_back = getTransformers(start_loc, end_loc)

    NN = 30

    print(
        start_loc,
        "->",
        transformer(start_loc),
        "->",
        transformer_back(transformer(start_loc)),
    )

    print(
        end_loc,
        "->",
        transformer(end_loc),
        "->",
        transformer_back(transformer(end_loc)),
    )

    transformed_segments = []

    for way_info in way_infos:
        for segment in way_info.segments:
            transformed_segments.append(
                Segment(
                    transformer(LatLon(segment.start_node.lat, segment.start_node.lon)),
                    transformer(LatLon(segment.end_node.lat, segment.end_node.lon)),
                )
            )

    # Put segments in bins if they cross a line (based on which line they cross). They may be in more that one bin...

    segment_bins = []
    for _ in range(NN):
        segment_bins.append([])

    bin_height = (transformer(end_loc).lat - transformer(start_loc).lat) / (NN + 1)

    for segment in transformed_segments:
        start_bin = segment.start_node.lat // bin_height
        end_bin = segment.end_node.lat // bin_height
        for ii in range(int(start_bin), int(end_bin)):
            try:
                segment_bins[ii].append(segment)
            except IndexError:
                # The segment starts or ends past one end of the route
                pass

    # Calculate where segments intersect lines

    intersections = []
    for _ in range(NN):
        intersections.append([])

    for bin_num, bin in enumerate(segment_bins):
        bin_lat = bin_height * (1 + bin_num)
        for segment in bin:
            frac = (bin_lat - segment.start_node.lat) / (
                segment.end_node.lat - segment.start_node.lat
            )
            intersection_lon = segment.start_node.lon + frac * (
                segment.end_node.lon - segment.start_node.lon
            )
            intersections[bin_num].append(intersection_lon)

    remotenesses = []

    # For each line, identify any interesections far from the others
    for jj, line_intersections in enumerate(intersections):
        line_lat = bin_height * (1 + jj)
        if len(line_intersections) == 0:
            continue
        elif len(line_intersections) == 1:
            remotenesses.append((-1, LatLon(line_lat, line_intersections[0])))
        else:
            sorted_li = sorted(line_intersections)
            remotenesses.append(
                (sorted_li[1] - sorted_li[0], LatLon(line_lat, sorted_li[0]))
            )
            remotenesses.append(
                (sorted_li[-1] - sorted_li[-2], LatLon(line_lat, sorted_li[-1]))
            )
            for ii in range(1, len(sorted_li) - 1):
                remotenesses.append(
                    (
                        min(
                            sorted_li[ii] - sorted_li[ii - 1],
                            sorted_li[ii + 1] - sorted_li[ii],
                        ),
                        LatLon(line_lat, sorted_li[ii]),
                    )
                )

    sorted_remotenesses = sorted(remotenesses, key=lambda x: x[0], reverse=True)

    bottlenecks = [x[1] for x in sorted_remotenesses[: len(remotenesses) // 10 + 1]]

    bottlenecks = [*map(transformer_back, bottlenecks)]

    return bottlenecks
