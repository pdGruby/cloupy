"""
Functions for IMGW database analysis.

get_meteorological_data(interval, stations_kind, years_range, file_format_index=0,
                        file_format=None,   specific_columns=None, keywords=None,
                        merge_split_stations=True, optimize_memory_usage=False)

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
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Absolutna temperatura maksymalna [??C]',
                'Status pomiaru TMAX', '??rednia temperatura maksymalna [??C]', 'Status pomiaru TMXS',
                'Absolutna temperatura minimalna [??C]', 'Status pomiaru TMIN', '??rednia temperatura minimalna [??C]',
                'Status pomiaru TMNS', '??rednia temperatura miesi??czna [??C]', 'Status pomiaru STM',
                'Minimalna temperatura przy gruncie [??C]', 'Status pomiaru TMNG', 'Miesieczna suma opad??w [mm]',
                'Status pomiaru SUMM', 'Maksymalna dobowa suma opad??w [mm]', 'Status pomiaru OPMX',
                'Pierwszy dzie?? wystapienia opadu maksymalnego', 'Ostatni dzie?? wyst??pienia opadu maksymalnego',
                'Maksymalna wysoko???? pokrywy ??nie??nej [cm]', 'Status pomiaru PKSN', 'Liczba dni z pokryw?? ??nie??n??',
                'Liczba dni z opadem deszczu', 'Liczba dni z opadem ??niegu']

    elif file_format == 'k_m_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', '??rednia miesi??czna temperatura [??C]',
                'Status pomiaru TEMP', '??rednia miesi??czna wilgotno???? wzgl??dna [%]', 'Status pomiaru WLGS',
                '??rednia miesi??czna pr??dko???? wiatru [m/s]', 'Status pomiaru FWS',
                '??rednie miesi??czne zachmurzenie og??lne [oktanty]', 'Status pomiaru NOS']

    elif file_format == 'o_m':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Miesi??czna suma opad??w [mm]', 'Status pomiaru SUMM',
                'Liczba dni z opadem ??niegu', 'Status pomiaru LDS', 'Opad maksymalny [mm]', 'Status pomiaru MAXO',
                'Dzie?? pierwszy wyst??pienia opadu maksymalnego', 'Dzie?? ostatni wyst??pienia opadu maksymalnego',
                'Liczba dni z pokryw?? ??nie??n??', 'Status pomiaru LDPS']

    elif file_format == 's_m_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Absolutna temperatura maksymalna [??C]',
                'Status pomiaru TMAX', '??rednia temperatura maksymalna [??C]', 'Status pomiaru TMXS',
                'Absolutna temperatura minimalna [??C]', 'Status pomiaru TMIN', '??rednia temperatura minimalna [??C]',
                'Status pomiaru TMNS', '??rednia temperatura miesi??czna [??C]', 'Status pomiaru STM',
                'Minimalna temperatura przy gruncie [??C]', 'Status pomiaru TMNG', 'Miesieczna suma opad??w [mm]',
                'Status pomiaru SUMM', 'Maksymalna dobowa suma opad??w [mm]', 'Status pomiaru OPMX',
                'Pierwszy dzie?? wystapienia opadu maksymalnego', 'Ostatni dzie?? wyst??pienia opadu maksymalnego',
                'Miesi??czna suma us??onecznienia [godziny]', 'Status pomiaru SUUS',
                'Maksymalna wysoko???? pokrywy ??nie??nej [cm]', 'Status pomiaru PKSN', 'Liczba dni z pokryw?? ??nie??n??',
                'Status pomiaru PSDN', 'Liczba dni z opadem deszczu', 'Status pomiaru DESD',
                'Liczba dni z opadem ??niegu',
                'Status pomiaru SNID', 'Liczba dni z opadem deszczu ze ??niegiem', 'Status pomiaru DSND',
                'Liczba dni z gradem', 'Status pomiaru GRDD', 'Liczba dni z mg????', 'Status pomiaru MGLD',
                'Liczba dni z zamgleniem', 'Status pomiaru ZAMD', 'Liczba dni z sadzi??', 'Status pomiaru SADD',
                'Liczba dni z go??oledzi??', 'Status pomiaru GOLD', 'Liczba dni z zamieci?? ??nie??n?? nisk??',
                'Status pomiaru ZAND', 'Liczba dni z zamieci?? ??nie??n?? wysok??', 'Status pomiaru ZAWD',
                'Liczba dni ze zm??tnieniem', 'Status pomiaru ZMED', 'Liczba dni z wiatrem >= 10m/s',
                'Status pomiaru W10D', 'Liczba dni z wiatrem >15m/s', 'Status pomiaru W15D', 'Liczba dni z burz??',
                'Status pomiaru BURD', 'Liczba dni z ros??', 'Status pomiaru ROSD', 'Liczba dni ze szronem',
                'Status pomiaru SZRD']

    elif file_format == 's_m_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', '??rednie miesi??czne zachmurzenie og??lne [oktanty]',
                'Status pomiaru NOS', '??rednia miesi??czna pr??dko???? wiatru [m/s]', 'Status pomiaru FWS',
                '??rednia miesi??czna temperatura [??C]', 'Status pomiaru TEMP',
                '??rednie miesi??czne ci??nienie pary wodnej [hPa]', 'Status pomiaru CPW',
                '??rednia miesi??czna wilgotno???? wzgl??dna [%]', 'Status pomiaru WLGS',
                '??rednie miesi??czne ci??nienie na poziomie stacji [hPa]', 'Status pomiaru PPPS',
                '??rednie miesi??czne ci??nienie na pozimie morza [hPa]', 'Status pomiaru PPPM', 'Suma opadu dzie?? [mm]',
                'Status pomiaru WODZ', 'Suma opadu noc [mm]', 'Status pomiaru WONO']

    elif file_format == 'k_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', 'Maksymalna temperatura dobowa [??C]',
                'Status pomiaru TMAX', 'Minimalna temperatura dobowa [??C]', 'Status pomiaru TMIN',
                '??rednia temperatura dobowa [??C]', 'Status pomiaru STD', 'Temperatura minimalna przy gruncie [??C]',
                'Status pomiaru TMNG', 'Suma dobowa opad??w [mm]', 'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]',
                'Wysoko???? pokrywy ??nie??nej [cm]', 'Status pomiaru PKSN']

    elif file_format == 'k_d_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', '??rednia dobowa temperatura [??C]',
                'Status pomiaru TEMP', '??rednia dobowa wilgotno???? wzgl??dna [%]', 'Status pomiaru WLGS',
                '??rednia dobowa pr??dko???? wiatru [m/s]', 'Status pomiaru FWS',
                '??rednie dobowe zachmurzenie og??lne [oktanty]', 'Status pomiaru NOS']

    elif file_format == 'o_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', 'Suma dobowa opad??w [mm]',
                'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]', 'Wysoko???? pokrywy ??nie??nej [cm]', 'Status pomiaru PKSN',
                'Wysoko???? ??wie??o spad??ego ??niegu [cm]', 'Status pomiaru HSS', 'Gatunek ??niegu [kod]',
                'Status pomiaru GATS', 'Rodzaj pokrywy ??nie??nej [kod]', 'Status pomiaru RPSN']

    elif file_format == 's_d':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', 'Maksymalna temperatura dobowa [??C]',
                'Status pomiaru TMAX', 'Minimalna temperatura dobowa [??C]', 'Status pomiaru TMIN',
                '??rednia temperatura dobowa [??C]', 'Status pomiaru STD', 'Temperatura minimalna przy gruncie [??C]',
                'Status pomiaru TMNG', 'Suma dobowa opadu [mm]', 'Status pomiaru SMDB', 'Rodzaj opadu [S/W/ ]',
                'Wysoko???? pokrywy ??nie??nej [cm]', 'Status pomiaru PKSN', 'R??wnowa??nik wodny ??niegu [mm/cm]',
                'Status pomiaru RWSN', 'Us??onecznienie [godziny]', 'Status pomiaru USL',
                'Czas trwania opadu deszczu [godziny]', 'Status pomiaru DESZ', 'Czas trwania opadu ??niegu [godziny]',
                'Status pomiaru SNEG', 'Czas trwania opadu deszczu ze ??niegiem [godziny]', 'Status pomiaru DISN',
                'Czas trwania gradu [godziny]', 'Status pomiaru GRAD', 'Czas trwania mg??y [godziny]',
                'Status pomiaru MGLA', 'Czas trwania zamglenia  [godziny]', 'Status pomiaru ZMGL',
                'Czas trwania sadzi [godziny]', 'Status pomiaru SADZ', 'Czas trwania go??oledzi [godziny]',
                'Status pomiaru GOLO', 'Czas trwania zamieci ??nie??nej niskiej [godziny]', 'Status pomiaru ZMNI',
                'Czas trwania zamieci ??nie??nej wysokiej [godziny]', 'Status pomiaru ZMWS',
                'Czas trwania zm??tnienia [godziny]', 'Status pomiaru ZMET', 'Czas trwania wiatru >=10m/s [godziny]',
                'Status pomiaru FF10', 'Czas trwania wiatru >15m/s [godziny]', 'Status pomiaru FF15',
                'Czas trwania burzy  [godziny]', 'Status pomiaru BRZA', 'Czas trwania rosy  [godziny]',
                'Status pomiaru ROSA', 'Czas trwania szronu [godziny]', 'Status pomiaru SZRO',
                'Wyst??pienie pokrywy ??nie??nej [0/1]', 'Status pomiaru DZPS', 'Wyst??pienie b??yskawicy [0/1]',
                'Status pomiaru DZBL', 'Stan gruntu [Z/R]', 'Izoterma dolna [cm]', 'Status pomiaru IZD',
                'Izoterma g??rna [cm]', 'Status pomiaru IZG', 'Aktynometria  [J/cm2]', 'Status pomiaru AKTN']

    elif file_format == 's_d_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', '??rednie dobowe zachmurzenie og??lne [oktanty]',
                'Status pomiaru NOS', '??rednia dobowa pr??dko???? wiatru [m/s]', 'Status pomiaru FWS',
                '??rednia dobowa temperatura [??C]', 'Status pomiaru TEMP', '??rednia dobowe ci??nienie pary wodnej [hPa]',
                'Status pomiaru CPW', '??rednia dobowa wilgotno???? wzgl??dna [%]', 'Status pomiaru WLGS',
                '??rednia dobowe ci??nienie na poziomie stacji [hPa]', 'Status pomiaru PPPS',
                '??rednie dobowe ci??nienie na pozimie morza [hPa]', 'Status pomiaru PPPM', 'Suma opadu dzie?? [mm]',
                'Status pomiaru WODZ', 'Suma opadu noc [mm]', 'Status pomiaru WONO']

    elif file_format == 'k_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', 'Godzina', 'Temperatura powietrza [??C]',
                'Status pomiaru TEMP', 'Temperatura termometru zwil??onego [??C]', 'Status pomiaru TTZW',
                'Wska??nik lodu [L/W]', 'Wska??nik wentylacji [W/N]', 'Wilgotno???? wzgl??dna [%]', 'Status pomiaru WLGW',
                'Kod kierunku wiatru [kod]', 'Status pomiaru DKDK', 'Pr??dko???? wiatru [m/s]', 'Status pomiaru FWR',
                'Zachmurzenie og??lne [0-10 do dn.31.12.1988/oktanty od dn.01.01.1989]', 'Status pomiaru ZOGK',
                'Widzialno???? [kod]', 'Status pomiaru WID']

    elif file_format == 's_t':
        return ['Kod stacji', 'Nazwa stacji', 'Rok', 'Miesi??c', 'Dzie??', 'Godzina',
                'Wysoko???? podstawy chmur CL CM szyfrowana [kod]', 'Status pomiaru HPOD',
                'Wysoko???? podstawy ni??szej [m]',
                'Status pomiaru HPON', 'Wysoko???? podstawy wy??szej [m]', 'Status pomiaru HPOW',
                'Wysoko???? podstawy tekstowy [opis]', 'Pomiar przyrzadem 1 (ni??sza) [P]',
                'Pomiar przyrzadem 2 (wy??sza) [P]',
                'Widzialno???? [kod]', 'Status pomiaru WID', 'Widzialno???? operatora [m]', 'Status pomiaru WIDO',
                'Widzialno???? automat [m]', 'Status pomiaru WIDA', 'Zachmurzenie og??lne [oktanty]', 'Status pomiaru NOG',
                'Kierunek wiatru  [??]', 'Status pomiaru KRWR', 'Pr??dko???? wiatru [m/s]', 'Status pomiaru FWR',
                'Poryw wiatru [m/s]', 'Status pomiaru PORW', 'Temperatura powietrza [??C]', 'Status pomiaru TEMP',
                'Temperatura termometru zwil??onego [??C]', 'Status pomiaru TTZW', 'Wska??nik wentylacji [W/N]',
                'Wska??nik lodu [L/W]', 'Ci??nienie pary wodnej [hPa]', 'Status pomiaru CPW', 'Wilgotno???? wzgl??dna [%]',
                'Status pomiaru WLGW', 'Temperatura punktu rosy [??C]', 'Status pomiaru TPTR',
                'Ci??nienie na pozimie stacji [hPa]', 'Status pomiaru PPPS', 'Ci??nienie na poziomie morza [hPa]',
                'Status pomiaru PPPM', 'Charakterystyka tendencji [kod]', 'Warto???? tendencji [warto????]',
                'Status pomiaru APP',
                'Opad za 6 godzin [mm]', 'Status pomiaru WO6G', 'Rodzaj opadu za 6 godzin [kod]', 'Status pomiaru ROPT',
                'Pogoda bie????ca [kod]', 'Pogoda ubieg??a [kod]', 'Zachmurzenie niskie [oktanty]', 'Status pomiaru CLCM',
                'Chmury CL [kod]', 'Status pomiaru CHCL', 'Chmury CL tekstem', 'Chmury CM [kod]', 'Status pomiaru CHCM',
                'Chmury CM tekstem', 'Chmury CH [kod]', 'Status pomiaru CHCH', 'Chmury CH tekstem', 'Stan gruntu [kod]',
                'Status pomiaru SGRN', 'Niedosyt wilgotno??ci [hPa]', 'Status pomiaru DEFI', 'Us??onecznienie',
                'Status pomiaru USLN', 'Wyst??pienie rosy [0/1]', 'Status pomiaru ROSW',
                'Poryw maksymalny za okres WW [m/s]', 'Status pomiaru PORK', 'Godzina wyst??pienia porywu',
                'Minuta wyst??pienia porywu', 'Temperatura gruntu -5 [??C]', 'Status pomiaru TG05',
                'Temperatura gruntu -10 [??C]', 'Status pomiaru TG10', 'Temperatura gruntu -20 [??C]',
                'Status pomiaru TG20', 'Temperatura gruntu -50 [??C]', 'Status pomiaru TG50',
                'Temperatura gruntu -100 [??C]',
                'Status pomiaru TG100', 'Temperatura minimalna za 12 godzin [??C]', 'Status pomiaru TMIN',
                'Temperatura maksymalna za 12 godzin [??C]', 'Status pomiaru TMAX',
                'Temperatura minimalna przy gruncie za 12 godzin [??C]', 'Status pomiaru TGMI',
                'R??wnowa??nik wodny ??niegu [mm/cm]', 'Status pomiaru RWSN', 'Wysoko???? pokrywy ??nie??nej [cm]',
                'Status pomiaru PKSN', 'Wysoko???? ??wie??o spad??ego ??niegu [cm]', 'Status pomiaru HSS',
                'Wysoko???? ??niegu na poletku [cm]', 'Status pomiaru GRSN', 'Gatunek ??niegu [kod]',
                'Ukszta??towanie pokrywy [kod]', 'Wysoko???? pr??bki [cm]', 'Status pomiaru HPRO', 'Ci????ar pr??bki [g]',
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
    if type(keywords) == str:
        keywords = [keywords]

    if file_format is None:
        intervals = ['monthly', 'daily', 'prompt']
        stations_kinds = ['synop', 'climat', 'fall']

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
            print("Data download started... 0% done")

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

    if isinstance(keywords, str):
        keywords = [keywords]

    df = pd.DataFrame()
    keywords_in_columns = []
    files_reading_dir_path = str(__file__).replace('imgw.py', 'files_reading_folder')

    for file in downloaded_files_names:
        if downloaded_files_names.index(file) == 0:
            print("Data concatenating started... 0% done")

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
            elif station == '????D??-LUBLINEK':
                new_stations_series.append('????D??')
            elif station == 'POZNA??-??AWICA':
                new_stations_series.append('POZNA??')
            elif station == 'WARSZAWA-OK??CIE':
                new_stations_series.append('WARSZAWA')
            elif station == 'WROC??AW-STRACHOWICE':
                new_stations_series.append('WROC??AW')
            elif station == 'ELBL??G-MILEJEWO':
                new_stations_series.append('ELBL??G')
            elif station == 'RESKO-SM??LSKO':
                new_stations_series.append('RESKO')
            elif station == 'KO??OBRZEG-D??WIRZYNO':
                new_stations_series.append('KO??OBRZEG')
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
        keywords=None, merge_split_stations=True, optimize_memory_usage=False,
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
        merge_split_stations -- merge stations which are the same but have
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
            raise ValueError("Invalid input for the 'file_format' argument. Use a single str or a list of strs.")
    else:
        file_formats = get_file_formats(interval, stations_kind, file_format_index)

    df = concatenate_data(downloaded_files_names, file_formats, specific_columns,
                          keywords, optimize_memory_usage, years_range,
                          merge_split_stations)

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

        print('Joining coordinates to the dataframe...')

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

        print('Coordinates joined!')

    return df
