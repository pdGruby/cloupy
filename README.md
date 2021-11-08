
#
<p align="center">
  <img src="https://i.ibb.co/YpN6MVS/logo-update3.png" />
</p>

cloupy is a Python package for climatological data downloading, processing and visualizing. The main goal of the package is to help its author in writing a BA thesis. The package is well adapted to academic work - used data sources are reliable and graphs are easy to modify. What's more, cloupy is intuitive and really easy to use, so even users who are not related to the climatological environment should have no problems with the library usage.

## Installation

Run the following command on the command line:

```bash
pip install cloupy
```
    
## Usage/Examples
### 1. Import cloupy library.
```python
import cloupy as cl
```

### 2. Download climatological data for a single station and for the whole country from the [WMO database](http://climexp.knmi.nl/start.cgi?id=someone@somewhere).
```python
single_station = cl.d_wmo_data(station_name='TOKYO', elements_to_scrape=['temp', 'preci'])
whole_country = cl.d_wmo_data(station_name='couJAPAN', elements_to_scrape=['temp', 'preci'])
```

### 3. Download climatological data for the station in Poznań (WMO ID: 12330) from the [IMGW database](https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/) and draw a Walter-Lieth diagram.
```python
wl = cl.g_WalterLieth(station_name='POZNAŃ')
wl.d_imgw_data(years_range=range(1966, 2020))
wl.draw()
```

### 4. How does the graph look like?
<p align="center">
  <img src="https://i.ibb.co/JdR4rV5/poznan.png" />
</p>

### 5. Download data, set as global dataframe and draw a Walter-Lieth diagram based on the global dataframe.
```python
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
  <img src="https://i.ibb.co/NYVgSCP/war.png" />
</p>

### 6. The graph style that better fits a scientific article.
```python
cl.choose_diagStyle('retro')
wl.draw()
```
<p align="center">
  <img src="https://i.ibb.co/XjyWQ6j/war-retro.png" />
</p>

### 7. Select which graph elements are to be drawn.

As you can see, the graph for POZNAŃ displays information about the coordinates, while the graphs for WARSZAWA do not. The coordinates for POZNAŃ are automatically imported when the `wl.d_imgw_data()` method is used. However, when we import data from the global dataframe for WARSZAWA, the `wl.import_global_df()` method does not add coordinates automatically and the coordinates have to be added manually when the `cl.g_WalterLieth()` object is being created. In our case, for the graph for WARSZAWA it would be: 

```python
cl.g_WalterLieth(station_name='WARSZAWA', lat=52.2, lon=21.0, elevation=100)
```

Now the `cl.draw()` method will display the coordinates box. So, **if the `cl.g_WalterLieth()` object does not find the unnecessary data, it will just simply not display missing values**. What is more, **you can manually decide which elements on the graph are to be drawn**.

**The `wl.draw()` method takes several arguments that let you to decide which element on the graph will be displayed**. For example, if you do not want to display the title (which actually is the station name), the yearly means box and the bottom freeze rectangles, you have to pass the following arguments to the `wl.draw()` method:
```python
wl.draw(title_text=False, yearly_means_box=False, freeze_rectangles=False)
```

### 8. Provide drawing data manually.

cloupy graphs can be drawn from the data provided manually. Every graph has its required data structure which must be preserved in the `pandas.DataFrame()` object. For a Walter-Lieth graph, the `pandas.DataFrame()` object must contain 5 or 6 columns, depending on the data interval (5 for a monthly interval, 6 for a daily interval). Data can be passed to the `dataframe` argument in the `cl.g_WalterLieth()` object. For example, the process might look like this:

```python
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

**More detailed information on the required data structure is available in the graphs classes docstrings.**

### 9. Recap of the drawing process.
**cloupy drawing system is easy and can be summarized as follows:**
- create a graph object, provide data for further processing and drawing (follow required data structure)
- optionally, use the graph object methods to download and process data
- use the `draw()` method to specify which elements of the graph will be displayed. Enjoy the graph!

## Brief Documentation (the most important functions and classes)

**DATA PROCESSING FUNCTIONS/CLASSES**

- `set_global_df(...)` -> set global data frame from which data can be imported in any time.
- `read_global_df(...)` -> return the global data frame as pandas.DataFrame.
- `DataFrame(...)` -> create pandas.DataFrame object.

**DATA SCRAPING FUNCTIONS**

-  `d_imgw_data(...)` -> download IMGW data files from the IMGW database and return it as one merged pd.DataFrame.
-  `i_imgw_get_file_formats(...)` -> return the available file formats for the given 'interval' and 'stations_kind' in the IMGW database (different file formats contain different data)
-  `i_imgw_serach_keywords_in_columns(...)` -> search for the given keywords in the column names and return a dictionary with the file formats in which the keywords were found
- `d_wmo_data(...)` -> download climatological data for specified station/stations from the WMO website.
- `i_wmo_get_stations(...)` -> return pandas.DataFrame with WMO stations information (WMO ids, coordinates, etc.).
- `i_wmo_search_near_station(...)` -> return the nearest stations from WMO database for the given coordinates.


**DATA VISUALIZATION FUNCTIONS**

- `choose_diagStyle(...)` -> choose global style for diagrams.
- `change_diagStyle_params(...)` -> change global parameters for drawing diagrams.
- `save_graph(...)` -> save created graph (this is the function 'savefig' from the matplotlib library).

**DATA VISUALIZATION CLASSES**

**Note that** every class for drawing diagrams contains some of the above functions as its methods (for data scraping and processing)

- `g_WalterLieth(...)` -> create a WalterLieth object where data for drawing a Walter-Lieth diagram can be downloaded, modified, manually provided.

**More detailed documentation for every function, class and method is available in the cloupy's Python files**

## Future Features

- more climatological data processing functions (e.g. completing missing data)
- more climatological graphs
- **drawing maps (e.g. interpolation maps)**

## Dependencies
**Packages/libraries**:
- [Pandas](https://pandas.pydata.org) version: 1.1.4; 1.3.4 or higher
- [Matplotlib](https://matplotlib.org) version: 3.3.2; 3.4.3 or higher
- [Requests](https://requests.readthedocs.io) version: 2.24.0; 2.26.0 or higher
- [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/) version: 4.9.3 or higher
- [Numpy](https://www.numpy.org) version: 1.19.4; 1.21.4 or higher
- [Pytest](https://docs.pytest.org/en/latest/) version: 6.2.5 or higher (only for running tests)
- [Mock](http://mock.readthedocs.org/en/latest/) version: 4.0.3 or higher (only for running tests)

**Python version**: 3.8.2; 3.9.6

**OS**: Windows; Linux

All of the above versions of packages/Python have been tested. **Note that** cloupy should also be compatible with the versions between mentioned (e.g. cloupy should work fine on any Pandas version between 1.1.4 and 1.3.4; any Python version between 3.8.2 and 3.9.6). However, it has not been tested and **it is recommended to use the most recent version of the packages/libraries**. At this moment, Python versions after 3.9.6 do not compile with some of the required packages, so **Python 3.9.6 is recommended for using cloupy**.
## Running Tests

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

**Note that** the integration testing may take some time (during the process, data downloading functions are being tested, so duration depends on several factors). The process usually takes about 9-10 minutes. 

**If you want to skip data downloading tests, run the following command:**
```bash
python -m pytest -k "not downloading"
```

## Contributing

Contributions are always welcome!

See `CONTRIBUTING.md` for ways to get started.

## Support

For support, please contact me via email: kamil.grala32466@gmail.com


## License

cloupy is licensed under [MIT](https://choosealicense.com/licenses/mit/).


## Author

[@Kamil Grala](https://github.com/pdGruby)

