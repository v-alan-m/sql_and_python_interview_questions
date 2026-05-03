import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
/* Global soft white text for a premium look */
.stApp {
    opacity: 0.75;
}

/* Reduce top padding of the main container */
.block-container {
    padding-top: 2.6rem !important;
    padding-bottom: 4rem !important;
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
 .scenario-text, .scenario-text p {
    font-weight: 400 !important;
    font-size: 1.25rem !important;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.9);
}

/* Premium Code Highlighting (One Dark inspired) */
code, pre {
    font-family: 'Fira Code', 'JetBrains Mono', 'Roboto Mono', monospace !important;
}

.token.keyword, .token.selector, .token.changed { color: #c678dd !important; } /* Purple */
.token.function, .token.attr-name { color: #61afef !important; } /* Blue */
.token.string, .token.char, .token.attr-value { color: #98c379 !important; } /* Green */
.token.number, .token.constant, .token.boolean { color: #d19a66 !important; } /* Orange */
.token.operator, .token.punctuation, .token.property { color: #56b6c2 !important; } /* Cyan */
.token.comment { color: #5c6370 !important; font-style: italic !important; } /* Grey */
.token.class-name, .token.type, .token.builtin { color: #e5c07b !important; } /* Yellow */
.token.regex, .token.important, .token.variable { color: #e06c75 !important; } /* Red */

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

/* Bottom-alignment for MCQ navigation buttons and code blocks */
.exercise-layout [data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

.exercise-layout [data-testid="stHorizontalBlock"] > div [data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important;
}

/* Ensure the scenario text area grows to fill space, pushing content down */
.scenario-text {
    display: flex !important;
    flex-direction: column !important;
    flex-grow: 1 !important;
}

/* Push the internal code block (pre) to the bottom of the scenario area */
.scenario-text pre {
    margin-top: auto !important;
}

/* Push the last element of each column (MCQ group, Buttons, or Data) to the bottom */
.exercise-layout [data-testid="stHorizontalBlock"] > div [data-testid="stVerticalBlock"] > div:last-child {
    margin-top: auto !important;
}

/* Fixed gap between MCQ questions and navigation buttons within their group */
.mcq-nav-gap {
    margin-top: 2.2rem !important;
}

/* Increase starting width of the sidebar */
[data-testid="stSidebar"][aria-expanded="true"],
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 315px !important;
}

/* Premium Center Metric in Sidebar */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.03);
    padding: 0.4rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin-bottom: 0.4rem !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] > div {
    justify-content: center !important;
    color: rgba(255, 255, 255, 0.6) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] > div {
    justify-content: center !important;
    font-weight: 700 !important;
}

/* Sidebar Header spacing - adds more breathing room below 'Training Menu' */
[data-testid="stSidebar"] h2 {
    margin-bottom: 0.8rem !important;
    margin-top: 0.4rem !important;
}

/* Style the sidebar radio as a list of premium boxes */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
    gap: 8px !important;
    padding-top: 8px !important;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: space-between !important;
    align-items: center !important;
    padding: 0px 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    background-color: #0E1117 !important; /* Match dropdown background */
    cursor: pointer !important;
    width: 100% !important;
    height: 45px !important; /* Match dropdown height */
    transition: all 0.2s ease !important;
}

/* Hover state */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:hover {
    background-color: rgba(31, 244, 151, 0.15) !important;
    border-color: rgba(31, 244, 151, 0.4) !important;
}

/* Selected state */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked),
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label[data-selected="true"] {
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    background-color: #0E1117 !important;
}

/* Hide the default radio circle */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Create the custom tick box on the right */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label::before {
    content: "";
    display: inline-block;
    width: 18px;
    height: 18px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    background-color: transparent;
    transition: all 0.2s ease;
    flex-shrink: 0;
}

/* Show tick in the custom box when selected */
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked)::before,
[data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] label[data-selected="true"]::before {
    background-color: rgba(255, 255, 255, 0.8) !important;
    border-color: rgba(255, 255, 255, 0.8) !important;
    content: "";
    color: #0E1117;
    font-size: 13px;
    line-height: 18px;
    text-align: center;
}

/* Premium Green Hover for action buttons */
div[data-testid="stButton"] button:hover:not(:disabled) {
    background-color: rgba(31, 244, 151, 0.15) !important;
    border-color: rgba(31, 244, 151, 0.4) !important;
}

/* Quiz Mode Button - Yellow */
.st-key-quiz_mode_btn button,
.st-key-quiz_mode_btn div[data-testid="stButton"] button,
div[data-testid="stButton"].st-key-quiz_mode_btn button {
    background-color: rgba(255, 215, 0, 0.02) !important;
    border: 1px solid rgba(255, 215, 0, 0.2) !important;
    color: rgba(255, 255, 255, 0.8) !important;
}
.st-key-quiz_mode_btn button:hover:not(:disabled),
.st-key-quiz_mode_btn div[data-testid="stButton"] button:hover:not(:disabled),
div[data-testid="stButton"].st-key-quiz_mode_btn button:hover:not(:disabled) {
    background-color: rgba(255, 234, 0, 0.25) !important;
    border-color: rgba(255, 234, 0, 0.5) !important;
    color: #FFFFFF !important;
}

/* Number Input Plus/Minus Buttons - Green Hover & Focus */
div[data-testid="stNumberInput"] button:hover,
div[data-testid="stNumberInput"] button:focus,
div[data-testid="stNumberInput"] button:active,
div[data-testid="stNumberInputStepUp"] button:hover,
div[data-testid="stNumberInputStepUp"] button:focus,
div[data-testid="stNumberInputStepUp"] button:active,
div[data-testid="stNumberInputStepDown"] button:hover,
div[data-testid="stNumberInputStepDown"] button:focus,
div[data-testid="stNumberInputStepDown"] button:active {
    background-color: rgba(31, 244, 151, 0.25) !important;
    border-color: rgba(31, 244, 151, 0.5) !important;
    color: #1FF497 !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)
