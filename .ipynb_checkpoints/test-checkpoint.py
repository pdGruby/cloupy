class WalterLieth:
    def __init__(
            self, dataframe, years_range=None, station_name=None,
            lat_lon=None, above_sea_level=None, language=None,
            figsize=(7.74, 7.74)
    ):

        self.dataframe = dataframe
        self.years_range = years_range
        self.station_name = station_name
        self.lat_lon = lat_lon
        self.above_sea_level = above_sea_level
        self.language = language
        self.figsize = figsize

    def draw(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        from matplotlib import rcParams

        if self.language == 'POL':
            asl = 'Wysokość: {} m n.p.m.'
            lat = 'Szerokość geograficzna: {}'
            lon = 'Długość geograficzna: {}'
            temp_label = 'Średnia roczna temperatura: {}°C'
            preci_label = 'Roczna suma opadów: {} mm'
            x_ticks_labels = ['S', 'L', 'M', 'K', 'M', 'C', 'L', 'S', 'W', 'P', 'L', 'G']
            temp_axis_ylabel = 'Średnia miesięczna temperatura powietrza [°C]'
            temp_axis_xlabel = 'Miesiące oraz prawdopodobieństwo wystąpienia przymrozku'
            preci_axis_ylabel = 'Średnia miesięczna suma opadów [mm]'
        else:
            asl = 'Altitude: {} m a.s.l.'
            lat = 'Latitude: {}'
            lon = 'Longitude: {}'
            temp_label = 'Average air temperature: {}°C'
            preci_label = 'Annual precipitation: {} mm'
            x_ticks_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
            temp_axis_ylabel = 'Average monthly air temperature [°C]'
            temp_axis_xlabel = 'Months and probability of freeze occurrence'
            preci_axis_ylabel = 'Average monthly precipitation sum [mm]'

        if self.station_name is not None:
            title = self.station_name
        else:
            title = False

        if self.above_sea_level is not None:
            asl = asl.format(self.above_sea_level)
        else:
            asl = False

        if self.years_range is not None:
            if type(self.years_range) is int:
                years = self.years_range
            else:
                years = f'{str(min(self.years_range))}-{str(max(self.years_range))}'
        else:
            years = False

        if self.lat_lon is not None:
            lat = lat.format(self.lat_lon[0])
            lon = lon.format(self.lat_lon[1])
        else:
            lat = False
            lon = False

        mean_temperature = self.dataframe.groupby(self.dataframe.columns[0]).mean().iloc[:, 0]
        precipitation = self.dataframe.groupby(self.dataframe.columns[0]).mean().iloc[:, 1]
        abs_max_temp = self.dataframe.groupby(self.dataframe.columns[0]).max().iloc[:, 2]
        abs_min_temp = self.dataframe.groupby(self.dataframe.columns[0]).min().iloc[:, 3]

        annual_mean_temp = round(mean_temperature.mean(), 1)
        sum_preci = round(precipitation.sum(), 1)

        maxtwm_mintcm = WalterLieth.get_max_twm_and_min_tcm(mean_temperature, abs_max_temp, abs_min_temp)
        max_temp = round(maxtwm_mintcm[0], 1)
        min_temp = round(maxtwm_mintcm[1], 1)

        x_major_ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
        x_minor_ticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        temp_yaxis_ticks = WalterLieth.get_temp_yticks(mean_temperature)
        preci_yaxis_ticks_labels = WalterLieth.get_yticks_labels_for_precipitation(temp_yaxis_ticks)
        log_yaxis_max_tick = WalterLieth.get_max_ytick_for_precipitation(precipitation)

        fig, temp_axis = plt.subplots(figsize=self.figsize)
        fig.patch.set_alpha(1)

        if title:
            fig.suptitle(title, x=0.14, size=16, fontweight='bold', ha='left')
        if asl:
            fig.text(0.14, 0.933, asl, size=11)
        if lat:
            fig.text(0.14, 0.91, lat, size=11)
        if lon:
            fig.text(0.14, 0.887, lon, size=11)
        if years:
            fig.text(0.88, 0.935, years, size=14, ha='right', fontweight='bold')
        fig.text(0.88, 0.91, temp_label.format(annual_mean_temp), ha='right', size=11)
        fig.text(0.88, 0.887, preci_label.format(sum_preci), ha='right', size=11)

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
        temp_axis.tick_params(axis='y', which='major', length=6, color='black')
        temp_axis.tick_params(axis='x', which='minor', length=10, color='black', direction='in')
        temp_axis.tick_params(axis='x', which='major', length=0)
        temp_axis.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                       [(k * 0) + (min(temp_yaxis_ticks) + 1.8) for k in range(0, 13)], color='black', linewidth=1)
        temp_axis.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [k * 0 for k in range(0, 13)], color='black',
                       linewidth=1, linestyle='dotted')

        preci_axis = temp_axis.secondary_yaxis('right')
        preci_axis.set_yticks(temp_yaxis_ticks)
        preci_axis.set_yticklabels(preci_yaxis_ticks_labels)
        preci_axis.tick_params(axis='both', which='major', length=6, color='black')

        divider = make_axes_locatable(temp_axis)
        log_yaxis = divider.append_axes("top", size=1, pad=0) # sprawdź czy jak zmienisz size=0 to czy będzie widoczna ta oś
        log_yaxis.set_yscale('log')
        log_yaxis.set_xticks(x_major_ticks)
        log_yaxis.set_xticks(x_minor_ticks, minor=True)
        log_yaxis.set_xticklabels(['', '', '', '', '', '', '', '', '', '', '', ''])
        log_yaxis.set_xlim(0, max(x_minor_ticks))
        log_yaxis.set_yticks([log_yaxis_max_tick])
        log_yaxis.set_yticks([], minor=True)
        log_yaxis.set_ylim((100, log_yaxis_max_tick))
        log_yaxis.yaxis.tick_right()
        log_yaxis.set_yticklabels([str(log_yaxis_max_tick)])
        log_yaxis.tick_params(axis='x', which='both', color=[0, 0, 0, 0])
        log_yaxis.spines['top'].set_color('white')
        log_yaxis.text(0, log_yaxis_max_tick + 4.15, '_', ha='right')

        temp_axis.set_ylabel(temp_axis_ylabel, size=10, fontweight='bold')
        temp_axis.set_xlabel(temp_axis_xlabel, size=10, fontweight='bold')
        preci_axis.set_ylabel(preci_axis_ylabel, size=10, fontweight='bold')

        if_freeze = WalterLieth.determine_if_freeze(abs_min_temp)
        likely = if_freeze[0]
        freeze = if_freeze[1]

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
                                   min(temp_yaxis_ticks) + 1.8,
                                   where=where)

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
                                   min(temp_yaxis_ticks) + 1.8,
                                   where=where, color='cyan')

        x_for_plotting = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12]
        interpolated_margins = WalterLieth.interpolate_margins(mean_temperature, precipitation)
        mean_temperature = interpolated_margins[0]
        precipitation = interpolated_margins[1]

        temp_axis.plot(x_for_plotting, mean_temperature, 'r')
        temp_axis.plot(x_for_plotting, [p / 2 for p in precipitation])
        log_yaxis.plot(x_for_plotting, precipitation)

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
                                   where=where, interpolate=True, hatch='||',
                                   color='none', edgecolor='#1f77b4', linewidth=0.0)
            log_yaxis.fill_between(x_for_plotting, precipitation, 100,
                                   where=where, interpolate=True, color='#1f77b4')

        for period in dry_periods:
            where = [False, False, False, False,
                     False, False, False, False,
                     False, False, False, False,
                     False, False]
            for index in range(period[0], period[1] + 1):
                where[index] = True
            temp_axis.fill_between(x_for_plotting, [p / 2 for p in precipitation], mean_temperature,
                                   where=where, interpolate=True, hatch='..',
                                   color='none', edgecolor='red', linewidth=0.0)

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

        return abs_max_temp[the_warmest_month], abs_min_temp[the_coldest_month]

    @staticmethod
    def get_temp_yticks(
            temperature
    ):
        available_temp_axis_ticks = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]
        min_temp = min(list(temperature))

        if available_temp_axis_ticks.count(min_temp) == 1:
            return available_temp_axis_ticks[available_temp_axis_ticks.index(min_temp) - 1:]

        temp_axis_ticks = []
        for avail_temp_tick in available_temp_axis_ticks:
            if avail_temp_tick < min_temp:
                if available_temp_axis_ticks[available_temp_axis_ticks.index(avail_temp_tick) + 1] > min_temp:
                    temp_axis_ticks.append(avail_temp_tick)
                continue
            else:
                temp_axis_ticks.append(avail_temp_tick)

        if temp_axis_ticks[0] > 0:
            temp_axis_ticks = [0, 10, 20, 30, 40, 50]

        return temp_axis_ticks

    @staticmethod
    def get_yticks_labels_for_precipitation(temp_yaxis_ticks):
        preci_ticks = []
        for index, tick in enumerate(temp_yaxis_ticks):
            if index == 0:
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
