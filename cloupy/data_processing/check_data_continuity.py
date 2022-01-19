
def check_data_continuity(df, main_column, precision):
    """
    Check data continuity and return a dataframe with the filtered values

    Keyword arguments:
        df -- a pandas.DataFrame object that stores the data
        main_column -- the column index by which the data will be filtered (unique
    values, usually station names)
        precision -- required precision for checking data continuity.The values
    must be in the 0-1 range. If the value is 1, then individual stations in the
    dataframe must have the same number of records as the station that has the
    longest data continuity. If the value is 0.5, then individual stations in the
    dataframe must have at least 50% of the number of records of the station that
    has the longest data continuity (e.g. if the largest number of records is 100,
    then at least 50 records are required) (default 0.3)
    """
    if precision < 0 or precision > 1:
        raise ValueError(f'Precision must be within 0-1 range (invalid value: {precision})')

    hm_records = df.iloc[:, main_column].value_counts()
    max_records = max(hm_records)

    valid_ids = []
    for _id, record in hm_records.items():
        if record >= max_records * precision:
            valid_ids.append(_id)

    before_filtering = len(df.iloc[:, main_column].unique())
    df = df[df.iloc[:, main_column].isin(valid_ids)]
    after_filtering = len(df.iloc[:, main_column].unique())

    print(
        'Data continuity checked. '
        f'Unique values in the main column before filtering: {before_filtering}. '
        f'Unique values in the main column after filtering: {after_filtering}.'
    )

    return df
