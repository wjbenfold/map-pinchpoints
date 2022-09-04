import numpy as np

from my_types import LatLon


def getTransformer(x0, y0, theta):
    def transformer(real_lat_lon):
        real_lat, real_lon = real_lat_lon
        model_lat = -np.sin(theta) * (real_lon - x0) + np.cos(theta) * (
            real_lat - y0
        )
        model_lon = np.cos(theta) * (real_lon - x0) + np.sin(theta) * (
            real_lat - y0
        )
        return LatLon(model_lat, model_lon)

    return transformer
