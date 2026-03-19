import pytest
import pandas as pd
import duckdb
from tests.conftest import get_exercise_modules, extract_test_cases

modules = get_exercise_modules("sql_and_pandas")

# Generate test parameters for Python solutions in this folder
python_test_cases = extract_test_cases(modules, mode="Python")

@pytest.mark.parametrize("exercise_key,test_name,test_data", python_test_cases)
def test_sql_folder_python_exercises(exercise_key, test_name, test_data):
    df = test_data["data"].copy()
    code = test_data["solution_code"]
    is_stage = test_data["is_stage"]
    
    ldict = {'df': df, 'pd': pd}
    
    try:
        exec(code, ldict, ldict)
    except Exception as e:
        pytest.fail(f"Execution failed with Exception: {e}")
        
    result = ldict.get('result', None)
    
    if result is None:
        pytest.fail("Python solution failed: 'result' variable not assigned.")
        
    if is_stage and "expected_output" in test_data:
        expected = test_data["expected_output"]
        if isinstance(result, pd.DataFrame):
            pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False)
        else:
            assert result == expected


# Generate test parameters for SQL solutions in this folder
sql_test_cases = extract_test_cases(modules, mode="SQL")

@pytest.mark.parametrize("exercise_key,test_name,test_data", sql_test_cases)
def test_sql_folder_sql_exercises(exercise_key, test_name, test_data):
    df_sql = test_data["data"].copy()
    code = test_data["solution_code"]
    table_name = test_data.get("table_name", "df")
    is_stage = test_data.get("is_stage", False)
    
    try:
        duckdb.register(table_name, df_sql)
        result = duckdb.query(code).to_df()
        
        if not isinstance(result, pd.DataFrame):
            pytest.fail(f"SQL did not return a DataFrame. Got {type(result)}")
            
        if is_stage and "expected_output" in test_data:
            expected = test_data["expected_output"]
            for col in expected.columns:
                if col in result.columns and str(expected[col].dtype).startswith('datetime64'):
                    result[col] = pd.to_datetime(result[col])
            pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False)
            
    except Exception as e:
        pytest.fail(f"SQL Execution failed with Exception: {e}")
    finally:
        # Cleanup registered table from duckdb
        duckdb.unregister(table_name)
