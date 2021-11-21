

def calc_the_distance(
        point1, point2
):
    """Calculate the distance between two given points"""
    import math

    a = abs(point1[0] - point2[0])
    b = abs(point1[1] - point2[1])
    c2 = a**2 + b**2

    c = math.sqrt(c2)

    return c


def draw_map_from_shapefile_and_return_extreme_points(
        ax, shapefile_path, coordinates_system,
        mask=False, color_to_be_transparent=None
):
    """Draw map contours from the given shapefile"""
    import shapefile as shp
    from pyproj import Transformer

    shape = shp.Reader(shapefile_path)
    shape = shape.shapes()
    transformer = Transformer.from_crs(coordinates_system, 'epsg:4326')

    all_xs = []
    all_ys = []

    starting_point = None
    for element in shape:
        x_for_plotting = []
        y_for_plotting = []
        for coords in element.points:

            x = coords[0]
            y = coords[1]
            x, y = transformer.transform(x, y)

            x_for_plotting.append(x)
            y_for_plotting.append(y)

            if starting_point is None:
                starting_point = (x, y)
                continue

            if starting_point == (x, y):

                ax.plot(x_for_plotting, y_for_plotting, color='black', lw=1)
                if mask:
                    ax.fill(x_for_plotting, y_for_plotting, color=color_to_be_transparent)

                for i, x_ in enumerate(x_for_plotting):
                    all_xs.append(x_)
                    all_ys.append(y_for_plotting[i])

                x_for_plotting.clear()
                y_for_plotting.clear()
                starting_point = None

        ax.plot(x_for_plotting, y_for_plotting, color='black', lw=1)
        if mask:
            ax.fill(x_for_plotting, y_for_plotting, color=color_to_be_transparent)

        for x_ in x_for_plotting:
            all_xs.append(x_)

        for y_ in y_for_plotting:
            all_ys.append(y_)

    the_low_x = min(all_xs)
    the_high_x = max(all_xs)
    the_low_y = min(all_ys)
    the_high_y = max(all_ys)

    return the_low_x, the_high_x, the_low_y, the_high_y
