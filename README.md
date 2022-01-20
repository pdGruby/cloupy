#
<p align="center">
  <img src="https://i.ibb.co/YpN6MVS/logo-update3.png" />
</p>

cloupy is a Python package for climatological data downloading, processing and visualizing. The main goal of the package is to help its author in writing a BA thesis. The package is well adapted to academic work - used data sources are reliable and graphs are easy to modify. What's more, cloupy is intuitive and really easy to use, so even users who are not related to the climatological environment should have no problems with the package usage.

![python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

![downloads](https://img.shields.io/github/downloads/pdgruby/cloupy/total)
![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![last_commit](https://img.shields.io/github/last-commit/pdgruby/cloupy) 

![license](https://img.shields.io/github/license/pdgruby/cloupy)
[![DOI](https://zenodo.org/badge/368965287.svg)](https://zenodo.org/badge/latestdoi/368965287)

# Installation

Run the following command on the command line:

**Windows:**
```bash
pip install cloupy
```

**Linux:**
```bash
pip3 install cloupy
```
    
# Usage/Examples

**This is just a demonstration of the cloupy functionality and some (in my opinion the most important) features** of the functions/classes. However, every function and class has many arguments which are not used in this tutorial, so **check the docstrings to see all features**

#### Table of contents
1. [Data downloading and processing](#data_downloading)

    a. [Download climatological data from the IMGW database](#data_downloading_imgw)
    
    b. [Download specific climatological elements from the IMGW database](#data_downloading_specific_elements_imgw)
    
    c. [Useful functions for working with the IMGW database](#data_downloading_useful_imgw)
    
    d. [Download climatological data from the WMO database](#data_downloading_wmo)
    
    e. [Useful functions for working with the WMO database](#data_downloading_useful_wmo)
    
    f. [Check data continuity](#data_processing_check_continuity)

2. [Maps](#maps_drawing)
    
    a. [Exemplary interpolation map](#maps_exemplary)
    
    b. [The same exemplary map, but without setting the map style and data filtering](#maps_exemplary_no_levels_no_data_filtering)
    
    c. [Zoom a map to a specific location, show the difference between default style and retro style](#maps_zooming_and_styles)
    
    d. [Draw a map from the manually provided data, select a non-default shapefile to draw borders of the country, plot additional shapes from an additional shapefile](#maps_manually_data_and_nondefault_shapes)
    
    e. [Import the data for drawing the interpolation map from the global dataframe and draw multi-country map. Zoom to a specific area without changing the extrapolation points](#maps_multicountry)
    
3. [Graphs](#graphs_drawing)
    
    a. [Download climatological data for the station in Poznań (WMO ID: 12330) from the IMGW and draw a Walter-Lieth diagram](#graphs_imgw)
    
    b. [Download climatological data for the station in Harare (WMO ID: 67775) from the WMO database](#graphs_wmo)
    
    c. [Download data, set as global dataframe and draw a Walter-Lieth diagram based on the global dataframe](#graphs_global_dataframe)
    
    d. [The graph style that better fits a scientific article](#graphs_styles)
    
    e. [Select which graph elements are to be drawn](#graphs_selecting_elements)
    
    f. [Provide drawing data manually](#graphs_manually_data)
    
**See also [recap of the drawing process](#drawing_process_recap) and [brief documentation](#brief_documentation)**
    
## Data downloading and processing <a name="data_downloading"></a>

### Download climatological data from the [IMGW database](https://s://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/) <a name="data_downloading_imgw"></a>
Use the `d_imgw_data()` function to download the data from the IMGW database. In the code below, the data will be downloaded from the synoptic stations of the IMGW database. In this case, the selected data interval is monthly, the data string starts in 1966 and ends in 2020. The coordinates will be added to the stations in the downloaded data:
```python
import cloupy as cl

data = cl.d_imgw_data(interval='monthly', stations_kind='synop', years_range=range(1966, 2021), return_coordinates=True)
```

### Download specific climatological elements from the [IMGW database](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/) <a name="data_downloading_specific_elements_imgw"></a>
You can specify which climatological elements from the IMGW database will be downloaded by setting the `keywords` argument of the `d_imgw_data()` function. The `keywords` argument must be a single string or a list of strings. If the given string is in a column name, the column will be added to the dataframe that will be returned. In the example below, the returned dataframe will contain the columns whose names contain the given words ('temperatura' means temperature, 'opad' means precipitation):

```python
import cloupy as cl

data = cl.d_imgw_data(
    interval='monthly', stations_kind='synop', years_range=range(1966, 2021), 
    keywords=['temperatura', 'opad'] # the function is not case-sensitive (try: ['tEmPeRaTURA', 'oPad'])
)
```

### Useful functions for working with the [IMGW database](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/) <a name="data_downloading_useful_imgw"></a>
See available file formats from the IMGW database for the given arguments:
```python
import cloupy as cl

cl.i_imgw_get_file_formats(interval='monthly', stations_kind='climat', file_format_index='all')
```

See column names in the given file format, see column names in all file formats, search for a keyword in all file formats:
```python
# column names in the 's_m_d' file format (monthly interval, synoptic station, the first file format from the available file formats)
colnames_in_sdt = cl.i_imgw_search_keywords_in_columns(keywords='', file_format='s_m_d')

# column names in all file formats (if the 'file_format' argument is None, then search in every file format)
colnames_in_all = cl.i_imgw_search_keywords_in_columns(keywords='', file_format=None)

# search for a keyword in all file formats
keywords_in_all = cl.i_imgw_search_keywords_in_columns(keywords='temperatura', file_format=None)
```

### Download climatological data from the [WMO database](http://climexp.knmi.nl/start.cgi?id=someone@somewhere) <a name="data_downloading_wmo"></a>
You can download data from the WMO database for a single station or for an entire country. If you would like to download the data for a single station, pass the station name (usually the city where the station is located) to the `station_name` argument. If you would like to download the data for an entire country, pass the country name prefixed with `cou` to the `station_name` argument (e.g. 'couGERMANY'). There are 5 elements that can be downloaded: mean air temperature ('mean'), precipitation ('preci'), minimum air temperature ('min_temp'), maximum air temperature ('max_temp') and sea level pressure ('sl_press'). To specify which element you would like to download, pass a single string or a list of strings to the `elements_to_scrape` argument:
```python
import cloupy as cl

single_station = cl.d_wmo_data(station_name='POZNAN', elements_to_scrape=['temp', 'preci', 'sl_press'])
entire_country = cl.d_wmo_data(station_name='couUnited Arab Emirates', elements_to_scrape='temp', return_coordinates=True)
```

### Useful functions for working with the [WMO database](http://climexp.knmi.nl/start.cgi?id=someone@somewhere) <a name="data_downloading_useful_wmo"></a>
You can see all available station and country names with the `cl.i_wmo_get_stations()` function:
```python
import cloupy as cl

info_df = cl.i_wmo_get_stations()
```

You can search for the nearest stations to the specified points with the `cl.i_wmo_search_near_station()` function:
```python
import cloupy as cl

close_to_london = cl.i_wmo_search_near_station(lon=0, lat=51)
higher_acceptable_distance = cl.i_wmo_search_near_station(lon=0, lat=51, degrees_range=3)
```

### Check data continuity <a name="data_processing_check_continuity"></a>
With the `cl.check_data_continuity()` function you can remove all stations that do not have satisfactory data continuity. The function will group a dataframe by unique values, count number of records for every single station and remove all stations that have too few number of records:
```python
import cloupy as cl

df = cl.d_imgw_data(interval='monthly', stations_kind='synop', years_range=range(1966, 2021))
df = cl.check_data_continuity(df=df, main_column=0, precision=1)
```
In the example above, the `check_data_continuity()` groups the dataframe by the unique values in the first column (0 is the index of the dataframe columns), counts the number of records for each station, takes the highest number of records (high_records) and removes stations with the number of records less than the high_records. The `precision` argument is set to 1, which means that the required number of records to keep a station is equal to 1 * high_records (if high_records is 1000, then the station must have 1000 records to be kept). If the `precision` argument was 0.5, then the required number of records to keep a station would be equal to 0.5 * high_records (if high_records is 1000, then the station must have at least 500 records to be kept)

## Maps <a name="maps_drawing"></a>

### Exemplary interpolation map <a name="maps_exemplary"></a>
```python
import cloupy as cl
import numpy as np

imap = cl.m_MapInterpolation(country='POLAND')

imap.d_imgw_data(
    years_range=range(1966, 2021), 
    column_with_values='temp', 
    check_continuity=True,
    continuity_precision=1
)
imap.dataframe = imap.dataframe[imap.dataframe.iloc[:, 0] > 5] # filter the dataframe to exclude
                                                               # alpine stations that negatively
                                                               # affect the interpolation result

imap.draw(
    levels=np.arange(5, 10.01, 0.05), # (start, end, step)
    show_contours=True,
    contours_levels=[5, 6, 7, 8, 9, 10],
    clabels_add=[
        (17.5, 54),
        (19.8, 53.5),
        (23, 54),
        (21, 50.8),
        (17, 50.8),
        (15, 53),
        (15.5, 51.1),
        (20, 49.5)
    ],
    cbar_ticks=[5, 6, 7, 8, 9, 10],
    cbar_title='Air temperature [°C]',
    title='Fig. N. Spatial layout of the mean temperature in Poland\n(1966-2020)',
    title_ha='center',
    title_x_position=0.5,
    save='air_temperature_poland.png'
)
```
<p align="center">
  <img src="https://i.ibb.co/f2cdDn9/air-temperature-poland.png"/>
</p>

### The same exemplary map, but without setting the map style and data filtering <a name="maps_exemplary_no_levels_no_data_filtering"></a>

**Note that** in the above code the most of the arguments are not necessary and are only optional for setting the map style - the code for drawing may be significantly shorter. However, in this case the map style may not be satisfactory and not filtered data may affect negatively the interpolation result:

```python
import cloupy as cl

# The map based on the same dataset, but without data filtering and style setting
imap = cl.m_MapInterpolation(country='POLAND')
imap.d_imgw_data(years_range=range(1966, 2021), column_with_values='temp')
imap.draw(save='ugly_map.png')

# The 'save' argument does not have to be specified either - the map will be displayed in your app with
# a lower DPI value, so the quality of the image may be poor. When the map is being saved, the DPI
# value is higher, so the image quality is much better. Different DPIs are used to enhance the 
# work - lower DPI makes the map creation process much faster, so it is used to preview the map
```

<p align="center">
  <img src="https://i.ibb.co/XjGvVhm/lev-data-comp.png"/>
</p>

**In the figure on the left, no levels were specified and no data was filtered. In the figure on the right, the data was not filtered** (alpine stations were still in the dataset, stations with poor data continuity were also in the dataset), **but the levels were specified by passing `levels=np.arange(5, 10.5, 0.5)` to the `imap.draw()` method.** The red spots in the lower parts of the map are the result of the alpine stations in the dataset - due to the significantly deviated values, the interpolation effect is somewhat distorted. The values inside the red spots are much higher than 12°C, so they are not within the specified levels, which would result in the appearance of white spots. However, to the `imap.draw()` method another argument was passed to force the interpolation process to interpolate within the given levels - `interpolation_within_levels=True`. When the `interpolation_within_levels` is set to True, the white spots are replaced with the lowest or highest color level (depending on whether the values are below the specified levels or above the specified levels)

Data filtering is not always necessary, but specifying manually levels is almost always necessary! Nevertheless, to get high-quality interpolation effect, **it is recommended to always check the dataset and specify the interpolation levels**

### Zoom a map to a specific location, show the difference between default style and retro style <a name="maps_zooming_and_styles"></a>

Sometimes you may want to highlight a specific region of a country and it is possible by passing the `zoom_in` argument to the `imap.draw()` method. This argument is also handy when you are working with a country that has overseas territories (e.g. France) and would like to show only a specific part of the country 

The `zoom_in` argument accepts a list of tuples where the first tuple holds the x-values to which the view will be adjusted, and the second tuple holds the y-values to which the view will be adjusted, e.g. `zoom_in=[(16, 18), (50, 51)]` will zoom into the region of Poland that is located between 16 and 18 degree of the east longitude and between 50 and 51 degree of the north latitude

The exemplary maps of France with the `zoom_in` argument in the default and retro styles:

```python
import cloupy as cl
import numpy as np
import matplotlib.pyplot as plt

# create the interpolation map class and prepare the data
imap=cl.m_MapInterpolation('FRANCE')
imap.d_wmo_data('couFRANCE', 'temp', check_continuity=True)
imap.dataframe = imap.dataframe[imap.dataframe.iloc[:, 0] > 9]  # remove alpine stations

# set the style, modify the map, draw
styles = ['default', 'retro']
for style in styles:
    
    cl.set_diagStyle(style) # set global style for cloupy
    
    imap.draw(
        zoom_in=[(-5.5, 10), (41, 51.5)], # zoom into the european part of France
        levels=np.arange(9.4, 16.5, 0.2),
        show_grid=True,
        show_contours=True,
        contours_levels=np.arange(6, 16, 1),
        clabels_add=[
            (5, 49),
            (3, 47),
            (2.5, 45.3),
            (2, 44),
            (2, 43),
            (6.7, 43.8)
        ],
        clabels_inline_spacing=-7,
        xticks=np.arange(-4, 9, 2),
        cbar_ticks=np.arange(9, 17, 1),
        cbar_title='Air temperature [°C]',
        title=f'Fig. N. Spatial layout of the mean temperature in France\n({style} style)',
        save=f'france_mean_temperature_layout_{style}.png'
    )

# merge the maps
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
ax1.axis('off')
ax2.axis('off')

img1 = plt.imread('france_mean_temperature_layout_default.png')
img2 = plt.imread('france_mean_temperature_layout_retro.png')

ax1.imshow(img1)
ax2.imshow(img2)

plt.subplots_adjust(wspace=-0.3)
plt.savefig('france_styles_comp.png', 
            dpi=300, bbox_inches='tight', 
            pad_inches=0.05, facecolor='white'
            )
```

<p align="center">
  <img src="https://i.ibb.co/1MPYRSB/france-styles-comp.png"/>
</p>

In this case, if the `zoom_in` argument was not specified, the maps would be completely indecipherable. This is due to the overseas territories of France which affects negatively the interpolation process and the default map zooming (by default the map is being zoomed into the extreme points of the shapefile):

<p align="center">
  <img src="https://i.ibb.co/txDRqDR/france-mean-temperature-layout-no-zoom-in.png"/>
</p>

### Draw a map from the manually provided data, select a non-default shapefile to draw borders of the country, plot additional shapes from an additional shapefile <a name="maps_manually_data_and_nondefault_shapes"></a>
The country borders do not have to be drawn from the default cloupy shapefile - you can provide your own non-default shapefile by passing its path to the `shapefile_path` argument of the `cl.m_MapInterpolation()` class

What is more, it is also possible to draw additional shapes (e.g. states, voivodeships, rivers, lakes) by passing a dictionary to the `add_shapes` argument of the `imap.draw()` method. The dictionary keys must be shapes' paths and the dictionary values must be style/coordinates system set arguments. The dictionary values must be a single `str` in which arguments are separated by commas, e.g.:
```python
add_shapes={
    'path/to/the/shapefile': 'crs=epsg:4326, linestyle=solid, linewidth=0.5',
    'path/to/another/shapefile': 'crs=epsg:2180,color=red,fill_color=blue'
}
```

The data for a map can be provided manually by passing a `pandas.DataFrame()` object to the `dataframe` argument of the `cl.m_MapInterpolation()`:
```python
import cloupy as cl

df = cl.d_imgw_data(
    interval='monthly', stations_kind='synop', 
    years_range=range(1966, 2021), return_coordinates=True
)

df = df.iloc[:, [1, 12, -3, -2]] # remove unnecessary columns from the data
df = cl.check_data_continuity(df=df, main_column=0, precision=1) # check data continuity
df = df.groupby('Nazwa stacji').mean() # calc the mean values for the stations
df = df[df.iloc[:, 0] > 5] # remove alpine stations which deviates significantly from the rest
```

When the dataframe meets the required data structure (see `cl.m_MapInterpolation` docs for more detailed information) for the interpolation map, it can be passed to the `cl.m_MapInterpolation()` class. So, if you want to provide the data manually, draw non-default borders and additional shapes, the code will look like this:
```python
import numpy as np

imap = cl.m_MapInterpolation(
    shapefile_path='path/to/shapefile', # specify the path to your non-default shapefile
    crs='epsg:4326', # specify the shapefile coordinates system
    dataframe=df # pass manually the dataframe
)

imap.draw(
    levels=np.arange(5, 10.2, 0.2),
    add_shape={
        'path/to/addit/shapefile': 'crs=epsg:4326, linewidth=0.5, linestyle=solid, color=black'
    },   # specify the path to the additional shapefile (as key) and its settings (as value)
    show_coordinates=False,
    show_frame=False,
    cbar_ticks=np.arange(5, 11, 1),
    cbar_title='Air temperature [°C]',
    title='Fig. N. Spatial layout of the mean temperature in Poland.',
    title_y_position=0.15,
    save='non-default_borders_and_additional_shp.png'
)   
```

<p align="center">
  <img src="https://i.ibb.co/pR76G8d/non-default-borders-and-additional-shp.png" />
</p>

For the above map, the shapefiles were downloaded from the **[GADM website](https://gadm.org/download_country.html)** under **[GADM license](https://gadm.org/license.html)**. 

### Import the data for drawing the interpolation map from the global dataframe and draw multi-country map. Zoom to a specific area without changing the extrapolation points <a name="maps_multicountry"></a>
```python
import cloupy as cl
import pandas as pd
import numpy as np

countries = ['ITALY', 'SWITZERLAND']
global_df = pd.DataFrame(columns=['station', 'year', 'month', 'temp', 'lon', 'lat', 'elv'])
for country in countries:
    data_for_country = cl.d_wmo_data(
        station_name='cou' + country, 
        elements_to_scrape='temp',
        return_coordinates=True
    )
    global_df = global_df.append(data_for_country)

cl.set_global_df(global_df)
imap = cl.m_MapInterpolation(country=countries)
imap.import_global_df(
    columns_order=[0, 3, 4, 5],
    check_continuity=True,
    continuity_precision=0.2
) 

# in this case, there is no need to remove the alpine stations (they are significantly relevant)
imap.draw(
    levels=np.arange(-5, 20.5, 0.5),
    cmap='coolwarm',
    save='multiple_countries.png'
)
```
<p align="center">
  <img src="https://i.ibb.co/p121MZD/multiple-countries.png" />
</p>

If you wished to take a closer look at the situation on the Italian-Swiss border, you could use the `zoom_in` argument of the `imap.draw()` method. You may notice some slight differences in the colors' layout between the map before zooming in and the map after zooming in. The differences result from different extrapolation points, which are always in the corners of the plot (when you zoom into a specific area, it means that you change the corner points of the plot, which affects the extrapolation result). **You can force the `imap.draw()` method to extrapolate the values to the points of the original plot (before zooming) by setting the `extrapolation_into_zoomed_area` argument to False:** 

```python
import matplotlib.pyplot as plt

# draw maps (1 = True, 0 = False)
for boolean in [1, 0]:
    imap.draw(
        levels=np.arange(-5, 20.5, 0.5),
        cmap='coolwarm',
        zoom_in=[(5, 12), (45, 48)],
        extrapolation_into_zoomed_area=boolean,
        figsize=(5, 2.5),
        title=f'extrapolation_into_zoomed_area={boolean}',
        title_ha='center',
        title_x_position=0.5,
        title_y_position=0,
        title_bold=True,
        save=f'multiple_countries_zoomed_in_{boolean}.png'
    )
    
# merge the maps
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(4, 8))
ax1.axis('off')
ax2.axis('off')

img1 = plt.imread('multiple_countries_zoomed_in_1.png')
img2 = plt.imread('multiple_countries_zoomed_in_0.png')

ax1.imshow(img1)
ax2.imshow(img2)

plt.subplots_adjust(hspace=-0.5)
plt.savefig('multpile_countries_extr_into_comp.png', 
            dpi=300, bbox_inches='tight', 
            pad_inches=0.05, facecolor='white'
            )
```
<p align="center">
  <img src="https://i.ibb.co/Htw7pZX/multpile-countries-extr-into-comp.png" />
</p>

As you can see, the slight differences are noticeable in the color layout. The `extrapolation_into_zoomed_area` argument must be set to True if the `zoom_in` argument is used for zooming into a specific part of the country that has overseas territories (like in the example of France above). If the `extrapolation_into_zoomed_area` argument was set to False in the case of France, the method would extrapolate values to the corners of the original plot (the plot before zooming, so the interpolation result in the European France would be completely distorted). In the case of Italy and Switzerland, some slight differences are noticeable, but these differences are still acceptable. However, **if you want to zoom into a specific part of the map with preserving the original color/contours layout, you can set the `extrapolation_into_zoomed_area` argument to False**

## Graphs <a name="graphs_drawing"></a>

### Download climatological data for the station in Poznań (WMO ID: 12330) from the [IMGW database](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/) and draw a Walter-Lieth diagram <a name="graphs_imgw"></a>
```python
import cloupy as cl

wl = cl.g_WalterLieth(station_name='POZNAŃ')
wl.d_imgw_data(years_range=range(1966, 2020))
wl.draw()
```

<p align="center">
  <img src="https://i.ibb.co/gJQVTry/poznan.png" />
</p>

### Download climatological data for the station in Harare (WMO ID: 67775) from the [WMO database](http://climexp.knmi.nl/start.cgi?id=someone@somewhere) and draw a Walter-Lieth diagram <a name="graphs_wmo"></a>
```python
import cloupy as cl

wl = cl.g_WalterLieth(station_name='HARARE')
wl.d_wmo_data()
wl.draw()
```

<p align="center">
  <img src="https://i.ibb.co/k4MxwWt/harare.png" />
</p>

### Download data, set as global dataframe and draw a Walter-Lieth diagram based on the global dataframe <a name="graphs_global_dataframe"></a>
```python
import cloupy as cl

global_df = cl.d_imgw_data(
    interval='monthly', 
    stations_kind='synop', 
    years_range=range(1966, 2020)
    )
cl.set_global_df(global_df)

wl = cl.g_WalterLieth('WARSZAWA')
wl.import_global_df(columns_order='imgw_monthly')
wl.draw()
```

<p align="center">
  <img src="https://i.ibb.co/xJnwQWt/warsaw.png" />
</p>

### The graph style that better fits a scientific article <a name="graphs_styles"></a>
```python
cl.set_diagStyle('retro')
wl.draw()
```
<p align="center">
  <img src="https://i.ibb.co/XjyWQ6j/war-retro.png" />
</p>

### Select which graph elements are to be drawn <a name="graphs_selecting_elements"></a>

As you can see, the graph for POZNAŃ displays information about the coordinates, while the graphs for WARSZAWA do not. The coordinates for POZNAŃ are automatically imported when the `wl.d_imgw_data()` method is used. However, when we import data from the global dataframe for WARSZAWA, the `wl.import_global_df()` method does not add coordinates automatically and the coordinates have to be added manually when the `cl.g_WalterLieth()` object is being created. In our case, for the graph for WARSZAWA it would be: 

```python
wl = cl.g_WalterLieth(station_name='WARSZAWA', lat=52.2, lon=21.0, elevation=100)
```

Now the `wl.draw()` method will display the coordinates box. So, **if the `cl.g_WalterLieth()` object does not find the unnecessary data, it will just simply not display missing values**. What is more, **you can manually decide which elements on the graph are to be drawn**

**The `wl.draw()` method takes several arguments that let you decide which element on the graph will be displayed**. For example, if you do not want to display the title (which actually is the station name), the yearly means box and the bottom freeze rectangles, you have to pass the following arguments to the `wl.draw()` method:
```python
wl.draw(title_text=False, yearly_means_box=False, freeze_rectangles=False)
```

### Provide drawing data manually <a name="graphs_manually_data"></a>

cloupy graphs can be drawn from the data provided manually. Every graph has its required data structure which must be preserved in the `pandas.DataFrame()` object. For a Walter-Lieth graph, the `pandas.DataFrame()` object must contain 5 or 6 columns, depending on the data interval (5 for a monthly interval, 6 for a daily interval). Data can be passed to the `dataframe` argument in the `cl.g_WalterLieth()` object. For example, the process might look like this:

```python
import cloupy as cl
import pandas as pd

data = pd.DataFrame(
    {
        'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'temp': [-2, -1, 0, 7, 15, 18, 19, 20, 18, 14, 8, 3],
        'preci': [50, 25, 55, 60, 70, 80, 90, 80, 68, 50, 45, 49],
        'max_temp': [10, 15, 17, 18, 19, 20, 35, 34, 25, 20, 15, 10],
        'min_temp': [-36, -29, -20, -15, -5, -1, 1, 2, -1, -4, -18, -22]
                            }
)
wl = cl.g_WalterLieth(station_name='TEST', dataframe=data)
wl.draw()
```

**More detailed information on the required data structure is available in the graphs classes docstrings**

# Recap of the drawing process <a name="drawing_process_recap"></a>
**cloupy drawing system is easy and can be summarized as follows:**
- create a graph/map class, provide data for further processing and drawing (follow required data structure)
- optionally, use the graph/map class methods to download and process data
- use the `draw()` method to specify the graph/map style

# Brief Documentation (the most important functions and classes) <a name="brief_documentation"></a>

**DATA PROCESSING FUNCTIONS/CLASSES**

- `check_data_continuity` -> check data continuity and return a dataframe with the filtered values
- `set_global_df(...)` -> set global data frame from which data can be imported in any time
- `read_global_df(...)` -> return the global data frame as pandas.DataFrame

**DATA SCRAPING FUNCTIONS**

-  `d_imgw_data(...)` -> download IMGW data files from the IMGW database and return it as one merged pd.DataFrame
-  `i_imgw_get_file_formats(...)` -> return the available file formats for the given 'interval' and 'stations_kind' in the IMGW database (different file formats contain different data)
-  `i_imgw_search_keywords_in_columns(...)` -> search for the given keywords in the column names and return a dictionary with the file formats in which the keywords were found
- `d_wmo_data(...)` -> download climatological data for specified station/stations from the WMO website
- `i_wmo_get_stations(...)` -> return pandas.DataFrame with WMO stations information (WMO ids, coordinates, etc.)
- `i_wmo_search_near_station(...)` -> return the nearest stations from WMO database for the given coordinates


**DATA VISUALIZATION FUNCTIONS**

- `set_diagStyle(...)` -> choose global style for diagrams
- `change_diagStyle_params(...)` -> change global parameters for drawing diagrams

**DATA VISUALIZATION CLASSES**

**Note that** every class for drawing diagrams contains some of the above functions as its methods (for data scraping and processing)

- `m_MapInterpolation(...)` -> create a MapInterpolation class where the data for drawing an interpolation map can be downloaded, modified, manually provided
- `g_WalterLieth(...)` -> create a WalterLieth object where the data for drawing a Walter-Lieth diagram can be downloaded, modified, manually provided

**More detailed documentation for every function, class and method is available in the cloupy's Python files**

# Future Features

- more climatological data processing functions (e.g. completing missing data)
- more climatological graphs

# Dependencies
**Packages/libraries**:
- [Pandas](https://pandas.pydata.org) version: 1.1.4; 1.3.5 or higher
- [Matplotlib](https://matplotlib.org) version: 3.3.2; 3.4.3 or higher
- [Requests](https://requests.readthedocs.io) version: 2.24.0; 2.26.0 or higher
- [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/) version: 4.9.3 or higher
- [pyshp](https://pypi.org/project/pyshp/) version: 2.1.3
- [pyproj](https://pyproj4.github.io/pyproj/stable/) version: 3.2.1 or higher
- [scipy](https://scipy.org) version: 1.7.2 or higher
- [Numpy](https://www.numpy.org) version: 1.19.4; 1.21.4 or higher
- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html) version: 8.4.0 or higher
- [cycler](https://pypi.org/project/cycler/) version: 0.11.0
- [Pytest](https://docs.pytest.org/en/latest/) version: 6.2.5 or higher (only for running tests)
- [Mock](http://mock.readthedocs.org/en/latest/) version: 4.0.3 or higher (only for running tests)

**Python version**: 3.8.2; 3.9.6, 3.10.2

**OS**: Windows; Linux

All the above versions of packages/Python have been tested. **Note that** cloupy should also be compatible with the versions between mentioned (e.g. cloupy should work fine on any Pandas' version between 1.1.4 and 1.3.5; any Python version between 3.8.2 and 3.9.6). However, it has not been tested and **it is recommended to use the most recent version of the packages/libraries and Python**.

# Running Tests

To run tests, run the following command from the root directory:

```bash
# change directory to the cloupy root directory, for example:
cd c:\Python\Lib\site-packages\cloupy

python -m pytest 
```

If you want to run only unit/integration testing:

```bash
python -m pytest test\test_unit

python -m pytest test\test_integration
```

**Note that** the integration testing may take some time (during the process, data downloading functions are being tested, so duration depends on several factors). The process usually takes about 9-10 minutes 

**If you want to skip data downloading tests, run the following command:**
```bash
python -m pytest -k "not downloading"
```

# Support

For support, please contact me via email: kamil.grala32466@gmail.com

If you want to report a bug, see `CONTRIBUTING.md`


# License

cloupy is licensed under [MIT](https://choosealicense.com/licenses/mit/).


# Author

[@Kamil Grala](https://github.com/pdGruby)

