import tkinter as tk

# Main window setup
root = tk.Tk()
root.title("Calculator")
root.geometry("360x640")
root.config(bg="#121212")
root.resizable(False, False)

# Input text variable
expression = ""

def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set("")

def equalpress():
    try:
        global expression
        # Percentage aur operators handle karne ke liye
        total = str(eval(expression.replace('%', '/100*').replace('×', '*').replace('÷', '/')))
        equation.set(total)
        expression = total
    except:
        equation.set("Error")
        expression = ""

equation = tk.StringVar()

# Display Screen (Upar ka hissa)
display_frame = tk.Frame(root, bg="#121212", height=180)
display_frame.pack(fill=tk.X, padx=20, pady=20)

screen = tk.Label(display_frame, textvariable=equation, font=('Arial', 36), bg="#121212", fg="#ffffff", anchor='e')
screen.pack(fill=tk.BOTH, expand=True)

# Keypad Frame (Neeche ka 4-column grid layout)
keypad_frame = tk.Frame(root, bg="#1c1c1e")
keypad_frame.pack(fill=tk.BOTH, expand=True)

# Buttons Configuration (Normal Calculator Pattern: 4 columns per row)
buttons = [
    ('C', 0, 0, '#ff5252'), ('%', 0, 1, '#25d366'), ('⌫', 0, 2, '#25d366'), ('÷', 0, 3, '#25d366'),
    ('7', 1, 0, '#ffffff'), ('8', 1, 1, '#ffffff'), ('9', 1, 2, '#ffffff'), ('×', 1, 3, '#25d366'),
    ('4', 2, 0, '#ffffff'), ('5', 2, 1, '#ffffff'), ('6', 2, 2, '#ffffff'), ('-', 2, 3, '#25d366'),
    ('1', 3, 0, '#ffffff'), ('2', 3, 1, '#ffffff'), ('3', 3, 2, '#ffffff'), ('+', 3, 3, '#25d366'),
    ('🎨', 4, 0, '#25d366'), ('0', 4, 1, '#ffffff'), ('.', 4, 2, '#ffffff'), ('=', 4, 3, '#ffffff')
]

for (text, row, col, fg_color) in buttons:
    if text == 'C':
        action = clear
    elif text == '=':
        action = equalpress
    elif text == '÷':
        action = lambda t='÷' : press(t)
    elif text == '×':
        action = lambda t='×' : press(t)
    else:
        action = lambda t=text: press(t)

    # Equal button ke liye special green background aur baakiyon ke liye dark theme
    bg_color = "#25d366" if text == '=' else "#1c1c1e"
    text_color = "#ffffff" if text == '=' else fg_color

    btn = tk.Button(
        keypad_frame, text=text, font=('Arial', 22, 'bold'),
        bg=bg_color, fg=text_color, bd=0, activebackground="#333",
        activeforeground=text_color, command=action
    )
    # Grid method ensure karta hai ki buttons aage (columns me) aur niche rows me theek se fit hon
    btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

# Grid weights set karna taaki saare buttons barabar space lein
for i in range(5):
    keypad_frame.rowconfigure(i, weight=1)
for i in range(4):
    keypad_frame.columnconfigure(i, weight=1)

root.mainloop()
