"""
Functions for IMGW database analysis.

get_meteorological_data(interval, stations_kind, years_range, file_format_index=0,
                        file_format=None,   specific_columns=None, keywords=None,
                        merge_splitted_stations=True, optimize_memory_usage=False)

get_file_formats(interval, stations_kind, file_format_index)
get_column_names(file_format)
look_for_keywords_in_columns(keywords, file_format=None)

get_urls(interval, stations_kind, years_range)
download_data(urls)
concatenate_data(downloaded_files_names, file_formats, specific_columns,
                keywords, optimize_memory_usage, years_range)
"""


def get_file_formats(
        interval, stations_kind, file_format_index
):
    """
    Return the available file formats for the given 'interval' and 'stations_kind'
    (different file formats contain different data).

    Keyword arguments:
        interval -- data interval from the IMGW database ('monthly', 'daily', 'prompt')
        stations_kind -- stations' kind ('synop', 'climat', 'fall')
        file_format_index -- which element from the list of available formats will
    be returned. Usually two file formats are available, so the length of the list
    is 2 ('all', 0, 1)
    """

    if interval == 'monthly':
        if stations_kind == 'synop':
            available_files_formats = ['s_m_d', 's_m_t']
        elif stations_kind == 'fall':
            available_files_formats = ['o_m']
        elif stations_kind == 'climat':
            available_files_formats = ['k_m_d', 'k_m_t']
        else:
            raise ValueError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    elif interval == 'daily':
        if stations_kind == 'synop':
            available_files_formats = ['s_d', 's_d_t']
        elif stations_kind == 'fall':
            available_files_formats = ['o_d']
        elif stations_kind == 'climat':
            available_files_formats = ['k_d', 'k_d_t']
        else:
            raise ValueError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    elif interval == 'prompt':
        if stations_kind == 'synop':
            available_files_formats = ['s_t']
        elif stations_kind == 'fall':
            raise NotADirectoryError("There's no '/dane_meteorologiczne/terminowe/opad/' directory in IMGW database.")
        elif stations_kind == 'climat':
            available_files_formats = ['k_t']
        else:
            raise ValueError(
                "Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

    else:
        raise ValueError("Invalid 'interval' input. Available inputs: 'monthly', 'daily', 'prompt'.")

    if file_format_index == 'all':
        chosen_file_format = available_files_formats
    elif file_format_index == 0 or file_format_index == 1:
        try:
            chosen_file_format = [available_files_formats[file_format_index]]
        except IndexError:
            if len(available_files_formats) == 1:
                chosen_file_format = [available_files_formats[0]]
            else:
                raise Exception("Something's wrong with the file format.")
    else:
        raise ValueError(
            "{} file formats for the given 'interval' and 'stations_kind' available. Use index of the file format or 'all' "
            "for 'file_format_index' argument (if 'all', both file formats will be taken): {}".format(
                len(available_files_formats), available_files_formats
            )
        )
    return chosen_file_format


def get_column_names(file_format):
    """
    Return the column names for the given file format.

    Keyword arguments:
        file_format -- IMGW database file format (e.g. 's_m_t'). Available file
    formats: k_m_d, k_m_t, o_m, s_m_d, s_m_t, k_d, k_d_t, o_d, s_d, s_d_t, k_t,
    s_t
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


def search_for_keywords_in_columns(
        keywords, file_format=None
):
    """
    Search for the given keywords in the column names and return a dictionary with
    the file formats in which the keywords were found.

    Keyword arguments:
        keywords -- keywords that will be looked for
        file_format -- IMGW database file format, the columns of which will be
    used to look for keywords. If 'file_format' is None, then every column from
    every file will be taken and the function will show you exactly where the
    keywords were found (default None)
    """

    if file_format is None:
        intervals = ['monthly', 'daily', 'prompt']
        stations_kinds = ['synop', 'climat', 'fall']
        if type(keywords) == str:
            keywords = [keywords]

        found_file_formats = {}
        for interval in intervals:
            for kind in stations_kinds:
                if interval == 'prompt' and kind == 'fall':
                    continue
                file_formats = get_file_formats(interval, kind, 'all')
                found_file_formats['interval=' + str(interval) + ', ' + 'stations_kind=' + str(kind)] = file_formats

        keywords_in_files = {}
        if type(keywords) == list:
            for interval_stkind, file_formats in found_file_formats.items():
                for file in file_formats:
                    columns_names = get_column_names(file)
                    for name in columns_names:
                        for keyword in keywords:
                            if keyword.upper() in name.upper():
                                try:
                                    keywords_in_files[str(interval_stkind) + ", " + "file_format=" + str(file)].append(
                                        name)
                                except KeyError:
                                    keywords_in_files[str(interval_stkind) + ", " + "file_format=" + str(file)] = [name]
        else:
            raise ValueError("Invalid input for 'keywords'. Use a list of strings or a single str.")
        return keywords_in_files

    else:
        if type(file_format) == str:
            keywords_in_columns = []
            columns_names = get_column_names(file_format)
            for name in columns_names:
                if type(keywords) == list:
                    for keyword in keywords:
                        if keyword.upper() in name.upper():
                            keywords_in_columns.append(name)
                else:
                    raise ValueError("Invalid input for 'keywords'. Use a list of strings or a single str.")
        else:
            raise ValueError("Invalid input for the 'file_format' argument. Use a single str.")
        return keywords_in_columns


def get_urls(
        interval, stations_kind, years_range
):
    """
    Return the urls to the IMGW database for the given 'interval', 'stations_kind'
    and 'years_range'.

    Keyword arguments:
        interval -- data interval from the IMGW database (monthly, daily, prompt)
        stations_kind -- stations' kind (synop, climat, fall)
        years_range -- years range (e.g. range(1966, 2021))
    """

    if interval == 'monthly':
        interval = 'miesieczne/'
    elif interval == 'daily':
        interval = 'dobowe/'
    elif interval == 'prompt':
        interval = 'terminowe/'
        if stations_kind == 'fall':
            raise NotADirectoryError("There's no '/dane_meteorologiczne/terminowe/opad/' directory.")
    else:
        raise ValueError("Invalid 'interval' input. Available inputs: 'monthly', 'daily', 'prompt'.")

    if stations_kind == 'synop':
        stations_kind = 'synop/'
    elif stations_kind == 'fall':
        stations_kind = 'opad/'
    elif stations_kind == 'climat':
        stations_kind = 'klimat/'
    else:
        raise ValueError("Invalid 'stations_kind' input. Available inputs: 'synop', 'fall', 'climat'.")

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
                raise ValueError("No data for {}. Available years range: 1960-2021.".format(str(year)))
        else:
            years_endings.append(str(year) + '/')

    urls = []
    base_url = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/'
    for ending in years_endings:
        url = base_url + interval + stations_kind + ending
        urls.append(url)
    return urls


def download_data(urls):
    """
    Download data from the IMGW database.

    Keyword arguments:
        urls -- urls for the data which is requested
    """

    import requests
    from bs4 import BeautifulSoup as bs
    import zipfile
    import io

    files_reading_dir_path = str(__file__).replace('imgw.py', 'files_reading_folder')

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
            zip_file.extractall(files_reading_dir_path)

        if (urls.index(url) + 1) % 5 == 0:
            print("Downloading data... {}% done".format(round((urls.index(url) / len(urls)) * 100)))
    print("Data downloaded! 100% done")


def concatenate_data(
        downloaded_files_names, file_formats, specific_columns,
        keywords, optimize_memory_usage, years_range,
        merge_splitted_stations
):
    """
    Merge tables from downloaded files and return them as one merged pd.DataFrame.

    Keyword arguments:
        downloaded_files_names -- list of downloaded file names
        file_formats -- IMGW file formats included in downloaded files
        specific_columns -- which columns will be taken for merge
        keywords -- words which must be in the column name if the column is to be
    merged
        optimize_memory_usage -- reduce pd.DataFrame memory usage
        years_range -- filter pd.DataFrame up to the given period
    """

    import pandas as pd
    import numpy as np
    import os

    if isinstance(file_formats, list) and len(file_formats) > 1:
        raise ValueError(
            f"""Invalid value for the 'file_format' argument. Data downloading is possible only for a single file. 
            {len(file_formats)} files given ({file_formats}).
            """
        )

    if isinstance(file_formats, str):
        file_formats = [file_formats]

    df = pd.DataFrame()
    keywords_in_columns = []
    files_reading_dir_path = str(__file__).replace('imgw.py', 'files_reading_folder')

    for file in downloaded_files_names:
        if downloaded_files_names.index(file) == 0:
            print("Starting data concatenating... 0% done")

        for file_format in file_formats:

            if file_format == 's_d' or file_format == 'k_d':
                avoid_file_format = file_format + '_t'
            else:
                avoid_file_format = 'NO FILE FORMAT TO AVOID'

            if file_format in file and avoid_file_format not in file:

                path = os.path.join(files_reading_dir_path, file)
                csv_DataFrame = pd.read_csv(path, encoding="windows-1250", header=None)

                if specific_columns is not None and keywords is None:
                    if type(specific_columns) == str:
                        specific_columns = [specific_columns]

                    if type(specific_columns) is list:
                        csv_DataFrame = csv_DataFrame[specific_columns]
                    else:
                        raise ValueError("Invalid 'specific_columns' type. Use a list of strs or a single str.")

                if keywords is not None and len(keywords_in_columns) == 0:
                    columns = get_column_names(file_format)
                    for keyword in keywords:
                        for column in columns:
                            if keyword.upper() in column.upper():
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
            years_range)]
        df = df[df[2] <= max(
            years_range)]
    except KeyError:
        print("No column with year has been specified. Can't limit data range to given 'years_range'.")

    if merge_splitted_stations and 1 in df.columns:
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


def download_imgw_climatological_data(
        interval, stations_kind, years_range,
        file_format_index=0, file_format=None, specific_columns=None,
        keywords=None, merge_splitted_stations=True, optimize_memory_usage=False,
        return_coordinates=False
):
    """
    Download the IMGW data files and return them as one merged pd.DataFrame.

    Keyword arguments:
        interval -- data interval from the IMGW database ('monthly', 'daily',
    'prompt')
        stations_kind -- stations' kind ('synop', 'climat', 'fall')
        years_range -- years range (e.g. range(2010, 2021))
        file_format_index -- for which element (from the list of the available file
    formats in the IMGW database) the data will be downloaded. Usually the length of
    the list is 2. Valid inputs: 0, 1, 'all' (default 0)
        file_format -- IMGW database file format. The argument has priority over
    'file_format_index'. If None, the data will be downloaded correspondingly to
    'file_format_index' (default None)
        specific_columns -- which columns from downloaded files will be taken
    to merge. If None, take all columns (default None)
        keywords -- words which must be in the column name if the column is to be
    merged. If None, do not filter the column names (default None)
        merge_splitted_stations -- merge stations which are the same but have
    different names (default True)
        optimize_memory_usage -- reduce pd.DataFrame memory usage (default False)
        return_coordinates -- add columns with latitude, longitude and elevation
    to the returned DataFrame (default False)
    """

    from os import listdir
    from os.path import isfile, join
    import shutil

    if file_format not in get_file_formats(interval, stations_kind, 'all') and file_format is not None:
        raise ValueError(
            f"""
            There's no such file format ({file_format}) for the specified combination of 'interval' and 'stations_kind'
            """
        )

    files_reading_dir_path = str(__file__).replace('imgw.py', 'files_reading_folder')

    urls = get_urls(interval, stations_kind, years_range)
    download_data(urls)
    downloaded_files_names = [f for f in listdir(files_reading_dir_path) if isfile(join(files_reading_dir_path, f))]

    if file_format is not None:
        if type(file_format) == str:
            file_formats = [file_format]
        elif type(file_format) == list:
            file_formats = [format_ for format_ in file_format]
        else:
            raise ValueError("Invalid input for the 'file_format' argument. Use a signle str or a list of strs.")
    else:
        file_formats = get_file_formats(interval, stations_kind, file_format_index)

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

        if specific_columns is not None and keywords is None:
            chosen_columns_names = []
            if type(specific_columns) == list:
                for column_index in specific_columns:
                    chosen_columns_names.append(column_names[column_index])
            df.columns = chosen_columns_names

        elif keywords is not None:
            chosen_columns_names = []
            for column_index in keywords_in_columns:
                chosen_columns_names.append(column_names[column_index])
            df.columns = chosen_columns_names

        else:
            df.columns = column_names

    shutil.rmtree(files_reading_dir_path)

    if return_coordinates:

        import pandas as pd

        lat = []
        lon = []
        elv = []

        path = str(__file__).replace('imgw.py', 'imgw_coordinates.csv')
        station_coordinates = pd.read_csv(path, index_col=0)

        for station in list(df['Nazwa stacji']):
            try:
                coordinates = station_coordinates[station]
            except KeyError:
                lat.append(None)
                lon.append(None)
                elv.append(None)
                continue

            lon.append(coordinates[1])
            lat.append(coordinates[0])
            elv.append(coordinates[2])

        df['lon'] = lon
        df['lat'] = lat
        df['elv'] = elv

    return df
