import streamlit as st
import time
from ui_components import render_exercise
from core import ExerciseManager

class QuizApp:
    def __init__(self, ex_manager: ExerciseManager):
        self.ex_manager = ex_manager

    def render(self):
        if 'quiz_state' not in st.session_state:
            st.session_state.quiz_state = 'selection'  # 'selection', 'execution', 'summary'
        
        if st.session_state.quiz_state == 'selection':
            self.render_selection_screen()
        elif st.session_state.quiz_state == 'execution':
            self.render_execution_screen()
        elif st.session_state.quiz_state == 'summary':
            self.render_summary_screen()

    def render_selection_screen(self):
        st.title("Quiz Setup")
        
        # Load presets for sidebar
        import json
        import os
        preset_file = "quiz_presets.json"
        presets = {}
        if os.path.exists(preset_file):
            try:
                with open(preset_file, "r") as f:
                    presets = json.load(f)
            except:
                presets = {}
        
        with st.sidebar:
            st.header("Quiz Presets")
            
            # Save As Preset UI
            preset_name = st.text_input("Save As Preset:", placeholder="Enter name...", key="preset_name_input")
            
            st.markdown("""
            <style>
            .st-key-save_preset_btn button {
                background-color: rgba(255, 215, 0, 0.1) !important;
                border: 1px solid rgba(255, 215, 0, 0.3) !important;
                color: rgba(255, 255, 255, 0.8) !important;
                margin-bottom: 25px !important;
            }
            .st-key-save_preset_btn button:hover:not(:disabled),
            .st-key-save_preset_btn div[data-testid="stButton"] button:hover:not(:disabled),
            div[data-testid="stButton"].st-key-save_preset_btn button:hover:not(:disabled) {
                background-color: rgba(255, 215, 0, 0.25) !important;
                border-color: rgba(255, 215, 0, 0.5) !important;
                color: #FFFFFF !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button("Save Preset", use_container_width=True, key="save_preset_btn"):
                selected_to_save = st.session_state.get('selected_quiz_exercises', [])
                if not preset_name:
                    st.error("Please enter a preset name.")
                elif not selected_to_save:
                    st.error("Please select at least one exercise to save.")
                else:
                    duration_to_save = st.session_state.get("quiz_duration_input", 10)
                    presets[preset_name] = {
                        "exercises": selected_to_save,
                        "duration": duration_to_save
                    }
                    try:
                        with open(preset_file, "w") as f:
                            json.dump(presets, f, indent=4)
                        st.success(f"Preset '{preset_name}' saved!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to save preset: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
            preset_names = ["None"] + list(presets.keys())
            
            current_preset = st.session_state.get('last_preset', "None")
            if current_preset not in preset_names:
                current_preset = "None"
            preset_index = preset_names.index(current_preset)
            
            selected_preset = st.radio(
                "Select Preset:",
                preset_names,
                index=preset_index,
                key="preset_radio"
            )
            
            if selected_preset != "None" and st.session_state.get('last_preset') != selected_preset:
                st.session_state.last_preset = selected_preset
                exercises = presets[selected_preset].get("exercises", [])
                st.session_state.selected_quiz_exercises = exercises
                st.session_state.quiz_duration = presets[selected_preset].get("duration", 10)
                
                # Explicitly sync checkbox states
                for key in self.ex_manager.exercises.keys():
                    st.session_state[f"chk_{key}"] = key in exercises
                    
                st.rerun()
            elif selected_preset == "None" and 'last_preset' in st.session_state:
                del st.session_state.last_preset
            if selected_preset != "None":
                st.markdown("""
                <style>
                .st-key-delete_preset_btn button {
                    background-color: rgba(255, 0, 0, 0.1) !important;
                    border: 1px solid rgba(255, 0, 0, 0.3) !important;
                    color: rgba(255, 255, 255, 0.8) !important;
                    margin-top: 10px !important;
                }
                .st-key-delete_preset_btn button:hover:not(:disabled),
                .st-key-delete_preset_btn div[data-testid="stButton"] button:hover:not(:disabled),
                div[data-testid="stButton"].st-key-delete_preset_btn button:hover:not(:disabled) {
                    background-color: rgba(255, 0, 0, 0.25) !important;
                    border-color: rgba(255, 0, 0, 0.5) !important;
                    color: #FFFFFF !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("Delete Preset", use_container_width=True, key="delete_preset_btn"):
                    if selected_preset in presets:
                        del presets[selected_preset]
                        try:
                            with open(preset_file, "w") as f:
                                json.dump(presets, f, indent=4)
                            st.session_state.last_preset = "None"
                            for key in self.ex_manager.exercises.keys():
                                st.session_state[f"chk_{key}"] = False
                            st.session_state.selected_quiz_exercises = []
                            st.success(f"Preset '{selected_preset}' deleted!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete preset: {e}")
                st.markdown('</div>', unsafe_allow_html=True)
        # Inject custom CSS for checkboxes and start button
        st.markdown("""
        <style>
        /* Style checkboxes to look like premium rows */
        div[data-testid="stCheckbox"] {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            background-color: #0E1117 !important;
            padding: 0px 14px !important;
            transition: all 0.2s ease !important;
            margin-bottom: 8px !important;
            cursor: pointer !important;
            height: 45px !important;
            display: flex !important;
            align-items: center !important;
        }
        div[data-testid="stCheckbox"]:hover {
            background-color: rgba(31, 244, 151, 0.15) !important;
            border-color: rgba(31, 244, 151, 0.4) !important;
        }
        div[data-testid="stCheckbox"] label {
            display: flex !important;
            flex-direction: row-reverse !important;
            justify-content: space-between !important;
            align-items: center !important;
            width: 100% !important;
            height: 100% !important;
            cursor: pointer !important;
        }
        /* Hide default checkbox visual */
        div[data-testid="stCheckbox"] label > span:first-child,
        div[data-testid="stCheckbox"] label > div:first-child {
            display: none !important;
        }
        /* Create custom tick box on the right */
        div[data-testid="stCheckbox"] label::before {
            content: "";
            display: inline-block;
            width: 18px;
            height: 18px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            background-color: transparent;
            transition: all 0.2s ease;
            flex-shrink: 0;
            margin-left: 12px !important;
        }
        /* Show tick when selected */
        div[data-testid="stCheckbox"]:has(input:checked) label::before,
        div[data-testid="stCheckbox"] label:has(input:checked)::before {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.8) !important;
        }
        /* Custom start button with yellow hover */
        .st-key-start_quiz_btn button {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        .st-key-start_quiz_btn button:hover:not(:disabled),
        .st-key-start_quiz_btn div[data-testid="stButton"] button:hover:not(:disabled),
        div[data-testid="stButton"].st-key-start_quiz_btn button:hover:not(:disabled) {
            background-color: rgba(255, 215, 0, 0.15) !important; /* Yellow hover */
            border-color: rgba(255, 215, 0, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Group exercises by top-level category and sub-topic
        categories = list(self.ex_manager.category_options.values())
        display_category_map = {v: k for k, v in self.ex_manager.category_options.items()}
        
        sub_topic_map = {}
        for k, v in self.ex_manager.sub_options.items():
            sub_topic_map[v] = k
        for k, v in self.ex_manager.level_options.items():
            sub_topic_map[v] = k

        topics = {cat: {} for cat in categories}
        for key, ex in self.ex_manager.exercises.items():
            parts = key.split(" > ")
            top_level = parts[0]
            if top_level in topics:
                sub_topic = parts[1] if len(parts) > 2 else "General"
                name = parts[-1]
                if sub_topic not in topics[top_level]:
                    topics[top_level][sub_topic] = []
                topics[top_level][sub_topic].append((key, name))
            else:
                if "General" not in topics:
                    topics["General"] = {"General": []}
                name = parts[-1]
                topics["General"]["General"].append((key, name))

        if 'selected_quiz_exercises' not in st.session_state:
            st.session_state.selected_quiz_exercises = []

        # Duration Input at the top
        default_duration = st.session_state.get('quiz_duration', 10)
        if not isinstance(default_duration, int):
            default_duration = 10
        quiz_duration = st.number_input("Quiz Duration (minutes)", min_value=1, value=default_duration, step=1, key="quiz_duration_input")

        st.write("Select the exercises you want to include in your quiz session:")

        # Create columns based on the number of topics (excluding empty ones)
        active_topics = {k: v for k, v in topics.items() if any(v.values())}
        cols = st.columns(len(active_topics))
        
        selected = []
        for i, (topic, sub_topics) in enumerate(active_topics.items()):
            with cols[i]:
                title = display_category_map.get(topic, topic.replace("_", " ").title())
                st.markdown(f"<h3 style='color: rgba(255,255,255,0.9); margin-top: 20px; font-size: 1.4rem; font-weight: 600;'>{title}</h3>", unsafe_allow_html=True)
                
                for sub_topic, exercises in sub_topics.items():
                    if sub_topic != "General" or len(sub_topics) > 1:
                        sub_title = sub_topic_map.get(sub_topic, sub_topic.replace("_", " ").title())
                        st.markdown(f"<h4 style='color: rgba(255,255,255,0.6); margin-top: 10px; font-size: 1.0rem; font-weight: 400;'>{sub_title}</h4>", unsafe_allow_html=True)
                    
                    for key, name in sorted(exercises, key=lambda x: x[1]):
                        is_checked = key in st.session_state.selected_quiz_exercises
                        if st.checkbox(name, value=is_checked, key=f"chk_{key}"):
                            selected.append(key)
        
        st.session_state.selected_quiz_exercises = selected

        st.divider()
        
        # Centered Start Button
        _, btn_col, _ = st.columns([0.8, 0.4, 0.8])
        with btn_col:
            st.markdown('<div class="start-btn">', unsafe_allow_html=True)
            if st.button("Start Quiz", use_container_width=True, key="start_quiz_btn"):
                if not st.session_state.selected_quiz_exercises:
                    st.error("Please select at least one exercise.")
                else:
                    st.session_state.quiz_duration = quiz_duration
                    st.session_state.quiz_state = 'execution'
                    st.session_state.quiz_start_time = time.time()
                    st.session_state.quiz_current_index = 0
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    def render_execution_screen(self):
        exercises = st.session_state.selected_quiz_exercises
        current_idx = st.session_state.quiz_current_index
        total_q = len(exercises)
        
        # We use a fragment to update the timer smoothly without rerunning the whole page
        self.render_progress_bars(current_idx, total_q)

        current_key = exercises[current_idx]
        ex = self.ex_manager.exercises[current_key]
        
        # Render the exercise
        category = current_key.split(" > ")[0] if " > " in current_key else "General"
        render_exercise(ex, current_key, category)
        
        st.divider()
        col1, col2 = st.columns([1, 1])
        with col1:
             if st.button("End Quiz Early", use_container_width=True):
                 st.session_state.quiz_state = 'summary'
                 st.rerun()
        with col2:
            if current_idx < total_q - 1:
                if st.button("Next Question", use_container_width=True, type="primary"):
                    st.session_state.quiz_current_index += 1
                    st.rerun()
            else:
                if st.button("Finish Quiz", use_container_width=True, type="primary"):
                    st.session_state.quiz_state = 'summary'
                    st.rerun()

    @st.fragment(run_every="1s")
    def render_progress_bars(self, current_idx, total_q):
        elapsed = time.time() - st.session_state.quiz_start_time
        total_time_sec = st.session_state.quiz_duration * 60
        time_progress = min(elapsed / total_time_sec, 1.0)
        
        q_progress = current_idx / total_q

        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-bottom: 4px;">Question Progress ({current_idx}/{total_q})</div>
            <div style="width: 100%; height: 12px; background-color: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden;">
                <div style="width: {q_progress * 100}%; height: 100%; background-color: #1FF497; transition: width 0.3s;"></div>
            </div>
        </div>
        <div style="margin-bottom: 25px;">
            <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-bottom: 4px;">Time Used ({int(elapsed//60)}m {int(elapsed%60):02d}s / {st.session_state.quiz_duration}m)</div>
            <div style="width: 100%; height: 12px; background-color: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden;">
                <div style="width: {time_progress * 100}%; height: 100%; background-color: #FFD700; transition: width 1s linear;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if time_progress >= 1.0:
            st.error("Time is up!")

    def render_summary_screen(self):
        st.title("Quiz Completed!")
        st.success("Great job on finishing the quiz.")
        
        elapsed = time.time() - st.session_state.quiz_start_time
        st.write(f"**Total Time:** {int(elapsed//60)}m {int(elapsed%60)}s")
        st.write(f"**Questions Viewed:** {st.session_state.quiz_current_index + 1} / {len(st.session_state.selected_quiz_exercises)}")
        
        if st.button("Return to Setup", use_container_width=True):
            st.session_state.quiz_state = 'selection'
            st.rerun()
        if st.button("Return to Normal Mode", use_container_width=True):
            st.session_state.app_mode = 'normal'
            st.rerun()
