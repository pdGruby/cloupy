from scraping import wmo
import pytest
import mock
import builtins


class TestReturningWmoidOrCoord:
    def test_default_returning_wmoid(self):
        with mock.patch.object(builtins, 'input', lambda _: '3'):
            assert wmo.return_wmoid_or_coord('PARIS', 'wmo_id') == {'PARIS/LE BOURGET': '7150'}

        with mock.patch.object(builtins, 'input', lambda _: '1'):
            assert wmo.return_wmoid_or_coord('LONDON', 'wmo_id') == {'LONDON A': '71623.3'}

        with mock.patch.object(builtins, 'input', lambda _: '0'):
            assert wmo.return_wmoid_or_coord('LAS VEGAS', 'wmo_id') == {'LAS VEGAS WWTP': '294.862'}

        with mock.patch.object(builtins, 'input', lambda _: '1'):
            assert wmo.return_wmoid_or_coord('SYDNEY', 'wmo_id') == {'SYDNEY AIRPOR': '94767'}

        with mock.patch.object(builtins, 'input', lambda _: '-1'):
            assert wmo.return_wmoid_or_coord('BERLIN', 'wmo_id') == {'BERLIN-TEMPEL': '10384'}

        with mock.patch.object(builtins, 'input', lambda _: '0'):
            assert wmo.return_wmoid_or_coord('QUITO', 'wmo_id') == {'QUITO/MARISCA': '84071'}

    def test_default_returning_coords(self):
        assert wmo.return_wmoid_or_coord('BUENOS AIRES', 'lat') == {'BUENOS AIRES': -34.58}

        assert wmo.return_wmoid_or_coord('CAPETOWN', 'lat') == {'CAPETOWN': -33.9}

        with mock.patch.object(builtins, 'input', lambda _: '0'):
            assert wmo.return_wmoid_or_coord('CAIR', 'lon') == {'CAIRO AIRPORT': 31.4}

        assert wmo.return_wmoid_or_coord('MURMANSK', 'lon') == {'MURMANSK': 33.05}

        assert wmo.return_wmoid_or_coord('TOKYO', 'elv') == {'TOKYO': 36.0}

        with mock.patch.object(builtins, 'input', lambda _: '5'):
            assert wmo.return_wmoid_or_coord('SRI', 'elv') == {'DIYATALAWA, SRI': 1248.0}

    def test_contains_station_name_arg(self):
        assert wmo.return_wmoid_or_coord(
            'PARIS', 'elv', contains_station_name=False
        ) == {'PARIS': 165.2}

        with pytest.raises(AttributeError):
            wmo.return_wmoid_or_coord('LAS VEGAS', 'elv', contains_station_name=False)

        assert wmo.return_wmoid_or_coord(
            'SIDNEY', 'lon', contains_station_name=False
        ) == {'SIDNEY': -84.2}

        assert wmo.return_wmoid_or_coord(
            'DIYATALAWA, SRI', 'lon', contains_station_name=False
        ) == {'DIYATALAWA, SRI': 81.0}

        assert wmo.return_wmoid_or_coord(
            'POZNAN', 'wmo_id', contains_station_name=False
        ) == {'POZNAN': '12330'}

        assert wmo.return_wmoid_or_coord(
            'KOLO', 'wmo_id', contains_station_name=False
        ) == {'KOLO': '12345'}

    def test_station_name_is_wmo_id_arg(self):
        assert wmo.return_wmoid_or_coord(
            80419, 'elv', station_name_is_wmo_id=True
        ) == {'BARCELONA': 7.0}

        assert wmo.return_wmoid_or_coord(
            67775, 'elv', station_name_is_wmo_id=True
        ) == {'HARARE': 1480.0}

        assert wmo.return_wmoid_or_coord(
            72386, 'lon', station_name_is_wmo_id=True
        ) == {'LAS VEGAS/MCC': -115.17}

        assert wmo.return_wmoid_or_coord(
            10763, 'lon', station_name_is_wmo_id=True
        ) == {'NUERNBERG': 11.05}

        assert wmo.return_wmoid_or_coord(
            '8220.1', 'lat', station_name_is_wmo_id=True
        ) == {'MADRID/RETIRO': 40.4}

        assert wmo.return_wmoid_or_coord(
            '325.220', 'lat', station_name_is_wmo_id=True
        ) == {'LISBON': 46.45}


class TestDataDecoderAndTransposingTable:
    def test_wmo_data_decoding_and_table_transposing(self):
        data = str(
            """
            # climexp_url :: https://climexp.knmi.nl/gettempall.cgi?WMO=12330
            # scripturl01 :: http://climexp.knmi.nl/gettempall.cgi?STATION=POZNAN&WMO=12330&id=$id
            # tavg [Celsius] daily mean temperature (unadjusted) from GHCN-M v3.3.0.20190817
            1951   -0.9    0.4    0.7    7.9   11.8   17.8   18.3   19.5   14.8    6.8    6.5    2.5
            1952    0.4   -0.2   -1.2   10.3   11.7   15.6   18.1   18.6   11.5    6.7    1.8   -1.9
            1953   -1.4   -1.1    3.6   10.0   13.7   19.3   19.7   16.8   13.7   10.6    3.7    0.3
            1954   -5.7   -8.2    2.2    5.3   13.8   19.0   16.2   17.5   14.6    9.0    2.5    2.7
            1955   -3.5   -3.3   -0.7    5.4   11.0   15.5   18.7   18.7   14.4    8.0    3.4    1.5
            """
        )

        decoded_data = wmo.downloaded_data_decoder(data)
        assert decoded_data == [
            ['1951', '-0.9', '0.4', '0.7', '7.9', '11.8', '17.8', '18.3', '19.5', '14.8', '6.8', '6.5', '2.5'],
            ['1952', '0.4', '-0.2', '-1.2', '10.3', '11.7', '15.6', '18.1', '18.6', '11.5', '6.7', '1.8', '-1.9'],
            ['1953', '-1.4', '-1.1', '3.6', '10.0', '13.7', '19.3', '19.7', '16.8', '13.7', '10.6', '3.7', '0.3'],
            ['1954', '-5.7', '-8.2', '2.2', '5.3', '13.8', '19.0', '16.2', '17.5', '14.6', '9.0', '2.5', '2.7'],
            ['1955', '-3.5', '-3.3', '-0.7', '5.4', '11.0', '15.5', '18.7', '18.7', '14.4', '8.0', '3.4', '1.5']
        ]

        transposed_table = wmo.transpose_table(decoded_data)
        assert transposed_table == [
            ['1951', 1, '-0.9'], ['1951', 2, '0.4'], ['1951', 3, '0.7'], ['1951', 4, '7.9'],
            ['1951', 5, '11.8'], ['1951', 6, '17.8'], ['1951', 7, '18.3'], ['1951', 8, '19.5'],
            ['1951', 9, '14.8'], ['1951', 10, '6.8'], ['1951', 11, '6.5'], ['1951', 12, '2.5'],
            ['1952', 1, '0.4'], ['1952', 2, '-0.2'], ['1952', 3, '-1.2'], ['1952', 4, '10.3'],
            ['1952', 5, '11.7'], ['1952', 6, '15.6'], ['1952', 7, '18.1'], ['1952', 8, '18.6'],
            ['1952', 9, '11.5'], ['1952', 10, '6.7'], ['1952', 11, '1.8'], ['1952', 12, '-1.9'],
            ['1953', 1, '-1.4'], ['1953', 2, '-1.1'], ['1953', 3, '3.6'], ['1953', 4, '10.0'],
            ['1953', 5, '13.7'], ['1953', 6, '19.3'], ['1953', 7, '19.7'], ['1953', 8, '16.8'],
            ['1953', 9, '13.7'], ['1953', 10, '10.6'], ['1953', 11, '3.7'], ['1953', 12, '0.3'],
            ['1954', 1, '-5.7'], ['1954', 2, '-8.2'], ['1954', 3, '2.2'], ['1954', 4, '5.3'],
            ['1954', 5, '13.8'], ['1954', 6, '19.0'], ['1954', 7, '16.2'], ['1954', 8, '17.5'],
            ['1954', 9, '14.6'], ['1954', 10, '9.0'], ['1954', 11, '2.5'], ['1954', 12, '2.7'],
            ['1955', 1, '-3.5'], ['1955', 2, '-3.3'], ['1955', 3, '-0.7'], ['1955', 4, '5.4'],
            ['1955', 5, '11.0'], ['1955', 6, '15.5'], ['1955', 7, '18.7'], ['1955', 8, '18.7'],
            ['1955', 9, '14.4'], ['1955', 10, '8.0'], ['1955', 11, '3.4'], ['1955', 12, '1.5']
        ]


class TestLookingForTheNearestStation:
    def test_default_settings(self):
        assert wmo.look_for_the_nearest_station(
            lat=50, lon=-100
        ).to_dict() == {
            'country': {2431: 'CANADA', 2432: 'CANADA', 2434: 'CANADA'},
            'station': {2431: 'BRANDON, MAN.', 2432: 'ST ALBANS', 2434: 'MINNEDOSA, MA'},
            'wmo_id': {2431: '71140', 2432: '71140.1', 2434: '71140.3'},
            'lat': {2431: 49.92, 2432: 49.7, 2434: 50.27},
            'lon': {2431: -99.95, 2432: -99.6, 2434: -99.83},
            'elv': {2431: 409.0, 2432: 360.0, 2434: 521.0}
                        }

    def test_other_degrees_range_arg(self):
        assert wmo.look_for_the_nearest_station(
            lat=45.9, lon=103.2, degrees_range=1
        ).to_dict() == {
            'country': {1507: 'MONGOLIA', 1527: 'MONGOLIA'},
            'station': {1507: 'ARVAIHEER', 1527: 'SAIKHAN-OVOO'},
            'wmo_id': {1507: '44288', 1527: '44336'},
            'lat': {1507: 46.27, 1527: 45.45},
            'lon': {1507: 102.78, 1527: 103.9},
            'elv': {1507: 1813.0, 1527: 1316.0}
                        }


class TestConcatenatingDataframes:
    def test_concatenating(self):
        data = [
             [['year', 'month', 'temp'], ['2017', 1, '-2.2'],
              ['2017', 2, '0.6'], ['2017', 3, '6.8'], ['2017', 4, '7.7'],
              ['2017', 5, '14.2'], ['2017', 6, '18.1'], ['2017', 7, '18.6'],
              ['2017', 8, '19.2'], ['2017', 9, '13.7'], ['2017', 10, '11.0'],
              ['2017', 11, '5.5'], ['2017', 12, '2.9'], ['2018', 1, '2.2'],
              ['2018', 2, '-2.6'], ['2018', 3, '1.1'], ['2018', 4, '13.1'],
              ['2018', 5, '17.9'], ['2018', 6, '19.4'], ['2018', 7, '20.9'],
              ['2018', 8, '21.7'], ['2018', 9, '16.0'], ['2018', 10, '11.0'],
              ['2018', 11, '5.2'], ['2018', 12, '2.8'], ['2019', 1, '-0.2'],
              ['2019', 2, '3.4'], ['2019', 3, '6.4'], ['2019', 4, '10.9'],
              ['2019', 5, '12.4'], ['2019', 6, '23.3'], ['2019', 7, '2'],
              ['2019', 8, '2'], ['2019', 9, '2'], ['2019', 10, '2'],
              ['2019', 11, '2'], ['2019', 12, '2']],
             [['year', 'month', 'temp'], ['2017', 1, '-2.2'],
              ['2017', 2, '0.6'], ['2017', 3, '6.8'], ['2017', 4, '7.7'],
              ['2017', 5, '14.2'], ['2017', 6, '18.1'], ['2017', 7, '18.6'],
              ['2017', 8, '19.2'], ['2017', 9, '13.7'], ['2017', 10, '11.0'],
              ['2017', 11, '5.5'], ['2017', 12, '2.9'], ['2018', 1, '2.2'],
              ['2018', 2, '-2.6'], ['2018', 3, '1.1'], ['2018', 4, '13.1'],
              ['2018', 5, '17.9'], ['2018', 6, '19.4'], ['2018', 7, '20.9'],
              ['2018', 8, '21.7'], ['2018', 9, '16.0'], ['2018', 10, '11.0'],
              ['2018', 11, '5.2'], ['2018', 12, '2.8'], ['2019', 1, '-0.2'],
              ['2019', 2, '3.4'], ['2019', 3, '6.4'], ['2019', 4, '10.9'],
              ['2019', 5, '12.4'], ['2019', 6, '23.3'], ['2019', 7, '2'],
              ['2019', 8, '2'], ['2019', 9, '2'], ['2019', 10, '2'],
              ['2019', 11, '2'], ['2019', 12, '2']]
             ]

        concatenated_data = wmo.concatenate_dfs(data)
        assert concatenated_data.to_dict() == {
            'year': {0: 2017, 1: 2017, 2: 2017, 3: 2017, 4: 2017, 5: 2017,
                     6: 2017, 7: 2017, 8: 2017, 9: 2017, 10: 2017, 11: 2017,
                     12: 2018, 13: 2018, 14: 2018, 15: 2018, 16: 2018, 17: 2018,
                     18: 2018, 19: 2018, 20: 2018, 21: 2018, 22: 2018, 23: 2018,
                     24: 2019, 25: 2019, 26: 2019, 27: 2019, 28: 2019, 29: 2019,
                     30: 2019, 31: 2019, 32: 2019, 33: 2019, 34: 2019, 35: 2019},
            'month': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10,
                      10: 11, 11: 12, 12: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6,
                      18: 7, 19: 8, 20: 9, 21: 10, 22: 11, 23: 12, 24: 1, 25: 2,
                      26: 3, 27: 4, 28: 5, 29: 6, 30: 7, 31: 8, 32: 9, 33: 10,
                      34: 11, 35: 12},
            'temp': {0: -2.2, 1: 0.6, 2: 6.8, 3: 7.7, 4: 14.2, 5: 18.1, 6: 18.6,
                     7: 19.2, 8: 13.7, 9: 11.0, 10: 5.5, 11: 2.9, 12: 2.2,
                     13: -2.6, 14: 1.1, 15: 13.1, 16: 17.9, 17: 19.4, 18: 20.9,
                     19: 21.7, 20: 16.0, 21: 11.0, 22: 5.2, 23: 2.8, 24: -0.2,
                     25: 3.4, 26: 6.4, 27: 10.9, 28: 12.4, 29: 23.3, 30: 2.0,
                     31: 2.0, 32: 2.0, 33: 2.0, 34: 2.0, 35: 2.0}
        }
