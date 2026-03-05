import os
import importlib.util
import pandas as pd
import duckdb
import sys

def load_and_test_exercises(base_folder="exercises"):
    total_exercises = 0
    passed_exercises = 0
    failed_exercises = []

    if not os.path.exists(base_folder):
        print(f"Error: Base folder '{base_folder}' does not exist.")
        return False

    print(f"Starting exercise tests in '{base_folder}'...")
    print("-" * 50)

    for root, dirs, files in os.walk(base_folder):
        # Skip __pycache__ directories
        if "__pycache__" in root:
            continue
            
        for filename in files:
            if filename.endswith(".py"):
                path = os.path.join(root, filename)
                relative_path = os.path.relpath(path, base_folder)
                exercise_key = relative_path.replace(os.sep, " > ")[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(filename[:-3], path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    ex = module.get_exercise()
                    
                    total_exercises += 1
                    print(f"Testing: {exercise_key} ({ex['title']})")
                    
                    success = True
                    df = ex['data'].copy()
                    
                    # Test Python solution if applicable
                    if "Python" in ex.get('allowed_modes', []):
                        if "solution_python" in ex and ex["solution_python"] and ex["solution_python"] != "Not applicable":
                            try:
                                ldict = {'df': df.copy(), 'pd': pd}
                                exec(ex["solution_python"], ldict, ldict)
                                result = ldict.get('result', None)
                                if result is None:
                                    print(f"  [X] Python Failed: 'result' variable not assigned.")
                                    success = False
                                elif not isinstance(result, pd.DataFrame) and not isinstance(result, pd.Series) and not isinstance(result, (int, float, str, bool, list, dict)):
                                    # Allow various return types, but usually dataframe
                                    print(f"  [X] Python Failed: 'result' type unexpected: {type(result)}")
                                    success = False
                                else:
                                    print(f"  [OK] Python Passed")
                            except Exception as e:
                                print(f"  [X] Python Failed with Exception: {e}")
                                success = False
                        else:
                             print(f"  [!] Python Skipped: No solution provided.")
                    
                    # Test SQL solution if applicable
                    if "SQL" in ex.get('allowed_modes', []):
                        if "solution_sql" in ex and ex["solution_sql"] and ex["solution_sql"] != "Not applicable":
                            try:
                                df_sql = df.copy()
                                # 'df' must be available in local scope for DuckDB to query it easily if it's named 'df'
                                # In the app it queries `table` or `df`. Many SQL solutions use 'FROM df'.
                                # We'll replace 'table_name' with 'df' if it exists just in case.
                                sql_code = ex["solution_sql"].replace("table_name", "df")
                                result = duckdb.query(sql_code).to_df()
                                if not isinstance(result, pd.DataFrame):
                                     print(f"  [X] SQL Failed: Did not return DataFrame.")
                                     success = False
                                else:
                                     print(f"  [OK] SQL Passed")
                            except Exception as e:
                                print(f"  [X] SQL Failed with Exception: {e}")
                                success = False
                        else:
                             print(f"  [!] SQL Skipped: No solution provided.")
                             
                    if success:
                        passed_exercises += 1
                    else:
                        failed_exercises.append(exercise_key)
                        
                except Exception as e:
                    print(f"Error loading module {path}: {e}")
                    total_exercises += 1
                    failed_exercises.append(exercise_key)

    print("-" * 50)
    print("Test Summary:")
    print(f"Total Exercises Executed: {total_exercises}")
    print(f"Passed: {passed_exercises}")
    print(f"Failed: {total_exercises - passed_exercises}")
    
    if failed_exercises:
        print("\nFailed Exercises List:")
        for f in failed_exercises:
            print(f" - {f}")
        return False
        
    return True

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    exercises_dir = os.path.join(current_dir, "exercises")
    
    success = load_and_test_exercises(exercises_dir)
    if not success:
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)
