import streamlit as st

# Page Configuration
st.set_page_config(page_title="Calculator", layout="centered")

# Custom CSS for Dark Theme and Calculator Buttons Alignment
st.markdown("""
    <style>
    /* Dark background */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Screen display styling */
    .display-screen {
        background-color: #000000;
        color: #ffffff;
        font-size: 48px;
        text-align: right;
        padding: 20px;
        font-weight: 300;
        min-height: 80px;
        word-wrap: break-word;
    }

    /* Base style for all buttons */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 28px !important;
        border-radius: 50% !important;
        border: none !important;
        background-color: #1c1c1e !important;
        color: #ffffff !important;
        font-weight: 400;
    }

    /* Red Text Button (Clear) */
    div.stButton > button[data-testid="baseButton-secondary"]:nth-child(1) {
        color: #ff5252 !important;
    }

    /* Equal Button Style */
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton > button {
        color: #25d366 !important;
    }

    /* Filled Equal Button */
    .equal-btn div.stButton > button {
        background-color: #25d366 !important;
        color: #ffffff !important;
        border-radius: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Equation
if "expression" not in st.session_state:
    st.session_state.expression = ""

def btn_click(symbol):
    if symbol == "C":
        st.session_state.expression = ""
    elif symbol == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
    elif symbol == "=":
        try:
            expr = st.session_state.expression.replace('%', '/100*').replace('×', '*').replace('÷', '/')
            st.session_state.expression = str(eval(expr))
        except Exception:
            st.session_state.expression = "Error"
    else:
        if st.session_state.expression == "Error":
            st.session_state.expression = ""
        st.session_state.expression += str(symbol)

# Display Screen
display_text = st.session_state.expression if st.session_state.expression else "0"
st.markdown(f'<div class="display-screen">{display_text}</div>', unsafe_allow_html=True)

# Grid Layout: 4 Columns per row (Normal Calculator Pattern)
buttons = [
    ['C', '%', '⌫', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['🎨', '0', '.', '=']
]

# Render Grid Buttons
for row in buttons:
    cols = st.columns(4)
    for col, btn in zip(cols, row):
        with col:
            # Special wrapper class for Equal button
            if btn == '=':
                st.markdown('<div class="equal-btn">', unsafe_allow_html=True)
                if st.button(btn, key=f"btn_{btn}"):
                    btn_click(btn)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button(btn, key=f"btn_{btn}"):
                    btn_click(btn)
