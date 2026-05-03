import os
import sys
import pytest

# Add parent dir to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import ExerciseManager
from quiz import QuizApp

def test_exercise_manager_initialization():
    manager = ExerciseManager(base_folder=os.path.join(os.path.dirname(__file__), '..', 'exercises'))
    assert isinstance(manager.category_options, dict)
    assert len(manager.category_options) > 0
    assert "Python (Core)" in manager.category_options

def test_quiz_app_initialization():
    manager = ExerciseManager(base_folder=os.path.join(os.path.dirname(__file__), '..', 'exercises'))
    app = QuizApp(manager)
    assert app.ex_manager == manager

def test_manager_get_filtered_exercises():
    manager = ExerciseManager(base_folder=os.path.join(os.path.dirname(__file__), '..', 'exercises'))
    # Assuming there's at least one python_core exercise, test the filtering logic
    filtered = manager.get_filtered_exercises("python_core")
    assert isinstance(filtered, dict)
    for key in filtered.keys():
        assert key.startswith("python_core")
