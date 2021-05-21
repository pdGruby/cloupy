import cloudy.errors
import pandas as pd
import os
from cycler import cycler
from matplotlib.pyplot import *
from matplotlib import rcParams

from cloudy.walter_lieth import WalterLieth

try:
    os.remove('global_df.csv')
    os.remove('global_df.json')
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
        raise errors.InvalidArgValue('cloudy.choose_diagStyle').invalid_arg(
            arg_name='diag_style', valid_values=['default', 'retro']
        )


def set_global_df(pd_DataFrame, file_format='csv'):
    try:
        os.remove('global_df.csv')
        os.remove('global_df.json')
    except FileNotFoundError:
        pass

    if not isinstance(type(pd_DataFrame), type(pd.DataFrame)):
        raise errors.InvalidArgValue('cloudy.set_global_df').invalid_arg(
            arg_name='pd_DataFrame', valid_values='pandas.DataFrame()',
            additional_info="""
            More info about creating pandas.DataFrame() object is available here:
            'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html'
                            """
        )

    if file_format == 'csv':
        pd_DataFrame.to_csv('global_df.csv')
    elif file_format == 'json':
        pd_DataFrame.to_json('global_df.json')
    else:
        raise errors.InvalidArgValue('cloudy.set_global_df').invalid_arg(
            arg_name='file_format', valid_values=['csv', 'json']
        )


def read_global_df():
    try:
        df = pd.read_csv('global_df.csv', index_col=0)
        return df
    except FileNotFoundError:
        pass

    try:
        df = pd.read_json('global_df.json')
        return df
    except ValueError:
        raise errors.NoDataError('cloudy.read_global_df').no_global_df_set(
            additional_info="""Use cloudy.set_global_df to set global dataframe and then use cloudy.read_global_df again."""
        )
