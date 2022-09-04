import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM


def plot_latlons(
    start_latlon, end_latlon, intersection_latlons, min_x, max_x, min_y, max_y
):
    extent = (min_x, max_x, min_y, max_y)

    imagery = OSM()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=imagery.crs)
    ax.set_extent(extent, ccrs.PlateCarree())

    # Add the imagery to the map.
    ax.add_image(imagery, 14)

    ys, xs = zip(*intersection_latlons)

    plt.scatter(xs, ys, transform=ccrs.PlateCarree(), marker="+")

    ys, xs = zip(start_latlon, end_latlon)

    print(xs, ys)

    plt.plot(xs, ys, transform=ccrs.PlateCarree(), marker="o")

    plt.title("Pinch points")

    plt.show()
