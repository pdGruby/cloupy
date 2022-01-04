
def check_data_continuity(df, main_column, precision):

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
