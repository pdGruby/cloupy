class MapInterpolation:
    """
    Create a MapInterpolation class where the data for drawing an interpolation
    map can be downloaded, modified, manually provided.

    Keyword arguments:
        country -- a country or a list of countries for which the shapefile will
    be drawn. Alternatively, if you pass the 'EUROPE' value, all European countries
    will be drawn on the map (default None)
        dataframe -- data for interpolation (default None)
        shapefile_path -- a path to the non-default shapefile from which boundaries
    will be drawn (default None)
        crs -- the imported shapefile's coordinates system (default None).
    This argument is required when specifying a path to the non-default shapefile
    (in the 'shapefile_path' argument). If the 'shapefile_path' argument is
    specified and the 'crs' argument is None, the boundaries will be drawn
    for the EPSG:4326 coordinates system. If it is not valid coordinates system,
    the coordinates on the map may be bizarre

    ---------------METHODS---------------
    draw()
    d_imgw_data()
    d_wmo_data()
    import_global_df()
    -------------------------------------

    ---------------DATA STRUCTURE---------------
    The supported data structure for MapInterpolation.dataframe is 3 columns of
    pandas.DataFrame object.

    1st column: values,
    2nd column: longitude,
    3rd column: latitude

    Exemplary dataframe:
    import pandas as pd
    dataframe = pd.DataFrame({
                'values': [7.9, 7.6, 7.4, 8.0, 8.6, 7.7, 8.4],
                'longitude': [19.4, 18.6, 16.2, 19.8, 14.6, 21.0, 16.9],
                'latitude': [54.2, 54.4, 54.2, 50.1, 53.4, 52.2, 51.1]
                            })

    The exemplary data is the air temperature and comes from a couple of synoptic
    stations from Poland.
    --------------------------------------------

    ---------------NOTE THAT---------------
    You can select country boundaries from the default shapefile by setting the
    'country' argument. The default shapefile comes from the Natural Earth Data
    website (https://www.naturalearthdata.com/about/terms-of-use/), which shares
    many shapefiles for free use. However, the 'shapefile_path' and 'crs'
    arguments allow you to select non-default boundaries from your PC. If you
    specify the non-default shapefile, the 'country' argument does not change
    anything.
    ---------------------------------------
    """
    def __init__(
            self, country=None, dataframe=None,
            shapefile_path=None, crs=None,
    ):
        self.country = country
        self.dataframe = dataframe
        self.shapefile_path = shapefile_path
        self.crs = crs

    def draw(
            self, levels=None, cmap='jet',
            fill_contours=True, show_contours=False, show_clabels=False,
            show_cbar=True, show_grid=False, show_frame=True, show_coordinates=True, show_ticks=True, add_shape=None,
            save=None, **kwargs
    ):
        """
        Specify which elements are to be drawn and draw an interpolation map.

        Keyword arguments:
            levels -- levels for which interpolated data will be displayed. If
        None, the levels will be adjusted automatically, but it may result in
        poor map's look, so it is recommended to specify the levels on your
        own. Exemplary 'levels' input: numpy.arange(5, 15, 0.5) (default None)
            cmap -- a colormap which will be used for displaying interpolated
        data. To see the available colormaps, see: https://matplotlib.org/stable
        /tutorials/colors/colormaps.html (default for default style 'jet';
        default for retro style 'Greys_r')
            fill_contours -- if the interpolated contours are to be filled with
        the selected colormap (default True)
            show_contours -- if the interpolated contours are to be shown (default
        False)
            show_clabels -- if the interpolated contours are to be labeled (default
        False)
            show_cbar -- if a colorbar for the interpolated data is to be shown
        (default True)
            show_grid -- if a grid for the coordinates is to be shown (default
        False)
            show_frame -- if the frame of the axis is to be shown (default True)
            show_coordinates -- if the coordinates are to be shown (default True)
            show_ticks -- if the x and y-ticks are to be shown (default True)
            add_shape -- if additional shapes are to be drawn. The argument takes
        a dictionary in which keys are the paths to the additional shapefile and
        values are style/coordinates system settings - the value must be a single
        string in which commas separate consecutive style/coordinates system
        arguments. There are 5 settings that may be changed: coordinates system
        (crs), linewidth (lw or linewidth), linestyle (ls or linestyle), fill color
        (fc or fill_color), boundaries color (c or color). The coordinates' system
        must be passed in EPSG code (if the coordinates' system is not specified,
        then EPSG:4326 code will be taken). Exemplary 'add_shape' input: {'home/
        python/test.shp': 'crs=2180, ls=dotted, lw=2, fc=black, c=yellow'}. Note
        that: inside the string which specifies settings no quotes should be used
        (default None)
            save -- if the interpolation map is to be saved. A string in which
        file name must be passed, for example: 'interpolated_map.png'. Note that
        other picture formats can also be passed, e.g. 'interpolated_map.jpg'
        (default None)
            **kwargs -- the rest of arguments which are less relevant than the
        above arguments (for setting the interpolation map style)

        **kwargs:
            title -- the map title (default None)
            title_bold -- if the map title font weight is to be bold (default
        False)
            title_x_position -- the map title relative position on the x-axis of
        the figure (default 0.13)
            title_y_position -- the map title relative position on the y-axis of
        the figure (default 0.06)
            title_ha -- the map title horizontal alignment. Valid inputs are:
        'left', 'right', 'center' (default 'left')
            xlabel -- the map x-axis title (default None)
            xlabel_bold -- if the map x-axis title font weight is to be bold
        (default True)
            ylabel -- the map y-axis title (default None)
            ylabel_bold -- if the map y-axis title font weight is to be bold
        (default True)
            text_size -- the map title text size. Another text elements will be
        adjusted automatically respectively to the 'text_size' value (default
        for default style: 8; default for retro style: 10)
            numcols -- number of columns for creating an interpolation grid.
        Depending on the figure' sides ratio, the contours shape may be changed
        slightly (default 240)
            numrows -- number of rows for creating an interpolation grid.
        Depending on the figure' sides ratio, the contours shape may be changed
        slightly (default 240)
            interpolation_method -- the interpolation method to be applied.
        Available interpolation methods: 'linear', 'nearest', 'cubic' (default
        'cubic')
            interpolation_within_levels -- if interpolated values must be within
        the given levels range specified in the 'levels' argument. It may be handy
        when interpolation process returns values which can not be returned, e.g.
        negative values for the number of cases. It is also useful when white
        polygons appear on the map, which means that the given levels range does
        not cover all interpolated values (default False)
            extrapolation_into_zoomed_area -- if the 'zoom_in' argument is
        specified, the extrapolation process will be conducted to the corners of
        the zoomed-in area. It is handy when a country with the overseas territories
        was chosen and the data concerns only a specific part of the shapefile -
        in such case, the map may be zoomed in the proper area and the extrapolation
        will be conducted to the corners of the zoomed-in area, not to the corners
        of the whole shapefile (default True)
            contours_levels -- non-default levels for the contours. If the argument
        is None, then the 'contours_levels' argument will be the same as the
        'levels' argument (default None)
            clabels_levels -- non-default levels for the contour labels. If the
        argument is None, then the 'clabels_levels' argument will be the same as
        the 'contours_levels' argument (default None)
            clabels_add -- add non-default contour labels to the map. Non-default
        contour labels can be placed by specifying coordinates in a list of tuples,
        in which tuples are x and y coordinates (e.g. [(15, 50)] will place a
        label on the closest contour to the given coordinates, in the closest point
        to the given coordinates). Note that the 'clabels_add' argument can be
        used even when the 'show_contours' argument is set to False. In such case,
        the labels will be placed on the invisible contours that respond to the
        'levels' argument (default None)
            clabels_inline_spacing -- the spacing between text on the contours and
        the contours. Generally, the more characters the text on the contour has,
        the less 'clabels_inline_spacing' value should be. Note the that DPI value
        also affects the spacing between the text on the contours and the contours,
        so the space may be different while previewing the map and while saving the
        map (default 0)
            clabels_decimal_place -- decimal places of the contour labels (default
        0)
            xticks -- non-default x ticks. Available input: a list of ints/floats
        (default None)
            yticks -- non-default y ticks. Available input: a list of ints/floats
        (default None)
            cbar_ticks -- non-default colorbar ticks. Available input: a list of
        ints/floats (default None)
            cbar_title -- the colorbar title (default None)
            cbar_title_bold -- if the colorbar title font weight is to be bold
        (default True)
            cbar_labelpad -- the space between the colorbar title and the colorbar
        (default 10)
            cbar_position -- the position of the colorbar. Available inputs: 'left',
        'right', 'bottom', 'top' (default 'top')
            cbar_pad -- the space between the colorbar and the axis (default 0.02)
            zoom_in -- the area to which the map is to be zoomed in. The argument
        takes a list of tuples, in which tuples are the minimum and maximum values
        of the x and y coordinates, e.g. [(10, 20), (40, 50)] will zoom in the map
        to the area that is located between 10 degrees and 20 degrees of the east
        longitude; and between 40-50 degrees of the north latitude (default None)
            show_points -- if the points for which data was interpolated are to
        be shown (default False)
            points_labels -- if the 'show_points' argument is set to True, the
        points may also be labeled by the 'points_labels' argument. The labels may
        be the points ids and the points values. It is only an auxiliary option, so
        the labels are not pretty. Available inputs: 'ids', 'values' (default None)
            boundaries_lw -- the line width of the shapefile boundaries (default
        1)
            boundaries_ls -- the line style of the shapefile boundaries (default
        'solid')
            grid_lw -- the line width of the grid (default 0.1)
            grid_ls -- the line style of the grid. Available inputs: 'dashed',
        'dotted', 'dashdot', 'solid' (default 'solid')
            figsize -- the figure size in inches (default (4, 5))
            figpad_inches -- the figure margin (default 0.1)

        ---------------NOTE THAT---------------
        The quality of the displayed maps may be poor, but when the map is saved,
        the quality is much better. This is due to the different DPI of the image
        when saving and when displaying the map (300 DPI is used for saving the
        map, 150 DPI is used for displaying the map in an application). Different
        DPIs are used for streamline the workflow - lower DPI makes the map
        creation process much faster, so it is used to preview the map.
        ---------------------------------------
        """
        from cloupy.maps.draw_shapes import get_shapes_for_plotting
        from cloupy.maps.draw_shapes import draw_additional_shapes
        import matplotlib.pyplot as plt
        from PIL import Image

        attrs_to_be_updated = MapInterpolation.check_if_valid_args_and_update_class_attrs(
            self.shapefile_path, self.country, self.crs, self.dataframe
        )
        self.shapefile_path = attrs_to_be_updated['shapefile_path']
        self.country = attrs_to_be_updated['country']
        self.crs = attrs_to_be_updated['crs']

        properties = {
            'title': None,
            'title_bold': False,
            'title_x_position': 0.13,
            'title_y_position': 0.06,
            'title_ha': 'left',
            'xlabel': None,
            'xlabel_bold': True,
            'ylabel': None,
            'ylabel_bold': True,
            'text_size': 8,
            'numcols': 240,
            'numrows': 240,
            'interpolation_method': 'cubic',
            'interpolation_within_levels': False,
            'extrapolation_into_zoomed_area': True,
            'contours_levels': None,
            'clabels_levels': None,
            'clabels_add': None,
            'clabels_inline_spacing': 0,
            'clabels_decimal_place': 0,
            'xticks': None,
            'yticks': None,
            'cbar_ticks': None,
            'cbar_title': None,
            'cbar_title_bold': True,
            'cbar_labelpad': 10,
            'cbar_position': 'top',
            'cbar_pad': 0.02,
            'zoom_in': None,
            'show_points': False,
            'points_labels': None,
            'boundaries_lw': 1,
            'boundaries_ls': 'solid',
            'grid_lw': 0.1,
            'grid_ls': 'solid',
            'figsize': (4, 5),
            'figpad_inches': 0.1
        }

        style = MapInterpolation.check_cloupy_graphs_chosen_style()
        if style == 'default':
            pass
        elif style == 'retro':
            properties['text_size'] = 10
            cmap = 'Greys_r'
        else:
            raise ValueError("Invalid style value in the 'current_diagStyle.txt file!'")

        for param, arg in kwargs.items():
            try:
                properties[param]
            except KeyError:
                raise ValueError(f'Invalid parameter: {param}')
            else:
                properties[param] = arg

        if save is None:
            fig_dpi = 150
        else:
            fig_dpi = 300
        if properties['contours_levels'] is None:
            contour_levels = levels
        else:
            contour_levels = properties['contours_levels']
        tick_labels_size = properties['text_size'] * 0.8
        clabels_size = properties['text_size'] * 0.6
        cbar_tick_labels_size = properties['text_size'] * 0.8
        cbar_title_size = properties['text_size'] * 0.8
        title_size = properties['text_size'] * 1
        xlabel_size = properties['text_size'] * 0.8
        ylabel_size = properties['text_size'] * 0.8

        path = str(__file__)

        df = self.dataframe
        df.columns = ['value', 'lon', 'lat']
        x = list(df.lon)
        y = list(df.lat)
        z = list(df.value)

        fig, ax = plt.subplots(figsize=properties['figsize'], facecolor='white')
        shapes_for_plotting = get_shapes_for_plotting(
            ax, self.shapefile_path,
            self.crs, country=self.country,
        )

        # get extreme shape points and create an invisible box on which points for extrapolation will be placed
        the_low_x, the_high_x, the_low_y, the_high_y = MapInterpolation.get_extreme_shape_points(shapes_for_plotting)
        nodes = MapInterpolation.get_boundary_box(
            the_low_x, the_high_x, the_low_y, the_high_y,
            properties['zoom_in'], properties['extrapolation_into_zoomed_area']
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

        ax.tick_params(labelsize=tick_labels_size)

        if not show_frame:
            ax.set_frame_on(False)

        if not show_coordinates:
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)

        if not show_ticks:
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
            fill_contours, show_grid, cbar_tick_labels_size,
            cbar_title_size, title_size, xlabel_size,
            ylabel_size, fig_dpi, show_cbar, path
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

        if properties['show_points']:
            ax.scatter(df.lon, df.lat, s=10, c='k')

            if properties['points_labels'] is not None:
                for i, lon in enumerate(df.lon):
                    x = lon
                    y = df.lat[i]
                    if properties['points_labels'] == 'values' or properties['points_labels'] == 'value':
                        text = str(round(df.value[i], 1))
                    elif properties['points_labels'] == 'ids' or properties['points_labels'] == 'id':
                        text = df.index[i]
                    else:
                        raise ValueError("Invalid input for the 'points_labels' argument. Available inputs: 'values', "
                                         "'ids'"
                                         )

                    ax.text(x, y+0.2, text, size=clabels_size, ha='center')

        if add_shape is not None:
            draw_additional_shapes(add_shape, ax)

        plt.close()

        fig.savefig(
            path.replace('interpolation_map.py', 'map.png'),
            bbox_inches='tight',
            pad_inches=properties['figpad_inches'],
            dpi=fig_dpi
        )
        MapInterpolation.merge_map_with_mask(show_grid, path)
        done_map = Image.open(path.replace('interpolation_map.py', 'masked_map.png'))

        image_size = done_map.size
        resized_map = done_map.resize(
            (700, int(round(image_size[1]*(700/image_size[0]))))
        )

        if save is not None:
            done_map.save(save)

        return resized_map

    def d_imgw_data(
            self, years_range, column_with_values,
            interval='monthly', stations_kind='synop', check_continuity=False,
            continuity_precision=0.8
    ):
        """
         Download data for a drawing from the IMGW database.

        Keyword arguments
            years_range -- years range (e.g. range(2010, 2021))
            column_with_values -- the column index where the values for interpolation
        are located (single integer)
            interval -- the data interval ('monthly', 'daily', 'prompt') (default
        'monthly')
            stations_kind -- stations kind from the IMGW database ('synop', 'climat',
        'fall') (default 'synop')
            check_continuity -- if data continuity is to be checked. If the
        continuity is not satisfactory, the data will be filtered appropriately
        (default False)
            continuity_precision -- required precision for checking data continuity.
        The values must be in the 0-1 range. If the value is 1, then individual
        stations in the dataframe must have the same number of records as the station
        that has the longest data continuity. If the value is 0.5, then individual
        stations in the dataframe must have at least 50% of the number of records
        of the station that has the longest data continuity (e.g. if the largest
        number of records is 100, then at least 50 records are required) (default
        0.8)
        """
        import cloupy as cl
        from cloupy.data_processing.check_data_continuity import check_data_continuity

        if column_with_values == 'temp' or column_with_values == 'preci':

            df = cl.d_imgw_data(
                'monthly', 'synop', years_range,
                file_format='s_m_d', return_coordinates=True
            )
            if check_continuity:
                df = check_data_continuity(df, 1, continuity_precision)

            if column_with_values == 'temp':
                df = df.iloc[:, [1, 12, -3, -2]]
                df = df.groupby('Nazwa stacji').mean()
                self.dataframe = df

            if column_with_values == 'preci':
                df = df.iloc[:, [1, 2, 16, -3, -2]]
                for_lon_lat = df.groupby(['Rok', 'Nazwa stacji']).mean()
                df = df.groupby(['Rok', 'Nazwa stacji']).sum()

                df['lon'] = for_lon_lat.lon
                df['lat'] = for_lon_lat.lat
                df['station'] = df.index.get_level_values(1)

                df = df.groupby('station').mean()

        else:
            if not isinstance(column_with_values, int):
                raise ValueError("Invalid 'columns_with_values' argument. Use a single int.")

            df = cl.d_imgw_data(
                interval, stations_kind, years_range,
                file_format_index=0, return_coordinates=True
            )
            if check_continuity:
                df = check_data_continuity(df, 1, continuity_precision)

            df = df.iloc[:, [1, column_with_values, -3, -2]]
            df = df.groupby('Nazwa stacji').mean()

        self.dataframe = df

    def d_wmo_data(
            self, station_name, element_to_scrape,
            what_to_calc='mean', check_continuity=False, continuity_precision=0.3
    ):
        """
        Download data for a drawing from the WMO database.

        Keywords arguments:
            station_name -- name of the station for which the data will be downloaded.
        If 'cou' prefix added to 'station_name' and a country name appears after the
        prefix, the function will search for all stations in the specified country
            element_to_scrape -- which element from the WMO website will be scraped
        Available elements: 'temp', 'preci', 'temp_min', 'temp_max', 'sl_press'
            what_to_calc -- what to calculate from the downloaded data. Available
        values: 'max', 'min', 'median', 'mean' (default 'mean')
            check_continuity -- if data continuity is to be checked. If the
        continuity is not satisfactory, the data will be filtered appropriately
        (default False)
            continuity_precision -- required precision for checking data continuity.
        The values must be in the 0-1 range. If the value is 1, then individual
        stations in the dataframe must have the same number of records as the station
        that has the longest data continuity. If the value is 0.5, then individual
        stations in the dataframe must have at least 50% of the number of records
        of the station that has the longest data continuity (e.g. if the largest
        number of records is 100, then at least 50 records are required) (default
        0.3)

        ---------------NOTE THAT---------------
        Checking continuity of the data downloaded from the WMO website may not
        be correct. In the WMO database, many stations from the same country have
        significantly different data strings - for one station the string may start
        in 1850 and end in 2010, in another station the string may start in 1950
        and end in 2020. In such case, both stations have a decent data string and
        probably are representative, but the latter one will be dropped if the
        continuity precision is too high. Some stations have also a long data string,
        but many None values, which can also result in incorrect filtering.
        However, a properly selected 'continuity_precision' argument may be
        still be useful, but the data should always be checked manually.
        ---------------------------------------
        """
        import cloupy as cl
        from cloupy.data_processing.check_data_continuity import check_data_continuity

        df = cl.d_wmo_data(station_name, element_to_scrape, return_coordinates=True)
        if check_continuity:
            df = check_data_continuity(df, 0, continuity_precision)

        if element_to_scrape == 'preci':
            df = df.iloc[:, [0, 1, 3, -3, -2]]
            df_lat_lon = df.groupby(['year', 'station']).mean().iloc[:, [-1, -2]]
            df = df.groupby(['year', 'station']).sum()
            df['lon'] = df_lat_lon['lon']
            df['lat'] = df_lat_lon['lat']
        elif element_to_scrape in ['temp', 'sl_press', 'temp_min', 'temp_max']:
            df = df.iloc[:, [0, 3, -3, -2]]
        else:
            raise ValueError(
                "Invalid value for the 'element_to_scrape. Valid values: temp, preci, temp_max, temp_min, sl_press"
            )

        if what_to_calc == 'mean':
            df = df.groupby('station').mean()
        elif what_to_calc == 'max':
            df = df.groupby('station').max()
        elif what_to_calc == 'min':
            df = df.groupby('station').min()
        elif what_to_calc == 'median':
            df = df.groupby('station').median()
        else:
            raise ValueError("Invalid value for the 'what_to_calc' argument.")

        self.dataframe = df

    def import_global_df(
            self, columns_order, what_to_calc='mean',
            check_continuity=False, continuity_precision=0.8
    ):
        """
        Import data for WalterLieth.MapInterpolation from the global dataframe.

        Keyword arguments:
            columns_order -- specify which columns from the global dataframe are
        to be taken (a list of indexes). The first column must be a list of unique
        values for which calculations will be executed (station names), the second
        column must be a list of values which will be interpolated, the third column
        must be a list of longitudes (x-axis) and the fourth column must be a list
        of latitudes (y-axis). Some data requires special data processing, e.g.
        precipitation, for which a column with year is required. If you want to
        process precipitation data, please insert a column with years into the
        first place (before the unique values)
            what_to_calc -- what to calculate from the downloaded data. Available
        values: 'max', 'min', 'median', 'mean' (default 'mean')
            check_continuity -- if data continuity is to be checked. If the
        continuity is not satisfactory, the data will be filtered appropriately
        (default False)
            continuity_precision -- required precision for checking data continuity.
        The values must be in the 0-1 range. If the value is 1, then individual
        stations in the dataframe must have the same number of records as the station
        that has the longest data continuity. If the value is 0.5, then individual
        stations in the dataframe must have at least 50% of the number of records
        of the station that has the longest data continuity (e.g. if the largest
        number of records is 100, then at least 50 records are required) (default
        0.3)

        ---------------NOTE THAT---------------
        When the length of the list from the 'columns_order' argument is 5, then
        the data will be firstly grouped by years and unique values. After that,
        the sum of the values will be calculated for individual stations in
        individual years. When the sum is calculated, the dataframe will be grouped
        again by unique values again and the selected statistic will be calculated.
        The discussed data processing will result in proper values for elements
        such as precipitation in the monthly data interval.
        ---------------------------------------
        """
        from cloupy import read_global_df
        from cloupy.data_processing.check_data_continuity import check_data_continuity
        import pandas as pd

        df = read_global_df()
        df = df.iloc[:, columns_order]

        if len(df.columns) == 5:
            sort_by = 1
        elif len(df.columns) == 4:
            sort_by = 0
        else:
            raise ValueError(
                "Invalid 'columns_order' argument. The 'columns_order' argument length must be 4 or 5 - see "
                "cloupy.MapInterpolation docstring for more info."
            )

        if check_continuity:
            df = check_data_continuity(df, sort_by, continuity_precision)

        if len(df.columns) == 5:
            df_lat_lon = df.groupby([df.columns[0], df.columns[1]]).mean().iloc[:, [-2, -1]]
            df = df.groupby([df.columns[0], df.columns[1]]).sum()
            stations = df.index.get_level_values(1)

            df = pd.DataFrame({
                0: stations,
                1: list(df.iloc[:, 0]),
                2: df_lat_lon.iloc[:, -2],
                3: df_lat_lon.iloc[:, -1]
            })

        if what_to_calc == 'mean':
            df = df.groupby(df.columns[0]).mean()
        elif what_to_calc == 'median':
            df = df.groupby(df.columns[0]).median()
        elif what_to_calc == 'max':
            df = df.groupby(df.columns[0]).max()
        elif what_to_calc == 'min':
            df = df.groupby(df.columns[0]).min()
        else:
            raise ValueError(
                "Invalid input for the 'what_to_calc' argument. Valid values: 'max', 'min', 'median', 'mean'. See "
                "MapInterpolation.import_global_df() docstring for more info."
            )

        self.dataframe = df
    
    @staticmethod
    def check_if_valid_args_and_update_class_attrs(
            shapefile_path, country, crs, dataframe
    ):
        """
        Check that the input values do not conflict with each other and return a
        dictionary with the attributes that will be updated if the check is positive
        """
        import os

        to_be_updated = {
            'shapefile_path': shapefile_path,
            'country':  country,
            'crs': crs
        }

        if shapefile_path is None and country is None:
            raise ValueError(
                "Specify which countries are to be drawn (by passing a string with the country name or a list of strings "
                "with the country names). Alternatively, you can specify your non-default shapefile for which boundaries "
                "will be drawn (by passing the shapefile's path to the 'shapefile_path' argument and passing the "
                "shapefile's coordinates system to the 'crs' argument."
            )

        elif shapefile_path is None and country is not None:
            shapefile_path = str(__file__).replace('interpolation_map.py', f'world{os.sep}ne_50m_admin_0_countries.shp')
            crs = 'epsg:4326'

            to_be_updated['shapefile_path'] = shapefile_path
            to_be_updated['crs'] = crs

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
                    "Invalid argument combination. The 'country' argument is valid only for the default cloupy "
                    "shapefile. Set 'country' back to None or 'shapefile_path' back to None."
                )

        else:
            country = None
            to_be_updated['country'] = country

        if dataframe is None:
            raise ValueError(
                "No data specified. Please provide the data for the interpolation manually or use one of "
                "the downloading methods"
                             )

        return to_be_updated

    @staticmethod
    def check_cloupy_graphs_chosen_style():
        import os

        with open(str(__file__).replace(f'maps{os.sep}interpolation_map.py', 'current_diagStyle.txt'), 'r') as f:
            style = f.readline()

        return style

    @staticmethod
    def get_extreme_shape_points(shapes_for_plotting):
        """Return extreme points of the shapes"""

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
        """
        Return points to draw an invisible box outside the shapes to which the
        values will be extrapolated
        """
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
        """
        Return points (located on the invisible box) on which the extrapolation
        process will be based
        """

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
        """
        Identify which points from the data are the closest to the points on which
        the extrapolation process will be based and return a dictionary in which
        keys are the extrapolation points and values are the values that the points
        take
        """
        from cloupy.maps.draw_shapes import calc_the_distance

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
        """Interpolate the data and return xi, yi, zi values"""
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
            shapes_for_plotting, fill_contours, show_grid,
            cbar_tick_labels_size, cbar_title_size, title_size,
            xlabel_size, ylabel_size, fig_dpi,
            show_cbar, path
    ):
        """Adjust the map for creating masks and create necessary masks"""
        import matplotlib.pyplot as plt

        fig_for_colorbar, ax_for_colorbar = plt.subplots()
        if fill_contours and show_cbar:
            cntr = ax_for_colorbar.contourf(xi, yi, zi, levels=levels, cmap=cmap)
            cbar = plt.colorbar(
                cntr, ax=ax, location=properties['cbar_position'],
                pad=properties['cbar_pad']
            )
            cbar.ax.tick_params(labelsize=cbar_tick_labels_size)

            if properties['cbar_ticks'] is not None:
                cbar.set_ticks(properties['cbar_ticks'])

            if properties['cbar_title'] is not None:
                if properties['cbar_title_bold']:
                    fontweight = 'bold'
                else:
                    fontweight = 'normal'
                cbar.set_label(
                    properties['cbar_title'], size=cbar_title_size,
                    fontweight=fontweight, labelpad=properties['cbar_labelpad']
                )

        if properties['title'] is not None:

            if properties['title_bold']:
                fontweight = 'bold'
            else:
                fontweight = 'normal'

            fig.suptitle(
                properties['title'], size=title_size, ha=properties['title_ha'],
                x=properties['title_x_position'], y=properties['title_y_position'],
                fontweight=fontweight
            )

        if properties['xlabel'] is not None:
            if properties['xlabel_bold']:
                fontweight = 'bold'
            else:
                fontweight = 'normal'
            ax.set_xlabel(properties['xlabel'], size=xlabel_size, fontweight=fontweight)

        if properties['ylabel'] is not None:
            if properties['ylabel_bold']:
                fontweight = 'bold'
            else:
                fontweight = 'normal'
            ax.set_ylabel(properties['ylabel'], size=ylabel_size, fontweight=fontweight)

        if show_grid:
            ax.grid(lw=properties['grid_lw'], ls=properties['grid_ls'])
            fig.savefig(
                path.replace('interpolation_map.py', 'grid_mask.png'),
                transparent=True,
                bbox_inches='tight',
                pad_inches=properties['figpad_inches'],
                dpi=fig_dpi
            )
            ax.grid(False)
        plt.close()

        rgba = MapInterpolation.suit_rgba_to_matplotlib((1, 0, 0, 1))
        for shape in shapes_for_plotting:
            ax.plot(shape[0], shape[1], color='k', lw=properties['boundaries_lw'], ls=properties['boundaries_ls'])
            ax.fill(shape[0], shape[1], color=rgba, zorder=0)

        fig.savefig(
            path.replace('interpolation_map.py', 'mask.png'),
            facecolor=fig.get_facecolor(),
            transparent=True,
            bbox_inches='tight',
            pad_inches=properties['figpad_inches'],
            dpi=fig_dpi
        )
        MapInterpolation.create_mask(path.replace('interpolation_map.py', 'mask.png'))
        for shape in shapes_for_plotting:
            ax.fill(shape[0], shape[1], color='white', zorder=0)

    @staticmethod
    def suit_rgba_to_matplotlib(rgba):
        """Convert typical RGBA values for the values which matplotlib accepts"""
        red = rgba[0] / 255
        green = rgba[1] / 255
        blue = rgba[2] / 255
        alpha = rgba[3]

        if alpha > 1 or alpha < 0:
            raise ValueError(f'Alpha should be within 0-1 range! Alpha: {alpha}')

        return red, green, blue, alpha

    @staticmethod
    def create_mask(fname):
        """Create the map mask"""
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
    def merge_map_with_mask(show_grid, path):
        """Merge completed map with the previously created masks"""
        from PIL import Image

        background = Image.open(path.replace("interpolation_map.py", "map.png"))
        foreground = Image.open(path.replace("interpolation_map.py", "mask.png"))
        background.paste(foreground, (0, 0), foreground)

        if show_grid:
            grid = Image.open(path.replace('interpolation_map.py', 'grid_mask.png'))
            background.paste(grid, (0, 0), grid)

        background.save(path.replace("interpolation_map.py", 'masked_map.png'))
