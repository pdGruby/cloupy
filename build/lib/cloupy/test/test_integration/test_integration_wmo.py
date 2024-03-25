import pytest
from cloupy.scraping import wmo
import mock
import builtins
from random import shuffle
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
    def stations(self):
        return ['POZNAN', 'PERTH', 'HARARE', 'PARIS', 'BARCELONA', 'QUITO']

    @pytest.fixture
    def input_dict(self):
        return {
            'BARCELONA': '0',
            'PERTH': '1',
            'HARARE': '1',
            'QUITO': '1',
            'PARIS': '3'
        }

    @pytest.fixture
    def elements(self):
        return ['temp', 'preci', 'temp_max', 'temp_min', 'sl_press']

    def test_default_settings(
            self, stations, elements,
            input_dict
    ):
        for station in stations:
            shuffle(elements)
            if station != 'POZNAN':
                with mock.patch.object(builtins, 'input', lambda _: input_dict[station]):
                    data = wmo.download_wmo_climatological_data(station, elements)
                    assert not data.empty
                    assert TestDataDownloading.check_if_columns_in_proper_order(
                        list(data.columns[3:]), elements
                    )
                    for column in data.columns:
                        assert not data[column].isnull().all()
            else:
                data = wmo.download_wmo_climatological_data(station, elements)
                assert not data.empty
                assert TestDataDownloading.check_if_columns_in_proper_order(
                    list(data.columns[3:]), elements
                )
                for column in data.columns:
                    assert not data[column].isnull().all()

    def test_return_coordinates_arg(
            self, stations, elements,
            input_dict
    ):
        for station in stations:
            if station != 'POZNAN':
                with mock.patch.object(builtins, 'input', lambda _: input_dict[station]):
                    data = wmo.download_wmo_climatological_data(
                        station, elements, return_coordinates=True
                    )
                    assert list(data.columns[-1:-4:-1]) == ['elv', 'lat', 'lon']
                    for element in ['lat', 'lon', 'elv']:
                        assert not data[element].isnull().any()
            else:
                data = wmo.download_wmo_climatological_data(
                    station, elements, return_coordinates=True
                )
                assert list(data.columns[-1:-4:-1]) == ['elv', 'lat', 'lon']
                for element in ['lat', 'lon', 'elv']:
                    assert not data[element].isnull().any()

    def test_nearby_stations_arg(
            self, elements
    ):
        stations_and_input_val = {
            'PARIS': '4',
            'NEW YORK': '1',
            'MADRID': '1',
            'KOLO': '1'
        }

        for station, input_val in stations_and_input_val.items():
            with mock.patch.object(builtins, 'input', lambda _: input_val):
                if station == 'KOLO':
                    data = wmo.download_wmo_climatological_data(
                        station, elements, nearby_stations=True,
                        degrees_range_for_nearby_stations=1
                    )
                else:
                    data = wmo.download_wmo_climatological_data(station, elements, nearby_stations=True)
                assert list(data.columns[3:]) == elements
                assert TestDataDownloading.check_if_columns_in_proper_order(
                    list(data.columns[3:]), elements
                )

    def test_downloading_for_countries(
            self, elements
    ):
        countries = [
            'couICELAND', 'couCONGO', 'couVENEZUELA',
            'couPARAGUAY', 'couURUGUAY', 'couCUBA'
        ]

        for country in countries:
            shuffle(elements)
            data = wmo.download_wmo_climatological_data(country, elements)

            for column in data.columns:
                assert not data[column].isnull().all()
            assert list(data.columns)[3:] == elements

    @staticmethod
    def check_if_columns_in_proper_order(
            columns, elements_
    ):
        filtered_elements = []
        for element in elements_:
            if element in columns:
                filtered_elements.append(element)

        if columns == filtered_elements:
            return True
        else:
            return False
