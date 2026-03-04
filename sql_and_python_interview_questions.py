import streamlit as st
import pandas as pd
import duckdb
import os
import importlib.util
import time

# --- APP CONFIG ---
st.set_page_config(page_title="DE Interview Lab Pro", layout="wide")

# --- DYNAMIC EXERCISE LOADER ---
def load_exercises(base_folder="exercises"):
    exercises = {}
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        os.makedirs(os.path.join(base_folder, "python"))
        os.makedirs(os.path.join(base_folder, "sql_and_pandas"))
    
    for root, dirs, files in os.walk(base_folder):
        for filename in files:
            if filename.endswith(".py"):
                path = os.path.join(root, filename)
                relative_path = os.path.relpath(path, base_folder)
                exercise_key = relative_path.replace(os.sep, " > ")[:-3]
                
                spec = importlib.util.spec_from_file_location(filename[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                exercises[exercise_key] = module.get_exercise()
    return exercises

exercises = load_exercises()

# --- SIDEBAR ---
st.sidebar.header("🎯 Training Menu")
if not exercises:
    st.sidebar.warning("No exercises found in /exercises folder!")
    selected_key = None
else:
    selected_key = st.sidebar.selectbox("Select Exercise:", sorted(list(exercises.keys())))
    ex = exercises[selected_key]

# Timer
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
timer_placeholder = st.sidebar.empty()
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, 1200 - elapsed)
timer_placeholder.metric("Session Timer", f"{remaining // 60}:{remaining % 60:02d}")

if st.sidebar.button("Reset Timer"):
    st.session_state.start_time = time.time()
    st.rerun()

# --- MAIN UI ---
if selected_key:
    st.title(f"Problem: {ex['title']}")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### 📋 Objective\n{ex['description']}")
        st.write("### 📥 Input Data")
        df = ex['data']
        st.dataframe(df, use_container_width=True)
        
        # Help Sections
        with st.expander("💡 View Hint"):
            st.info(ex.get('hint_sql' if 'SQL' in ex.get('allowed_modes', ["SQL", "Python"]) else 'hint_python', "No hint available."))
        
        with st.expander("✅ View Reference Solution"):
            mode_choice = st.selectbox("Solution for:", ex.get('allowed_modes', ["SQL", "Python"]))
            sol_key = f"solution_{mode_choice.lower()}"
            st.code(ex.get(sol_key, "Solution not yet added."), language='python' if mode_choice == "Python" else "sql")
            
            if 'deep_dive' in ex:
                st.markdown("#### 🧠 The 'Why' behind this logic")
                st.success(ex['deep_dive'])

    with col2:
        st.write("### 💻 Workspace")
        mode = st.radio("Language:", ex.get('allowed_modes', ["SQL", "Python"]), horizontal=True)
        user_code = st.text_area(f"Write your {mode} code here:", height=300, placeholder="Assign your final result to a variable named 'result'...")
        
        if st.button("🚀 Run Code"):
            try:
                if mode == "SQL":
                    result = duckdb.query(user_code).to_df()
                else:
                    ldict = {'df': df, 'pd': pd}
                    exec(user_code, globals(), ldict)
                    result = ldict.get('result', "Error: Please assign output to 'result' variable.")
                
                st.write("### 📤 Output")
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"Execution Error: {e}")
