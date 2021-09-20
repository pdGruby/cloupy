import pandas as pd
import os
from cycler import cycler
from matplotlib.pyplot import *
from matplotlib import rcParams

from cloudy.scraping.imgw import get_meteorological_data as d_imgw_data
from cloudy.scraping.climex_scraping import download_meteo_data as d_wmo_data
from cloudy.scraping.climex_scraping import get_wmo_stations_info as i_wmo_stations
from cloudy.diagrams.walter_lieth import WalterLieth

try:
    path = str(__file__).replace('__init__.py', '')

    os.remove(path + r'global_df.csv')
    os.remove(path + r'global_df.json')
except FileNotFoundError:
    pass

default_style = {
    'font.family': 'Calibri',
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'figure.figsize': (6, 6 / 1.618),
    'axes.edgecolor': 'black',
    'axes.labelsize': 10,
    'axes.prop_cycle':
        (
                cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']) +
                cycler(linestyle=['-' for solid in range(0, 10)])
        )
}

retro_style = {
    'font.family': 'Times New Roman',
    'axes.titleweight': 'bold',
    'axes.labelweight': 'light',
    'figure.figsize': (6, 6 / 1.618),
    'axes.edgecolor': 'black',
    'axes.labelsize': 12,
    'axes.prop_cycle':
        (
                cycler(color=['k' for k in range(0, 6)]) +
                cycler(linestyle=['-', '--', '-.',
                                  (0, (1, 5)),
                                  (0, (3, 1, 1, 1)),
                                  (0, (3, 10, 1, 10, 1, 10))
                                  ]
                       )
        )
}
diagStyle = rcParams
diagStyle['savefig.dpi'] = 300
diagStyle['savefig.bbox'] = 'tight'
diagStyle['savefig.pad_inches'] = 0.3
for param, value in default_style.items():
    diagStyle[param] = value


def change_diagStyle_params(diagStyle_dict):
    global diagStyle
    for changed_param, changed_value in diagStyle_dict.items():
        diagStyle[changed_param] = changed_value


def choose_diagStyle(diag_style='default'):
    if diag_style == 'default':
        for default_param, default_value in default_style.items():
            diagStyle[default_param] = default_value
    elif diag_style == 'retro':
        for retro_param, retro_value in retro_style.items():
            diagStyle[retro_param] = retro_value
    else:
        raise AttributeError(
            "Invalid 'diag_style' argument. Available arguments: 'default', 'retro'"
        )


def set_global_df(pd_DataFrame, file_format='csv'):

    path = str(__file__).replace('__init__.py', '')

    try:
        os.remove(path + r'global_df.csv')
        os.remove(path + r'global_df.json')
    except FileNotFoundError:
        pass

    if not isinstance(type(pd_DataFrame), type(pd.DataFrame)):
        raise AttributeError(
            """
            Invalid object type for 'pd_DataFrame' which must be 'pandas.DataFrame()'.
            More info about creating pandas.DataFrame() object is available here:
            'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html'
            """
        )

    if file_format == 'csv':
        pd_DataFrame.to_csv(path + r'global_df.csv')
    elif file_format == 'json':
        pd_DataFrame.to_json(path + r'global_df.json')
    else:
        raise AttributeError(
            """
            Invalid input for 'file_format'. Available inputs: 'csv', 'json'
            """
        )


def read_global_df():

    path = str(__file__).replace('__init__.py', '')

    try:
        df = pd.read_csv(path + r'global_df.csv', index_col=0)
    except FileNotFoundError:
        pass
    else:
        return df

    try:
        df = pd.read_json(path + r'global_df.json')
    except ValueError:
        raise FileNotFoundError("Use cloudy.set_global_df to set global dataframe and then use cloudy.read_global_df again.")
    else:
        return df
