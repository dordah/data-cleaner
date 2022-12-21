from typing import List
from consts import *
import pandas as pd
from Column import Column


class DataAnalyzer:
    """
    Loads a pandas dataframe which represents data and cleans the data with the available functions.
    After using the cleaning function, it saves the clean data as a new csv file.
    Input: Pandas dataframe (from csv) and a filename.
    Output: Clean data after using cleaning functions.
    """

    def __init__(self, data: pd.DataFrame, filename: str = "result.csv"):
        self.data = data
        self.filename = filename
        self.columns: List[Column] = [Column(self.data[col]) for col in self.data.columns]

    def column_summary(self) -> dict:
        """
        Generate column summary
        :return: A dictionary with columns as key and summary of values as value.
        """
        columns = {}
        for col in self.columns:
            columns[col.name] = {
                'name': col.name,
                'type': col.column_type,
                'total_values': col.amount_of_total_values,
                'empty_values': col.amount_of_empty_values,
                'unique_values': col.amount_of_unique_values
            }
        return columns

    def clean(self, instructions: dict) -> bool:
        """
        Clean the data loaded in the DataAnalyzer object according to cleaning instructions
        :param instructions: A dictionary with cleaning instructions coming from the frontend
        :return: True if cleaning was successful, and saves the clean data version to "clean_<filename>.csv"
        """
        for column in instructions:  # Per column, check if a specific operation is selected, if so, apply it to column.
            strategy = instructions.get(column)
            col_name = strategy['name']
            if strategy['strategyModel'] == REMOVE:
                self.drop_column(col_name)
                continue  # We continue since we don't want to do any other operations on a removed column
            if NULL_REMOVE_ROW in strategy['nullModel']:
                self.data = self.data[self.data[col_name].notna()]
            if NULL_CUSTOM_VALUE in strategy['nullModel']:
                self.fill_with_custom_value(col_name, strategy['nullCustomValue'])
            if NUMERIC_FILL_AVG in strategy['nullModel']:
                self.fill_nan_with_average(col_name)
            if OUTLIER_REMOVE in strategy['outliersModel']:
                self.remove_outliers(col_name, strategy['deviationsNumber'])
        # Once done, save data to CSV.
        self.data.to_csv("clean_" + self.filename, index=False)
        return True

    def drop_column(self, col_name):
        self.data.drop(labels=col_name, axis=1, inplace=True)

    def fill_nan_with_average(self, col_name):
        mean = self.data[col_name].mean(axis=0)
        self.data[col_name].fillna(value=mean, inplace=True)

    def fill_with_custom_value(self, col_name, val: float):
        self.data[col_name].fillna(value=val, inplace=True)

    def remove_outliers(self, col_name, n_std):
        """
        Removes outlier values above a number of standard deviations
        :param col_name: Column to look for outlier values
        :param n_std: Number of
        :return: Nothing. Operation happens inplace.
        """
        n_std = OUTLIER_DEFAULT_NSTD if n_std is None else n_std  # Can't use default argument here since n_std is never empty, but could be "None"
        mean = self.data[col_name].mean()
        std = self.data[col_name].std()
        outliers = self.data[col_name][self.data[col_name] > mean + n_std * std]  # Find outlier numeric values
        for outlier in outliers:  # For each outlier numeric value, find all indexes with this value and remove them.
            indexes = self.data.index[self.data[col_name] == outlier].to_list()
            for index in indexes:
                self.data.drop(index=index, inplace=True)

    def drop_row(self, row_name):
        return self.data.drop(labels=row_name, axis=0, inplace=True)
