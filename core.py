import os
import importlib.util

class ExerciseManager:
    def __init__(self, base_folder="exercises"):
        self.base_folder = base_folder
        self.category_options = {
            "Python (Core)": "python_core",
            "Pandas (Python)": "python",
            "SQL and Pandas": "sql_and_pandas",
            "Sorting Algorithms": "sorting_algorithms",
            "Real-World Scenarios": "real_world_scenarios"
        }
        self.level_options = {
            "Entry Level": "entry_algos",
            "Mid Level": "mid_algos",
            "Senior Level": "senior_algos",
            "Data Engineering (DE) Level": "de_algos"
        }
        self.sub_options = {
            "System": "python_system",
            "Coding": "python_coding"
        }
        self.exercises = self.load_exercises()

    def load_exercises(self):
        exercises = {}
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
            os.makedirs(os.path.join(self.base_folder, "python"))
            os.makedirs(os.path.join(self.base_folder, "sql_and_pandas"))
        
        for root, dirs, files in os.walk(self.base_folder):
            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)
                    relative_path = os.path.relpath(path, self.base_folder)
                    exercise_key = relative_path.replace(os.sep, " > ")[:-3]
                    
                    spec = importlib.util.spec_from_file_location(filename[:-3], path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    exercises[exercise_key] = module.get_exercise()
        return exercises

    def get_filtered_exercises(self, folder_prefix):
        return {k: v for k, v in self.exercises.items() if k.startswith(folder_prefix)}
