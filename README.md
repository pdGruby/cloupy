
# cloupy
![logo](https://i.ibb.co/X7jjYn1/logo1.png)

cloupy is a Python library for climatological data downloading, processing and visualizing. The main goal of the library is to help its author in writing a BA thesis. The library is well adapted to academic work - used data sources are reliable and graphs are easy to modify. What's more, cloupy is intuitive and really easy to use, so even users who are not related to the climatological environment should have no problems with the library usage.

## Installation

Use the git function [clone](https://git-scm.com/docs/git-clone/) to install cloupy.

```bash
# your local path to Python's libraries
cd c:/Python/Lib/site-packages
 
git clone https://github.com/pdGruby/cloupy.git
```
    
## Usage/Examples
1. Import cloupy library.
```python
import cloupy as cl
```

2. Download climatological data for a single station and for the whole country from the WMO database.
```python
single_station = cl.d_wmo_data(station_name='TOKYO', elements_to_scrape=['temp', 'preci'])
whole_country = cl.d_wmo_data(station_name='couJAPAN', elements_to_scrape=['temp', 'preci'])
```

3. Download climatological data for the station in Poznań (WMO ID: 12330) from the IMGW database and draw a Walter-Lieth diagram.
```python
wl = cl.WalterLieth(station_name='POZNAŃ')
wl.d_imgw_data(years_range=range(1966, 2020))
wl.draw()
```

4. Download data, set as global dataframe and draw a Walter-Lieth diagram based on the global dataframe.
```python
global_df = cl.d_imgw_data(
    interval='monthly', 
    stations_kind='synop', 
    years_range=range(1966, 2020)
    )
cl.set_global_df(global_df)

wl = cl.WalterLieth('WARSZAWA')
wl.import_global_df(columns_order='imgw_monthly')
wl.draw()
```

5. How does the graph look like?

![wl_warsaw](https://i.ibb.co/NYVgSCP/war.png)

6. The graph style that better fits a scientific article.
```python
cl.choose_diagStyle('retro')
wl.draw()
```
![wl_warsaw_retro](https://i.ibb.co/XjyWQ6j/war-retro.png)

## Future Features

- more climatological data processing functions (e.g. completing missing data)
- more climatological graphs
- **drawing maps (e.g. interpolation maps)**
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
- `save_graph(...)` -> save created graph (this is the function 'savefig' from the matplotlib library)

**DATA VISUALIZATION CLASSES**

**Note that** every class for drawing diagrams contains some of the above functions as its methods (for data scraping and processing)

- `g_WalterLieth()` -> create a WalterLieth object where data for drawing a Walter-Lieth diagram can be downloaded, modified, manually provided.

**More detailed documentation for every function, method and class is available in the cloupy's Python files**




## Dependencies
- [Pandas](https://pandas.pydata.org) version: 1.1.4
- [Matplotlib](https://matplotlib.org) version: 3.3.2
- [Requests](https://requests.readthedocs.io) version: 2.24.0
- [bs4](https://beautiful-soup-4.readthedocs.io/en/latest/) version: 4.9.3
- [Numpy](https://www.numpy.org) version: 1.19.4
- [Pytest](https://docs.pytest.org/en/latest/) version: 6.2.5 (only for running tests)
- [Mock](http://mock.readthedocs.org/en/latest/) version: 4.0.3 (only for running tests)

The library has been created in the **Windows 10 OS** and **Python 3.8.2**
## Running Tests

To run tests, run the following command:

```bash
# change directory to the cloupy root directory
cd c:\Python\Lib\site-packages\cloupy

python -m pytest 
```

If you want to run only unit/integration testing:

```bash
cd c:\Python\Lib\site-packages\cloupy

python -m pytest test\test_unit

python -m pytest test\test_integration
```

**Note that** the integration testing may take some time (during the process, data downloading functions are being tested, so duration depends on several factors). The process usually takes about 9-10 minutes.

## Support

If you find any bug, encounter a problem or just would like to ask a question, please contact me via email: kamil.grala32466@gmail.com


## License

cloupy is licensed under [MIT](https://choosealicense.com/licenses/mit/).


## Author

[@Kamil Grala](https://github.com/pdGruby)

