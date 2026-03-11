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

category_options = {
    "Pandas (Python)": "python",
    "SQL and Pandas": "sql_and_pandas",
    "Sorting Algorithms": "sorting_algorithms"
}
selected_category = st.sidebar.selectbox("Select Category:", list(category_options.keys()))
folder_prefix = f"{category_options[selected_category]} > "

if selected_category == "Sorting Algorithms":
    level_options = {
        "Entry Level": "entry_algos",
        "Mid Level": "mid_algos",
        "Senior Level": "senior_algos",
        "Data Engineering (DE) Level": "de_algos"
    }
    selected_level = st.sidebar.selectbox("Select Level:", list(level_options.keys()))
    folder_prefix = f"sorting_algorithms > {level_options[selected_level]} > "

if not exercises:
    st.sidebar.warning("No exercises found in /exercises folder!")
    selected_key = None
else:
    filtered_exercises = {k: v for k, v in exercises.items() if k.startswith(folder_prefix)}
    if not filtered_exercises:
        st.sidebar.warning(f"No exercises found for {selected_category}!")
        selected_key = None
    else:
        selected_key = st.sidebar.selectbox("Select Exercise:", sorted(list(filtered_exercises.keys())))
        ex = filtered_exercises[selected_key]

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
                # 1. Run user code
                if mode == "SQL":
                    table_name = ex.get("table_name", "df")
                    duckdb.register(table_name, df)
                    result = duckdb.query(user_code).to_df()
                else:
                    ldict = {'df': df.copy(), 'pd': pd}
                    exec(user_code, ldict, ldict)
                    result = ldict.get('result', "Error: Please assign output to 'result' variable.")
                
                # 2. Run expected solution
                sol_key = f"solution_{mode.lower()}"
                expected_result = None
                if sol_key in ex and ex[sol_key]:
                    if mode == "SQL":
                        # We must re-register the df in case the user query messed with it, though it shouldn't
                        duckdb.register(table_name, df)
                        expected_result = duckdb.query(ex[sol_key]).to_df()
                    else:
                        sol_dict = {'df': df.copy(), 'pd': pd}
                        exec(ex[sol_key], sol_dict, sol_dict)
                        expected_result = sol_dict.get('result')

                # 3. Compare
                is_correct = False
                if isinstance(result, pd.DataFrame) and isinstance(expected_result, pd.DataFrame):
                    try:
                        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result.reset_index(drop=True), check_dtype=False)
                        is_correct = True
                    except Exception:
                        is_correct = False
                elif result == expected_result:
                    is_correct = True

                # 4. Display results
                if is_correct:
                    st.success("✅ Correct! Your code produced the expected output.")
                    st.write("### 📤 Your Output")
                    st.dataframe(result, use_container_width=True)
                else:
                    st.error("❌ Incorrect. Your output did not match the expected result.")
                    st.write("### 📤 Your Output")
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.write(result)
                    
                    st.write("### ✅ Reference Solution")
                    st.code(ex.get(sol_key, "No reference solution available."), language='python' if mode == "Python" else "sql")
                    
                    if expected_result is not None:
                        st.write("### 🎯 Expected Output")
                        st.dataframe(expected_result, use_container_width=True)
                        
            except Exception as e:
                st.error(f"Execution Error: {e}")
