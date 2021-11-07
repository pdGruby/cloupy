import cloupy as cl
import pytest
import matplotlib.pyplot as plt
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

    def test_drawing_and_daily_data_downloading(self):
        plotted_figures_before = plt.gcf().number
        wl = cl.g_WalterLieth('POZNAŃ')
        wl.d_imgw_data(interval='daily', stations_kind='synop', years_range=range(2010, 2011))
        wl.draw()
        plotted_figures_after = plt.gcf().number

        assert plotted_figures_before < plotted_figures_after

    def test_daily_data_downloading_and_drawing_from_global_df(self):
        data = cl.d_imgw_data('daily', 'synop', range(2010, 2011))
        cl.set_global_df(data)

        plotted_figures_before = plt.gcf().number
        assert TestDrawingWithDailyData.draw_from_global_df('WARSZAWA') > plotted_figures_before

        plotted_figures_before = plt.gcf().number
        assert TestDrawingWithDailyData.draw_from_global_df('KOŁOBRZEG') > plotted_figures_before

        plotted_figures_before = plt.gcf().number
        assert TestDrawingWithDailyData.draw_from_global_df('KOŁO') > plotted_figures_before

    @staticmethod
    def draw_from_global_df(station_name):
        wl = cl.g_WalterLieth(station_name)
        wl.import_global_df('imgw_daily')
        wl.draw()
        return plt.gcf().number
