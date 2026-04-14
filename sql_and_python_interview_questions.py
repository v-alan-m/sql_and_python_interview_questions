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
    "Sorting Algorithms": "sorting_algorithms",
    "Real-World Scenarios": "real_world_scenarios"
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
        selected_key = st.sidebar.selectbox(
            "Select Exercise:", 
            sorted(list(filtered_exercises.keys())),
            format_func=lambda x: x.split(" > ")[-1]
        )
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
    has_stages = "interview_stages" in ex
    stages = ex.get("interview_stages", [])
    total_stages = len(stages)

    # --- Mode & Stage session state ---
    mode_key = f"mode_{selected_key}"
    default_mode = ex.get('allowed_modes', ["SQL", "Python"])[0]
    current_mode = st.session_state.get(mode_key, default_mode)

    stage_key = f"stage_{selected_key}"
    if stage_key not in st.session_state:
        if has_stages:
            st.session_state[stage_key] = 1
        else:
            st.session_state[stage_key] = 0  # 0 = original exercise, 1..N = interview stages

    # If no stages exist, always show base exercise
    if not has_stages and st.session_state.get(stage_key, 0) > 0:
        st.session_state[stage_key] = 0
    elif has_stages and st.session_state.get(stage_key, 0) == 0:
        st.session_state[stage_key] = 1

    current_stage_idx = st.session_state[stage_key]

    # Determine active content based on stage
    if has_stages and current_stage_idx > 0:
        active_stage = stages[current_stage_idx - 1]
        active_title = f"Stage {active_stage['stage_number']} — {active_stage['title']}"
        active_scenario = active_stage["scenario"]
        active_data = active_stage["data"]
        active_hint = active_stage.get("hint", "No hint available.")
        if current_mode == "SQL" and "solution_sql" in active_stage:
            active_solution = active_stage.get("solution_sql", "No SQL solution available.")
        else:
            active_solution = active_stage.get("solution_code", "No solution available.")
        active_expected_output = active_stage.get("expected_output", None)
        active_evaluation = active_stage.get("evaluation_criteria", [])
        active_followups = active_stage.get("follow_up_probes", [])
    else:
        active_title = None
        active_scenario = ex["description"]
        active_data = ex["data"]
        active_hint = ex.get('hint_sql' if 'SQL' in ex.get('allowed_modes', ["SQL", "Python"]) else 'hint_python', "No hint available.")
        active_solution = ex.get("solution_python", "No solution available.")
        active_expected_output = None
        active_evaluation = []
        active_followups = []

    # --- Title ---
    if active_title:
        st.title(f"Problem: {ex['title']}")
        if "subtitle" in ex:
            st.caption(f"**Concepts:** {ex['subtitle']}")
        st.caption(f"🎤 **{active_title}**")
    else:
        st.title(f"Problem: {ex['title']}")
        if "subtitle" in ex:
            st.caption(f"**Concepts:** {ex['subtitle']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Objective / Scenario
        if active_title:
            st.markdown(f"### 🎯 Scenario\n{active_scenario}")
        else:
            st.markdown(f"### 📋 Objective\n{active_scenario}")

        # Data
        st.write("### 📥 Sample Data" if active_title else "### 📥 Input Data")
        df = active_data
        st.dataframe(df, use_container_width=True)

        # Hint
        with st.expander("💡 View Hint"):
            st.info(active_hint)

        # Reference Solution
        with st.expander("✅ View Reference Solution"):
            if active_title:
                lang = "sql" if current_mode == "SQL" else "python"
                st.code(active_solution, language=lang)
            else:
                mode_choice = st.selectbox("Solution for:", ex.get('allowed_modes', ["SQL", "Python"]))
                sol_key = f"solution_{mode_choice.lower()}"
                st.code(ex.get(sol_key, "Solution not yet added."), language='python' if mode_choice == "Python" else "sql")

            if 'deep_dive' in ex:
                st.markdown("#### 🧠 The 'Why' behind this logic")
                st.success(ex['deep_dive'])

        # Evaluation Criteria (stage only)
        if active_evaluation:
            with st.expander("🔍 What the Interviewer Evaluates"):
                for criterion in active_evaluation:
                    st.markdown(f"- {criterion}")

        # Expected Output (stage only)
        if active_expected_output is not None:
            with st.expander("📤 Expected Output"):
                st.dataframe(active_expected_output, use_container_width=True)

        # Follow-Up Probes (stage only)
        if active_followups:
            with st.expander("💬 Follow-Up Probes"):
                for j, probe in enumerate(active_followups, 1):
                    st.markdown(f"{j}. *{probe}*")

        # --- Conceptual Questions (MCQ) Section ---
        mcq_questions = ex.get("mcq_questions", [])
        if mcq_questions and has_stages:
            # Filter MCQs for current stage or all previous stages
            relevant_mcqs = [q for q in mcq_questions if q["stage_number"] <= current_stage_idx]
            if relevant_mcqs:
                st.markdown("### 🧠 Conceptual Questions")
                for i, mcq in enumerate(relevant_mcqs):
                    mcq_col1, mcq_col2 = st.columns([20, 1])
                    with mcq_col1:
                        st.markdown(f"**Q{i+1}.** {mcq['question']}")
                    with mcq_col2:
                        with st.popover("❓"):
                            st.markdown(mcq["explanation"])

                    # Radio buttons for options
                    options = [f"{opt['label']}) {opt['text']}" for opt in mcq["options"]]
                    answer_key = f"mcq_{selected_key}_{i}"
                    selected = st.radio(
                        "Select your answer:",
                        options,
                        key=answer_key,
                        label_visibility="collapsed"
                    )

                    # Check answer on selection
                    if selected:
                        selected_label = selected[0]  # Get "A", "B", "C", or "D"
                        correct_opt = next(o for o in mcq["options"] if o["is_correct"])
                        if selected_label == correct_opt["label"]:
                            st.success(f"✅ Correct! {correct_opt['label']}) {correct_opt['text']}")
                        else:
                            st.error(f"❌ Incorrect. The correct answer is {correct_opt['label']}) {correct_opt['text']}")
                    st.markdown("---")
                    
        # Big O Notation & Optimization (Cumulative)
        if current_stage_idx > 0 or "big_o_explanation" in ex:
            # We want to show base exercise explanation if no stages, or cumulative up to current stage
            explanations = []
            if "big_o_explanation" in ex:
                explanations.append(("Base Approach", ex["big_o_explanation"]))
            
            if has_stages and current_stage_idx > 0:
                for i in range(current_stage_idx):
                    stage_dict = stages[i]
                    if "big_o_explanation" in stage_dict:
                        title = stage_dict.get('title', f"Stage {i+1}")
                        explanations.append((f"Stage {i+1} : {title}", stage_dict["big_o_explanation"]))
                        
            if explanations:
                with st.expander("⏱️ Big O Notation & Optimization"):
                    for title, exp in explanations:
                        st.markdown(f"#### {title}")
                        st.markdown(exp)
                        st.markdown("---")

    with col2:
        st.write("### 💻 Workspace")
        mode = st.radio("Language:", ex.get('allowed_modes', ["SQL", "Python"]), horizontal=True, key=mode_key)
        user_code = st.text_area(f"Write your {mode} code here:", height=300, placeholder="Assign your final result to a variable named 'result'...")

        # --- Run Code + Stage Navigation Buttons ---
        if has_stages:
            btn_cols = st.columns([2, 1, 1, 1])
            with btn_cols[0]:
                run_clicked = st.button("🚀 Run Code")
            with btn_cols[1]:
                stage_label = f"Stage {current_stage_idx}/{total_stages}" if current_stage_idx > 0 else "Original"
                st.markdown(f"<div style='text-align:center; padding-top:6px; font-weight:600; color:#6c757d;'>{stage_label}</div>", unsafe_allow_html=True)
            with btn_cols[2]:
                prev_disabled = current_stage_idx <= 1
                if st.button("◀ Prev", disabled=prev_disabled):
                    st.session_state[stage_key] = current_stage_idx - 1
                    st.rerun()
            with btn_cols[3]:
                next_disabled = current_stage_idx >= total_stages
                if st.button("Next ▶", disabled=next_disabled):
                    st.session_state[stage_key] = current_stage_idx + 1
                    st.rerun()
        else:
            run_clicked = st.button("🚀 Run Code")

        if run_clicked:
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

                # 2. Determine expected solution
                if active_title:
                    # Stage mode: run the stage solution code
                    expected_result = active_expected_output
                else:
                    # Original mode: run the exercise solution
                    sol_key = f"solution_{mode.lower()}"
                    expected_result = None
                    if sol_key in ex and ex[sol_key]:
                        if mode == "SQL":
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
                        # Normalize datetime columns so DuckDB date types
                        # match expected_output datetime64 types
                        result_cmp = result.reset_index(drop=True).copy()
                        expected_cmp = expected_result.reset_index(drop=True).copy()
                        for col in expected_cmp.columns:
                            if col in result_cmp.columns:
                                if str(expected_cmp[col].dtype).startswith('datetime64'):
                                    result_cmp[col] = pd.to_datetime(result_cmp[col])
                                elif str(result_cmp[col].dtype).startswith('datetime64'):
                                    expected_cmp[col] = pd.to_datetime(expected_cmp[col])
                        pd.testing.assert_frame_equal(result_cmp, expected_cmp, check_dtype=False)
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
                    if active_title:
                        st.code(active_solution, language="python")
                    else:
                        st.code(ex.get(sol_key, "No reference solution available."), language='python' if mode == "Python" else "sql")

                    if expected_result is not None:
                        st.write("### 🎯 Expected Output")
                        st.dataframe(expected_result, use_container_width=True)

            except Exception as e:
                st.error(f"Execution Error: {e}")
