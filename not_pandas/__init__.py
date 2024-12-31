"""
.. include:: ../README.md
"""

from copy import copy, deepcopy
from itertools import groupby
from not_pandas.errors import LengthError
from not_pandas.utils import to_list, to_tuple
from operator import itemgetter
from tabulate import tabulate
from typing import Callable, Iterable, Iterator, Self


class Series(list):
    """
    A Series is a single column of data in a `not_pandas.DataFrame`, we subclass a basic
    Python list and override its methods to perform element wise comparison instead of
    object level comparison.
    """

    def _pre_check_comparison(self, other):
        if isinstance(other, Series):
            if self.__len__() != other.__len__():
                raise LengthError("Series lengths must match for comparison")

    def __eq__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__eq__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__eq__(other), self))

    def __ne__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__ne__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__ne__(other), self))

    def __and__(self, other):
        """
        NOTE: Is this better? Series(map(operator.truth, self))
        """

        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__and__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__and__(other), self))

    def __invert__(self):
        return Series(map(lambda x: not bool(x), self))

    def __add__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__add__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__add__(other), self))

    def __sub__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__sub__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__sub__(other), self))

    def __mul__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__mul__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__mul__(other), self))

    def __truediv__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__truediv__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__truediv__(other), self))

    def __floordiv__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__floordiv__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__floordiv__(other), self))

    def __lt__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__lt__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__lt__(other), self))

    def __le__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__le__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__le__(other), self))

    def __gt__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__gt__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__gt__(other), self))

    def __ge__(self, other):
        self._pre_check_comparison(other)
        if isinstance(other, Series):
            return Series(a.__ge__(b) for a, b in zip(self, other))

        return Series(map(lambda x: x.__ge__(other), self))

    def isin(self, values: Iterable):
        return Series(map(lambda x: x in values, self))

    def len(self):
        return len(self)

    def max(self):
        return max(self)

    def mean(self):
        return sum(self) / len(self)

    def min(self):
        return min(self)

    def rank(self, ascending: bool = True):
        """
        NOTE: This does not take into account duplicate values
        """

        # Capture the original ordering of the data
        data = [{"index": i, "elem": elem} for i, elem in enumerate(self)]

        # Sort the data by the original data `elem`
        data.sort(key=itemgetter("elem"), reverse=ascending)

        # Add a basic rank to the array
        data = [{"rank": i, **elem} for i, elem in enumerate(data, start=1)]

        # Sort the data back into the original order
        data.sort(key=itemgetter("index"))

        # Return just the rank as a Series
        return Series(map(itemgetter("rank"), data))

    def sum(self):
        return sum(self)

    def unique(self):
        return sorted(set(self))


class DataFrame(object):
    """
    The DataFrame object is the main object in Pandas, it holds all the data and allows
    users to perform various queries to fetch certain columns and rows as well as
    performing aggregations. The underlying data is stored as a basic list of
    dictionaries, when you perform certain methods that return a single column of data,
    this will be returned as a `not_pandas.Series` object.
    """

    def __init__(self, data: list[dict]):
        self._data = list(data)

    def __getitem__(self, item):
        if isinstance(item, Series):
            return DataFrame([row for row, bool_ in zip(self._data, item) if bool_])
        elif isinstance(item, list):
            return DataFrame(
                [{k: row[k] for k in item if k in item} for row in self._data]
            )

        return Series(map(itemgetter(item), self._data))

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        if isinstance(value, Series):
            for row, value_ in zip(self._data, value):
                row[key] = value_
        else:
            for row in self._data:
                row[key] = value

    def __str__(self):
        if self._data:
            return tabulate(self._data, headers="keys")
        else:
            return "Empty DataFrame"

    def columns(self):
        return sorted(set(k for row in self._data for k in row.keys()))

    def copy(self, deep: bool = True) -> Self:
        """
        Return a copy of this object
        """

        if deep:
            return DataFrame(deepcopy(self._data))
        else:
            return DataFrame(copy(self._data))

    def empty(self) -> bool:
        """
        Is the DataFrame is empty
        """

        if self._data is None or self.__len__() == 0:
            return True

    def groupby(self, keys: list | str, ascending=True) -> Iterator[tuple[tuple, Self]]:
        """
        Group a DataFrame by one or more keys and return sections of the DataFrame
        """

        keys = to_list(keys)
        for keys_group, df_group in groupby(
            self.sort_values(keys, ascending)._data, itemgetter(*keys)
        ):
            yield to_tuple(keys_group), DataFrame(list(df_group))

    def groupby_agg(
        self,
        keys: list | str,
        agg_cols: list | str,
        agg_func: Callable,
        ascending=True,
    ) -> Self:
        """
        Group a DataFrame by one or more keys and perform an aggregation on a column of
        the sections, return a DataFrame of the results.
        """

        keys = to_list(keys)
        agg_cols = to_list(agg_cols)
        data = []
        for keys_group, df_group in self.groupby(keys, ascending):
            row = {}

            for col in agg_cols:
                row[col] = agg_func(df_group[col])

            row |= dict(zip(keys, keys_group))

            data.append(row)

        return DataFrame(data)

    def head(self, n: int = 10):
        return DataFrame(self._data[: min(n, self.__len__())])

    def rename(self, *, columns: dict | Callable):
        """
        Rename columns of the DataFrame
        """

        data = []
        if callable(columns):
            columns = {col: columns(col) for col in self.columns()}

        for row in self._data:
            data.append({columns.get(k, k): v for k, v in row.items()})

        return DataFrame(data)

    def sort_values(self, keys: list | str, ascending=True):
        keys = to_list(keys)
        return DataFrame(
            sorted(self._data, key=itemgetter(*keys), reverse=not ascending)
        )

    def tail(self, n: int = 10):
        raise NotImplementedError
