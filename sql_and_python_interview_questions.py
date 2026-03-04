import streamlit as st
import pandas as pd
import duckdb
import time

# --- APP CONFIG ---
st.set_page_config(page_title="DE Interview Pro", layout="wide")
st.title("🚀 Data Engineering Interview Practice Lab")

# --- SAMPLE DATA GENERATION ---
data = {
    'user_id': [101, 102, 101, 103, 102, 101],
    'timestamp': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-01', '2025-01-04', '2025-01-05']),
    'revenue': [50, 150, 200, 50, 300, 100],
    'category': ['Tech', 'Health', 'Tech', 'Retail', 'Health', 'Tech']
}
df = pd.DataFrame(data)

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("Practice Settings")
category = st.sidebar.selectbox("Choose a Pattern:", 
    ["Deduplication (Latest Record)", "Cumulative Revenue", "Category Aggregates", "String Mutation"])

# Timer Logic
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

timer_placeholder = st.sidebar.empty()
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, 1200 - elapsed) # 20 minute limit
timer_placeholder.metric("Time Remaining", f"{remaining // 60}:{remaining % 60:02d}")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Inspect Source Data")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("2. Problem Statement")
    if category == "Deduplication (Latest Record)":
        st.write("Find the **most recent** record for each `user_id` based on the `timestamp`.")
    elif category == "Cumulative Revenue":
        st.write("Calculate a **running total** of revenue ordered by timestamp.")
    elif category == "String Mutation":
        st.write("Create a new column where 'Category' is converted to Pig Latin (move 1st letter to end + 'ay').")

with col2:
    mode = st.radio("Solution Mode:", ["SQL (DuckDB)", "Python (Pandas)"], horizontal=True)
    
    # Code Input
    if mode == "SQL (DuckDB)":
        default_code = "SELECT * FROM df LIMIT 5"
        user_code = st.text_area("Write your SQL here (Refer to table as 'df'):", default_code, height=200)
    else:
        default_code = "df.head(5)"
        user_code = st.text_area("Write your Python/Pandas here:", default_code, height=200)

    if st.button("▶ Run Solution"):
        st.subheader("Results")
        try:
            if mode == "SQL (DuckDB)":
                result = duckdb.query(user_code).to_df()
            else:
                # Security note: In a real app, use a safer eval/exec method
                # This is for local practice only
                local_vars = {'df': df, 'pd': pd}
                exec(f"st.session_state['res'] = {user_code}", {}, local_vars)
                result = st.session_state['res']
            
            st.dataframe(result, use_container_width=True)
            st.success("Code executed successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- FOOTER ---
st.divider()
if st.checkbox("Show Hint"):
    if mode == "SQL (DuckDB)":
        st.info("Hint: Use ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY timestamp DESC)")
    else:
        st.info("Hint: Try df.sort_values().drop_duplicates(subset=['user_id'], keep='first')")
