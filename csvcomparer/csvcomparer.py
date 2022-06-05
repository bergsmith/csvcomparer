"""
**csvcomparer** is an open-source Python project used for determining
differences between two delimited files (referred to here as "left" 
and "right" files) that share a common key, or index. 

Specifically, csvcomparer determines:

  - Columns exclusive to the left and right files, respectively.
  - Rows exclusive to the left and right files, respectively.
  - Field-level differences for rows/columns in common between files.

"""

from functools import wraps
import json
from dataclasses import asdict, dataclass
from typing import Any, Callable, ClassVar, Dict, List
import pandas as pd


MULTI_COL_KEY_SEP: str = ", "
"""Default separator used for multi-index output format"""


def requires_data_load(func: Callable) -> Callable:
    """Decorator that loads csv files if required.

    All of the diff attributes require that data be loaded into respective
    dataframes. This decorator checks to see if the files have been loaded,
    and if not, loads them.

    Args:
        func (_type_): _description_

    Returns:
        Callable: _description_
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        self_ = args[0]  # args[0] is "self" in this context
        if self_._l_df.empty or self_._r_df.empty:
            self_._load_csvs()
        return func(*args, **kwargs)

    return wrapper


@dataclass
class CsvCompareDiffs:
    """Convenience dataclass for CsvCompare.

    Provides an accumulation all of the difference types:
      
      - Rows added to the right file (``rows_added``)
      - Rows removed from the left file (``rows_removed``)
      - Rows with deltas between files (``rows_changed``)
      - Columns added to the right file (``cols_added``)
      - Columns removed from the left file (``cols_removed``)

    Additionally provides:

      - ``row_key`` as reference to ``CsvCompare``'s index column(s)
      - ``to_json()`` for converting diffs to JSON format

    """
    row_key: List[str]
    rows_added: Dict[str, Dict[str, Any]]
    rows_removed: Dict[str, Dict[str, Any]]
    rows_changed: Dict[str, List[Dict[str, Any]]]
    cols_added: List[str]
    cols_removed: List[str]
    _ROW_DIFF_ATTRS: ClassVar = ["rows_added", "rows_changed", "rows_removed"]

    def to_dict(self):
        """Convenience function to use instead of dataclasses.asdict().

        Returns:
            dict: ``CsvCompareDiffs`` converted to dictionary.
        """
        return asdict(self)

    def to_json(self):
        """Convert ``CsvCompareDiffs`` to JSON format.

        Returns:
            str: Serialization of Python JSON object.
        """
        if self.is_multi_index:
            self._map_attr_keys()
        return json.dumps(self.to_dict())

    def _map_attr_keys(self):
        for attr in self._ROW_DIFF_ATTRS:
            current_val = getattr(self, attr)
            new_val = self._tuple_keys_to_str(current_val)
            setattr(self, attr, new_val)

    def _tuple_keys_to_str(self, dict_):
        return {MULTI_COL_KEY_SEP.join([str(k) for k in k]): v
                for k, v in dict_.items()}

    @property
    def is_multi_index(self) -> bool:
        return len(self.row_key) > 1

class CsvCompare:
    def __init__(
        self,
        left_csv_path: str,
        right_csv_path: str,
        index_col: List[str],
        *,
        kwargs: dict = {},
        read_csv_kwargs: dict = {},
    ) -> None:
        """
        Args:
            left_csv_path: str, path object or file-like object
                Any valid string path is acceptable. The string could be a URL.
                Valid URL schemes include http, ftp, s3, gs, and file.
                For file URLs, a host is expected.
            right_csv_path: str, path object or file-like object
                Any valid string path is acceptable. The string could be a URL.
                Valid URL schemes include http, ftp, s3, gs, and file.
                For file URLs, a host is expected.
            index_col: str or sequence of str
                Column(s) to be used as the index (key) for both input files.
            kwargs, optional:
                Arguments specific to options for the compare results, by default {}.
            read_csv_kwargs, optional:
                Arguments for reading in the input files. Uses the same
                interface as pandas.read_csv. By default {}

        Note:
            Additionally initializes empty dataframes for the input files.

        """

        self._l_csv_path = left_csv_path
        self._r_csv_path = right_csv_path
        self._index_col = index_col
        self._kwargs = kwargs
        self._read_csv_kwargs = read_csv_kwargs
        self._l_df = pd.DataFrame()
        self._r_df = pd.DataFrame()

    def __repr__(self):
        return f"CsvCompare('{self._l_csv_path}', '{self._r_csv_path}', {self._index_col})"

    def _load_csvs(self) -> None:
        """Loads the "left" and "right" files into respective dataframes."""
        
        self._l_df = pd.read_csv(
            self._l_csv_path, index_col=self._index_col, **self._read_csv_kwargs
        )
        self._r_df = pd.read_csv(
            self._r_csv_path, index_col=self._index_col, **self._read_csv_kwargs
        )

    def _map_diff_rows(self, row) -> pd.DataFrame:
        """Maps the output of pandas' .compare to a list of tuples.

        The mapping iterates over each row of pandas compare dataframe,
        essentially squashing the multi-level columns into a 3-tuple of
        (column_name, left_file_value, right_file_value). These tuples
        become the new values for the original indexes.

        Args:
            row (pd.DataFrame): Pandas' .compare output

        Returns:
            pd.DataFrame: Mapped version of Pandas' .compare output

        See also:
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.compare.html
        """
        # Only need to iterate over non-null labels that actually have diffs
        row.dropna(inplace=True)
        diff_cols = row.index.get_level_values(0).unique()
        return [(col, row[(col, "self")], row[(col, "other")]) for col in diff_cols]


    @property
    @requires_data_load
    def cols_added(self) -> List[str]:
        """Columns added to the "right" file.

        Returns:
            List[str]: Set difference between the left file's column names and
            the right file's column names.
        """
        return self._r_df.columns.difference(self._l_df.columns).to_list()

    @property
    @requires_data_load
    def cols_removed(self) -> List[str]:
        """Columns removed from the "left" file.

        Returns:
            List[str]: Set difference between the right file's column names and
            the left file's column names.
        """
        return self._l_df.columns.difference(self._r_df.columns).to_list()

    @property
    @requires_data_load
    def rows_added(self) -> Dict[str, Dict[str, Any]]:
        """Rows added to the "right" file.

        Returns:
            Dict[str, Dict[str, Any]]: Rows in the right file where the
            index is the set difference between the right file's index
            and the left_file's index.
        """
        r_only_idxs = self._r_df.index.difference(self._l_df.index)
        return self._r_df.loc[r_only_idxs].to_dict("index")

    @property
    @requires_data_load
    def rows_removed(self) -> Dict[str, Dict[str, Any]]:
        """Rows removed from the "left" file.

        Returns:
            Dict[str, Dict[str, Any]]: Rows in the left file where the
            index is the set difference between the left file's index
            and the right_file's index.
        """
        l_only_idxs = self._l_df.index.difference(self._r_df.index)
        return self._l_df.loc[l_only_idxs].to_dict("index")

    @property
    @requires_data_load
    def rows_changed(self) -> Dict[str, List[Dict[str, Any]]]:
        """Rows with fields that have different values between files.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Field value differences for
            rows/columns in common between left and right files.
        """
        common_idxs = self._l_df.index.intersection(self._r_df.index)
        common_cols = self._l_df.columns.intersection(self._r_df.columns)
        compare_df = self._l_df.loc[common_idxs, common_cols].compare(
            self._r_df.loc[common_idxs, common_cols]
        )
        return compare_df.apply(self._map_diff_rows, axis=1).to_dict()

    @property
    def diffs(self) -> CsvCompareDiffs:
        """Accumulation of all differences found between files."""
        return CsvCompareDiffs(
            row_key=self._index_col,
            rows_added=self.rows_added,
            rows_removed=self.rows_removed,
            rows_changed=self.rows_changed,
            cols_added=self.cols_added,
            cols_removed=self.cols_removed,
        )


