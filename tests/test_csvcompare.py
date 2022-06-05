import json
import pytest
from csvcomparer import CsvCompare

left_csv_path = "./tests/files/menu_l.csv"
right_csv_path = "./tests/files/menu_r.csv"
single_index = ["id"]
multi_index = ["id", "name"]


@pytest.fixture(scope="class")
def single_index_diffs():
    return {'row_key': ['id'], 'rows_added': {'4C': {'name': 'taco', 'pic': '🌮', 'price': '$8.33', 'stars': 3.1}, '5B': {'name': 'pizza', 'pic': '🍕', 'price': '$9.99', 'stars': 2.4}}, 'rows_removed': {'3A': {'name': 'bacon', 'pic': '🥓', 'price': '$3.33', 'score': 4.9, 'togo': 'Y'}}, 'rows_changed': {'1A': [('pic', '🍺', '🍻'), ('price', '$6.00', '$5.25')], '2A': [('price', '$4.10', '$3.95')]}, 'cols_added': ['stars'], 'cols_removed': ['score', 'togo']}

@pytest.fixture(scope="class")
def multi_index_diffs():
    return {'row_key': ['id', 'name'], 'rows_added': {('4C', 'taco'): {'pic': '🌮', 'price': '$8.33', 'stars': 3.1}, ('5B', 'pizza'): {'pic': '🍕', 'price': '$9.99', 'stars': 2.4}}, 'rows_removed': {('3A', 'bacon'): {'pic': '🥓', 'price': '$3.33', 'score': 4.9, 'togo': 'Y'}}, 'rows_changed': {('1A', 'beer'): [('pic', '🍺', '🍻'), ('price', '$6.00', '$5.25')], ('2A', 'cheese'): [('price', '$4.10', '$3.95')]}, 'cols_added': ['stars'], 'cols_removed': ['score', 'togo']}

@pytest.fixture(scope="class")
def single_index_diffs_json():
    return json.dumps({"row_key": ["id"], "rows_added": {"4C": {"name": "taco", "pic": "\ud83c\udf2e", "price": "$8.33", "stars": 3.1}, "5B": {"name": "pizza", "pic": "\ud83c\udf55", "price": "$9.99", "stars": 2.4}}, "rows_removed": {"3A": {"name": "bacon", "pic": "\ud83e\udd53", "price": "$3.33", "score": 4.9, "togo": "Y"}}, "rows_changed": {"1A": [["pic", "\ud83c\udf7a", "\ud83c\udf7b"], ["price", "$6.00", "$5.25"]], "2A": [["price", "$4.10", "$3.95"]]}, "cols_added": ["stars"], "cols_removed": ["score", "togo"]})

@pytest.fixture(scope="class")
def multi_index_diffs_json():
    return json.dumps({"row_key": ["id", "name"], "rows_added": {"4C, taco": {"pic": "\ud83c\udf2e", "price": "$8.33", "stars": 3.1}, "5B, pizza": {"pic": "\ud83c\udf55", "price": "$9.99", "stars": 2.4}}, "rows_removed": {"3A, bacon": {"pic": "\ud83e\udd53", "price": "$3.33", "score": 4.9, "togo": "Y"}}, "rows_changed": {"1A, beer": [["pic", "\ud83c\udf7a", "\ud83c\udf7b"], ["price", "$6.00", "$5.25"]], "2A, cheese": [["price", "$4.10", "$3.95"]]}, "cols_added": ["stars"], "cols_removed": ["score", "togo"]})

@pytest.fixture(scope="class")
def single_index_test_obj():
    return CsvCompare(left_csv_path, right_csv_path, single_index)

@pytest.fixture(scope="class")
def multi_index_test_obj():
    return CsvCompare(left_csv_path, right_csv_path, multi_index)


class TestCsvCompareSingleIndex:
    def test_cols_added(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.cols_added == single_index_diffs["cols_added"]

    def test_cols_removed(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.cols_removed == single_index_diffs["cols_removed"]

    def test_rows_added(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.rows_added == single_index_diffs["rows_added"]

    def test_rows_removed(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.rows_removed == single_index_diffs["rows_removed"]

    def test_rows_changed(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.rows_changed == single_index_diffs["rows_changed"]

    def test_diffs(self, single_index_test_obj, single_index_diffs):
        assert single_index_test_obj.diffs.to_dict() == single_index_diffs


class TestCsvCompareMultiIndex:
    def test_cols_added(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.cols_added == multi_index_diffs["cols_added"]

    def test_cols_removed(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.cols_removed == multi_index_diffs["cols_removed"]

    def test_rows_added(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.rows_added == multi_index_diffs["rows_added"]

    def test_rows_removed(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.rows_removed == multi_index_diffs["rows_removed"]

    def test_rows_changed(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.rows_changed == multi_index_diffs["rows_changed"]

    def test_diffs(self, multi_index_test_obj, multi_index_diffs):
        assert multi_index_test_obj.diffs.to_dict() == multi_index_diffs

class TestCsvCompareHelpers:
    def test_load_csvs(self):
        csv_compare = CsvCompare(left_csv_path, right_csv_path, single_index)
        csv_compare._load_csvs()
        l_df, r_df = csv_compare._l_df, csv_compare._r_df
        assert not (l_df.empty or r_df.empty)

class TestCsvCompareDunders:
    def test_repr(self):
        csv_compare = CsvCompare(left_csv_path, right_csv_path, single_index)
        expected = f"CsvCompare('{left_csv_path}', '{right_csv_path}', {single_index})"
        assert str(csv_compare) == expected

class TestCsvCompareDiffsSingleIndex:
    def test_to_json(self, single_index_test_obj, single_index_diffs_json):
        assert single_index_test_obj.diffs.to_json() == single_index_diffs_json

class TestCsvCompareDiffsMultiIndex:
    def test_to_json(self, multi_index_test_obj, multi_index_diffs_json):
        assert multi_index_test_obj.diffs.to_json() == multi_index_diffs_json


