import streamlit as st
import pandas as pd
import duckdb
import os
import importlib.util
import time

# --- APP CONFIG ---
st.set_page_config(page_title="DE Interview Lab Pro", layout="wide")

from styles import inject_custom_css
from core import ExerciseManager
from ui_components import render_exercise
from quiz import QuizApp

# Global CSS Tweaks
inject_custom_css()

# --- EXERCISE MANAGER ---
if 'ex_manager' not in st.session_state:
    st.session_state.ex_manager = ExerciseManager()
ex_manager = st.session_state.ex_manager
exercises = ex_manager.exercises

# --- STATE ---
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'normal'

# --- SIDEBAR ---
with st.sidebar:
    if st.session_state.app_mode == 'normal':
        if st.button("Quiz Mode", use_container_width=True, key="quiz_mode_btn"):
            st.session_state.app_mode = 'quiz'
            st.rerun()
# Timer
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

@st.fragment(run_every="1s")
def display_timer():
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 300 - elapsed)
    st.metric("Session Timer", f"{remaining // 60}:{remaining % 60:02d}")

with st.sidebar:
    display_timer()
    if st.button("Reset Timer", use_container_width=True):
        st.session_state.start_time = time.time()
        st.rerun()

if st.session_state.app_mode == 'normal':
    st.sidebar.header("Training Menu")

    selected_category = st.sidebar.selectbox("Select Category:", list(ex_manager.category_options.keys()))
    folder_prefix = f"{ex_manager.category_options[selected_category]} > "

    if selected_category == "Sorting Algorithms":
        selected_level = st.sidebar.selectbox("Select Level:", list(ex_manager.level_options.keys()))
        folder_prefix = f"sorting_algorithms > {ex_manager.level_options[selected_level]} > "

    if selected_category == "Python (Core)":
        selected_sub = st.sidebar.selectbox("Select Topic:", list(ex_manager.sub_options.keys()))
        folder_prefix = f"python_core > {ex_manager.sub_options[selected_sub]} > "

    if not exercises:
        st.sidebar.warning("No exercises found in /exercises folder!")
        selected_key = None
    else:
        filtered_exercises = ex_manager.get_filtered_exercises(folder_prefix)
        if not filtered_exercises:
            st.sidebar.warning(f"No exercises found for {selected_category}!")
            selected_key = None
        else:
            exercise_list = sorted(list(filtered_exercises.keys()))
            if 'selected_exercise' not in st.session_state or st.session_state.selected_exercise not in exercise_list:
                st.session_state.selected_exercise = exercise_list[0] if exercise_list else None
                
            current_index = exercise_list.index(st.session_state.selected_exercise) if st.session_state.selected_exercise in exercise_list else 0

            selected_key = st.sidebar.radio(
                "Select Exercise:", 
                exercise_list,
                index=current_index,
                format_func=lambda x: x.split(" > ")[-1],
                key="exercise_radio"
            )
            st.session_state.selected_exercise = selected_key
            ex = filtered_exercises[selected_key]

    # --- MAIN UI ---
    if selected_key:
        render_exercise(ex, selected_key, selected_category)

elif st.session_state.app_mode == 'quiz':
    QuizApp(ex_manager).render()

