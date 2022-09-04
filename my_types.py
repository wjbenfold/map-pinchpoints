from collections import namedtuple

WayInfo = namedtuple("WayInfo", ["name", "type", "segments"])
Segment = namedtuple("Segment", ["start_node", "end_node"])
LatLon = namedtuple("LatLon", ["lat", "lon"])
