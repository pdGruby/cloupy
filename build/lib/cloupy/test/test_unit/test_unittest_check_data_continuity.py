from cloupy.data_processing.check_data_continuity import check_data_continuity
import pytest
import pandas as pd


class TestDataChecking:

    @pytest.fixture
    def data(self):
        return pd.DataFrame({
            'station': ['POZNAŃ', 'POZNAŃ', 'POZNAŃ', 'POZNAŃ', 'POZNAŃ',
                        'POZNAŃ', 'POZNAŃ', 'POZNAŃ', 'POZNAŃ', 'POZNAŃ',
                        'KOŁO', 'KOŁO', 'KOŁO', 'KOŁO', 'KOŁO',
                        'KOŁO', 'KOŁO', 'KOŁO', 'TARNÓW', 'TARNÓW',
                        'TARNÓW'
                        ],
            'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                       1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3
                       ]
        })

    def test_data_continuity_checking(self, data):
        assert len(check_data_continuity(data, 0, 1).station) == 10
        assert len(check_data_continuity(data, 0, 0.8)) == 18
        assert len(check_data_continuity(data, 0, 0.3)) == 21
