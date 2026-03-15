import os
import importlib.util

def get_exercise_modules(category_folder):
    """
    Dynamically discovers and yields all exercise modules in a given category folder.
    Returns tuples of (exercise_key, module).
    """
    base_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exercises")
    target_folder = os.path.join(base_folder, category_folder)
    
    if not os.path.exists(target_folder):
        return []

    modules = []
    for root, dirs, files in os.walk(target_folder):
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
                    modules.append((exercise_key, module))
                except Exception as e:
                    print(f"Error loading module {path}: {e}")
                    
    return modules

def extract_test_cases(modules, mode="Python"):
    """
    Flattens the modules into a list of specific test cases to be parameterized.
    Each test case is a tuple: (exercise_key, test_name, test_data_dict)
    """
    test_cases = []
    for exercise_key, module in modules:
        try:
            ex = module.get_exercise()
            
            # 1. Base test (Original feature)
            if mode in ex.get('allowed_modes', []):
                sol_key = f"solution_{mode.lower()}"
                if sol_key in ex and ex[sol_key] and ex[sol_key] != "Not applicable":
                     test_cases.append((
                         exercise_key, 
                         "Base Solution", 
                         {
                             "is_stage": False,
                             "data": ex["data"],
                             "solution_code": ex[sol_key],
                             "table_name": ex.get("table_name", "df")
                         }
                     ))
            
            # 2. Stage tests (New feature)
            if "interview_stages" in ex:
                 for stage in ex["interview_stages"]:
                     # Only stage Python right now as SQL stages aren't standard yet in the structure
                     if mode == "Python" and "solution_code" in stage:
                         test_cases.append((
                             exercise_key,
                             f"Stage {stage['stage_number']} - {stage['title']}",
                             {
                                 "is_stage": True,
                                 "data": stage["data"],
                                 "solution_code": stage["solution_code"],
                                 "expected_output": stage.get("expected_output", None)
                             }
                         ))
                         
        except Exception as e:
             print(f"Error parsing exercise {exercise_key}: {e}")
             
    return test_cases
