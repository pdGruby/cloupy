import pytest
import cloupy.maps.draw_shapes as ds
import matplotlib.pyplot as plt
import os


class TestShapesDrawing:
    figures_plotted = 0

    @pytest.fixture
    def path(self):
        sep = os.sep
        path = str(__file__).replace(
            f'{sep}test{sep}test_unit{sep}test_unittest_drawing_shapes.py',
            f'{sep}maps{sep}world{sep}ne_50m_admin_0_countries.shp'
        )
        return path

    def test_drawing_additional_shapes(self, path):
        plotted_figures_before = TestShapesDrawing.figures_plotted
        fig, ax = plt.subplots(figsize=(1, 1))
        ds.draw_additional_shapes({path: ''}, ax)
        TestShapesDrawing.figures_plotted += 1
        plotted_figures_after = TestShapesDrawing.figures_plotted
        assert plotted_figures_before < plotted_figures_after

        plotted_figures_before = TestShapesDrawing.figures_plotted
        fig, ax = plt.subplots(figsize=(1, 1))
        ds.draw_additional_shapes(
            {
                path: 'ls=dotted,lw=2,fc=red,c=blue,crs=epsg:4326'
            },
            ax
        )
        TestShapesDrawing.figures_plotted += 1
        plotted_figures_after = TestShapesDrawing.figures_plotted
        assert plotted_figures_before < plotted_figures_after

    def test_getting_shapes_for_plotting(self, path):
        fig, ax = plt.subplots(figsize=(1, 1))
        shapes = ds.get_shapes_for_plotting(ax, path, 'epsg:4326', 'MALTA')

        assert shapes == [([14.566210937500017,
                            14.53271484375,
                            14.436425781250023,
                            14.352343750000017,
                            14.351269531250011,
                            14.448339843750006,
                            14.537011718750023,
                            14.566210937500017],
                           [35.852734375,
                            35.820214843749994,
                            35.821679687499994,
                            35.872265625,
                            35.978417968749994,
                            35.957421874999994,
                            35.886279296874996,
                            35.852734375]),
                          ([14.3134765625,
                            14.253613281250011,
                            14.194238281250023,
                            14.180371093750011,
                            14.263281250000006,
                            14.3037109375,
                            14.320898437500006,
                            14.3134765625],
                           [36.027587890625,
                            36.012158203125,
                            36.042236328125,
                            36.060400390625,
                            36.07578125,
                            36.062304687499996,
                            36.03623046875,
                            36.027587890625]),
                          ([14.566210937500017,
                            14.53271484375,
                            14.436425781250023,
                            14.352343750000017,
                            14.351269531250011,
                            14.448339843750006,
                            14.537011718750023,
                            14.566210937500017],
                           [35.852734375,
                            35.820214843749994,
                            35.821679687499994,
                            35.872265625,
                            35.978417968749994,
                            35.957421874999994,
                            35.886279296874996,
                            35.852734375]),
                          ([14.3134765625,
                            14.253613281250011,
                            14.194238281250023,
                            14.180371093750011,
                            14.263281250000006,
                            14.3037109375,
                            14.320898437500006,
                            14.3134765625],
                           [36.027587890625,
                            36.012158203125,
                            36.042236328125,
                            36.060400390625,
                            36.07578125,
                            36.062304687499996,
                            36.03623046875,
                            36.027587890625])]
