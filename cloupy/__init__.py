"""
Enjoy easy data scraping from websites and its processing. What's more, enjoy
even easier data visualization!

-----DATA PROCESSING FUNCTIONS/CLASSES----
    check_data_continuity -- check data continuity and return a dataframe with the
filtered values
    set_global_df() -- set a global dataframe from which data can be imported at
any time and place
    read_global_df() -- return the global data frame as pandas.DataFrame
-------------------------------------------

---------DATA SCRAPING FUNCTIONS--------
    d_imgw_data() -- download IMGW data files from the IMGW database and return them
as one merged pd.DataFrame
    i_imgw_get_file_formats() -- return the available file formats for the given
'interval' and 'stations_kind' in the IMGW database (different file formats contain
different data)
    i_imgw_search_keywords_in_columns() -- search for the given keywords in the column
names and return a dictionary with the file formats in which the keywords were found

    d_wmo_data() -- download climatological data for specified station/stations
from the WMO website
    i_wmo_get_stations() -- return pandas.DataFrame with WMO stations information
(WMO ids, coordinates, etc.)
    i_wmo_search_near_station() -- return the nearest stations from the WMO database
for the given coordinates
----------------------------------------

-------DATA VISUALIZATION FUNCTIONS------
    set_diagStyle() -- choose a global style for diagrams
    change_diagStyle_params() -- change global parameters for drawing diagrams
-----------------------------------------

--------DATA VISUALIZATION CLASSES-------
# Note that every class for drawing diagrams contains some of the above functions
as its methods (for data scraping and processing)

    m_MapInterpolation() -- create a MapInterpolation class where the data for
drawing an interpolation map can be downloaded, modified, manually provided
    g_WalterLieth() -- create a WalterLieth object in which data for drawing a
Walter-Lieth diagram can be downloaded, modified, manually provided
-----------------------------------------
"""
import pandas as pd
import os
from matplotlib.pyplot import *
from matplotlib import rcParams
import warnings

from cloupy.data_processing.check_data_continuity import check_data_continuity as check_data_continuity

from cloupy.scraping.imgw import download_imgw_climatological_data as d_imgw_data
from cloupy.scraping.imgw import get_file_formats as i_imgw_get_file_formats
from cloupy.scraping.imgw import search_for_keywords_in_columns as i_imgw_search_keywords_in_columns

from cloupy.scraping.wmo import download_wmo_climatological_data as d_wmo_data
from cloupy.scraping.wmo import get_wmo_stations_info as i_wmo_get_stations
from cloupy.scraping.wmo import search_for_the_nearest_station as i_wmo_search_near_station

from cloupy.diagrams.walter_lieth import WalterLieth as g_WalterLieth
from cloupy.maps.interpolation_map import MapInterpolation as m_MapInterpolation

from pandas import DataFrame as DataFrame

warnings.warn('The cloupy package is NO LONGER SUPPORTED. Due to unmaintainable code and numerous outdated '
              'functionalities, development and maintenance of the cloupy package have been discontinued. If you '
              'installed the cloupy package to create interpolation maps, there is a much better tool available: '
              'https://pypi.org/project/geokrige/. Significant changes have been made to the data sources from which '
              'the cloupy package downloads data, rendering cloupy tools potentially dysfunctional. The only '
              'components that are relatively up-to-date are the Walter-Lieth diagrams.')

try:  # delete global data frame from the previous session
    path_ = str(__file__).replace('__init__.py', '')

    os.remove(path_ + r'global_df.csv')
    os.remove(path_ + r'global_df.json')
except FileNotFoundError:
    pass

#  dictionaries of styles for drawing
default_style = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Dejavu Sans', 'Tahoma', 'Lucida Grande', 'Verdana'],
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'axes.edgecolor': 'black',
    'axes.labelsize': 10,
}

retro_style = {
    'font.family': 'Times New Roman',
    'axes.titleweight': 'bold',
    'axes.labelweight': 'light',
    'axes.edgecolor': 'black',
    'axes.labelsize': 12,
}

#  set default style for cloudy
with open(str(__file__).replace('__init__.py', '') + os.sep + 'current_diagStyle.txt', 'w+') as f:
    f.write('default')
diagStyle = rcParams
diagStyle['savefig.dpi'] = 300
diagStyle['savefig.bbox'] = 'tight'
diagStyle['savefig.pad_inches'] = 0.3
for param, value in default_style.items():
    diagStyle[param] = value


def change_diagStyle_params(diagStyle_dict):
    """
    Change global parameters for drawing diagrams.

    Keyword arguments:
        diagStyle_dict -- a dictionary in which the keys are parameters that have
    to be changed; values are the values to which default values have to be changed

    ---------------NOTE THAT---------------
    For available parameters and their valid values you can check matplotlib's
    'rcParams' documentation:
    https://matplotlib.org/stable/tutorials/introductory/customizing.html
    ---------------------------------------
    """

    global diagStyle
    for changed_param, changed_value in diagStyle_dict.items():
        diagStyle[changed_param] = changed_value


def set_diagStyle(diag_style='default'):
    """
    Choose a global style for diagrams.

    Keyword arguments:
        diag_style -- a style for diagrams. Available styles: 'default', 'retro'
    (default 'default')
    """
    if diag_style == 'default':
        for default_param, default_value in default_style.items():
            diagStyle[default_param] = default_value
        with open(str(__file__).replace('__init__.py', '') + os.sep + 'current_diagStyle.txt', 'w+') as file:
            file.write('default')

    elif diag_style == 'retro':
        for retro_param, retro_value in retro_style.items():
            diagStyle[retro_param] = retro_value
        with open(str(__file__).replace('__init__.py', '') + os.sep + 'current_diagStyle.txt', 'w+') as file:
            file.write('retro')

    else:
        raise ValueError(
            "Invalid 'diag_style' argument. Available arguments: 'default', 'retro'"
        )


def set_global_df(
        pd_DataFrame
):
    """
    Set global dataframe from which data can be imported at any time and place.

    Keyword arguments:
        pd_DataFrame -- a pandas DataFrame object which will be the global DataFrame
    """

    path = str(__file__).replace('__init__.py', '')

    try:
        os.remove(path + r'global_df.csv')
    except FileNotFoundError:
        pass

    if not isinstance(pd_DataFrame, pd.DataFrame):
        raise ValueError(
            """
            Invalid object type for 'pd_DataFrame' which must be 'pandas.DataFrame'. More info on creating pandas.DataFrame() 
            object is available here: 'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html'
            """
        )

    pd_DataFrame.to_csv(path + r'global_df.csv')


def read_global_df():
    """
    Return the global dataframe which was previously set by the 'set_global_df'
    function.
    """
    path = str(__file__).replace('__init__.py', '')

    try:
        df = pd.read_csv(path + r'global_df.csv', index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Use cloudy.set_global_df to set a global dataframe and then use cloudy.read_global_df again.")
    else:
        return df
