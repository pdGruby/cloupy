class WalterLieth:
    """
    Create WalterLieth object where data for drawing Walter-Lieth diagram can be
    downloaded, modified, manually provided.

    Keyword arguments:
    station_name -- station name for which data will be drawn
    years_range -- years range for which data will be drawn
    dataframe -- data for drawing (default None)
    lat -- latitude of the station (default None)
    lon -- longitude of the station (default None)
    elevation -- elevation of the station (default None)

    ---------------METHODS---------------
    draw()
    d_imgw_data()
    d_imgw_coordinates()
    dw_wmo_data()
    import_global_df()
    -------------------------------------

    ---------------DATA STRUCTURE---------------
    Supported data structure for WalterLieth.dataframe is 5 or 6 columns of
    pandas.DataFrame object, depending on the data interval. Supported data
    intervals are daily and monthly.

    If data interval is monthly, then 5 columns are required:
    1st column: months,
    2nd column: average air temperature,
    3rd column: average sum of precipitation,
    4th column: absolute maximum air temperature,
    5th column: absolute minimum air temperature

    If data interval is daily, then 6 columns are required:
    1st column: years,
    2nd column: months,
    3rd column: average air temperature,
    4th column: sum of precipitation,
    5th column: absoulte maximum air temperature,
    6th column: absolute minimum air temperature

    Exemplary dataframe:
    import pandas as pd
    dataframe = pd.DataFrame({
                'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'temp': [-2, -1, 0, 7, 15, 18, 19, 20, 18, 14, 8, 3],
                'preci': [50, 25, 55, 60, 70, 80, 90, 80, 68, 50, 45, 49],
                'max_temp': [10, 15, 17, 18, 19, 20, 35, 34, 25, 20, 15, 10],
                'min_temp': [-36, -29, -20, -15, -5, -1, 1, 2, -1, -4, -18, -22]
                            })

    Note that data must be provided for every single month. In another case,
    Walter-Lieth diagram is not possible to be drawn.
    --------------------------------------------
    """

    def __init__(
            self, station_name, years_range=None,
            dataframe=None, lat=False, lon=False,
            elevation=False
    ):
        self.dataframe = dataframe
        self.years_range = years_range
        self.station_name = station_name.upper()
        self.lat = lat
        self.lon = lon
        self.elevation = elevation

    def draw(
            self, figsize=(7.74, 7.74), language=None,
            freeze_rectangles=True, title_text=True, years_text=True,
            coordinates_box=True, yearly_means_box=True, extremes_box=True,
            legend_box=True
    ):
        """
        Specify which elements have to be drawn and draw Walter-Lieth diagram.

        Keyword arguments:
        figsize -- figure size (default (7.74, 7.74))
        language -- choose language (None, 'POL', 'ENG') (default None). If
        None, then choose default language, which is 'ENG'
        freeze_rectangles -- if bottom rectangles which show freeze periods have
        to be drawn (default True)
        title_text -- if station name has to be drawn (default True)
        years_text -- if years range has to be drawn (default True)
        coordinates_box -- if box with coordinates info has to be drawn (default
        True)
        yearly_means_box -- if box with yearly means has to be drawn (default
        True)
        extremes_box -- if box with extreme temperatures has to be drawn
        (default True)
        legend_box -- if legend has to be drawn (default True)
        """

        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        from matplotlib import rcParams

        if self.dataframe is None or self.dataframe.empty:
            raise AttributeError(
                """
                No data in WalterLieth.dataframe. Input data on your own or use WalterLieth's methods: WalterLieth.d_imgw_data,
                WalterLieth.d_wmo_data, WalterLieth.import_global_df
                """)

        ls_prop_cycle = rcParams['axes.prop_cycle'].by_key()['linestyle']
        color_prop_cycle = rcParams['axes.prop_cycle'].by_key()['color']
        if WalterLieth.check_cloudy_graphs_chosen_style(ls_prop_cycle, color_prop_cycle) == 'retro':
            temp_linecolor = 'k'
            temp_linestyle = '-.'

            preci_linecolor = 'k'
            preci_linestyle = '-'

            zero_linecolor = 'k'
            zero_linestyle = 'dotted'

            freeze_color = '#767676'
            likely_freeze_color = '#b6b6b6'

            dry_period_hatch = '..'
            dry_period_hatch_color = '#b6b6b6'

            wet_period_hatch = '||'
            wet_period_hatch_color = 'k'

        else:  # default or customized
            temp_linecolor = 'r'
            temp_linestyle = '-'

            preci_linecolor = '#1f77b4'
            preci_linestyle = '-'

            zero_linecolor = 'k'
            zero_linestyle = 'dotted'

            freeze_color = '#09d1d9'
            likely_freeze_color = '#c8f8fa'  # b3fcff

            dry_period_hatch = '..'
            dry_period_hatch_color = 'r'

            wet_period_hatch = '||'
            wet_period_hatch_color = '#1f77b4'

        if language == 'POL':
            asl = 'Wysokość: {} m n.p.m.'
            lat = 'Szerokość geograficzna: {}'
            lon = 'Długość geograficzna: {}'
            temp_label = 'Średnia roczna temperatura: {}°C'
            preci_label = 'Roczna suma opadów: {} mm'
            x_ticks_labels = ['S', 'L', 'M', 'K', 'M', 'C', 'L', 'S', 'W', 'P', 'L', 'G']
            temp_axis_ylabel = 'Średnia miesięczna temperatura powietrza [°C]'
            if freeze_rectangles:
                temp_axis_xlabel = 'Miesiące z prawdopodobieństwem wystąpienia przymrozku'
            else:
                temp_axis_xlabel = 'Miesiące'
            preci_axis_ylabel = 'Średnia miesięczna suma opadów [mm]'
            freeze_legend_label = 'przymrozek'
            likely_freeze_legend_label = 'możliwy przymr.'
            temp_legend_label = 'temp. powietrza'
            preci_legend_label = 'opad atmosf.'
            humid_period_legend_label = 'okres wilg.'
            wet_period_legend_label = 'okres mokry'
            dry_period_legend_label = 'okres suchy'
        else:
            asl = 'Elevation: {} m a.s.l.'
            lat = 'Latitude: {}'
            lon = 'Longitude: {}'
            temp_label = 'Average air temperature: {}°C'
            preci_label = 'Annual precipitation: {} mm'
            x_ticks_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
            temp_axis_ylabel = 'Average monthly air temperature [°C]'
            if freeze_rectangles:
                temp_axis_xlabel = 'Months and probability of freeze occurrence'
            else:
                temp_axis_xlabel = 'Months'
            preci_axis_ylabel = 'Average monthly precipitation sum [mm]'
            freeze_legend_label = 'freeze'
            likely_freeze_legend_label = 'likely freeze'
            temp_legend_label = 'air temp.'
            preci_legend_label = 'precipit.'
            humid_period_legend_label = 'humid period'
            wet_period_legend_label = 'wet period'
            dry_period_legend_label = 'dry period'

        title = self.station_name
        if self.years_range is None:
            years = False
        elif len(self.years_range) == 1:
            years = self.years_range[0]
        else:
            years = f'{str(min(self.years_range))}-{str(max(self.years_range))}'

        if self.lat:
            lat = lat.format(self.lat)

        if self.lon:
            lon = lon.format(self.lon)

        if self.elevation:
            asl = asl.format(self.elevation)

        #  data converting
        if len(self.dataframe.columns) == 5:
            mean_temperature = self.dataframe.groupby(self.dataframe.columns[0]).mean().iloc[:, 0]
            precipitation = self.dataframe.groupby(self.dataframe.columns[0]).mean().iloc[:, 1]
            abs_max_temp = self.dataframe.groupby(self.dataframe.columns[0]).max().iloc[:, 2]
            abs_min_temp = self.dataframe.groupby(self.dataframe.columns[0]).min().iloc[:, 3]
        elif len(self.dataframe.columns) == 6:
            mean_temperature = self.dataframe.groupby(self.dataframe.columns[1]).mean().iloc[:, 1]
            precipitation = self.dataframe.groupby([self.dataframe.columns[0], self.dataframe.columns[1]]).sum()
            precipitation = precipitation.groupby(self.dataframe.columns[1]).mean().iloc[:, 1]
            abs_max_temp = self.dataframe.groupby(self.dataframe.columns[1]).max().iloc[:, 3]
            abs_min_temp = self.dataframe.groupby(self.dataframe.columns[1]).min().iloc[:, 4]
        else:
            raise AttributeError(
                f"""
                Data in cloudy.WalterLieth.dataframe has {len(self.dataframe.index)} columns which is invalid. Input 5 or 6 columns
                depending on data interval.
                """)

        if precipitation.min() < 0:
            raise ValueError(
                f"""
                Value below 0 mm occured in precipitation series.
                Invalid value: {precipitation.min()}
                """)

        if mean_temperature.max() > 50:
            raise ValueError(
                f"""
                Monthly mean temperature exceeded 50°C!
                Invalid value: {mean_temperature.max()}
                """)

        annual_mean_temp = round(mean_temperature.mean(), 1)
        sum_preci = round(precipitation.sum(), 1)

        maxtwm_mintcm = WalterLieth.get_max_twm_and_min_tcm(mean_temperature, abs_max_temp, abs_min_temp)
        max_temp = round(maxtwm_mintcm[0], 1)
        min_temp = round(maxtwm_mintcm[1], 1)

        x_major_ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
        x_minor_ticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        temp_yaxis_ticks = WalterLieth.get_temp_yticks(mean_temperature)
        upper_axis_max_tick = WalterLieth.get_max_ytick_for_precipitation(precipitation)

        if freeze_rectangles:
            if min(temp_yaxis_ticks) < -45:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 2.7
            elif min(temp_yaxis_ticks) == -40:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 2.5
            elif min(temp_yaxis_ticks) == -30:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 2.3
            elif min(temp_yaxis_ticks) == -20:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 2
            elif min(temp_yaxis_ticks) == -10:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 1.65
            else:
                y_value_for_closing_bottom_rectangles = min(temp_yaxis_ticks) + 1.45
        else:
            y_value_for_closing_bottom_rectangles = None

        fig, temp_axis = plt.subplots(figsize=figsize)
        fig.patch.set_alpha(1)

        if title and title_text:
            fig.suptitle(title, x=0.14, size=16, ha='left', fontweight='bold')
        if self.elevation and coordinates_box:
            fig.text(0.14, 0.933, asl)
        if self.lat and coordinates_box:
            fig.text(0.14, 0.91, lat)
        if self.lon and coordinates_box:
            fig.text(0.14, 0.887, lon)
        if years and years_text:
            fig.text(0.88, 0.935, years, size=14, ha='right', fontweight='bold')
        if yearly_means_box:
            fig.text(0.88, 0.91, temp_label.format(annual_mean_temp), ha='right')
            fig.text(0.88, 0.887, preci_label.format(sum_preci), ha='right')
        if extremes_box:
            fig.text(0.08, 0.86, 'Max:', ha='center')
            fig.text(0.08, 0.86 - 0.023, f'{str(max_temp)}°C', ha='center')
            fig.text(0.08, 0.80, 'Min:', ha='center')
            fig.text(0.08, 0.80 - 0.023, f'{str(min_temp)}°C', ha='center')

        temp_axis.set_xticks(x_major_ticks)
        temp_axis.set_xticks(x_minor_ticks, minor=True)
        temp_axis.set_xticklabels(x_ticks_labels)
        temp_axis.set_xlim(0, max(x_minor_ticks))
        temp_axis.set_yticks(temp_yaxis_ticks)
        temp_axis.set_ylim(min(temp_yaxis_ticks), max(temp_yaxis_ticks))
        temp_axis.tick_params(axis='y', which='major', length=6)
        temp_axis.tick_params(axis='x', which='minor', length=0)
        temp_axis.tick_params(axis='x', which='major', length=0)

        if freeze_rectangles and y_value_for_closing_bottom_rectangles is not None:
            temp_axis.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                           [(k * 0) + y_value_for_closing_bottom_rectangles for k in range(0, 13)],
                           linewidth=1, color='k')

        for month in range(0, 13):
            temp_axis.plot([month, month],
                           [min(temp_yaxis_ticks), y_value_for_closing_bottom_rectangles],
                           color='k', linestyle='solid', linewidth=1)

        if min(mean_temperature) < 0:
            temp_axis.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [k * 0 for k in range(0, 13)],
                           color=zero_linecolor, linewidth=1, linestyle=zero_linestyle)

        preci_axis = temp_axis.secondary_yaxis('right')
        preci_axis.set_yticks([tick for tick in temp_yaxis_ticks if tick >= 0])
        preci_axis.set_yticklabels([tick * 2 for tick in temp_yaxis_ticks if tick >= 0])
        preci_axis.tick_params(axis='both', which='major', length=6)

        divider = make_axes_locatable(temp_axis)
        upper_axis = divider.append_axes("top", size=1, pad=0)
        upper_axis.tick_params(axis='y', length=6)
        upper_axis.set_xticks(x_major_ticks)
        upper_axis.set_xticks(x_minor_ticks, minor=True)
        upper_axis.set_xticklabels(['', '', '', '', '', '', '', '', '', '', '', ''])
        upper_axis.set_xlim(0, max(x_minor_ticks))
        upper_axis.set_yticks([upper_axis_max_tick])
        upper_axis.set_yticks([], minor=True)
        upper_axis.set_ylim((100, upper_axis_max_tick))
        upper_axis.yaxis.tick_right()
        upper_axis.set_yticklabels([str(upper_axis_max_tick)])
        upper_axis.tick_params(axis='x', which='both', color=[0, 0, 0, 0])
        upper_axis.spines['top'].set_color('white')
        upper_axis.text(-0.01, upper_axis_max_tick + (upper_axis_max_tick * 0.015),
                        '_', ha='right', fontweight='bold', size=11).set_fontname('Times New Roman')
        temp_axis.set_ylabel(temp_axis_ylabel)
        temp_axis.set_xlabel(temp_axis_xlabel)
        preci_axis.set_ylabel(preci_axis_ylabel)

        x_for_plotting = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12]
        interpolated_margins = WalterLieth.interpolate_margins(mean_temperature, precipitation)
        mean_temperature = interpolated_margins[0]
        precipitation = interpolated_margins[1]

        temp_axis.plot(x_for_plotting, mean_temperature, color=temp_linecolor, linestyle=temp_linestyle,
                       label=temp_legend_label)
        temp_axis.plot(x_for_plotting, [p / 2 for p in precipitation], color=preci_linecolor, linestyle=preci_linestyle,
                       label=preci_legend_label)
        upper_axis.plot(x_for_plotting, precipitation, color=preci_linecolor, linestyle=preci_linestyle,
                        label=preci_legend_label)

        periods = WalterLieth.distinguish_between_wet_and_dry(mean_temperature, precipitation)
        wet_periods = periods[0]
        dry_periods = periods[1]

        for period in wet_periods:
            where = [False, False, False, False,
                     False, False, False, False,
                     False, False, False, False,
                     False, False]
            for index in range(period[0], period[1] + 1):
                where[index] = True
            temp_axis.fill_between(x_for_plotting, [p / 2 for p in precipitation], mean_temperature,
                                   where=where, interpolate=True, hatch=wet_period_hatch,
                                   color='none', edgecolor=wet_period_hatch_color, linewidth=0.0,
                                   label=humid_period_legend_label)
            if max(precipitation) > 100:
                upper_axis.fill_between(x_for_plotting, precipitation, 100,
                                        where=where, interpolate=True, hatch=None,
                                        color=wet_period_hatch_color, label=wet_period_legend_label)

        for period in dry_periods:
            where = [False, False, False, False,
                     False, False, False, False,
                     False, False, False, False,
                     False, False]
            for index in range(period[0], period[1] + 1):
                where[index] = True
            temp_axis.fill_between(x_for_plotting, [p / 2 for p in precipitation], mean_temperature,
                                   where=where, interpolate=True, hatch=dry_period_hatch,
                                   color='none', edgecolor=dry_period_hatch_color, linewidth=0.0,
                                   label=dry_period_legend_label)

        if freeze_rectangles:
            if_freeze = WalterLieth.determine_if_freeze(abs_min_temp)
            likely = if_freeze[0]
            freeze = if_freeze[1]

            temp_axis.fill_between([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                   [k * 0 + min(temp_yaxis_ticks) for k in range(0, 13)],
                                   y_value_for_closing_bottom_rectangles,
                                   color='white',
                                   )

            if freeze:
                where = [False, False, False, False,
                         False, False, False, False,
                         False, False, False, False,
                         False]
                for index in freeze:
                    where[index] = True
                    where[index + 1] = True
                temp_axis.fill_between([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                       [k * 0 + min(temp_yaxis_ticks) for k in range(0, 13)],
                                       y_value_for_closing_bottom_rectangles,
                                       where=where, color=freeze_color,
                                       label=freeze_legend_label)

            if likely:
                where = [False, False, False, False,
                         False, False, False, False,
                         False, False, False, False,
                         False]
                for index in likely:
                    where[index] = True
                    where[index + 1] = True
                temp_axis.fill_between([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                       [k * 0 + min(temp_yaxis_ticks) for k in range(0, 13)],
                                       y_value_for_closing_bottom_rectangles,
                                       where=where, color=likely_freeze_color,
                                       label=likely_freeze_legend_label)

        if legend_box:
            handles, labels = temp_axis.get_legend_handles_labels()
            if max(precipitation) > 100:
                handles.append(upper_axis.get_legend_handles_labels()[0][1])
                labels.append(upper_axis.get_legend_handles_labels()[1][1])

            doubled_labels = []
            for label in labels:
                if labels.count(label) > 1:
                    doubled_labels.append(label)

            for label in doubled_labels:
                while labels.count(label) > 1:
                    labels.remove(label)
                    handles.remove(handles[labels.index(label)])

            if len(labels) % 3 == 0:
                NCOL = 3
            elif len(labels) % 2 == 0:
                NCOL = 2
            elif len(labels) % 5 == 0:
                NCOL = 5
            else:
                NCOL = 4

            fig.legend(handles, labels, loc='lower center', ncol=NCOL, bbox_to_anchor=(0.52, 0))

    def d_imgw_data(
            self, years_range, interval='monthly',
            stations_kind='synop', filtr_station=True, check_years=True
    ):
        """
        Download data for drawing from IMGW database.

        Keyword arguments:
        years_range -- years range (eg. range(2010, 2021))
        interval -- data interval ('monthly', 'daily', 'prompt') (default
        'monthly')
        stations_kind -- stations kind from IMGW database ('synop', 'climat',
        'fall') (default 'synop')
        filtr_station -- if downloaded data has to be filtered by
        WalterLieth.station_name (default True)
        check_years -- check if years range in downloaded data matches years
        range from WalterLieth.years_range. If not, change
        WalterLieth.years_range depending on years range in downloaded data
        (default True)
        """

        import cloudy.scraping.imgw as imgw_scraping

        if interval == 'monthly':
            data = imgw_scraping.get_meteorological_data(
                years_range=years_range, period=interval,
                stations_kind=stations_kind, file_format_index=0,
                keywords=['Rok', 'Nazwa stacji', 'Miesiąc',
                          'Średnia temperatura miesięczna [°C]',
                          'Miesieczna suma opadów [mm]',
                          'Absolutna temperatura maksymalna [°C]',
                          'Absolutna temperatura minimalna [°C]']
            )
            if filtr_station:
                data = data[data['Nazwa stacji'] == self.station_name]

            if check_years:
                max_year = data.loc[:, 'Rok'].max()
                min_year = data.loc[:, 'Rok'].min()
                self.years_range = range(min_year, max_year + 1)

            data = data.drop(['Nazwa stacji', 'Rok'], axis=1)
            if data.empty:
                raise ValueError(
                    """
                    No data for specified parameters found. Check if input arguments in 'WalterLieth.d_imgw_data' method
                    are valid.
                    """)

        elif interval == 'daily':
            if not filtr_station:
                raise AttributeError(
                    """
                        'cloudy.WalterLieth.d_imgw_data' does not support given combination: 
                        interval='daily', filtr_station=False. Use interval='monthly' instead 
                        or stick with daily interval and input filtr_station=True.
                        """)

            data = imgw_scraping.get_meteorological_data(
                years_range=self.years_range, period=interval,
                stations_kind=stations_kind, file_format_index=0,
                keywords=['Rok', 'Nazwa stacji', 'Miesiąc',
                          'Średnia temperatura dobowa [°C]',
                          'Suma dobowa opadów [mm]',  # w k_d jest 'ów'
                          'Suma dobowa opadu [mm]',  # w s_d jest 'u'. dziwne.
                          'Maksymalna temperatura dobowa [°C]',
                          'Minimalna temperatura dobowa [°C]']
            )

            data = data[data['Nazwa stacji'] == self.station_name]
            if check_years:
                max_year = data.loc[:, 'Rok'].max()
                min_year = data.loc[:, 'Rok'].min()
                self.years_range = range(min_year, max_year + 1)

            data = data.drop(['Nazwa stacji'], axis=1)
            if data.empty:
                raise ValueError(
                    """
                    No data for specified parameters found. Check if input arguments in 'WalterLieth.d_imgw_data' method
                    are valid.
                    """)
        else:
            raise ValueError(
                """
                    No data for specified parameters found. Check if input arguments in 'WalterLieth.d_imgw_data' method
                    are valid. Check 'interval' argument.
                    """)

        self.dataframe = data

    def d_wmo_data(
            self, nearby_stations=True, return_coordinates=True,
            check_years=True
    ):

        import cloudy.scraping.climex_scraping as wmo_scraping

        data = wmo_scraping.download_meteo_data(
            self.station_name, ['temp', 'preci', 'temp_max', 'temp_min'],
            nearby_stations=nearby_stations, return_coordinates=return_coordinates
        )

        if check_years:
            min_year = data['year'].min()
            max_year = data['year'].max()
            self.years_range = range(min_year, max_year + 1)

        data = data.drop(['station', 'year'], axis=1)

        if return_coordinates:
            lat = data['lat'].mean()
            lon = data['lon'].mean()
            elv = data['elv'].mean()

            self.lat = float(round(lat, 2))
            self.lon = float(round(lon, 2))
            self.elevation = int(round(elv))

            data = data.drop(['lat', 'lon', 'elv'], axis=1)

        for element in ['temp', 'preci', 'temp_max', 'temp_min']:
            try:
                data[element]
            except KeyError:
                if element == 'preci' or element == 'temp':
                    raise AttributeError(
                        f"""
                        No essential data for '{element}' was downloaded - please, try again. If it does not fix the 
                        problem, there's a high possibility of required data lack on the WMO website.
                        """
                    )
                else:
                    data[element] = [None] * len(data.index)
            else:
                continue

        for element in ['temp', 'preci', 'temp_max', 'temp_min']:
            if data[element].isnull().all():
                if element == 'temp' or element == 'preci':
                    raise AttributeError(
                        f"""
                        No required data for '{element}'. It seems like the data was downloaded, but actually the column contains
                        only None values.
                        """
                    )
                elif element == 'temp_min':
                    print(
                        f"""
                        WARNING: no data found for '{element}'. It is not required for drawing, but the box with extreme
                        temperatures will show None value. The probability of freeze occurence neither can be calculated,
                        so the rectangles will be blank. You can tell drawing function not to draw above elements:
                        freeze_rectangles=False, extreme_box=False.
                        """
                    )
                else:
                    print(
                        f"""
                        WARNING: no data found for '{element}'. It is not required for drawing, but the box with extreme
                        temperatures will show None value. You can tell drawing function not to draw box with extreme temperatures:
                        extreme_box=False.
                        """
                    )
        self.dataframe = data

    def d_imgw_coordinates(
            self, latitude=True, longitude=True, elevation=True
    ):
        """
        Download coordinates for the specified station of IMGW database.

        Keyword arguments:
        latitude -- if WalterLieth.lat has to be updated (default True)
        longitude -- if WalterLieth.lon has to be updated (default True)
        elevation -- if WalterLieth.elv has to be updated (default True)
        """

        import cloudy.scraping.imgw as imgw_scraping

        cor_elev = imgw_scraping.get_coordinates_and_elevation(self.station_name)

        for key, value in cor_elev.items():

            if key != 'elv':
                if '.' in str(value):
                    new_value = str(value)
                else:
                    new_value = str(value) + '.'

                while len(new_value.split('.')[1]) != 2:
                    new_value += '0'

                cor_elev[key] = new_value

            else:
                cor_elev[key] = round(value)

        if latitude:
            self.lat = cor_elev['lat']
        if longitude:
            self.lon = cor_elev['lon']
        if elevation:
            self.elevation = cor_elev['elv']

    def import_global_df(
            self, columns_order, filtr_station=True,
            check_years=True
    ):
        """
        Import data for WalterLieth.dataframe from global data frame.

        Keyword arguments:
        columns_order -- specify which columns from global data frame have to be
        taken (list of indexes, 'imgw_monthly', 'imgw_daily'). If global data frame
        comes from IMGW database and it's structure has not been modified in any
        way, then 'imgw_monthly' or 'imgw_daily' can be used - depending on data
        interval
        filtr_station -- if downloaded data has to be filtered by WalterLieth.station_name.
        It makes a difference only if 'columns_order' argument is 'imgw_monthly'
        or 'imgw_daily' (default True)
        check_years -- check if years range in global DataFrame matches WalterLieth.years_range.
        If not, change WalterLieth.years_range depending on years range in global DataFrame
        data. It makes a difference only if 'columns_order' argument is 'imgw_monthly'
        or 'imgw_daily' (default True)
        """

        from cloudy import read_global_df

        if isinstance(columns_order, list) and not isinstance(columns_order[0], int):
            raise AttributeError(
                """
                1. Use list of ints to specify which columns from global pandas.DataFrame are necessary for drawing.
                2. Remember that you can get accurate info about required data structure in cloudy.WalterLieth docs.
                3. Alternatively, if your data's source is IMGW database you can use 'imgw_monthly' or 'imgw_daily' strings 
                for your input.
                """)

        if columns_order != 'imgw_monthly' and columns_order != 'imgw_daily' and not isinstance(columns_order, list):
            raise AttributeError(
                """
                Valid arguments 'columns_order': 'imgw_monthly', 'imgw_daily', [list of 5 or 6 ints]
                If your data's source is IMGW database and default columns order of the dataframe is preserved,
                you can input 'imgw_monthly' or 'imgw_daily' values for 'columns_order' argument (depending on data interval).
                """)

        df = read_global_df()

        if 'imgw' in columns_order:
            if columns_order == 'imgw_monthly':
                df_for_object = df.iloc[:, [1, 2, 3, 12, 16, 4, 8]]
            else:
                df_for_object = df.iloc[:, [1, 2, 3, 9, 13, 5, 7]]

            if filtr_station:
                df_for_object = df_for_object[df_for_object.iloc[:, 0] == self.station_name]
                if df_for_object.empty:
                    raise ValueError(
                        """
                        Dataframe has just been filtered and the output was empty. Check your inputs which may affect filtering.
                        
                        1. It's possible that input for 'station_name' in 'cloudy.WalterLieth' is invalid.
                        2. You can also be looking for the station which is not available in global pandas.DataFrame.
                        3. If you have changed default column order from IMGW database the function will return this exception.
                        4. Check if your DataFrame does not contain any unnecessary column. It is possible that 'index_col=0'
                        argument will handle the problem if you have read csv file by pandas.read_csv() for setting the global
                        DataFrame.
                        5. If you're willing not to filtr data by 'station_name', you can set 'filtr_station' argument to
                        {False}. It's not recommended to plot data from more stations than one, but this argument
                        has been created mainly for this purpose - just in case.
                        """
                    )

            if check_years:
                max_year = df_for_object.iloc[:, 1].max()
                min_year = df_for_object.iloc[:, 1].min()
                self.years_range = range(min_year, max_year + 1)

            df_for_object = df_for_object.drop(df_for_object.columns[0], axis=1)  # station names
            if columns_order == 'imgw_monthly':
                df_for_object = df_for_object.drop(df_for_object.columns[0], axis=1)  # years

            self.dataframe = df_for_object
        else:
            df_for_object = df.iloc[:, columns_order]
            self.dataframe = df_for_object

    @staticmethod
    def check_cloudy_graphs_chosen_style(
            ls_prop_cycle, color_prop_cycle
    ):
        if ls_prop_cycle.count('-') == 10:
            return 'default'
        elif ls_prop_cycle.count('-') == 1 and color_prop_cycle.count('k') == 6:
            return 'retro'
        else:
            return 'customized'

    @staticmethod
    def get_max_twm_and_min_tcm(
            mean_temperature, abs_max_temp, abs_min_temp
    ):

        the_highest_temp = mean_temperature.max()
        the_lowest_temp = mean_temperature.min()

        the_warmest_month = None
        the_coldest_month = None
        for index, temp in enumerate(mean_temperature):
            if temp == the_highest_temp:
                the_warmest_month = index + 1
            if temp == the_lowest_temp:
                the_coldest_month = index + 1
        try:
            return abs_max_temp[the_warmest_month], abs_min_temp[the_coldest_month]
        except KeyError:
            raise ValueError(
                """
                Invalid data structure in 'cloudy.WalterLieth.dataframe'. Check 'cloudy.WalterLieth' docs for more info.
                
                1. Check if you haven't mistaken column order in 'cloudy.WalterLieth.dataframe'. 
                2. It's also possible that you have tried to pass daily interval and there's a lack of column/columns. 
                Note that daily interval data must contain 6 columns - for more info about required data structure check 
                'cloudy.WalterLieth' docs. If you have used 'cloudy.WalterLieth.import_global_df' method for data from IMGW
                database, check values for argument 'columns_order' (if 'imgw_monthly' or 'imgw_daily' have been used properly,
                depending on IMGW data interval).
                """)

    @staticmethod
    def get_temp_yticks(
            temperature
    ):
        available_temp_axis_ticks = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]
        min_temp = min(list(temperature))

        if available_temp_axis_ticks.count(min_temp) == 1:
            return available_temp_axis_ticks[available_temp_axis_ticks.index(min_temp) - 1:]

        temp_axis_ticks = []
        try:
            for avail_temp_tick in available_temp_axis_ticks:
                if avail_temp_tick < min_temp:
                    if available_temp_axis_ticks[available_temp_axis_ticks.index(avail_temp_tick) + 1] > min_temp:
                        temp_axis_ticks.append(avail_temp_tick)
                    continue
                else:
                    temp_axis_ticks.append(avail_temp_tick)
        except IndexError:
            raise ValueError(
                """
                Invalid data structure in 'cloudy.WalterLieth.dataframe'. Check 'cloudy.WalterLieth' docs for more info.
                
                If you have downloaded data on your own from IMGW database and set global dataframe, check if you have
                chosen correct file format. Available file formats for 'cloudy.WalterLieth' from IMGW database are: 
                ['s_m_d', 's_d'].
                
                cloudy.get_meteorological_data(..., file_format='s_m_d')
                cloudy.get_meteorological_data(..., file_format='s_d')
                """)

        if temp_axis_ticks[0] > 0:
            temp_axis_ticks = [0, 10, 20, 30, 40, 50]

        return temp_axis_ticks

    @staticmethod
    def get_yticks_labels_for_precipitation(temp_yaxis_ticks):
        preci_ticks = []
        for index, tick in enumerate(temp_yaxis_ticks):
            if index == 0 and tick != 0:
                preci_ticks.append('')
            else:
                preci_ticks.append(tick * 2)

        return preci_ticks

    @staticmethod
    def get_max_ytick_for_precipitation(precipitation):
        available_ticks = [200, 300, 400, 500, 600,
                           700, 800, 900, 1000, 1100,
                           1200, 1300, 1400, 1500, 1600,
                           1700, 1800, 1900, 2000]
        max_tick = max(list(precipitation))

        for tick in available_ticks:
            if tick >= max_tick:
                return tick
        raise Exception(f"Precipitation is too high! {max_tick}")

    @staticmethod
    def determine_if_freeze(abs_min_temp):
        likely = []
        freeze = []

        for index, temp in enumerate(abs_min_temp):
            if temp < -5:
                freeze.append(index)
            elif temp < 0:
                likely.append(index)
            else:
                continue

        if len(likely) == 0:
            likely = False
        if len(freeze) == 0:
            freeze = False

        return likely, freeze

    @staticmethod
    def interpolate_margins(mean_temperature, precipitation):
        temperature = list(mean_temperature)
        precipitation = list(precipitation)

        if temperature[1] - temperature[0] > 0:
            temperature_trend = 'decrease'
        elif temperature[1] - temperature[0] == 0:
            temperature_trend = 'stable'
        else:
            temperature_trend = 'increase'

        if precipitation[1] - precipitation[0] > 0:
            precipitation_trend = 'decrease'
        elif precipitation[1] - precipitation[0] == 0:
            precipitation_trend = 'stable'
        else:
            precipitation_trend = 'increase'

        if temperature_trend == 'decrease':
            if temperature[0] < 0:
                temperature_0 = temperature[0] - ((temperature[0] * 0.05) * -1)
            else:
                temperature_0 = temperature[0] - (temperature[0] * 0.05)
        elif temperature_trend == 'increase':
            if temperature[0] < 0:
                temperature_0 = temperature[0] + ((temperature[0] * 0.05) * -1)
            else:
                temperature_0 = temperature[0] + (temperature[0] * 0.05)
        else:
            temperature_0 = temperature[0]

        if precipitation_trend == 'decrease':
            precipitation_0 = precipitation[0] - (precipitation[0] * 0.05)
        elif precipitation_trend == 'increase':
            precipitation_0 = precipitation[0] + (precipitation[0] * 0.05)
        else:
            precipitation_0 = precipitation[0]

        new_temperature = []
        for index, temp in enumerate(temperature):
            if index == 0:
                new_temperature.append(temperature_0)
                new_temperature.append(temp)
            else:
                new_temperature.append(temp)
        new_temperature.append(temperature_0)

        new_precipitation = []
        for index, preci in enumerate(precipitation):
            if index == 0:
                new_precipitation.append(precipitation_0)
                new_precipitation.append(preci)
            else:
                new_precipitation.append(preci)
        new_precipitation.append(precipitation_0)

        return new_temperature, new_precipitation

    @staticmethod
    def distinguish_between_wet_and_dry(mean_temperature, precipitation):
        corrected_precipitation = []
        for preci in precipitation:
            if preci < 100:
                corrected_precipitation.append(preci / 2)
            else:
                corrected_precipitation.append(preci)

        dry_months_indexes = []
        wet_months_indexes = []

        for index, preci in enumerate(corrected_precipitation):
            if preci > mean_temperature[index]:
                wet_months_indexes.append(index)
            else:
                dry_months_indexes.append(index)

        wet_periods = []
        period = []
        for i, index in enumerate(wet_months_indexes):
            if i == 0:
                period.append(index)
            elif index - wet_months_indexes[i - 1] != 1:
                period.append(wet_months_indexes[i - 1])
                wet_periods.append((period[0], period[1]))
                period.clear()

                period.append(index)
            else:
                continue
        if len(period) == 1:
            wet_period_starts_with = period[0]
            wet_period_ends_with = wet_months_indexes[-1]
            wet_periods.append((wet_period_starts_with, wet_period_ends_with))

        dry_periods = []
        period = []
        for i, index in enumerate(dry_months_indexes):
            if i == 0:
                period.append(index)
            elif index - dry_months_indexes[i - 1] != 1:
                period.append(dry_months_indexes[i - 1])
                dry_periods.append((period[0], period[1]))
                period.clear()

                period.append(index)
            else:
                continue
        try:
            if len(period) == 1:
                dry_period_starts_with = period[0]
                dry_period_ends_with = dry_months_indexes[-1]
                dry_periods.append((dry_period_starts_with, dry_period_ends_with))
        except KeyError:
            pass

        return wet_periods, dry_periods
