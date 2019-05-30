import pandas as pd
import numpy as np
import pytest

from column_completer import ColumnCompleter


X = np.random.randint(0, 100, (8, 3))


def test_name_collision_value_error_1():
    df = pd.DataFrame(X, columns=["Col A", "Col_A", "Col B"])
    with pytest.raises(ValueError) as err:
        q = ColumnCompleter(df)
    assert "spaces causes a collision of column names" in str(err.value)


def test_attribute_space_replaced_1():
    df = pd.DataFrame(X, columns=["Col A", "col B", "Col C"])
    q = ColumnCompleter(df)
    assert all([col.startswith('Col_')
                for col in vars(q) if col.startswith('Col')])


def test_attribute_space_replaced_2():
    df = pd.DataFrame(X, columns=["Col A", "col B", "Col C"])
    space_filler = '___'
    q = ColumnCompleter(df, space_filler=space_filler)
    assert all([col.startswith('Col' + space_filler)
                for col in vars(q) if col.startswith('Col')])


def test_warn_spaces_at_edges_of_column_names_1():
    df = pd.DataFrame(X, columns=["Col A ", "Col B", "Col C"])
    with pytest.raises(Warning) as warn:
        q = ColumnCompleter(df)
    assert "The following columns ends with one or more spaces:" in str(
        warn.value)


def test_warn_spaces_at_edges_of_column_names_2():
    df = pd.DataFrame(X, columns=["Col A", " Col B", "Col C"])
    with pytest.raises(Warning) as warn:
        q = ColumnCompleter(df)
    assert "The following columns starts with one or more spaces:" in str(
        warn.value)


def test_rename_columns_1():
    df_org = pd.DataFrame(X, columns=["col a", "col b", "col c"])
    df_new = ColumnCompleter.replace_df_column_spaces(df_org, '_')
    assert df_new.columns.tolist() == ["col_a", "col_b", "col_c"]


def test_rename_columns_2():
    df_org = pd.DataFrame(X, columns=["col a", "col b", "col c"])
    df_new = ColumnCompleter.replace_df_column_spaces(
        df_org, '_', capatilize_first_letter=True)
    assert df_new.columns.tolist() == ["Col_a", "Col_b", "Col_c"]


def test_rename_columns_3():
    df_org = pd.DataFrame(X, columns=["col a", "col_a", "col c"])
    with pytest.raises(ValueError) as err:
        df_new = ColumnCompleter.replace_df_column_spaces(df_org, '_')
    assert "Renaming the columns in such a way would cause a" in str(err.value)


def test_df_with_numeric_column_names():
    df = pd.DataFrame(X)
    q = ColumnCompleter(df)  # no error should be raised
