from enum import Enum

from pandas.core.dtypes.common import is_string_dtype
from pandas.core.series import Series


class ColumnType(Enum):
    NUMERIC = 'Numeric'
    STRING = 'String'


class Column:
    def __init__(self, column: Series):
        self.column = column

    @property
    def name(self):
        return self.column.name

    @property
    def amount_of_total_values(self):
        return self.column.size

    @property
    def amount_of_empty_values(self):
        return int(self.column.isna().sum())

    @property
    def amount_of_unique_values(self):
        return self.column.unique().size

    @property
    def column_type(self):
        return ColumnType.STRING.name if is_string_dtype(self.column) else ColumnType.NUMERIC.name
