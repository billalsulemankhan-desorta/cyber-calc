import streamlit as st

# Set responsive page layout
st.set_page_config(page_title="CYBER-CALC", page_icon="⚡", layout="centered")

# Custom Responsive Cyberpunk CSS (Optimized for Mobile & Laptop)
st.markdown("""
    <style>
    /* Dark Neon Theme */
    .stApp {
        background-color: #08090d;
        color: #00F0FF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Container styling to look like a mobile device frame */
    .block-container {
        max-width: 420px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Neon HUD Screen */
    .hud-screen {
        background: #030406;
        border: 2px solid #FF007F;
        border-radius: 12px;
        padding: 15px 20px;
        text-align: right;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.4);
        margin-bottom: 20px;
    }
    
    .hud-history {
        color: #00F0FF;
        font-size: 14px;
        min-height: 20px;
        opacity: 0.7;
    }
    
    .hud-main {
        color: #00FF66;
        font-size: 38px;
        font-weight: bold;
        word-wrap: break-word;
        font-family: 'Courier New', monospace;
    }
    
    /* Button Base Styling */
    .stButton>button {
        border-radius: 10px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        height: 62px !important;
        width: 100% !important;
        margin-bottom: 8px;
        transition: all 0.15s ease-in-out;
    }
    
    /* Specific Button Variants */
    /* Number Keys */
    div[data-testid="column"] button {
        background-color: #121420;
        color: #00F0FF;
        border: 1px solid #00F0FF;
        box-shadow: 0 0 6px rgba(0, 240, 255, 0.2);
    }
    
    /* Operator Keys (*, /, +, -) */
    div[data-testid="column"]:nth-child(4) button {
        background-color: #1a0926;
        color: #FF007F;
        border: 1px solid #FF007F;
        box-shadow: 0 0 8px rgba(255, 0, 127, 0.3);
    }
    
    /* Equal Button */
    .equal-btn button {
        background-color: #00FF66 !important;
        color: #000000 !important;
        border: none !important;
        box-shadow: 0 0 15px #00FF66 !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.03);
        filter: brightness(1.2);
    }
    </style>
""", unsafe_allow_html=True)

# State initialization
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "history" not in st.session_state:
    st.session_state.history = ""

# Header
st.markdown("<h3 style='text-align: center; color: #00F0FF; margin-bottom: 15px;'>⚡ CYBER-CALC</h3>", unsafe_allow_html=True)

# HUD Screen Render
history_disp = st.session_state.history if st.session_state.history else "&nbsp;"
main_disp = st.session_state.expr if st.session_state.expr else "0"

st.markdown(f"""
    <div class="hud-screen">
        <div class="hud-history">{history_disp}</div>
        <div class="hud-main">{main_disp}</div>
    </div>
""", unsafe_allow_html=True)

# Input handler function
def press(val):
    if val == "C":
        st.session_state.expr = ""
        st.session_state.history = ""
    elif val == "⌫":
        st.session_state.expr = st.session_state.expr[:-1]
    elif val == "=":
        if st.session_state.expr:
            try:
                # Replace visual operators with math operators
                clean_expr = st.session_state.expr.replace("×", "*").replace("÷", "/")
                res = eval(clean_expr)
                st.session_state.history = f"{st.session_state.expr} ="
                st.session_state.expr = str(int(res) if isinstance(res, float) and res.is_integer() else round(res, 6))
            except Exception:
                st.session_state.expr = "ERROR"
    elif val == "%":
        try:
            val_num = float(st.session_state.expr)
            st.session_state.expr = str(val_num / 100)
        except Exception:
            st.session_state.expr = "ERROR"
    else:
        if st.session_state.expr == "ERROR":
            st.session_state.expr = ""
        st.session_state.expr += str(val)

# App Keypad Layout
layout = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="]
]

for row in layout:
    cols = st.columns(4)
    for i, symbol in enumerate(row):
        key_id = f"k_{symbol}"
        if symbol == "=":
            # Wrap equal button for distinct styling
            with cols[i]:
                st.markdown('<div class="equal-btn">', unsafe_allow_html=True)
                st.button(symbol, key=key_id, on_click=press, args=(symbol,))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            cols[i].button(symbol, key=key_id, on_click=press, args=(symbol,))
