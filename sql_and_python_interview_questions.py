import streamlit as st
import pandas as pd
import duckdb
import os
import importlib.util
import time

st.set_page_config(page_title="DE Interview Lab", layout="wide")

# --- DYNAMIC EXERCISE LOADER ---
def load_exercises(folder="exercises"):
    exercises = {}
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            path = os.path.join(folder, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            exercises[filename[:-3]] = module.get_exercise()
    return exercises

exercises = load_exercises()

# --- SIDEBAR ---
st.sidebar.header("Select Exercise")
selected_key = st.sidebar.selectbox("Choose Problem:", list(exercises.keys()))
ex = exercises[selected_key]

# Timer
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
    mode = st.radio("Language:", ["SQL", "Python"], horizontal=True)
    user_code = st.text_area(f"Write your {mode} code here:", height=250)
    
    if st.button("Run Code"):
        try:
            if mode == "SQL":
                # DuckDB queries the 'df' variable in scope
                res = duckdb.query(user_code).to_df()
            else:
                # We execute the string and capture the result
                ldict = {'df': df, 'pd': pd}
                exec(f"result = {user_code}", globals(), ldict)
                res = ldict['result']
            
            st.write("### Output")
            st.dataframe(res, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

if st.sidebar.checkbox("Show Hint"):
    st.sidebar.info(ex['hint_sql'] if mode == "SQL" else ex['hint_python'])
