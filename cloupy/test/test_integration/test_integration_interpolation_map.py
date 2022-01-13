import cloupy as cl
from cloupy.maps.interpolation_map import MapInterpolation
import pytest
import urllib.request
import urllib.error


def check_if_NOT_connected_to_the_internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return False
    except urllib.error.URLError:
        return True


@pytest.mark.skipif(check_if_NOT_connected_to_the_internet(), reason='internet connection required')
class TestDrawingWithDownloadedData:
    figures_plotted = 0

    def test_drawing_and_imgw_data_downloading(self):
        plotted_figures_before = TestDrawingWithDownloadedData.figures_plotted

        imap = MapInterpolation('POLAND')
        imap.d_imgw_data(range(2010, 2011), 'temp')
        imap.draw(figsize=(1, 1))
        TestDrawingWithDownloadedData.figures_plotted += 1

        plotted_figures_after = TestDrawingWithDownloadedData.figures_plotted
        assert plotted_figures_before < plotted_figures_after

    def test_drawing_and_wmo_data_downloading(self):
        plotted_figures_before = TestDrawingWithDownloadedData.figures_plotted

        imap = MapInterpolation('HUNGARY')
        imap.d_wmo_data('couHUNGARY', 'preci')
        imap.draw(figsize=(1, 1))
        TestDrawingWithDownloadedData.figures_plotted += 1

        plotted_figures_after = TestDrawingWithDownloadedData.figures_plotted
        assert plotted_figures_before < plotted_figures_after

    def test_daily_data_downloading_and_drawing_from_global_df(self):
        plotted_figures_before = TestDrawingWithDownloadedData.figures_plotted

        df = cl.d_imgw_data('daily', 'synop', range(2012, 2013), return_coordinates=True)
        cl.set_global_df(df)

        imap = MapInterpolation('POLAND')
        imap.import_global_df([1, 9, -3, -2])
        imap.draw(figsize=(1, 1))
        TestDrawingWithDownloadedData.figures_plotted += 1

        plotted_figures_after = TestDrawingWithDownloadedData.figures_plotted
        assert plotted_figures_before < plotted_figures_after
