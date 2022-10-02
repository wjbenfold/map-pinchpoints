import csv
import get_data

from shortest_detour import getBottlenecks


def main(config):

    way_infos = get_data.get_ways_from_file(
        config["download"]["output_filename_xml"],
        filtered_highways=config["pinchpoints"]["filtered_highways"],
    )

    # fyi way_infos can have duplicates in

    bottlenecks = getBottlenecks(way_infos)

    min_detour = config["pinchpoints"]["min_detour"]

    with open(config["pinchpoints"]["output_filename_csv"], "w+") as fh:
        csv_writer = csv.writer(fh)
        for bottleneck in bottlenecks:
            (node1, node2, _), detour_weight = bottleneck
            if detour_weight < min_detour:
                break

            csv_writer.writerow(
                [node1.lat, node1.lon, node2.lat, node2.lon, detour_weight]
            )


if __name__ == "__main__":
    main()
