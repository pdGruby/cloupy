class NoDataError(Exception):
    def __init__(self, object_name):
        self.object_name = object_name

    def for_drawing(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise NoDataError(
            f"""
            No data has been input for '{self.object_name}'. Please input data on your own (you can find proper 
            data format in '{self.object_name}' docs) or use '{self.object_name}.download_data' method. 
            {additional_info}
            """
        )

    def no_data_scraped(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise NoDataError(
            f"""
            No data for specified parameters found. Check if data for specified parameters in '{self.object_name}' exists. 
            {additional_info}
            """
        )

    def no_global_df_set(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise NoDataError(
            f"""
            Error occured in '{self.object_name}' cause no global dataframe has been set.
            {additional_info}
            """
        )


    def filtered_and_empty(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise NoDataError(
            f"""
            Dataframe has just been filtered and the output was empty. Check your inputs which may affect filtering.
            {additional_info}
            """
        )


class InvalidDataInput(Exception):
    def __init__(self, object_name):
        self.object_name = object_name

    def invalid_structure_for_drawing(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise InvalidDataInput(
            f"""
            Data input for '{self.object_name}' is invalid. Check {self.object_name} docs and input valid data structure. 
            {additional_info}
            """
        )

    def invalid_value_inside(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise InvalidDataInput(
            f"""
            Invalid value inside the dataframe in {self.object_name}. Check your data.
            {additional_info}
            """
        )


class NoElementFoundError(Exception):
    def __init__(self, element_name):
        self.element_name = element_name

    def from_webscraping(self, additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise NoElementFoundError(
            f"""Web scraping went wrong and no '{self.element_name}' has been found. 
            {additional_info}
            """
        )


class InvalidArgValue(Exception):
    def __init__(self, object_name):
        self.object_name = object_name

    def invalid_arg(self, arg_name, valid_values,
                    additional_info=None):
        if additional_info is None:
            additional_info = ''
        raise InvalidArgValue(
            f"""
            Invalid values for '{arg_name}' in '{self.object_name}' input. 
            Valid values: {valid_values}
            {additional_info}
            """
        )
