import streamlit as st

st.set_page_config(page_title="CYBER-CALC", page_icon="⚡", layout="centered")

# Custom Cyberpunk CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0f18;
        color: #00F0FF;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #1a1c2e;
        color: #00FF66;
        border: 2px solid #00F0FF;
        box-shadow: 0 0 10px #00F0FF;
        border-radius: 5px;
        font-size: 22px;
        font-weight: bold;
        width: 100%;
        height: 60px;
    }
    .stButton>button:hover {
        background-color: #FF007F;
        color: #ffffff;
        border-color: #FF007F;
        box-shadow: 0 0 15px #FF007F;
    }
    .display-box {
        background-color: #050608;
        color: #00FF66;
        border: 2px solid #FF007F;
        font-size: 32px;
        text-align: right;
        padding: 10px 15px;
        box-shadow: 0 0 12px #FF007F;
        border-radius: 5px;
        min-height: 60px;
        margin-bottom: 20px;
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ CYBER-CALC v1.0")

if "expr" not in st.session_state:
    st.session_state.expr = ""

# Live HUD Screen Display
display_val = st.session_state.expr if st.session_state.expr else "0"
st.markdown(f'<div class="display-box">{display_val}</div>', unsafe_allow_html=True)

# Button click handler
def press(val):
    if val == "C":
        st.session_state.expr = ""
    elif val == "=":
        try:
            st.session_state.expr = str(eval(st.session_state.expr))
        except Exception:
            st.session_state.expr = "ERROR"
    else:
        st.session_state.expr += str(val)

# Keypad Layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+']
]

for row in buttons:
    cols = st.columns(4)
    for i, button_text in enumerate(row):
        cols[i].button(button_text, key=f"btn_{button_text}", on_click=press, args=(button_text,))
