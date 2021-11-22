class MapInterpolation:
    """
    Create a MapInterpolation object in which data for drawing an interpolation
    map can be downloaded, modified, manually provided.

    Keyword arguments:
        shapefile_path -- a path to the shapefile from which contours will be
    drawn (default None)
        dataframe -- data for the drawing (default None)

    ---------------DATA STRUCTURE---------------
    The supported data structure for MapInterpolation.dataframe is 4 columns of
    pandas.DataFrame object.

    1st column: values,
    2nd column: longitude,
    3rd column: latitude

    Exemplary dataframe:
    import pandas as pd
    dataframe = pd.DataFrame({
                'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'temp': [-2, -1, 0, 7, 15, 18, 19, 20, 18, 14, 8, 3],
                'preci': [50, 25, 55, 60, 70, 80, 90, 80, 68, 50, 45, 49],
                'max_temp': [10, 15, 17, 18, 19, 20, 35, 34, 25, 20, 15, 10],
                'min_temp': [-36, -29, -20, -15, -5, -1, 1, 2, -1, -4, -18, -22]
                            })
    --------------------------------------------
    """

    def __init__(
            self, country=None, dataframe=None,
            shapefile_path=None, epsg_crs=None,
    ):
        self.country = country
        self.shapefile_path = shapefile_path
        self.epsg_crs = epsg_crs
        self.dataframe = dataframe

    def draw(
            self, figsize=(10, 10), numcols=240,
            numrows=240, interpolation_method='cubic',
            levels=None, cmap='coolwarm', show_points=False,
            show_contours=True, fill_contours=True,
            add_shape=None, save=False
    ):
        """"""
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import griddata
        from PIL import Image
        from cloupy.maps.drawing_shapes import draw_map_from_shapefile_and_return_extreme_points
        import os

        if self.shapefile_path is None and self.country is None:  # przeanalizuj wszystkie możliwe przypadki, porób błędy itd.
            raise ValueError

        elif self.shapefile_path is None and self.country is not None:
            self.shapefile_path = str(__file__).replace(
                'interpolation_map.py',
                f'world{os.sep}ne_50m_admin_0_countries.shp'
            )
            self.epsg_crs = 'epsg:4326'

        elif self.shapefile_path is not None and self.country is None:
            pass

        elif self.shapefile_path is not None and self.country is not None:
            if self.shapefile_path == str(__file__).replace(
                'interpolation_map.py',
                f'world{os.sep}ne_50m_admin_0_countries.shp'
            ):
                pass
            else:
                raise ValueError(
                    """
                    Invalid argument combination. The 'country' argument is valid only for the default cloupy shapefile.
                    Set 'country' back to None or 'shapefile_path' back to None.
                    """
                )

        else:
            self.country = None

        fig, ax = plt.subplots(nrows=1, figsize=figsize, facecolor='white')
        extreme_points = draw_map_from_shapefile_and_return_extreme_points(
            ax, self.shapefile_path,
            self.epsg_crs, country=self.country,
            add_shape=add_shape
        )

        df = self.dataframe
        df.columns = ['value', 'lon', 'lat']

        x = list(df.lon)
        y = list(df.lat)
        z = list(df.value)

        nodes = MapInterpolation.get_boundary_box(
            extreme_points[0], extreme_points[1],
            extreme_points[2], extreme_points[3]
        )
        x_node = nodes[0]
        y_node = nodes[1]

        boundary_points = MapInterpolation.get_boundary_points(x_node, y_node)
        the_closest_to_boundary_points = MapInterpolation.get_the_closest_points_to_boundary_points(boundary_points, df)

        for point, closest_value in the_closest_to_boundary_points.items():
            x.append(point[0])
            y.append(point[1])
            z.append(closest_value[2])

        xi = np.linspace(min(x), max(x), numcols)
        yi = np.linspace(min(y), max(y), numrows)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(
            (x, y),
            np.array(z),
            (xi, yi),
            method=interpolation_method
        )

        if show_contours:
            clabels = ax.contour(xi, yi, zi, levels=levels, linewidths=0.5, colors='k')
            # ax.clabel(clabels, levels=[6, 7, 8, 9], fontsize=6, fmt='%1.0f') # przyjrzyj się temu, może się da to zrobić bardziej zaawansowanie
        if fill_contours:
            cntr = ax.contourf(xi, yi, zi, levels=levels, cmap=cmap)
            plt.colorbar(cntr, ax=ax)
        else:
            cntr = None

        if show_points:
            ax.scatter(df.lon, df.lat, s=10, c='k')

        plt.close()

        lower_left = boundary_points[5]
        upper_right = boundary_points[-1]
        ax.set_xlim(lower_left[0], upper_right[0])
        ax.set_ylim(lower_left[1], upper_right[1])

        rgba = (121, 128, 0, 1)
        MapInterpolation.get_raster_mask(
            self.shapefile_path, rgba, figsize,
            self.epsg_crs, cntr, lower_left,
            upper_right, self.country
        )

        fig.savefig('map.png')
        MapInterpolation.merge_map_with_mask()
        done_map = Image.open('masked_map.png')

        image_size = done_map.size
        resized_map = done_map.resize(
            (700, int(round(image_size[1]*(700/image_size[0]))))
        )

        if save:
            done_map.save(save)

        return resized_map

    @staticmethod
    def get_boundary_box(
            low_x, high_x, low_y,
            high_y, distance=0.5
    ):
        """"""
        node_1 = (high_x + distance, low_y - distance)
        node_2 = (low_x - distance, low_y - distance)
        node_3 = (low_x - distance, high_y + distance)
        node_4 = (high_x + distance, high_y + distance)
        node_5 = (high_x + distance, low_y - distance)

        nodes = [node_1, node_2, node_3, node_4, node_5]

        x_node = []
        y_node = []
        for node in nodes:
            x_node.append(node[0])
            y_node.append(node[1])

        return x_node, y_node

    @staticmethod
    def get_boundary_points(x_node, y_node):
        """"""
        x = x_node
        y = y_node

        dist_1 = abs((x_node[0] - x_node[1])) / 2
        dist_2 = abs((y_node[1] - y_node[2])) / 2
        dist_3 = abs((x_node[3]) - x_node[2]) / 2
        dist_4 = abs((y_node[3] - y_node[4])) / 2

        point_1 = (x_node[0] - dist_1, y_node[0])
        point_2 = (x_node[1], y_node[1] + dist_2)
        point_3 = (x_node[2] + dist_3, y_node[2])
        point_4 = (x_node[3], y_node[3] - dist_4)

        point_5 = x[0], y[0]
        point_6 = x[1], y[1]
        point_7 = x[2], y[2]
        point_8 = x[3], y[3]

        return point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8

    @staticmethod
    def get_the_closest_points_to_boundary_points(
            boundary_points, df
    ):
        """"""
        from cloupy.maps.drawing_shapes import calc_the_distance

        the_closest_to_boundary_points = {}
        for point in boundary_points:
            the_closest_dist = None
            the_closest_point = None
            for i, y in enumerate(df.lat):
                dist = calc_the_distance(point, (df.lon[i], y))

                if the_closest_dist is None:
                    the_closest_dist = dist
                    the_closest_point = (df.lon[i], y, df.value[i])
                    continue

                if the_closest_dist > dist:
                    the_closest_dist = dist
                    the_closest_point = (df.lon[i], y, df.value[i])

            the_closest_to_boundary_points[point] = the_closest_point

        return the_closest_to_boundary_points

    @staticmethod
    def suit_rgba_to_matplotlib(rgba):
        """"""
        red = rgba[0] / 255
        green = rgba[1] / 255
        blue = rgba[2] / 255
        alpha = rgba[3]

        if alpha > 1 or alpha < 0:
            raise ValueError(f'Alpha should be within 0-1 range! Alpha: {alpha}')

        return red, green, blue, alpha

    @staticmethod
    def get_raster_mask(
            shapefile_path, rgba, figsize,
            epsg_crs, colorbar, lower_left,
            upper_right, country
    ):
        """"""
        import matplotlib.pyplot as plt
        from cloupy.maps.drawing_shapes import draw_map_from_shapefile_and_return_extreme_points

        transparent_color = MapInterpolation.suit_rgba_to_matplotlib(rgba)
        fig, ax = plt.subplots(nrows=1, figsize=figsize, facecolor='white')
        draw_map_from_shapefile_and_return_extreme_points(
            ax, shapefile_path, epsg_crs,
            mask=True, color_to_be_transparent=transparent_color,
            country=country
        )

        ax.set_xlim(lower_left[0], upper_right[0])
        ax.set_ylim(lower_left[1], upper_right[1])

        if colorbar is not None:
            plt.colorbar(colorbar, ax=ax)

        fig.savefig('mask.png', facecolor=fig.get_facecolor(), transparent=True)
        MapInterpolation.create_mask('mask.png', rgba)
        plt.close()

    @staticmethod
    def create_mask(fname, rgba):
        """"""
        from PIL import Image

        img = Image.open(fname)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == rgba[0] and rgba[1] == rgba[1] and item[2] == rgba[2]:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(fname, "PNG")

        return newData

    @staticmethod
    def merge_map_with_mask():
        """"""
        from PIL import Image

        background = Image.open("map.png")
        foreground = Image.open("mask.png")
        background.paste(foreground, (0, 0), foreground)

        background.save('masked_map.png')
