from cloupy.diagrams.walter_lieth import WalterLieth
import pytest
import pandas as pd
import matplotlib.pyplot as plt
import os


class TestDrawing:

    @pytest.fixture
    def data_for_humid_period(self):
        return pd.DataFrame(
            {
                'months': {
                    0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10,
                    10: 11, 11: 12
                },
                'temp': {
                    0: -1.36, 1: -0.59, 2: 3.03, 3: 8.35, 4: 13.55, 5: 17.02, 6: 18.64,
                    7: 18.07, 8: 13.76, 9: 8.82, 10: 3.87, 11: 0.36
                },
                'preci': {
                    0: 32.70, 1: 26.76, 2: 31.40, 3: 33.63, 4: 51.10, 5: 61.09,
                    6: 79.37, 7: 57.99, 8: 42.59, 9: 37.12, 10: 37.18, 11: 38.74
                },
                'temp_max': {
                    0: 5.45, 1: 6.79, 2: 13.54, 3: 20.07, 4: 24.67, 5: 28.25, 6: 29.65,
                    7: 29.21, 8: 25.24, 9: 18.88, 10: 11.63, 11: 7.66
                },
                'temp_min': {
                    0: -11.22, 1: -10.60, 2: -6.38, 3: -1.66, 4: 2.95, 5: 6.77, 6: 9.38,
                    7: 8.72, 8: 4.23, 9: 0.31, 10: -3.72, 11: -8.56
                }
            }
        )

    @pytest.fixture
    def default_settings(self):
        return {
            'figsize': (7.74, 7.74), 'language': None, 'freeze_rectangles': True,
            'title_text': True, 'years_text': True, 'coordinates_box': True,
            'yearly_means_box': True, 'extremes_box': True, 'legend_box': True
        }

    @pytest.fixture
    def opposite_settings(self):
        return {
            'figsize': (7.74, 7.74), 'language': 'POL', 'freeze_rectangles': False,
            'title_text': False, 'years_text': False, 'coordinates_box': False,
            'yearly_means_box': False, 'extremes_box': False, 'legend_box': False
        }

    @pytest.fixture
    def path_for_saving(self):
        return str(__file__).replace('test_unittest_walter_lieth.py', 'check_size.jpg')

    def test_humid_period_and_elements_viewing(
            self, default_settings, opposite_settings,
            data_for_humid_period, path_for_saving
    ):
        valid_bytes = {
            0: 105374, 1: 112557, 2: 100299, 3: 93739, 4: 93467, 5: 86343,
            6: 82451, 7: 80671, 8: 73267
        }
        index = 0
        for setting, value in opposite_settings.items():
            default_settings[setting] = value

            wl = WalterLieth(
                'POZNAŃ', dataframe=data_for_humid_period, years_range=range(1951, 2020),
                lat=52.42, lon=16.83, elevation=92
            )
            wl.draw(
                figsize=default_settings['figsize'], language=default_settings['language'],
                freeze_rectangles=default_settings['freeze_rectangles'], title_text=default_settings['title_text'],
                years_text=default_settings['years_text'], coordinates_box=default_settings['coordinates_box'],
                yearly_means_box=default_settings['yearly_means_box'], extremes_box=default_settings['extremes_box'],
                legend_box=default_settings['legend_box']
            )

            plt.savefig(path_for_saving, dpi=100)
            size = os.path.getsize(path_for_saving)
            assert size == valid_bytes[index]
            index += 1
        os.remove(path_for_saving)

    def test_dry_period(
            self, data_for_humid_period, path_for_saving
    ):
        data_for_dry_period = data_for_humid_period
        data_for_dry_period.preci = [0] * 12

        wl = WalterLieth(
            'POZNAŃ', dataframe=data_for_dry_period, years_range=range(1951, 2020),
            lat=52.42, lon=16.83, elevation=92
        )
        wl.draw()

        plt.savefig(path_for_saving, dpi=100)
        size = os.path.getsize(path_for_saving)
        assert size == 113968
        os.remove(path_for_saving)

    def test_mixed_all_periods(
            self, data_for_humid_period, path_for_saving
    ):
        data_for_mixed_periods = data_for_humid_period
        data_for_mixed_periods['preci'] = [110, 70, 50, 40, 30, 20, 0, 0, 20, 30, 70, 110]

        wl = WalterLieth(
            'POZNAŃ', dataframe=data_for_mixed_periods, years_range=range(1951, 2020),
            lat=52.42, lon=16.83, elevation=92
        )
        wl.draw()

        plt.savefig(path_for_saving, dpi=100)
        size = os.path.getsize(path_for_saving)
        assert size == 131139
        os.remove(path_for_saving)
