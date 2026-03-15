import pytest
import pandas as pd
from tests.conftest import get_exercise_modules, extract_test_cases

# Dynamically gather all sorting modules
entry = get_exercise_modules("sorting_algorithms/entry_algos")
mid = get_exercise_modules("sorting_algorithms/mid_algos")
senior = get_exercise_modules("sorting_algorithms/senior_algos")
de = get_exercise_modules("sorting_algorithms/de_algos")

# Combine all into one massive test list for parametrization
all_sorting_cases = extract_test_cases(entry + mid + senior + de, mode="Python")

@pytest.mark.parametrize("exercise_key,test_name,test_data", all_sorting_cases)
def test_sorting_algorithms(exercise_key, test_name, test_data):
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
