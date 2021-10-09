import pytest
import cloudy.scraping.imgw as imgw
import urllib.request
import urllib.error


def check_if_NOT_connected_to_the_internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return False
    except urllib.error.URLError:
        return True


@pytest.mark.skipif(check_if_NOT_connected_to_the_internet(), reason='internet connection required')
class TestDataDownloading:

    @pytest.fixture
    def periods(self):
        return ['monthly', 'daily', 'prompt']

    @pytest.fixture
    def st_kinds(self):
        return ['synop', 'climat', 'fall']

    @pytest.mark.filterwarnings("ignore::pandas.errors.DtypeWarning")
    def test_if_column_2_is_always_year(
            self, periods, st_kinds
    ):

        from os import listdir
        from os.path import isfile, join
        import shutil
        from random import shuffle

        y_range = range(2018, 2019)
        files_reading_dir_path = str(__file__).replace(
            'test\\test_integration\\test_integration_imgw.py', 'scraping\\files_reading_folder'
        )

        for period in periods:
            for st_kind in st_kinds:

                if st_kind == 'fall' and period == 'prompt':
                    continue

                urls = imgw.get_urls(period, st_kind, y_range)
                imgw.download_data(urls)
                downloaded_files_names = [f for f in listdir(files_reading_dir_path) if
                                          isfile(join(files_reading_dir_path, f))]

                file_formats = imgw.get_file_formats(period, st_kind, 'all')
                keywords = ['nazwa stacji', 'temperatura', 'rok', 'opad', 'wiatr']
                shuffle(keywords)

                for file in file_formats:

                    if isinstance(file_formats, str):
                        file = file_formats

                    df = imgw.concatenate_data(
                        downloaded_files_names=downloaded_files_names, file_formats=file, years_range=y_range,
                        keywords=keywords, specific_columns=None, optimize_memory_usage=False,
                        merge_splitted_stations=True
                    )

                    df = df[0][df[1]]

                    assert min(df[2]) == 2018

                shutil.rmtree(files_reading_dir_path)

    @pytest.mark.filterwarnings("ignore::pandas.errors.DtypeWarning")
    def test_data_downloading_for_years_before_2001(
            self, periods, st_kinds
    ):
        years_range = range(1984, 1987)
        TestDataDownloading.download_and_test_data(periods, st_kinds, years_range)

    @pytest.mark.filterwarnings("ignore::pandas.errors.DtypeWarning")
    def test_data_downloading_for_years_after_2000(
            self, periods, st_kinds
    ):
        years_range = range(2011, 2013)
        TestDataDownloading.download_and_test_data(periods, st_kinds, years_range)

    @pytest.mark.filterwarnings("ignore::pandas.errors.DtypeWarning")
    def test_data_downloading_for_years_between_2000_and_2001(
            self, periods, st_kinds
    ):
        years_range = range(2000, 2002)
        TestDataDownloading.download_and_test_data(periods, st_kinds, years_range)

    @pytest.mark.filterwarnings("ignore::pandas.errors.DtypeWarning")
    def test_adding_coordinates_to_dataframe(
            self, periods, st_kinds
    ):
        years_range = range(2010, 2011)
        for period in periods:
            for st_kind in st_kinds:

                if st_kind == 'fall' and period == 'prompt':
                    continue

                df = imgw.get_meteorological_data(
                    period, st_kind, years_range,
                    specific_columns=[0, 1, 2, 3],
                    optimize_memory_usage=True,
                    return_coordinates=True
                )

                assert 'lat' in df.columns
                assert 'lon' in df.columns
                assert 'elv' in df.columns

                assert not df['lat'].isnull().all()
                assert not df['lon'].isnull().all()
                assert not df['elv'].isnull().all()

    @staticmethod
    def download_and_test_data(
            periods, st_kinds, years_range
    ):
        for period in periods:
            for st_kind in st_kinds:
                if period == 'prompt' and st_kind == 'fall':
                    with pytest.raises(NotADirectoryError):
                        imgw.get_meteorological_data(
                            period, st_kind, years_range
                        )
                        continue
                else:
                    df = imgw.get_meteorological_data(
                        period, st_kind, years_range,
                        optimize_memory_usage=True,
                        specific_columns=[0, 1, 2, 3]
                    )

                assert not df.empty
