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
            self, levels=None, cmap='coolwarm',
            fill_contours=True, show_contours=True, show_clabels=False,
            show_points=False, show_grid=False, save=None,
            add_shape=None, **kwargs
    ):
        """"""
        from cloupy.maps.drawing_shapes import get_shapes_for_plotting
        from cloupy.maps.drawing_shapes import draw_additional_shapes
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import griddata
        from PIL import Image
        import os

        properties = {
            'text_size': 10,
            'numcols': 240,
            'numrows': 240,
            'interpolation_method': 'cubic',
            'contour_levels': None,
            'clabels_levels': None,
            'clabels_add': None,
            'clabels_inline_spacing': -3,
            'clabels_decimal_place': 0,
            'grid_lw': 0.1,
            'grid_ls': 'solid',
            'figsize': (4, 4),
        }

        for param, arg in kwargs.items():
            try:
                properties[param]
            except KeyError:
                raise ValueError(f'Invalid parameter: {param}')
            else:
                properties[param] = arg

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

        clabels_size = properties['text_size'] * 0.6

        if properties['contour_levels'] is None:
            contour_levels = levels
        else:
            contour_levels = properties['contour_levels']

        fig, ax = plt.subplots(figsize=properties['figsize'], facecolor='white')
        shapes_for_plotting = get_shapes_for_plotting(
            ax, self.shapefile_path,
            self.epsg_crs, country=self.country,
        )

        ax.tick_params(labelsize=properties['text_size'])

        the_low_x = None
        the_high_x = None
        the_low_y = None
        the_high_y = None

        for shape in shapes_for_plotting:
            high_x = max(shape[0])
            low_x = min(shape[0])
            high_y = max(shape[1])
            low_y = min(shape[1])

            if the_low_x is None:
                the_low_x = low_x
                the_high_x = high_x
                the_low_y = low_y
                the_high_y = high_y
                continue

            if the_low_x > low_x:
                the_low_x = low_x
            if the_high_x < high_x:
                the_high_x = high_x
            if the_low_y > low_y:
                the_low_y = low_y
            if the_high_y < high_y:
                the_high_y = high_y

        df = self.dataframe
        df.columns = ['value', 'lon', 'lat']

        x = list(df.lon)
        y = list(df.lat)
        z = list(df.value)

        nodes = MapInterpolation.get_boundary_box(
            the_low_x, the_high_x,
            the_low_y, the_high_y
        )
        x_node = nodes[0]
        y_node = nodes[1]

        boundary_points = MapInterpolation.get_boundary_points(x_node, y_node)
        the_closest_to_boundary_points = MapInterpolation.get_the_closest_points_to_boundary_points(boundary_points, df)

        for point, closest_value in the_closest_to_boundary_points.items():
            x.append(point[0])
            y.append(point[1])
            z.append(closest_value[2])

        xi = np.linspace(min(x), max(x), properties['numcols'])
        yi = np.linspace(min(y), max(y), properties['numrows'])
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(
            (x, y),
            np.array(z),
            (xi, yi),
            method=properties['interpolation_method']
        )

        lower_left = boundary_points[5]
        upper_right = boundary_points[-1]
        ax.set_xlim(lower_left[0], upper_right[0])
        ax.set_ylim(lower_left[1], upper_right[1])

        fig_for_colorbar, ax1 = plt.subplots()
        if fill_contours:
            cntr = ax1.contourf(xi, yi, zi, levels=levels, cmap=cmap)
            cbar = plt.colorbar(cntr, ax=ax)
            cbar.ax.tick_params(labelsize=properties['text_size'] * 0.8)

        if show_grid:
            ax.grid(lw=properties['grid_lw'], ls=properties['grid_ls'])
            fig.savefig('grid_mask.png', transparent=True)
            ax.grid(False)
        plt.close()

        rgba = MapInterpolation.suit_rgba_to_matplotlib((1, 0, 0, 1))
        for shape in shapes_for_plotting:
            ax.plot(shape[0], shape[1], color='k', lw=1)
            ax.fill(shape[0], shape[1], color=rgba, zorder=0)

        fig.savefig('mask.png', facecolor=fig.get_facecolor(), transparent=True)
        MapInterpolation.create_mask('mask.png')
        for shape in shapes_for_plotting:
            ax.fill(shape[0], shape[1], color='white', zorder=0)

        if show_contours:
            clabels = ax.contour(xi, yi, zi, levels=contour_levels, linewidths=0.5, colors='k')

            if show_clabels:
                ax.clabel(
                    clabels, fontsize=clabels_size, fmt=f'%1.{properties["clabels_decimal_place"]}f',
                    levels=properties['clabels_levels'], inline_spacing=properties['clabels_inline_spacing']
                    )

            if properties['clabels_add']:
                ax.clabel(
                    clabels, fontsize=clabels_size, fmt=f'%1.{properties["clabels_decimal_place"]}f',
                    inline_spacing=properties['clabels_inline_spacing'], manual=properties['clabels_add']
                )

        if properties['clabels_add'] and not show_contours:
            clabels = ax.contour(xi, yi, zi, levels=contour_levels, linewidths=0, colors='k')
            ax.clabel(
                clabels, fontsize=clabels_size, fmt=f'%1.{properties["clabels_decimal_place"]}f',
                inline_spacing=properties['clabels_inline_spacing'], manual=properties['clabels_add']
            )

        if fill_contours:
            ax.contourf(xi, yi, zi, levels=levels, cmap=cmap)
        if show_points:
            ax.scatter(df.lon, df.lat, s=10, c='k')
        if add_shape is not None:
            draw_additional_shapes(add_shape, ax)

        plt.close()

        fig.savefig('map.png')
        MapInterpolation.merge_map_with_mask(show_grid)
        done_map = Image.open('masked_map.png')

        image_size = done_map.size
        resized_map = done_map.resize(
            (700, int(round(image_size[1]*(700/image_size[0]))))
        )

        if save is not None:
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
    def create_mask(fname):
        """"""
        from PIL import Image

        img = Image.open(fname)
        img = img.convert("RGBA")

        pixdata = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y][0] == 1 and pixdata[x, y][1] == 0 and pixdata[x, y][2] == 0:
                    pixdata[x, y] = (255, 255, 255, 0)

        img.save(fname, "PNG")

    @staticmethod
    def merge_map_with_mask(show_grid):
        """"""
        from PIL import Image

        background = Image.open("map.png")
        foreground = Image.open("mask.png")
        background.paste(foreground, (0, 0), foreground)

        if show_grid:
            grid = Image.open('grid_mask.png')
            background.paste(grid, (0, 0), grid)

        background.save('masked_map.png')
