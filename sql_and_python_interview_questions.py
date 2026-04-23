import streamlit as st
import pandas as pd
import duckdb
import os
import importlib.util
import time

# --- APP CONFIG ---
st.set_page_config(page_title="DE Interview Lab Pro", layout="wide")

# Global CSS Tweaks
st.markdown("""
<style>
/* Global soft white text for a premium look */
.stApp {
    opacity: 0.75;
}

/* Reduce top padding of the main container */
.block-container {
    padding-top: 2.6rem !important;
    padding-bottom: 0rem !important;
}

/* Default state (closed): Perfectly transparent border */
div[data-testid="stExpander"] details {
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    transition: border 0.3s ease, background-color 0.3s ease;
}

/* Visible state (open): The border reveals itself when the user clicks/expands */
div[data-testid="stExpander"] details[open] {
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    background-color: rgba(255, 255, 255, 0.02);
}

/* Reduced padding for the divider line and matched it to the MCQ highlight blue */
hr {
    margin-top: 1.7rem !important;
    margin-bottom: 1.7rem !important;
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Strips the default Streamlit container border/shadow to clear the visual clutter */
div[data-testid="stExpander"] {
    border: none !important;
    box-shadow: none !important;
}
 
 /* Ensures Scenario/Objective descriptions are not bold but keep H4 size */
 .scenario-text h4 {
    font-weight: 400 !important;
    font-size: 1.3rem !important;
    line-height: 1.6;
}

/* Premium Typography for Concepts & Stages */
.concepts-subtitle {
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.03rem !important;
    font-weight: 400 !important;
    text-align: center !important;
}

.stage-indicator {
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 1.3rem !important;
    font-weight: 400 !important;
    margin-top: 4px !important;
    margin-bottom: 12px !important;
    text-align: center !important;
}

h1 {
    text-align: center !important;
}

.header-spacing {
    margin-top: 2.2rem !important;
}
</style>
""", unsafe_allow_html=True)

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
st.sidebar.header("Training Menu")

category_options = {
    "Python (Core)": "python_core",
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

if selected_category == "Python (Core)":
    sub_options = {
        "System": "python_system",
        "Coding": "python_coding"
    }
    selected_sub = st.sidebar.selectbox("Select Topic:", list(sub_options.keys()))
    folder_prefix = f"python_core > {sub_options[selected_sub]} > "

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

@st.fragment(run_every="1s")
def display_timer():
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 300 - elapsed)
    st.metric("Session Timer", f"{remaining // 60}:{remaining % 60:02d}")

with st.sidebar:
    display_timer()

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
        active_title = f"Stage {active_stage['stage_number']} - {active_stage['title']}"
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
            st.markdown(f"<div class='concepts-subtitle'>Concepts: {ex['subtitle']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stage-indicator'>{active_title}</div>", unsafe_allow_html=True)
    else:
        st.title(f"Problem: {ex['title']}")
        if "subtitle" in ex:
            st.markdown(f"<div class='concepts-subtitle'>Concepts: {ex['subtitle']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.88, 0.99], gap="large")

    with col1:
        # Objective / Scenario
        if active_title:
            st.markdown(f"<div class='header-spacing'>\n\n## Scenario\n<div class='scenario-text'>\n\n#### {active_scenario}\n\n</div>\n</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='header-spacing'>\n\n## Objective\n<div class='scenario-text'>\n\n#### {active_scenario}\n\n</div>\n</div>", unsafe_allow_html=True)

        # Data
        st.write("## Sample Data" if active_title else "### Input Data")
        df = active_data
        if isinstance(df, pd.DataFrame):
            st.dataframe(df, use_container_width=True)
        elif isinstance(df, str):
            st.code(df, language="python")
        else:
            st.write(df)

        # --- Conceptual Questions (MCQ) Section ---
        pass

    with col2:
        is_python_mcq = selected_category == "Python (Core)" and ex.get("mcq_questions")
        run_clicked = False

        if is_python_mcq:
            # Add top margin to align with Scenario
            st.markdown("<div class='header-spacing'></div>", unsafe_allow_html=True)
            # st.write("### Conceptual Questions")
            
            # Modern CSS for MCQ Premium cards
            st.markdown("""
            <style>
            /* Container styling (matching the expander aesthetic) */
            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 12px !important;
            }

            /* Targeting radio buttons to look like cards */
            div[data-testid="stRadio"] [role="radiogroup"] {
                gap: 10px;
                padding-top: 10px;
            }

            div[data-testid="stRadio"] [role="radiogroup"] label {
                padding: 14px 20px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 10px !important;
                background-color: rgba(255, 255, 255, 0.02) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                cursor: pointer !important;
                width: 100%;
            }

            div[data-testid="stRadio"] [role="radiogroup"] label:hover {
                border-color: rgba(30, 144, 255, 0.5) !important;
                background-color: rgba(30, 144, 255, 0.08) !important;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            
            /* Highlighting selected option (Simplified approach for Streamlit) */
            div[data-testid="stRadio"] [role="radiogroup"] label[data-selected="true"] {
                border-color: #1E90FF !important;
                background-color: rgba(30, 144, 255, 0.1) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            mcq_questions = ex.get("mcq_questions", [])
            relevant_mcqs = [q for q in mcq_questions if q["stage_number"] <= current_stage_idx] if has_stages else mcq_questions
            
            for i, mcq in enumerate(relevant_mcqs):
                with st.container():
                    mcq_col1, mcq_col2 = st.columns([20, 1])
                    with mcq_col1:
                        if len(relevant_mcqs) > 1:
                            st.markdown(f"#### Q{i+1}")
                        # st.markdown(f"#### Q{i+1}. {mcq['question']}")
                    with mcq_col2:
                        with st.popover("?", help="Click for explanation"):
                            st.markdown("### Explanation")
                            st.info(mcq["explanation"])

                    # Radio buttons for options
                    options = [f"{opt['label']}) {opt['text']}" for opt in mcq["options"]]
                    answer_key = f"mcq_{selected_key}_{i}"
                    
                    selected = st.radio(
                        "Select your answer:",
                        options,
                        key=answer_key,
                        index=None,
                        label_visibility="collapsed"
                    )

                    # Check answer on selection
                    if selected:
                        selected_label = selected[0]  # Get "A", "B", "C", or "D"
                        correct_opt = next(o for o in mcq["options"] if o["is_correct"])
                        if selected_label == correct_opt["label"]:
                            st.success(f"**Correct!** {correct_opt['label']}) {correct_opt['text']}")
                        else:
                            st.error(f"**Incorrect.** The correct answer is {correct_opt['label']}) {correct_opt['text']}")

            # --- Stage Navigation Buttons ---
            if has_stages:
                btn_cols = st.columns([5, 1.2, 1, 1])
                with btn_cols[1]:
                    stage_label = f"Stage {current_stage_idx}/{total_stages}" if current_stage_idx > 0 else "Original"
                    st.markdown(f"<div style='text-align:center; padding-top:6px; font-weight:600; color:#6c757d;'>{stage_label}</div>", unsafe_allow_html=True)
                with btn_cols[2]:
                    prev_disabled = current_stage_idx <= 1
                    if st.button("Prev", disabled=prev_disabled, use_container_width=True):
                        st.session_state[stage_key] = current_stage_idx - 1
                        st.rerun()
                with btn_cols[3]:
                    next_disabled = current_stage_idx >= total_stages
                    if st.button("Next", disabled=next_disabled, use_container_width=True):
                        st.session_state[stage_key] = current_stage_idx + 1
                        st.rerun()
        else:
            st.markdown("<div class='header-spacing'>\n\n## Workspace\n\n</div>", unsafe_allow_html=True)
            mode = st.radio("Language:", ex.get('allowed_modes', ["SQL", "Python"]), horizontal=True, key=mode_key)
            user_code = st.text_area(f"Write your {mode} code here:", height=300, placeholder="Assign your final result to a variable named 'result'...")

            # --- Run Code + Stage Navigation Buttons ---
            if has_stages:
                btn_cols = st.columns([2, 3, 1.2, 1, 1])
                with btn_cols[0]:
                    run_clicked = st.button("Run Code", use_container_width=True)
                with btn_cols[2]:
                    stage_label = f"Stage {current_stage_idx}/{total_stages}" if current_stage_idx > 0 else "Original"
                    st.markdown(f"<div style='text-align:center; padding-top:6px; font-weight:600; color:#6c757d;'>{stage_label}</div>", unsafe_allow_html=True)
                with btn_cols[3]:
                    prev_disabled = current_stage_idx <= 1
                    if st.button("Prev", disabled=prev_disabled, use_container_width=True):
                        st.session_state[stage_key] = current_stage_idx - 1
                        st.rerun()
                with btn_cols[4]:
                    next_disabled = current_stage_idx >= total_stages
                    if st.button("Next", disabled=next_disabled, use_container_width=True):
                        st.session_state[stage_key] = current_stage_idx + 1
                        st.rerun()
            else:
                run_clicked = st.button("Run Code")

        if run_clicked:
            try:
                # 1. Run user code
                if mode == "SQL":
                    table_name = ex.get("table_name", "df")
                    duckdb.register(table_name, df)
                    result = duckdb.query(user_code).to_df()
                else:
                    ldict = {'pd': pd}
                    if isinstance(df, pd.DataFrame):
                        ldict['df'] = df.copy()
                    elif isinstance(df, str):
                        ldict['data_snippet'] = df
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
                            sol_dict = {'pd': pd}
                            if isinstance(df, pd.DataFrame):
                                sol_dict['df'] = df.copy()
                            elif isinstance(df, str):
                                sol_dict['data_snippet'] = df
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
                    st.success("Correct! Your code produced the expected output.")
                    st.write("### Your Output")
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.write(result)
                else:
                    st.error("Incorrect. Your output did not match the expected result.")
                    st.write("### Your Output")
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.write(result)

                    st.write("### Reference Solution")
                    if active_title:
                        st.code(active_solution, language="python")
                    else:
                        st.code(ex.get(sol_key, "No reference solution available."), language='python' if mode == "Python" else "sql")

                    if expected_result is not None:
                        st.write("### Expected Output")
                        st.dataframe(expected_result, use_container_width=True)

            except Exception as e:
                st.error(f"Execution Error: {e}")

    # --- Reference Area (Below the fold) ---
    st.divider()
    
    ref_col1, ref_col2 = st.columns([1, 1])
    with ref_col1:
        # Hint
        with st.expander("View Hint"):
            st.info(active_hint)

        # Reference Solution
        with st.expander("View Reference Solution"):
            if active_title:
                lang = "sql" if current_mode == "SQL" else "python"
                st.code(active_solution, language=lang)
            else:
                mode_choice = st.selectbox("Solution for:", ex.get('allowed_modes', ["SQL", "Python"]))
                sol_key = f"solution_{mode_choice.lower()}"
                st.code(ex.get(sol_key, "Solution not yet added."), language='python' if mode_choice == "Python" else "sql")

            if 'deep_dive' in ex:
                st.markdown("#### The 'Why' behind this logic")
                st.success(ex['deep_dive'])

        # Evaluation Criteria (stage only)
        if active_evaluation:
            with st.expander("What the Interviewer Evaluates"):
                for criterion in active_evaluation:
                    st.markdown(f"- {criterion}")

        # Expected Output (stage only)
        if active_expected_output is not None:
            with st.expander("Expected Output"):
                if isinstance(active_expected_output, pd.DataFrame):
                    st.dataframe(active_expected_output, use_container_width=True)
                else:
                    st.write(active_expected_output)

        # Follow-Up Probes (stage only)
        if active_followups:
            with st.expander("Follow-Up Probes"):
                for j, probe in enumerate(active_followups, 1):
                    st.markdown(f"{j}. *{probe}*")

        # Big O Notation & Optimization (Cumulative)
        if current_stage_idx > 0 or "big_o_explanation" in ex:
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
                with st.expander("Big O Notation & Optimization"):
                    for title, exp in explanations:
                        st.markdown(f"#### {title}")
                        st.markdown(exp)
                        st.markdown("---")
