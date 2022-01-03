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
            self, levels=None, cmap='jet',
            fill_contours=True, show_contours=True, show_clabels=False,
            show_points=False, show_grid=False, save=None,
            add_shape=None, **kwargs
    ):
        """"""
        from cloupy.maps.drawing_shapes import get_shapes_for_plotting
        from cloupy.maps.drawing_shapes import draw_additional_shapes
        import matplotlib.pyplot as plt
        from PIL import Image

        attrs_to_be_updated = MapInterpolation.check_if_valid_args_and_update_class_attrs(
            self.shapefile_path, self.country, self.epsg_crs
        )
        self.shapefile_path = attrs_to_be_updated['shapefile_path']
        self.country = attrs_to_be_updated['country']
        self.epsg_crs = attrs_to_be_updated['epsg_crs']

        properties = {
            'text_size': 10,
            'numcols': 240,
            'numrows': 240,
            'interpolation_method': 'cubic',
            'interpolation_within_levels': False,
            'extrapolate_into_zoomed_area': True,
            'contour_levels': None,
            'clabels_levels': None,
            'clabels_add': None,
            'clabels_inline_spacing': -3,
            'clabels_decimal_place': 0,
            'grid_lw': 0.1,
            'grid_ls': 'solid',
            'figsize': (4, 4),
            'zoom_in': None,
            'show_frame': True,
            'show_coordinates': True,
            'show_ticks': True,
            'show_cbar': True,
            'xticks': None,
            'yticks': None,
            'cbar_ticks': None
        }

        for param, arg in kwargs.items():
            try:
                properties[param]
            except KeyError:
                raise ValueError(f'Invalid parameter: {param}')
            else:
                properties[param] = arg

        if properties['contour_levels'] is None:
            contour_levels = levels
        else:
            contour_levels = properties['contour_levels']
        clabels_size = properties['text_size'] * 0.6

        df = self.dataframe
        df.columns = ['value', 'lon', 'lat']
        x = list(df.lon)
        y = list(df.lat)
        z = list(df.value)

        fig, ax = plt.subplots(figsize=properties['figsize'], facecolor='white')
        shapes_for_plotting = get_shapes_for_plotting(
            ax, self.shapefile_path,
            self.epsg_crs, country=self.country,
        )

        # get extreme shape points and create an invisible box on which points for extrapolation will be placed
        the_low_x, the_high_x, the_low_y, the_high_y = MapInterpolation.get_extreme_shape_points(shapes_for_plotting)
        nodes = MapInterpolation.get_boundary_box(
            the_low_x, the_high_x, the_low_y, the_high_y,
            properties['zoom_in'], properties['extrapolate_into_zoomed_area']
        )
        x_nodes, y_nodes = nodes[0], nodes[1]

        # place the points to which data will be extrapolated on the invisible box boundaries and add them to the
        # data before creating the interpolation
        boundary_points = MapInterpolation.get_boundary_points(x_nodes, y_nodes)
        the_closest_to_boundary_points = MapInterpolation.get_the_closest_points_to_boundary_points(boundary_points, df)
        for point, closest_value in the_closest_to_boundary_points.items():
            x.append(point[0])
            y.append(point[1])
            z.append(closest_value[2])

        xi, yi, zi = MapInterpolation.interpolate_data(x, y, z, properties, levels)

        # PLOT SETTINGS
        if properties['zoom_in'] is not None:
            x = properties['zoom_in'][0]
            y = properties['zoom_in'][1]
            ax.set_xlim(x[0], x[1])
            ax.set_ylim(y[0], y[1])
        else:
            lower_left = boundary_points[5]
            upper_right = boundary_points[-1]
            ax.set_xlim(lower_left[0], upper_right[0])
            ax.set_ylim(lower_left[1], upper_right[1])

        ax.tick_params(labelsize=properties['text_size'])

        if not properties['show_frame']:
            ax.set_frame_on(False)

        if not properties['show_coordinates']:
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)

        if not properties['show_ticks']:
            ax.tick_params(color=(0, 0, 0, 0))

        if properties['xticks'] is not None:
            ax.set_xticks(properties['xticks'])

        if properties['yticks'] is not None:
            ax.set_yticks(properties['yticks'])
        # ///PLOT SETTINGS

        MapInterpolation.adjust_ax_for_creating_masks_and_create_masks(
            ax, fig, xi,
            yi, zi, levels,
            cmap, properties, shapes_for_plotting,
            fill_contours, show_grid
        )

        if show_contours:
            clabels = ax.contour(xi, yi, zi, levels=contour_levels, linewidths=0.5, colors='k', linestyles='solid')
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
    def check_if_valid_args_and_update_class_attrs(
            shapefile_path, country, epsg_crs
    ):
        """"""
        import os

        to_be_udpated = {
            'shapefile_path': shapefile_path,
            'country':  country,
            'epsg_crs': epsg_crs
        }

        if shapefile_path is None and country is None:  # przeanalizuj wszystkie możliwe przypadki, porób błędy itd.
            raise ValueError

        elif shapefile_path is None and country is not None:
            shapefile_path = str(__file__).replace('interpolation_map.py', f'world{os.sep}ne_50m_admin_0_countries.shp')
            epsg_crs = 'epsg:4326'

            to_be_udpated['shapefile_path'] = shapefile_path
            to_be_udpated['epsg_crs'] = epsg_crs

        elif shapefile_path is not None and country is None:
            pass

        elif shapefile_path is not None and country is not None:
            if shapefile_path == str(__file__).replace(
                'interpolation_map.py',
                f'world{os.sep}ne_50m_admin_0_countries.shp'
            ):
                pass
            else:
                raise ValueError(
                    "Invalid argument combination. The 'country' argument is valid only for the default cloupy shapefile. "
                    " Set 'country' back to None or 'shapefile_path' back to None."
                )

        else:
            country = None
            to_be_udpated['country'] = country

        return to_be_udpated

    @staticmethod
    def get_extreme_shape_points(shapes_for_plotting):
        """"""

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

        return the_low_x, the_high_x, the_low_y, the_high_y

    @staticmethod
    def get_boundary_box(
            low_x, high_x, low_y,
            high_y, zoom_in, extrapolate_into_zoomed_area,
            distance=0.5
    ):
        """"""
        if zoom_in is not None and extrapolate_into_zoomed_area:
            low_x = zoom_in[0][0]
            high_x = zoom_in[0][1]
            low_y = zoom_in[1][0]
            high_y = zoom_in[1][1]

        node_1 = (high_x + distance, low_y - distance)
        node_2 = (low_x - distance, low_y - distance)
        node_3 = (low_x - distance, high_y + distance)
        node_4 = (high_x + distance, high_y + distance)
        node_5 = (high_x + distance, low_y - distance)

        nodes = [node_1, node_2, node_3, node_4, node_5]

        x_nodes = []
        y_nodes = []
        for node in nodes:
            x_nodes.append(node[0])
            y_nodes.append(node[1])

        return x_nodes, y_nodes

    @staticmethod
    def get_boundary_points(
            x_node, y_node
    ):
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
                dist = calc_the_distance(point, (list(df.lon)[i], y))

                if the_closest_dist is None:
                    the_closest_dist = dist
                    the_closest_point = (list(df.lon)[i], y, list(df.value)[i])
                    continue

                if the_closest_dist > dist:
                    the_closest_dist = dist
                    the_closest_point = (list(df.lon)[i], y, list(df.value)[i])

            the_closest_to_boundary_points[point] = the_closest_point

        return the_closest_to_boundary_points

    @staticmethod
    def interpolate_data(
            x, y, z,
            properties, levels
    ):
        """"""
        import numpy as np
        from scipy.interpolate import griddata
        import pandas as pd

        xi = np.linspace(min(x), max(x), properties['numcols'])
        yi = np.linspace(min(y), max(y), properties['numrows'])
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(
            (x, y),
            np.array(z),
            (xi, yi),
            method=properties['interpolation_method']
        )

        if properties['interpolation_within_levels']:
            max_level = max(levels)
            min_level = min(levels)

            new_ndarray = []
            for array in zi:
                all_above_max_level = pd.Series(array, dtype='float64')
                all_above_max_level = all_above_max_level[all_above_max_level > max_level]

                all_below_min_level = pd.Series(array, dtype='float64')
                all_below_min_level = all_below_min_level[all_below_min_level < min_level]

                if all_above_max_level.empty:
                    new_array = pd.Series(array)
                else:
                    new_array = pd.Series(array).replace(list(all_above_max_level), max_level)

                if all_below_min_level.empty:
                    pass
                else:
                    new_array = new_array.replace(list(all_below_min_level), min_level)

                new_ndarray.append(new_array)

            zi = new_ndarray

        return xi, yi, zi

    @staticmethod
    def adjust_ax_for_creating_masks_and_create_masks(
            ax, fig, xi, yi, zi,
            levels, cmap, properties,
            shapes_for_plotting, fill_contours, show_grid
    ):
        """"""
        import matplotlib.pyplot as plt

        fig_for_colorbar, ax_for_colorbar = plt.subplots()
        if fill_contours and properties['show_cbar']:
            cntr = ax_for_colorbar.contourf(xi, yi, zi, levels=levels, cmap=cmap)
            cbar = plt.colorbar(cntr, ax=ax)
            cbar.ax.tick_params(labelsize=properties['text_size'] * 0.8)

            if properties['cbar_ticks'] is not None:
                cbar.set_ticks(properties['cbar_ticks'])

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
