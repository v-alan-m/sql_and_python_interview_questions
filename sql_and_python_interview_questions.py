import streamlit as st
import pandas as pd
import duckdb
import os
import importlib.util
import time

st.set_page_config(page_title="DE Interview Lab", layout="wide")

# --- UPDATED DYNAMIC EXERCISE LOADER (Subfolder Support) ---
def load_exercises(base_folder="exercises"):
    exercises = {}
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        os.makedirs(os.path.join(base_folder, "python"))
        os.makedirs(os.path.join(base_folder, "sql_and_pandas"))
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(base_folder):
        for filename in files:
            if filename.endswith(".py"):
                path = os.path.join(root, filename)
                # Create a unique key using folder + filename
                relative_path = os.path.relpath(path, base_folder)
                exercise_key = relative_path.replace(os.sep, " > ")[:-3]
                
                spec = importlib.util.spec_from_file_location(filename[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                exercises[exercise_key] = module.get_exercise()
    return exercises

exercises = load_exercises()

# --- SIDEBAR ---
st.sidebar.header("Select Exercise")
selected_key = st.sidebar.selectbox("Choose Problem:", sorted(list(exercises.keys())))
ex = exercises[selected_key]

# Timer logic
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
timer_placeholder = st.sidebar.empty()
remaining = max(0, 1200 - int(time.time() - st.session_state.start_time))
timer_placeholder.metric("Time Remaining", f"{remaining // 60}:{remaining % 60:02d}")

# --- MAIN UI ---
st.title(f"Problem: {ex['title']}")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"**Goal:** {ex['description']}")
    st.write("### Input Data")
    df = ex['data']
    st.dataframe(df, use_container_width=True)

with col2:
    # Check if the exercise is restricted to one mode or allows both
    available_modes = ex.get("allowed_modes", ["SQL", "Python"])
    mode = st.radio("Language:", available_modes, horizontal=True)
    
    user_code = st.text_area(f"Write your {mode} code here:", height=250)
    
    if st.button("Run Code"):
        try:
            if mode == "SQL":
                res = duckdb.query(user_code).to_df()
            else:
                ldict = {'df': df, 'pd': pd}
                exec(f"result = {user_code}", globals(), ldict)
                res = ldict['result']
            
            st.write("### Output")
            st.dataframe(res, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

if st.sidebar.checkbox("Show Hint"):
    st.sidebar.info(ex['hint_sql'] if mode == "SQL" else ex['hint_python'])
