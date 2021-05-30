"""
Functions for IMGW's database analysis.

get_meteorological_data(period, stations_kind, years_range, file_format_index=1,
                        file_format=None,   specific_columns=None, keywords=None,
                        merge_splitted_stations=True, optimize_memory_usage=False)

get_file_formats(period, stations_kind, file_format_index)
get_column_names(file_format)
look_for_keywords_in_columns(keywords, file_format=None)

get_urls(period, stations_kind, years_range)
download_data(urls)
concatenate_data(downloaded_files_names, file_formats, specific_columns,
                keywords, optimize_memory_usage, years_range)
"""


def get_file_formats(
        period, stations_kind, file_format_index
):
    """
    Return available file formats for the given 'period' and 'stations_kind'.

    Keyword arguments:
    period -- period kind of IMGW's database ('monthly', 'daily', 'prompt')
    stations_kind -- stations' kind ('synop', 'climat', 'fall')
    file_format_index -- which element from the list will be returned ('all', 1, 2)
    """

    if period == 'monthly':
        if stations_kind == 'synop':
            available_files_formats = ['s_m_d', 's_m_t']
        elif stations_kind == 'fall':
            available_files_formats = ['o_m']
        elif stations_kind == 'climat':
            available_files_formats = ['k_m_d', 'k_m_t']
        else:
            raise AttributeError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    elif period == 'daily':
        if stations_kind == 'synop':
            available_files_formats = ['s_d', 's_d_t']
        elif stations_kind == 'fall':
            available_files_formats = ['o_d']
        elif stations_kind == 'climat':
            available_files_formats = ['k_d', 'k_d_t']
        else:
            raise AttributeError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    elif period == 'prompt':
        if stations_kind == 'synop':
            available_files_formats = ['s_t']
        elif stations_kind == 'fall':
            raise NotADirectoryError("There's no '/dane_meteorologiczne/terminowe/opad/' directory in IMGW database.")
        elif stations_kind == 'climat':
            available_files_formats = ['k_t']
        else:
            raise AttributeError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    else:
        raise AttributeError("Invalid 'period' input. Available inputs: 'monthly', 'daily', 'prompt'.")

    if file_format_index == 'all':
        chosen_file_format = available_files_formats
    elif file_format_index == 0 or file_format_index == 1:
        try:
            chosen_file_format = [available_files_formats[file_format_index]]
        except IndexError:
            if len(available_files_formats) == 1:
                chosen_file_format = [available_files_formats[0]]
            else:
                raise Exception("Something wrong with file format.")
    else:
        raise AttributeError(
            "{} file formats for given 'period' and 'stations_kind' available. Use index of the file format or 'all' "
            "for 'file_format_index' (both file formats will be taken): {}".format(len(available_files_formats), available_files_formats))
    return chosen_file_format


def get_column_names(
        file_format
):
    """
    Return columns names for the given file format.

    Keyword arguments:
    file_format -- file format of IMGW's database (eg. 's_m_t')
    """

    if file_format == 'k_m_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Absolutna temperatura maksymalna [°C]',
                'Status pomiaru TMAX', 'Średnia temperatura maksymalna [°C]', 'Status pomiaru TMXS',
                'Absolutna temperatura minimalna [°C]', 'Status pomiaru TMIN', 'Średnia temperatura minimalna [°C]',
                'Status pomiaru TMNS', 'Średnia temperatura miesięczna [°C]', 'Status pomiaru STM',
                'Minimalna temperatura przy gruncie [°C]', 'Status pomiaru TMNG', 'Miesieczna suma opadów [mm]',
                'Status pomiaru SUMM', 'Maksymalna dobowa suma opadów [mm]', 'Status pomiaru OPMX',
                'Pierwszy dzień wystapienia opadu maksymalnego', 'Ostatni dzień wystąpienia opadu maksymalnego',
                'Maksymalna wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN', 'Liczba dni z pokrywą śnieżną',
                'Liczba dni z opadem deszczu', 'Liczba dni z opadem śniegu']

    elif file_format == 'k_m_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Średnia miesięczna temperatura [°C]',
                'Status pomiaru TEMP', 'Średnia miesięczna wilgotność względna [%]', 'Status pomiaru WLGS',
                'Średnia miesięczna prędkość wiatru [m/s]', 'Status pomiaru FWS',
                'Średnie miesięczne zachmurzenie ogólne [oktanty]', 'Status pomiaru NOS']

    elif file_format == 'o_m':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Miesięczna suma opadów [mm]', 'Status pomiaru SUMM',
                'Liczba dni z opadem śniegu', 'Status pomiaru LDS', 'Opad maksymalny [mm]', 'Status pomiaru MAXO',
                'Dzień pierwszy wystąpienia opadu maksymalnego', 'Dzień ostatni wystąpienia opadu maksymalnego',
                'Liczba dni z pokrywą śnieżną', 'Status pomiaru LDPS']

    elif file_format == 's_m_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Absolutna temperatura maksymalna [°C]',
                'Status pomiaru TMAX', 'Średnia temperatura maksymalna [°C]', 'Status pomiaru TMXS',
                'Absolutna temperatura minimalna [°C]', 'Status pomiaru TMIN', 'Średnia temperatura minimalna [°C]',
                'Status pomiaru TMNS', 'Średnia temperatura miesięczna [°C]', 'Status pomiaru STM',
                'Minimalna temperatura przy gruncie [°C]', 'Status pomiaru TMNG', 'Miesieczna suma opadów [mm]',
                'Status pomiaru SUMM', 'Maksymalna dobowa suma opadów [mm]', 'Status pomiaru OPMX',
                'Pierwszy dzień wystapienia opadu maksymalnego', 'Ostatni dzień wystąpienia opadu maksymalnego',
                'Miesięczna suma usłonecznienia [godziny]', 'Status pomiaru SUUS',
                'Maksymalna wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN', 'Liczba dni z pokrywą śnieżną',
                'Status pomiaru PSDN', 'Liczba dni z opadem deszczu', 'Status pomiaru DESD',
                'Liczba dni z opadem śniegu',
                'Status pomiaru SNID', 'Liczba dni z opadem deszczu ze śniegiem', 'Status pomiaru DSND',
                'Liczba dni z gradem', 'Status pomiaru GRDD', 'Liczba dni z mgłą', 'Status pomiaru MGLD',
                'Liczba dni z zamgleniem', 'Status pomiaru ZAMD', 'Liczba dni z sadzią', 'Status pomiaru SADD',
                'Liczba dni z gołoledzią', 'Status pomiaru GOLD', 'Liczba dni z zamiecią śnieżną niską',
                'Status pomiaru ZAND', 'Liczba dni z zamiecią śnieżną wysoką', 'Status pomiaru ZAWD',
                'Liczba dni ze zmętnieniem', 'Status pomiaru ZMED', 'Liczba dni z wiatrem >= 10m/s',
                'Status pomiaru W10D', 'Liczba dni z wiatrem >15m/s', 'Status pomiaru W15D', 'Liczba dni z burzą',
                'Status pomiaru BURD', 'Liczba dni z rosą', 'Status pomiaru ROSD', 'Liczba dni ze szronem',
                'Status pomiaru SZRD']

    elif file_format == 's_m_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Średnie miesięczne zachmurzenie ogólne [oktanty]',
                'Status pomiaru NOS', 'Średnia miesięczna prędkość wiatru [m/s]', 'Status pomiaru FWS',
                'Średnia miesięczna temperatura [°C]', 'Status pomiaru TEMP',
                'Średnie miesięczne ciśnienie pary wodnej [hPa]', 'Status pomiaru CPW',
                'Średnia miesięczna wilgotność względna [%]', 'Status pomiaru WLGS',
                'Średnie miesięczne ciśnienie na poziomie stacji [hPa]', 'Status pomiaru PPPS',
                'Średnie miesięczne ciśnienie na pozimie morza [hPa]', 'Status pomiaru PPPM', 'Suma opadu dzień [mm]',
                'Status pomiaru WODZ', 'Suma opadu noc [mm]', 'Status pomiaru WONO']

    elif file_format == 'k_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Maksymalna temperatura dobowa [°C]',
                'Status pomiaru TMAX', 'Minimalna temperatura dobowa [°C]', 'Status pomiaru TMIN',
                'Średnia temperatura dobowa [°C]', 'Status pomiaru STD', 'Temperatura minimalna przy gruncie [°C]',
                'Status pomiaru TMNG', 'Suma dobowa opadów [mm]', 'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]',
                'Wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN']

    elif file_format == 'k_d_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Średnia dobowa temperatura [°C]',
                'Status pomiaru TEMP', 'Średnia dobowa wilgotność względna [%]', 'Status pomiaru WLGS',
                'Średnia dobowa prędkość wiatru [m/s]', 'Status pomiaru FWS',
                'Średnie dobowe zachmurzenie ogólne [oktanty]', 'Status pomiaru NOS']

    elif file_format == 'o_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Suma dobowa opadów [mm]',
                'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]', 'Wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN',
                'Wysokość świeżo spadłego śniegu [cm]', 'Status pomiaru HSS', 'Gatunek śniegu [kod]',
                'Status pomiaru GATS', 'Rodzaj pokrywy śnieżnej [kod]', 'Status pomiaru RPSN']

    elif file_format == 's_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Maksymalna temperatura dobowa [°C]',
                'Status pomiaru TMAX', 'Minimalna temperatura dobowa [°C]', 'Status pomiaru TMIN',
                'Średnia temperatura dobowa [°C]', 'Status pomiaru STD', 'Temperatura minimalna przy gruncie [°C]',
                'Status pomiaru TMNG', 'Suma dobowa opadu [mm]', 'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]',
                'Wysokość pokrywy śnieżnej [cm]', 'Status pomiaru PKSN', 'Równoważnik wodny śniegu [mm/cm]',
                'Status pomiaru RWSN', 'Usłonecznienie [godziny]', 'Status pomiaru USL',
                'Czas trwania opadu deszczu [godziny]', 'Status pomiaru DESZ', 'Czas trwania opadu śniegu [godziny]',
                'Status pomiaru SNEG', 'Czas trwania opadu deszczu ze śniegiem [godziny]', 'Status pomiaru DISN',
                'Czas trwania gradu [godziny]', 'Status pomiaru GRAD', 'Czas trwania mgły [godziny]',
                'Status pomiaru MGLA', 'Czas trwania zamglenia  [godziny]', 'Status pomiaru ZMGL',
                'Czas trwania sadzi [godziny]', 'Status pomiaru SADZ', 'Czas trwania gołoledzi [godziny]',
                'Status pomiaru GOLO', 'Czas trwania zamieci śnieżnej niskiej [godziny]', 'Status pomiaru ZMNI',
                'Czas trwania zamieci śnieżnej wysokiej [godziny]', 'Status pomiaru ZMWS',
                'Czas trwania zmętnienia [godziny]', 'Status pomiaru ZMET', 'Czas trwania wiatru >=10m/s [godziny]',
                'Status pomiaru FF10', 'Czas trwania wiatru >15m/s [godziny]', 'Status pomiaru FF15',
                'Czas trwania burzy  [godziny]', 'Status pomiaru BRZA', 'Czas trwania rosy  [godziny]',
                'Status pomiaru ROSA', 'Czas trwania szronu [godziny]', 'Status pomiaru SZRO',
                'Wystąpienie pokrywy śnieżnej [0/1]', 'Status pomiaru DZPS', 'Wystąpienie błyskawicy [0/1]',
                'Status pomiaru DZBL', 'Stan gruntu [Z/R]', 'Izoterma dolna [cm]', 'Status pomiaru IZD',
                'Izoterma górna [cm]', 'Status pomiaru IZG', 'Aktynometria  [J/cm2]', 'Status pomiaru AKTN']

    elif file_format == 's_d_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Średnie dobowe zachmurzenie ogólne [oktanty]',
                'Status pomiaru NOS', 'Średnia dobowa prędkość wiatru [m/s]', 'Status pomiaru FWS',
                'Średnia dobowa temperatura [°C]', 'Status pomiaru TEMP', 'Średnia dobowe ciśnienie pary wodnej [hPa]',
                'Status pomiaru CPW', 'Średnia dobowa wilgotność względna [%]', 'Status pomiaru WLGS',
                'Średnia dobowe ciśnienie na poziomie stacji [hPa]', 'Status pomiaru PPPS',
                'Średnie dobowe ciśnienie na pozimie morza [hPa]', 'Status pomiaru PPPM', 'Suma opadu dzień [mm]',
                'Status pomiaru WODZ', 'Suma opadu noc [mm]', 'Status pomiaru WONO']

    elif file_format == 'k_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Godzina', 'Temperatura powietrza [°C]',
                'Status pomiaru TEMP', 'Temperatura termometru zwilżonego [°C]', 'Status pomiaru TTZW',
                'Wskaźnik lodu [L/W]', 'Wskaźnik wentylacji [W/N]', 'Wilgotność względna [%]', 'Status pomiaru WLGW',
                'Kod kierunku wiatru [kod]', 'Status pomiaru DKDK', 'Prędkość wiatru [m/s]', 'Status pomiaru FWR',
                'Zachmurzenie ogólne [0-10 do dn.31.12.1988/oktanty od dn.01.01.1989]', 'Status pomiaru ZOGK',
                'Widzialność [kod]', 'Status pomiaru WID']

    elif file_format == 's_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesiąc', 'Dzień', 'Godzina',
                'Wysokość podstawy chmur CL CM szyfrowana [kod]', 'Status pomiaru HPOD',
                'Wysokość podstawy niższej [m]',
                'Status pomiaru HPON', 'Wysokość podstawy wyższej [m]', 'Status pomiaru HPOW',
                'Wysokość podstawy tekstowy [opis]', 'Pomiar przyrzadem 1 (niższa) [P]',
                'Pomiar przyrzadem 2 (wyższa) [P]',
                'Widzialność [kod]', 'Status pomiaru WID', 'Widzialność operatora [m]', 'Status pomiaru WIDO',
                'Widzialność automat [m]', 'Status pomiaru WIDA', 'Zachmurzenie ogólne [oktanty]', 'Status pomiaru NOG',
                'Kierunek wiatru  [°]', 'Status pomiaru KRWR', 'Prędkość wiatru [m/s]', 'Status pomiaru FWR',
                'Poryw wiatru [m/s]', 'Status pomiaru PORW', 'Temperatura powietrza [°C]', 'Status pomiaru TEMP',
                'Temperatura termometru zwilżonego [°C]', 'Status pomiaru TTZW', 'Wskaźnik wentylacji [W/N]',
                'Wskaźnik lodu [L/W]', 'Ciśnienie pary wodnej [hPa]', 'Status pomiaru CPW', 'Wilgotność względna [%]',
                'Status pomiaru WLGW', 'Temperatura punktu rosy [°C]', 'Status pomiaru TPTR',
                'Ciśnienie na pozimie stacji [hPa]', 'Status pomiaru PPPS', 'Ciśnienie na poziomie morza [hPa]',
                'Status pomiaru PPPM', 'Charakterystyka tendencji [kod]', 'Wartość tendencji [wartość]',
                'Status pomiaru APP',
                'Opad za 6 godzin [mm]', 'Status pomiaru WO6G', 'Rodzaj opadu za 6 godzin [kod]', 'Status pomiaru ROPT',
                'Pogoda bieżąca [kod]', 'Pogoda ubiegła [kod]', 'Zachmurzenie niskie [oktanty]', 'Status pomiaru CLCM',
                'Chmury CL [kod]', 'Status pomiaru CHCL', 'Chmury CL tekstem', 'Chmury CM [kod]', 'Status pomiaru CHCM',
                'Chmury CM tekstem', 'Chmury CH [kod]', 'Status pomiaru CHCH', 'Chmury CH tekstem', 'Stan gruntu [kod]',
                'Status pomiaru SGRN', 'Niedosyt wilgotności [hPa]', 'Status pomiaru DEFI', 'Usłonecznienie',
                'Status pomiaru USLN', 'Wystąpienie rosy [0/1]', 'Status pomiaru ROSW',
                'Poryw maksymalny za okres WW [m/s]', 'Status pomiaru PORK', 'Godzina wystąpienia porywu',
                'Minuta wystąpienia porywu', 'Temperatura gruntu -5 [°C]', 'Status pomiaru TG05',
                'Temperatura gruntu -10 [°C]', 'Status pomiaru TG10', 'Temperatura gruntu -20 [°C]',
                'Status pomiaru TG20', 'Temperatura gruntu -50 [°C]', 'Status pomiaru TG50',
                'Temperatura gruntu -100 [°C]',
                'Status pomiaru TG100', 'Temperatura minimalna za 12 godzin [°C]', 'Status pomiaru TMIN',
                'Temperatura maksymalna za 12 godzin [°C]', 'Status pomiaru TMAX',
                'Temperatura minimalna przy gruncie za 12 godzin [°C]', 'Status pomiaru TGMI',
                'Równoważnik wodny śniegu [mm/cm]', 'Status pomiaru RWSN', 'Wysokość pokrywy śnieżnej [cm]',
                'Status pomiaru PKSN', 'Wysokość świeżo spadłego śniegu [cm]', 'Status pomiaru HSS',
                'Wysokość śniegu na poletku [cm]', 'Status pomiaru GRSN', 'Gatunek śniegu [kod]',
                'Ukształtowanie pokrywy [kod]', 'Wysokość próbki [cm]', 'Status pomiaru HPRO', 'Ciężar próbki [g]',
                'Status pomiaru CIPR']


def look_for_keywords_in_columns(
        keywords, file_format=None
):
    """
    Look for the given keywords in the columns of IMGW's database file formats.

    Keyword arguments:
    keywords -- keywords that will be looked for
    file_format -- IMGW's database file format of which columns will be taken to
    look for keywords. If 'file_format' is None, then every column from every file
    will be taken (default None)
    """

    if file_format is None:
        periods = ['monthly', 'daily', 'prompt']
        stations_kinds = ['synop', 'climat', 'fall']
        if type(keywords) == str:
            keywords = [keywords]

        found_file_formats = {}
        for period in periods:
            for kind in stations_kinds:
                file_formats = get_file_formats(period, kind, 'all')
                found_file_formats['period=' + str(period) + ', ' + 'stations_kind=' + str(kind)] = file_formats

        keywords_in_files = {}
        if type(keywords) == list:
            for period_stkind, file_formats in found_file_formats.items():
                for file in file_formats:
                    columns_names = get_column_names(file)
                    for name in columns_names:
                        for keyword in keywords:
                            if keyword in name:
                                try:
                                    keywords_in_files[str(period_stkind) + ", " + "file_format=" + str(file)].append(
                                        name)
                                except KeyError:
                                    keywords_in_files[str(period_stkind) + ", " + "file_format=" + str(file)] = [name]
        else:
            raise AttributeError("Invalid input for 'keywords'. Use list of strs or str.")
        return keywords_in_files

    else:
        if type(file_format) == str:
            keywords_in_columns = []
            columns_names = get_column_names(file_format)
            for name in columns_names:
                if type(keywords) == list:
                    for keyword in keywords:
                        if keyword in name:
                            keywords_in_columns.append(name)
                else:
                    raise AttributeError("Invalid input for 'keywords'. Use list of strs or str.")
        else:
            raise AttributeError("Invalid input for 'file_format'. Use single str.")
        return keywords_in_columns


def get_urls(
        period, stations_kind, years_range
):
    """
    Return urls for IMGW's database for the given 'period', 'stations_kind' and
    'years_range'.

    Keyword arguments:
    period -- period kind of IMGW's database (monthly, daily, prompt)
    stations_kind -- stations' kind (synop, climat, fall)
    years_range -- years range
    """
    if period == 'monthly':
        period = 'miesieczne/'
    elif period == 'daily':
        period = 'dobowe/'
    elif period == 'prompt':
        period = 'terminowe/'
        if stations_kind == 'fall':
            raise NotADirectoryError("There's no '/dane_meteorologiczne/terminowe/opad/' directory.")
    else:
        raise AttributeError("Invalid 'period' input. Available inputs: 'monthly', 'daily', 'prompt'.")

    if stations_kind == 'synop':
        stations_kind = 'synop/'
    elif stations_kind == 'fall':
        stations_kind = 'opad/'
    elif stations_kind == 'climat':
        stations_kind = 'klimat/'
    else:
        raise AttributeError("Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    years_endings = []
    for year in years_range:
        if year < 2001:
            if year > 1995:
                if years_endings.count('1996_2000/') == 0:
                    years_endings.append('1996_2000/')
            elif year > 1990:
                if years_endings.count('1991_1995/') == 0:
                    years_endings.append('1991_1995/')
            elif year > 1985:
                if years_endings.count('1986_1990/') == 0:
                    years_endings.append('1986_1990/')
            elif year > 1980:
                if years_endings.count('1981_1985/') == 0:
                    years_endings.append('1981_1985/')
            elif year > 1975:
                if years_endings.count('1976_1980/') == 0:
                    years_endings.append('1976_1980/')
            elif year > 1970:
                if years_endings.count('1971_1975/') == 0:
                    years_endings.append('1971_1975/')
            elif year > 1965:
                if years_endings.count('1966_1970/') == 0:
                    years_endings.append('1966_1970/')
            elif year > 1959:
                if years_endings.count('1960_1965/') == 0:
                    years_endings.append('1960_1965/')
            else:
                raise AttributeError("No data for {}. Available years range: 1960-2021.".format(str(year)))
        else:
            years_endings.append(str(year) + '/')

    urls = []
    base_url = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/'
    for ending in years_endings:
        url = base_url + period + stations_kind + ending
        urls.append(url)
    return urls


def download_data(
        urls
):
    """
    Download data from IMGW's database.

    Keyword arguments:
    urls -- urls for data which is wanted
    """
    import requests
    from bs4 import BeautifulSoup as bs
    import zipfile
    import io

    for url in urls:
        if urls.index(url) == 0:
            print("Starting data download... 0% done")

        r = requests.get(url)
        soup = bs(r.content, features="html.parser")

        zip_file_paths = []
        for element in soup.find_all('a'):
            if '.zip' in element.get_text():
                zip_file_paths.append(element.get_text())

        for path in zip_file_paths:
            zip_file = requests.get(url + path)
            zip_file = zipfile.ZipFile(io.BytesIO(zip_file.content))
            zip_file.extractall('./files_reading_folder')

        if (urls.index(url) + 1) % 5 == 0:
            print("Downloading data... {}% done".format(round((urls.index(url) / len(urls)) * 100)))
    print("Data downloaded! 100% done")


def concatenate_data(
        downloaded_files_names, file_formats, specific_columns,
        keywords, optimize_memory_usage, years_range, merge_splitted_stations
):
    """
    Merge tables from downloaded files and return merged pd.DataFrame.

    Keyword arguments:
    downloaded_files_names -- names list of downloaded files
    file_formats -- IMGW"s file formats which are in downloaded files
    specific_columns -- specified columns which will be taken to merge
    keywords -- words which have to be in column name if a column has to be merged
    optimize_memory_usage -- reduce pd.DataFrame memory usage
    years_range -- filtr pd.DataFrame to given period
    """

    import pandas as pd
    import numpy as np

    df = pd.DataFrame()
    keywords_in_columns = []

    for file in downloaded_files_names:
        if downloaded_files_names.index(file) == 0:
            print("Starting data concatenating... 0% done")

        for file_format in file_formats:

            if file_format == 's_d' or file_format == 'k_d':
                avoid_file_format = file_format + '_t'
            else:
                avoid_file_format = 'NO FILE FORMAT TO AVOID'

            if file_format in file and avoid_file_format not in file:

                path = './files_reading_folder/' + file
                csv_DataFrame = pd.read_csv(path, encoding="ANSI", header=None)

                if specific_columns is not None:
                    if type(specific_columns) == str:
                        specific_columns = [specific_columns]

                    if type(specific_columns) is list:
                        csv_DataFrame = csv_DataFrame[specific_columns]
                    else:
                        raise AttributeError("Invalid 'specific_columns' type. Use list of strs or single str.")

                if keywords is not None and len(keywords_in_columns) == 0:
                    columns = get_column_names(file_format)
                    for keyword in keywords:
                        for column in columns:
                            if keyword in column:
                                keywords_in_columns.append(columns.index(column))

                if keywords is not None:
                    csv_DataFrame = csv_DataFrame[keywords_in_columns]

                if optimize_memory_usage:
                    for column in csv_DataFrame.columns:
                        if column == 0:
                            csv_DataFrame[column] = csv_DataFrame[column].astype('object', errors='ignore')
                        elif csv_DataFrame[column].dtype == np.dtype('int64'):
                            csv_DataFrame[column] = csv_DataFrame[column].astype('int16', errors='ignore')
                        elif csv_DataFrame[column].dtype == np.dtype('float64'):
                            csv_DataFrame[column] = csv_DataFrame[column].astype('float16', errors='ignore')
                        else:
                            csv_DataFrame[column] = csv_DataFrame[column].astype('float16', errors='ignore')

                df = df.append(csv_DataFrame)

        try:
            if (downloaded_files_names.index(file) + 1) % (round(len(downloaded_files_names) * 0.1)) == 0:
                print("Concatenating data... {}% done".format(
                    round((downloaded_files_names.index(file) / len(downloaded_files_names)) * 100)))
        except ZeroDivisionError:
            pass
    print("Data concatenated! 100% done \n")

    try:
        df = df[df[2] >= min(
            years_range)]  # Zmień tak, żeby szukało najniższego roku z serii. df[2] wcale nie musi być rokiem jeżeli ktoś się pobawi z keywords.
        df = df[df[2] <= max(
            years_range)]  # Zmień tak, żeby szukało najwyższego roku z serii. df[2] wcale nie musi być rokiem jeżeli ktoś się pobawi z keywords.
    except KeyError:
        print("No column with year has been specified. Can't limit data range to given 'years_range'.")

    if merge_splitted_stations:

        stations_series = df[1]
        new_stations_series = []
        for station in stations_series:
            if station == 'KATOWICE-MUCHOWIEC':
                new_stations_series.append('KATOWICE')
            elif station == 'ŁÓDŹ-LUBLINEK':
                new_stations_series.append('ŁÓDŹ')
            elif station == 'POZNAŃ-ŁAWICA':
                new_stations_series.append('POZNAŃ')
            elif station == 'WARSZAWA-OKĘCIE':
                new_stations_series.append('WARSZAWA')
            elif station == 'WROCŁAW-STRACHOWICE':
                new_stations_series.append('WROCŁAW')
            elif station == 'ELBLĄG-MILEJEWO':
                new_stations_series.append('ELBLĄG')
            elif station == 'RESKO-SMÓLSKO':
                new_stations_series.append('RESKO')
            elif station == 'KOŁOBRZEG-DŹWIRZYNO':
                new_stations_series.append('KOŁOBRZEG')
            else:
                new_stations_series.append(station)
        df[1] = new_stations_series

    if keywords is not None:
        return df, keywords_in_columns
    else:
        return df


def get_meteorological_data(
        period, stations_kind, years_range,
        file_format_index=0, file_format=None,
        specific_columns=None, keywords=None,
        merge_splitted_stations=True, optimize_memory_usage=False
):
    """
    Download IMGW's data files and return data as one merged pd.DataFrame.

    Keyword arguments:
    period -- period kind of IMGW's database ('monthly', 'daily', 'prompt')
    stations_kind -- stations' kind ('synop', 'climat', 'fall')
    years_range -- years range (eg. range(2010, 2021))
    file_format_index -- which element from the list of file formats will be
    returned (default 0)
    file_format -- file format of IMGW's database (default None)
    specific_columns -- specified columns which will be taken to merge (default None)
    keywords -- words which have to be in a column name if a column
    has to be merged (default None)
    merge_splitted_stations - merge stations which are the same but have different
    name (default True)
    optimize_memory_usage - reduce pd.DataFrame memory usage (default False)
    """

    from os import listdir
    from os.path import isfile, join
    import shutil

    urls = get_urls(period, stations_kind, years_range)
    download_data(urls)
    downloaded_files_names = [f for f in listdir('./files_reading_folder') if isfile(join('./files_reading_folder', f))]

    if file_format is not None:
        if type(file_format) == str:
            file_formats = [file_format]
        elif type(file_format) == list:
            file_formats = [format_ for format_ in file_format]
        else:
            raise AttributeError("Invalid input for 'file_format'. Use str or list of strs.")
    else:
        file_formats = get_file_formats(period, stations_kind, file_format_index)

    df = concatenate_data(downloaded_files_names, file_formats, specific_columns,
                          keywords, optimize_memory_usage, years_range,
                          merge_splitted_stations)

    if keywords is not None:
        keywords_in_columns = df[1]
        df = df[0]
    else:
        df = df
        keywords_in_columns = None

    if len(file_formats) == 1:
        column_names = get_column_names(file_formats[0])

        if specific_columns is not None:
            chosen_columns_names = []
            if type(specific_columns) == list:
                for column_index in specific_columns:
                    chosen_columns_names.append(column_names[column_index])
            df.columns = chosen_columns_names

        if keywords is not None:
            chosen_columns_names = []
            for column_index in keywords_in_columns:
                chosen_columns_names.append(column_names[column_index])
            df.columns = chosen_columns_names

        else:
            df.columns = column_names

    shutil.rmtree('./files_reading_folder')
    return df


def get_coordinates_and_elevation(station_name):
    from bs4 import BeautifulSoup as bs
    import requests
    import re

    station_name = station_name.capitalize()
    if station_name == 'Warszawa':
        station_name = 'Warsaw'
    if station_name == 'Kraków-balice':
        station_name = 'Cracow'
    if station_name == 'Kasprowy wierch':
        return {'lat': 49.23, 'lon': 19.97, 'elv': 1987}
    if station_name == 'Przemyśl':
        return {'lat': 49.78, 'lon': 22.78, 'elv': 279}
    if station_name == 'Śnieżka':
        return {'lat': 50.73, 'lon': 15.74, 'elv': 1603}
    if station_name == 'Żarnowiec':
        return {'lat': 50.48, 'lon': 19.86, 'elv': 325}
    if station_name == 'Hala gąsienicowa':
        return {'lat': 49.24, 'lon': 20.01, 'elv': 1564}

    splitter = False
    if '-' in station_name:
        splitter = '-'
    if ' ' in station_name:
        splitter = ' '
    if splitter:
        splitted = station_name.split(splitter)

        start = splitted[0]
        connector = splitter
        end = splitted[1].capitalize()

        station_name = start + connector + end
        station_name = station_name.strip()

    list_of_locations_url = 'http://www.altitude-maps.com/country/170,Poland'

    r = requests.get(list_of_locations_url)
    soup = bs(r.content, features="html.parser")

    href = None
    for element in soup.find_all('a'):
        if station_name in element.get_text():
            href = element['href']
            break

    if href is None:
        station_name = station_name.split('-')[0]
        for element in soup.find_all('a'):
            if station_name in element.get_text():
                href = element['href']
                break

    if href is None:
        raise KeyError(
            """
            No coordinates have been found for the 'station_name' argument.
            Check if input 'station_name' is correct and if it is available on the website: 
            'http://www.altitude-maps.com/country/170,Poland'
            If 'station_name' input is correct and it is not available on the website, you have to input data on your own.    
            """)

    full_url = 'http://www.altitude-maps.com/' + href

    text = requests.get(full_url).text
    lat = re.search(r"geoplugin_latitude.*?([\d.-]+)", text).group(1)
    lon = re.search(r"geoplugin_longitude.*?([\d.-]+)", text).group(1)
    elv = re.search(r"geoip_elevation.*?([\d.-]+)", text).group(1)

    lat = round(float(lat), 2)
    lon = round(float(lon), 2)
    elv = round(float(elv), 2)
    return {'lat': lat, 'lon': lon, 'elv': elv}