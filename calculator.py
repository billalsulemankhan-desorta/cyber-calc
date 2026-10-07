import streamlit as st

# Set responsive page configuration
st.set_page_config(page_title="CYBER-CALC", page_icon="⚡", layout="centered")

# Custom Cyberpunk Styling: Dark Gradient Background, Neon Display, Electric Yellow Buttons
st.markdown("""
    <style>
    /* Dark Cyberpunk Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0a0814 0%, #04060f 50%, #110722 100%);
        color: #00F0FF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Responsive App Container (Mobile & Laptop Viewport) */
    .block-container {
        max-width: 440px !important;
        padding: 1rem 0.8rem !important;
    }
    
    /* Neon HUD Screen Display */
    .hud-screen {
        background: #02050a;
        border: 2px solid #00F0FF;
        border-radius: 16px;
        padding: 16px 20px;
        text-align: right;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.5), inset 0 0 12px rgba(0, 240, 255, 0.2);
        margin-bottom: 20px;
    }
    
    /* Neon History Line */
    .hud-history {
        color: #FF007F;
        font-size: 16px;
        min-height: 24px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Neon Green Main Output */
    .hud-main {
        color: #00FF66;
        font-size: 42px;
        font-weight: 800;
        word-wrap: break-word;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px #00FF66;
    }
    
    /* High-Visibility Electric Yellow Buttons */
    .stButton>button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: 2px solid #FFA500 !important;
        border-radius: 14px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        height: 64px !important;
        width: 100% !important;
        margin-bottom: 6px;
        box-shadow: 0 0 14px rgba(255, 215, 0, 0.4) !important;
        transition: all 0.12s ease-in-out;
        -webkit-tap-highlight-color: transparent;
    }
    
    /* Touch & Hover Glowing Effects */
    .stButton>button:active, .stButton>button:hover {
        background-color: #FFEE55 !important;
        transform: scale(0.97);
        box-shadow: 0 0 22px rgba(255, 238, 85, 0.9) !important;
    }
    
    /* Operator Keys (*, /, +, -) */
    div[data-testid="column"]:nth-child(4) button {
        background-color: #FF9900 !important;
        border: 2px solid #FF6600 !important;
        box-shadow: 0 0 16px rgba(255, 153, 0, 0.5) !important;
    }
    
    /* Glowing Equal Key (=) */
    .equal-btn button {
        background-color: #00FF66 !important;
        color: #000000 !important;
        border: 2px solid #00CC55 !important;
        box-shadow: 0 0 22px #00FF66 !important;
    }
    </style>
""", unsafe_allow_html=True)

# State Management
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "history" not in st.session_state:
    st.session_state.history = ""

# Header
st.markdown("<h3 style='text-align: center; color: #00F0FF; text-shadow: 0 0 12px #00F0FF; margin-bottom: 14px;'>⚡ CYBER-CALC</h3>", unsafe_allow_html=True)

# Calculation Logic
def press(val):
    if val in ["C", "clear"]:
        st.session_state.expr = ""
        st.session_state.history = ""
    elif val in ["⌫", "backspace"]:
        st.session_state.expr = st.session_state.expr[:-1]
    elif val in ["=", "enter"]:
        if st.session_state.expr:
            try:
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

# Render Neon Display Screen
history_disp = st.session_state.history if st.session_state.history else "&nbsp;"
main_disp = st.session_state.expr if st.session_state.expr else "0"

st.markdown(f"""
    <div class="hud-screen">
        <div class="hud-history">{history_disp}</div>
        <div class="hud-main">{main_disp}</div>
    </div>
""", unsafe_allow_html=True)

# Optional Laptop Keyboard Input Field
with st.expander("⌨️ Laptop Keyboard Input"):
    kb_input = st.text_input("Type numbers/math directly:", key="kb_field", placeholder="e.g. 125*8")
    if kb_input:
        try:
            res = eval(kb_input)
            st.session_state.history = f"{kb_input} ="
            st.session_state.expr = str(int(res) if isinstance(res, float) and res.is_integer() else round(res, 6))
        except Exception:
            st.session_state.expr = "ERROR"

# Touch Keypad Grid Layout
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
            with cols[i]:
                st.markdown('<div class="equal-btn">', unsafe_allow_html=True)
                st.button(symbol, key=key_id, on_click=press, args=(symbol,))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            cols[i].button(symbol, key=key_id, on_click=press, args=(symbol,))
