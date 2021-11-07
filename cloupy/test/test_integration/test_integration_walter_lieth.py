import cloupy as cl
import pytest
import matplotlib.pyplot as plt
import os
import urllib.request
import urllib.error


def check_if_NOT_connected_to_the_internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return False
    except urllib.error.URLError:
        return True


@pytest.mark.skipif(check_if_NOT_connected_to_the_internet(), reason='internet connection required')
class TestDrawingWithDailyData:

    @pytest.fixture
    def path_for_saving(self):
        return str(__file__).replace('test_integration_walter_lieth.py', 'check_size.jpg')

    def test_drawing_and_daily_data_downloading(
            self, path_for_saving
    ):
        wl = cl.g_WalterLieth('POZNAŃ')
        wl.d_imgw_data(interval='daily', stations_kind='synop', years_range=range(2010, 2011))
        wl.draw()

        plt.savefig(path_for_saving, dpi=100)
        size = os.path.getsize(path_for_saving)
        assert size == 126632
        os.remove(path_for_saving)

    def test_drawing_from_global_df(
            self, path_for_saving
    ):
        data = cl.d_imgw_data('daily', 'synop', range(2010, 2011))
        cl.set_global_df(data)

        assert TestDrawingWithDailyData.draw_and_return_file_size('WARSZAWA') == 124133
        assert TestDrawingWithDailyData.draw_and_return_file_size('KOŁOBRZEG') == 124260
        assert TestDrawingWithDailyData.draw_and_return_file_size('KOŁO') == 120510
        assert TestDrawingWithDailyData.draw_and_return_file_size('PIŁA') == 124977
        assert TestDrawingWithDailyData.draw_and_return_file_size('CHOJNICE') == 125360
        assert TestDrawingWithDailyData.draw_and_return_file_size('BIAŁYSTOK') == 115133
        assert TestDrawingWithDailyData.draw_and_return_file_size('KATOWICE') == 125708

        os.remove(path_for_saving)

    @staticmethod
    def draw_and_return_file_size(station_name):
        wl = cl.g_WalterLieth(station_name)
        wl.import_global_df('imgw_daily')
        wl.draw()

        path_for_saving = str(__file__).replace('test_integration_walter_lieth.py', 'check_size.jpg')
        plt.savefig(path_for_saving, dpi=100)
        size = os.path.getsize(path_for_saving)
        return size
