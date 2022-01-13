def get_wmo_stations_info():
    """Return pandas.DataFrame with WMO stations information (WMO ids, coordinates, etc.)"""

    import pandas as pd

    wmo_ids_path = str(__file__).replace('wmo.py', 'wmo_ids_and_coords.csv')
    ids_coords = pd.read_csv(wmo_ids_path, dtype={3: 'object'}, sep=';', index_col=0)
    return ids_coords


def get_wmoid_or_coord(
        station_name, to_return, contains_station_name=True,
        station_name_is_wmo_id=False
):
    """
    Return WMO ids or coordinates of the WMO stations which contains 'station_name'
    in their names.

    Keyword arguments:
        station_name -- name of the station for which WMO id or coordinates will
    be returned. If 'cou' prefix added to 'station_name' and a country name appears
    after the prefix, the function will search for all stations in the specified
    country (e.g. 'couPOLAND' will return WMO ids or coordinates for all stations
    in Poland)
        to_return -- which parameter has to be returned ('wmo_id', 'lat', 'lon',
    'elv')
        contains_station_name -- if set to True, the function will search for
    stations which CONTAIN 'station_name' in their name. If set to False, the
    function will search for stations with NAMES EXACTLY as in 'station_name'
    (default True)
        station_name_is_wmo_id -- if set to True, the function will search for a
    station by its WMO id. In this case, in 'station_name' argument you have to
    pass WMO id
    """

    import pandas as pd

    if not isinstance(station_name, str) and not isinstance(station_name, int):
        raise ValueError(
            f"The 'station_name' argument must be a single string or a single int (given type: {type(station_name)})"
        )

    wmo_ids_path = str(__file__).replace('wmo.py', 'wmo_ids_and_coords.csv')
    station_name = str(station_name)
    station_name = station_name.upper()
    
    ids_coords = pd.read_csv(wmo_ids_path, dtype={3: 'object'}, sep=';', index_col=0)
    if station_name.startswith('COU'):
        data = ids_coords[ids_coords['country'].str.contains(station_name.replace('COU', ''))]
    elif station_name_is_wmo_id:
        data = ids_coords[ids_coords['wmo_id'] == station_name]
    else:
        if contains_station_name:
            data = ids_coords[ids_coords['station'].str.contains(station_name)]
        else:
            data = ids_coords[ids_coords['station'] == station_name]

    if len(data.index) == 0:
        raise ValueError(
            """
            No data found for the given 'station_name'.
            """
        )
    elif station_name.startswith('COU'):
        indexes = [i for i in range(0, len(data.index))]
    elif len(data.index) > 1:
        stations_info = ''
        for i, station in enumerate(list(data.station)):
            stations_info += f'{i}: {list(data.country)[i]}, {list(data.wmo_id)[i]}, {station}\n            '

        indexes = input(
            f"""
            Data found for more than one station. Specify which station you are interested in (by selecting indexes. Use
            '*' if you are interested in every found station).            
            
            ---COUNTRY, WMO ID, STATION---
            {stations_info}
            """)

        if indexes == '*':
            all_indexes = []
            for i, station in enumerate(list(data.station)):
                all_indexes.append(i)
            indexes = all_indexes
        else:
            indexes = indexes.split(',')
        indexes = [int(i) for i in indexes]
    else:
        indexes = [0]

    dict_to_return = {}
    for index in indexes:
        dict_to_return[data.iloc[index, 1]] = data.iloc[index, :][to_return]

    return dict_to_return


def decode_downloaded_data(data_table):
    """
    Decode the data from .dat file from the WMO website. Return more
    computer-friendly data for further adaptation.
    """

    table = data_table.split('#')

    data = table[-1]
    row_to_del = data.split('\n')[0]
    data = data.replace(row_to_del, "")
    data = data.split('\n')

    decoded = []
    for row in data:
        dec_row = row.split(' ')
        while '' in dec_row:
            dec_row.remove('')
        decoded.append(dec_row)

    while [] in decoded:
        decoded.remove([])

    return decoded


def download_data(url):
    """Download and return the data from the given URL of the WMO website"""

    from bs4 import BeautifulSoup as bs
    import requests

    r = requests.get(url)
    soup = bs(r.content, features='html.parser')

    data_href = None
    for element in soup.find_all('a'):
        if '.dat' in element['href']:
            data_href = element['href']
            break

    if data_href is None:
        raise FileNotFoundError(
            f"""
            No data file was found for {url}.
            """
        )

    full_url_for_data = 'http://climexp.knmi.nl/' + data_href
    r = requests.get(full_url_for_data)
    soup = bs(r.content, features='html.parser')

    table = soup.get_text()
    downloaded_data = decode_downloaded_data(table)

    if not downloaded_data:
        raise FileNotFoundError(
            f"""
            No data file was found for {url}
            """
        )

    return downloaded_data


def concatenate_dfs(dfs):
    """Concatenate given dataframes into one consistent dataframe"""

    import pandas as pd

    min_year = 3000
    max_year = 0
    for df in dfs:
        if df[1][0] is not None:
            if int(df[1][0]) < min_year:
                min_year = int(df[1][0])
        if df[-1][0] is not None:
            if int(df[-1][0]) > max_year:
                max_year = int(df[-1][0])

    years = []
    months = []
    for year in range(min_year, max_year + 1):
        for month in range(1, 13):
            years.append(str(year))
            months.append(month)

    concatenated_df = pd.DataFrame({
        'year': years,
        'month': months,
    })

    for df in dfs:

        if df[1] == [None, None, None]:
            values_to_add = [None] * len(concatenated_df['month'])
            concatenated_df[df[0][2]] = values_to_add
        else:
            values_to_add = []

            index_to_start = None
            for i, year in enumerate(years):
                if year == df[1][0]:
                    index_to_start = i
                    break
                else:
                    values_to_add.append(None)

            if index_to_start is None:
                raise ValueError("'index_to_start' value is None.")

            for i, row in enumerate(df[1:]):
                if row[0] == years[index_to_start + i]:
                    if row[1] == months[index_to_start + i]:
                        if float(row[2]) > -90:
                            values_to_add.append(row[2])
                        else:
                            values_to_add.append(None)
                    else:
                        values_to_add.append(None)
                else:
                    values_to_add.append(None)

            while len(values_to_add) != len(years):
                values_to_add.append(None)

            concatenated_df[df[0][2]] = values_to_add

    for column in concatenated_df.columns[:2]:
        concatenated_df = concatenated_df.astype({column: int})
    for column in concatenated_df.columns[2:]:
        concatenated_df = concatenated_df.astype({column: float})

    return concatenated_df


def transpose_table(table):
    """Transpose the table for further adaptation"""

    new_table = []
    for row in table:
        for i, value in enumerate(row):
            if i != 0:
                new_row = [row[0], i, value]
                new_table.append(new_row)

    return new_table


def search_for_the_nearest_station(
        lat, lon, degrees_range=0.5
):
    """
    Return the nearest stations from the WMO database for the given coordinates.

    Keyword arguments:
        lat -- the latitude for which station will be searched
        lon -- the longitude for which station will be searched
        degrees_range -- acceptable range in degrees in all directions (default 0.5)
    """

    import pandas as pd

    wmo_ids_path = str(__file__).replace('wmo.py', 'wmo_ids_and_coords.csv')

    ids_coords = pd.read_csv(wmo_ids_path, dtype={3: 'object'}, sep=';', index_col=0)

    ids_coords = ids_coords[
        (ids_coords['lat'] < lat + degrees_range) &
        (ids_coords['lat'] > lat - degrees_range) &
        (ids_coords['lat'] != lat)
        ]

    ids_coords = ids_coords[
        (ids_coords['lon'] < lon + degrees_range) &
        (ids_coords['lon'] > lon - degrees_range) &
        (ids_coords['lon'] != lon)
        ]

    return ids_coords


def download_wmo_climatological_data(
        station_name, elements_to_scrape, nearby_stations=False,
        degrees_range_for_nearby_stations=0.5, return_coordinates=False
):
    """
    Download climatological data for specified station/stations from the WMO website.
    There are 5 elements which can be downloaded: average air temperature,
    sum of precipitation, absolute minimum air temperature, absolute maximum air
    temperature, sea level pressure. The interval for downloaded data is always
    monthly.

    Keyword arguments:
        station_name -- name of the station for which the data will to downloaded.
    If 'cou' prefix added to 'station_name' and a country name appears after the
    prefix, the function will search for all stations in the specified country
    (e.g. 'couPOLAND' will download data for Poland)
        elements_to_scrape -- which elements from the WMO website will be scraped.
    ('temp', 'preci', 'temp_min', 'temp_max', 'sl_press')
        nearby_stations -- if there is no data or a single element is missing, and
    if 'nearby_stations' argument is set to True, the function will search for the
    nearest stations and try to complete the lack (default False)
        degrees_range_for_nearby_stations -- acceptable range in degrees in all
    directions if nearby stations have to be searched (default 0.5)
        return_coordinates -- if set to True, the function will add columns with
    latitude, longitude and elevation for the specified station/stations (default False)
    """

    import pandas as pd

    if isinstance(elements_to_scrape, str):
        elements_to_scrape = [elements_to_scrape]

    elements_with_urls = {
        'temp': 'http://climexp.knmi.nl/gettempall.cgi?id=someone@somewhere&WMO={}',
        'preci': 'http://climexp.knmi.nl/getprcpall.cgi?id=someone@somewhere&WMO={}',
        'temp_min': 'http://climexp.knmi.nl/getminall.cgi?id=someone@somewhere&WMO={}',
        'temp_max': 'http://climexp.knmi.nl/getmaxall.cgi?id=someone@somewhere&WMO={}',
        'sl_press': 'http://climexp.knmi.nl/getslp.cgi?id=someone@somewhere&WMO={}'
    }

    wmo_ids = get_wmoid_or_coord(station_name, 'wmo_id')
    wmo_ids_list = [wmo_id for station, wmo_id in wmo_ids.items()]

    full_df = pd.DataFrame()
    print('Starting downloading data. It may take a while.')
    for station, wmo_id in wmo_ids.items():
        data = []
        for element in elements_to_scrape:
            url = elements_with_urls[element].format(wmo_id)

            try:
                downloaded_data = download_data(url)
            except FileNotFoundError:
                if 'cou' in station_name:
                    continue
                elif not nearby_stations:
                    print(
                        f"""
                        WARNING: No data for '{element}' in '{station}' (WMO ID: {wmo_id}).
                        If you want to search for data in the nearest stations, set 'nearby_stations'
                        argument to True.
                        """)
                    continue
                else:
                    lat = get_wmoid_or_coord(wmo_id, 'lat', station_name_is_wmo_id=True)[station]
                    lon = get_wmoid_or_coord(wmo_id, 'lon', station_name_is_wmo_id=True)[station]
                    nearest_stations = search_for_the_nearest_station(
                        lat, lon, degrees_range=degrees_range_for_nearby_stations
                    )
                    if nearest_stations.empty:
                        print(
                            f"""
                            WARNING: No data for '{element}' in '{station}' (WMO ID: {wmo_id}).
                            No nearby station found either.
                            """
                        )
                        continue

                    data_from_near_stations = {}
                    for near_wmo_id in nearest_stations['wmo_id']:
                        if near_wmo_id in wmo_ids_list:
                            continue

                        url = elements_with_urls[element].format(near_wmo_id)
                        try:
                            data_for_station = download_data(url)
                        except FileNotFoundError:
                            data_from_near_stations[near_wmo_id] = None
                        else:
                            data_from_near_stations[near_wmo_id] = data_for_station

                    hm_elements = 0
                    more_elements_in = None
                    for near_wmo_id, data_for_station in data_from_near_stations.items():
                        try:
                            if len(data_for_station) > hm_elements:
                                hm_elements = len(data_for_station)
                                more_elements_in = near_wmo_id
                        except TypeError:
                            continue

                    if more_elements_in is None:
                        downloaded_data = None
                    else:
                        downloaded_data = data_from_near_stations[more_elements_in]
                        print(
                            f"""
                            Warning: no '{element}' data was found for the chosen station ({station}), so the data was 
                            taken from the nearest station (WMO ID: {more_elements_in}). Latitude and longitude differences 
                            were below 0.5 degrees (default) or as in the 'degrees_range_for_nearby_stations' argument (if 
                            specified). If you do not want to download data from the nearest station, change 'nearby_stations' 
                            argument value to False. If you would like to change acceptable latitude and longitude differences, 
                            you can do it by passing float/int to 'degrees_range_for_nearby_stations' argument.
                            """)
            else:
                pass

            if downloaded_data is not None:
                downloaded_data = transpose_table(downloaded_data)
                downloaded_data.insert(0, ['year', 'month', element])
            else:
                downloaded_data = [[None, None, None]]
                downloaded_data.insert(0, ['year', 'month', element])

            data.append(downloaded_data)

        concatenated_df = concatenate_dfs(data)
        station_series = [station] * len(concatenated_df.index)
        concatenated_df.insert(0, 'station', station_series)

        if return_coordinates:
            lat = get_wmoid_or_coord(wmo_id, 'lat', station_name_is_wmo_id=True)[station]
            lon = get_wmoid_or_coord(wmo_id, 'lon', station_name_is_wmo_id=True)[station]
            elv = get_wmoid_or_coord(wmo_id, 'elv', station_name_is_wmo_id=True)[station]

            lat_series = [lat] * len(concatenated_df.index)
            lon_series = [lon] * len(concatenated_df.index)
            elv_series = [elv] * len(concatenated_df.index)

            concatenated_df['lat'] = lat_series
            concatenated_df['lon'] = lon_series
            concatenated_df['elv'] = elv_series

        full_df = full_df.append(concatenated_df)

        if 'cou' in station_name:
            columns_order = elements_to_scrape
            filtered_columns_order = ['station', 'year', 'month']

            for element in columns_order:
                if element in list(full_df.columns):
                    filtered_columns_order.append(element)

            if return_coordinates:
                filtered_columns_order += ['lat', 'lon', 'elv']
            full_df = full_df[filtered_columns_order]

    print('Data downloaded.')
    return full_df
