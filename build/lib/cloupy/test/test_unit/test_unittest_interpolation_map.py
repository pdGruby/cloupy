from cloupy.maps.interpolation_map import MapInterpolation
import pytest
import pandas as pd
import numpy as np
from random import shuffle


class TestDrawing:

    figures_plotted = 0

    @pytest.fixture
    def data_for_poland(self):
        return pd.DataFrame(
            {
                'values': [7.9, 7.6, 7.4, 8.0, 8.6, 7.7, 8.4],
                'longitude': [19.4, 18.6, 16.2, 19.8, 14.6, 21.0, 16.9],
                'latitude': [54.2, 54.4, 54.2, 50.1, 53.4, 52.2, 51.1]
            }
        )

    @pytest.fixture
    def available_drawing_settings(self):
        return {
            'levels': [np.arange(5, 12.5, 0.5), np.arange(5, 13, 1)],
            'cmap': ['jet', 'turbo', 'Reds', 'Blues'],
            'fill_contours': [True, False],
            'show_contours': [True, False],
            'show_clabels': [True, False],
            'show_cbar': [True, False],
            'show_grid': [True, False],
            'show_frame': [True, False],
            'show_coordinates': [True, False],
            'show_ticks': [True, False],
            'title': [None, 'TITLE TEST'],
            'title_bold': [True, False],
            'title_x_position': list(np.arange(0, 1, 0.1)),
            'title_y_position': list(np.arange(0, 1, 0.1)),
            'title_ha': ['left', 'right', 'center'],
            'xlabel': [None, 'XLABEL TEST'],
            'xlabel_bold': [True, False],
            'ylabel': [None, 'YLABEL TEST'],
            'ylabel_bold': [True, False],
            'text_size': [10, 8, 6, 4],
            'numcols': [120, 240, 360, 480],
            'numrows': [120, 240, 360, 480],
            'interpolation_method': ['cubic', 'linear', 'nearest'],
            'interpolation_within_levels': [True, False],
            'extrapolation_into_zoomed_area': [True, False],
            'contours_levels': [None, [5, 6, 7, 8, 9, 10, 11, 12]],
            'clabels_levels': [None, [7, 8, 9]],
            'clabels_add': [None, [(19, 50), (22, 53)]],
            'clabels_decimal_place': [0, 1, 2],
            'clabels_inline_spacing': [-3, 0, 3],
            'xticks': [None, [16, 17, 18], [19, 20, 21]],
            'yticks': [None, [48, 49, 50], [51, 52, 52]],
            'cbar_ticks': [None, [5, 6, 7], [9, 6, 10]],
            'cbar_title': [None, 'CBAR TITLE TEST'],
            'cbar_title_bold': [True, False],
            'cbar_labelpad': [10, 0, 20],
            'cbar_position': ['top', 'bottom', 'left', 'right'],
            'cbar_pad': [0.1, 0.02, 0.05],
            'zoom_in': [None, [(14, 17), (52.5, 54.8)], [(17.5, 21.5), (50.5, 52.5)]],
            'show_points': [True, False],
            'points_labels': [None, 'ids', 'values'],
            'boundaries_lw': [1, 2, 0.5],
            'boundaries_ls': ['dotted', 'solid', 'dashed'],
            'grid_lw': [0.1, 0.2, 0.3],
            'grid_ls': ['dashed', 'dotted', 'solid', 'dashdot'],
            'figsize': [(1, 1)]
        }

    def test_default_drawing(self, data_for_poland):
        plotted_figures_before = TestDrawing.figures_plotted

        imap = MapInterpolation('POLAND', dataframe=data_for_poland)
        imap.draw()
        TestDrawing.figures_plotted += 1

        plotted_figures_after = TestDrawing.figures_plotted
        assert plotted_figures_before < plotted_figures_after

    def test_nondefault_drawing(self, data_for_poland, available_drawing_settings):
        for i in range(5):
            plotted_figures_before = TestDrawing.figures_plotted

            args = TestDrawing.mix_available_settings(available_drawing_settings)
            imap = MapInterpolation('POL', dataframe=data_for_poland)
            imap.draw(**args)
            TestDrawing.figures_plotted += 1

            plotted_figures_after = TestDrawing.figures_plotted
            assert plotted_figures_before < plotted_figures_after

    @staticmethod
    def mix_available_settings(available_drawing_settings):
        args = {}
        for arg, values in available_drawing_settings.items():
            shuffle(values)
            args[arg] = values[0]

        return args
