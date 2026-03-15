import pytest
import pandas as pd
from tests.conftest import get_exercise_modules, extract_test_cases

# Dynamically discover all tests in exercises/python/
modules = get_exercise_modules("python")
test_cases = extract_test_cases(modules, mode="Python")

@pytest.mark.parametrize("exercise_key,test_name,test_data", test_cases)
def test_python_exercises(exercise_key, test_name, test_data):
    """
    Tests an exercise using the Python engine.
    test_data dict contains: data (DataFrame), solution_code (str), and expected_output (DataFrame) if it's a stage.
    """
    df = test_data["data"].copy()
    code = test_data["solution_code"]
    is_stage = test_data["is_stage"]
    
    # Isolate execution namespace
    ldict = {'df': df, 'pd': pd}
    
    try:
        exec(code, ldict, ldict)
    except Exception as e:
        pytest.fail(f"Execution failed with Exception: {e}")
        
    result = ldict.get('result', None)
    
    if result is None:
        pytest.fail("Python solution failed: 'result' variable not assigned.")
        
    if not isinstance(result, pd.DataFrame) and not isinstance(result, pd.Series) and not isinstance(result, (int, float, str, bool, list, dict)):
        pytest.fail(f"Python solution returned unexpected type: {type(result)}")
        
    # If this is a specific interview stage, we can strictly compare the output
    if is_stage and "expected_output" in test_data:
        expected = test_data["expected_output"]
        if isinstance(result, pd.DataFrame) and isinstance(expected, pd.DataFrame):
            try:
                pd.testing.assert_frame_equal(
                    result.reset_index(drop=True), 
                    expected.reset_index(drop=True), 
                    check_dtype=False
                )
            except Exception as e:
                pytest.fail(f"Stage output mismatch: {e}")
        else:
             assert result == expected, f"Stage output mismatch. Expected {expected}, got {result}"
