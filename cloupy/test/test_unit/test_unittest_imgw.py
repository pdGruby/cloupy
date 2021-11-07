from cloupy.scraping import imgw
import pytest


class TestFileFormats:
    def test_monthly_arg(self):
        # stations_kind = 'synop'
        assert imgw.get_file_formats('monthly', 'synop', 0) == ['s_m_d']
        assert imgw.get_file_formats('monthly', 'synop', 1) == ['s_m_t']
        assert imgw.get_file_formats('monthly', 'synop', 'all') == ['s_m_d', 's_m_t']

        # stations_kind = 'fall'
        for file_format_index in [0, 1, 'all']:
            assert imgw.get_file_formats('monthly', 'fall', file_format_index) == ['o_m']

        # stations_kind = 'climat'
        assert imgw.get_file_formats('monthly', 'climat', 0) == ['k_m_d']
        assert imgw.get_file_formats('monthly', 'climat', 1) == ['k_m_t']
        assert imgw.get_file_formats('monthly', 'climat', 'all') == ['k_m_d', 'k_m_t']

        # stations_kind is invalid
        with pytest.raises(ValueError):
            imgw.get_file_formats('monthly', 'abc', 0)

    def test_daily_arg(self):
        # stations_kind = 'synop'
        assert imgw.get_file_formats('daily', 'synop', 0) == ['s_d']
        assert imgw.get_file_formats('daily', 'synop', 1) == ['s_d_t']
        assert imgw.get_file_formats('daily', 'synop', 'all') == ['s_d', 's_d_t']

        # stations_kind = 'fall'
        for file_format_index in [0, 1, 'all']:
            assert imgw.get_file_formats('daily', 'fall', file_format_index) == ['o_d']

        # stations_kind = 'climat'
        assert imgw.get_file_formats('daily', 'climat', 0) == ['k_d']
        assert imgw.get_file_formats('daily', 'climat', 1) == ['k_d_t']
        assert imgw.get_file_formats('daily', 'climat', 'all') == ['k_d', 'k_d_t']

        # stations_kind is invalid
        with pytest.raises(ValueError):
            imgw.get_file_formats('daily', 'abc', 0)

    def test_prompt_arg(self):
        # stations_kind = 'synop' and 'climat'
        for file_format_index in [0, 1, 'all']:
            assert imgw.get_file_formats('prompt', 'synop', file_format_index) == ['s_t']
            assert imgw.get_file_formats('prompt', 'climat', file_format_index) == ['k_t']

        # stations_kind = 'fall'
        with pytest.raises(NotADirectoryError):
            imgw.get_file_formats('prompt', 'fall', 0)

        # stations_kind is invalid
        with pytest.raises(ValueError):
            imgw.get_file_formats('prompt', 'abc', 0)


class TestKeywordsInColumns:
    def test_None_file_format(self):
        lowercased_keywords = ['temperatura', 'opad']
        uppercased_keywords = ['TEMPERATURA', 'OPAD']
        capitalized_keywords = ['Temperatura', 'Opad']

        lowercased_result = TestKeywordsInColumns.values_counter(
            imgw.search_for_keywords_in_columns(lowercased_keywords)
        )

        uppercased_result = TestKeywordsInColumns.values_counter(
            imgw.search_for_keywords_in_columns(uppercased_keywords)
        )

        capitalized_result = TestKeywordsInColumns.values_counter(
            imgw.search_for_keywords_in_columns(capitalized_keywords)
        )

        assert lowercased_result == uppercased_result == capitalized_result

    def test_specific_file_format(self):
        lowercased_keywords = ['temperatura', 'opad']
        uppercased_keywords = ['TEMPERATURA', 'OPAD']
        capitalized_keywords = ['Temperatura', 'Opad']

        expected_lengths = {
            'k_m_d': 12,
            'k_m_t': 1,
            'o_m': 5,
            's_m_d': 13,
            's_m_t': 3,
            'k_d': 6,
            'k_d_t': 1,
            'o_d': 2,
            's_d': 9,
            's_d_t': 3,
            'k_t': 2,
            's_t': 13
        }
        for format_, expected_value in expected_lengths.items():
            lowercased_result = len(imgw.search_for_keywords_in_columns(lowercased_keywords, format_))

            uppercased_result = len(imgw.search_for_keywords_in_columns(uppercased_keywords, format_))

            capitalized_result = len(imgw.search_for_keywords_in_columns(capitalized_keywords, format_))

            assert lowercased_result == uppercased_result == capitalized_result == expected_lengths[format_]

    @staticmethod
    def values_counter(dictionary):
        counter = 0
        for key in dictionary:
            counter += len(dictionary[key])
        return counter
