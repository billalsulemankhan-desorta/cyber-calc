#!/usr/bin/env python3
"""
[ CYBER_CALC_v2.0 ]  --  ULTRA-NEON HACKER MATH KERNEL
Enhanced electric-cyberpunk 4-function calculator with high-visibility glow borders.

Pure standard library (tkinter + decimal). Run:  python cyber_calc_v2.py

  * Strict 4-operator keypad: + - * /   (plus C, AC, =)
  * Live terminal audit feed, live HEX / BINARY HUD
  * Flashing keypress feedback (mouse AND keyboard)
  * Division-by-zero breach alert
  * Keyboard: 0-9 . + - * /  Enter/=  Backspace  Esc (AC)  c/Del (C)
"""

import time
import tkinter as tk
from decimal import Decimal, InvalidOperation, getcontext
from tkinter import font as tkfont

getcontext().prec = 40

# ───────────────────────────── ULTRA-NEON PALETTE ──────────────────────────────
VOID = "#05080E"       # ultra pitch black-blue
PANEL = "#080D14"      # recessed dark panel
KEY_BG = "#0D1520"     # dark slate button fill
KEY_HOVER = "#1B2C3F"  # glowing hover state

GREEN = "#00FF66"      # electric matrix green
CYAN = "#00F0FF"       # electric cyber cyan
MAGENTA = "#FF007F"    # high-voltage magenta (AC / C keys)
YELLOW = "#FFE600"     # high-voltage yellow (operators)
RED = "#FF0055"        # breach red
DIM = "#2A4D3E"        # muted cyber text

MAX_DIGITS = 16       # input length limit (register width)
FLASH_MS = 110        # keypress flash duration

BANNER = (
    "╔════════════════════════════════════════╗\n"
    "║   [ CYBER_CALC_v2.0 ]  //  NEON KERNEL ║\n"
    "╚════════════════════════════════════════╝"
)


def pick_font():
    """Prefer Consolas, fall back to Courier New, then Tk's fixed font."""
    available = set(tkfont.families())
    for name in ("Consolas", "Courier New", "DejaVu Sans Mono", "Menlo"):
        if name in available:
            return name
    return "TkFixedFont"


def fmt(d: Decimal) -> str:
    """Format a Decimal as a clean plain string (no exponent, no trailing zeros)."""
    try:
        if d != d.to_integral_value():
            d = d.quantize(Decimal("1e-12"))  # trim long division tails
    except InvalidOperation:
        pass
    s = format(d.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


class CyberCalc:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.F = pick_font()
        root.title("[ CYBER_CALC_v2.0 ]")
        root.configure(bg=VOID)
        root.minsize(860, 640)

        # ── calculator state machine ──
        self.acc = None            # left operand / accumulator (Decimal)
        self.op = None             # pending operator
        self.entry = "0"           # string currently on the display
        self.new_entry = True      # next digit starts a fresh number
        self.just_evaluated = False
        self.error = False
        self.expr_text = ""
        self.cursor_on = True
        self.keys = {}             # key id -> (label widget, color)

        self._build_ui()
        self._bind_keyboard()
        self._boot_sequence()
        self._blink()
        self.refresh()

    # ═══════════════════════════ UI CONSTRUCTION ═══════════════════════════
    def _font(self, size, bold=False):
        return (self.F, size, "bold" if bold else "normal")

    def _panel(self, parent, title, color=GREEN):
        """Neon-bordered panel with a title tag. Returns the inner frame."""
        outer = tk.Frame(parent, bg=color, padx=2, pady=2)
        inner = tk.Frame(outer, bg=PANEL)
        inner.pack(fill="both", expand=True)
        tk.Label(inner, text=f"┤ {title} ├", bg=PANEL, fg=color,
                 font=self._font(9, True), anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        return outer, inner

    def _build_ui(self):
        # Outer shell: its background doubles as the window border (flashes red on breach)
        self.shell = tk.Frame(self.root, bg=GREEN, padx=3, pady=3)
        self.shell.pack(fill="both", expand=True, padx=6, pady=6)
        body = tk.Frame(self.shell, bg=VOID)
        body.pack(fill="both", expand=True)

        # Header: ASCII banner + status line
        tk.Label(body, text=BANNER, bg=VOID, fg=GREEN, font=self._font(11, True),
                 justify="center").pack(pady=(8, 0))
        self.status = tk.Label(body, text="NODE: ONLINE  ▮  LINK: ENCRYPTED  ▮  NEON_ICE: ACTIVE",
                               bg=VOID, fg=CYAN, font=self._font(9))
        self.status.pack(pady=(0, 6))

        cols = tk.Frame(body, bg=VOID)
        cols.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        cols.columnconfigure(0, weight=3)
        cols.columnconfigure(1, weight=4)
        cols.rowconfigure(0, weight=1)

        left = tk.Frame(cols, bg=VOID)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        right = tk.Frame(cols, bg=VOID)
        right.grid(row=0, column=1, sticky="nsew")

        self._build_display(left)
        self._build_keypad(left)
        self._build_hud(right)
        self._build_feed(right)

    def _build_display(self, parent):
        outer, inner = self._panel(parent, "REGISTER // DISPLAY", CYAN)
        outer.pack(fill="x", pady=(0, 8))
        self.expr_lbl = tk.Label(inner, text="", bg=PANEL, fg=YELLOW, anchor="e",
                                 font=self._font(11))
        self.expr_lbl.pack(fill="x", padx=10, pady=(2, 0))
        self.disp_lbl = tk.Label(inner, text="0", bg=PANEL, fg=GREEN, anchor="e",
                                 font=self._font(32, True))
        self.disp_lbl.pack(fill="x", padx=10, pady=(0, 8))

    def _build_keypad(self, parent):
        outer, inner = self._panel(parent, "KEYPAD MATRIX")
        outer.pack(fill="both", expand=True)
        grid = tk.Frame(inner, bg=PANEL)
        grid.pack(fill="both", expand=True, padx=6, pady=6)
        for c in range(4):
            grid.columnconfigure(c, weight=1, uniform="k")
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="r")

        # (label, key id, colour, row, col, rowspan, colspan)
        layout = [
            ("AC", "AC", MAGENTA, 0, 0, 1, 1), ("C", "C", MAGENTA, 0, 1, 1, 1),
            ("/", "/", YELLOW, 0, 2, 1, 1),    ("*", "*", YELLOW, 0, 3, 1, 1),
            ("7", "7", CYAN, 1, 0, 1, 1),      ("8", "8", CYAN, 1, 1, 1, 1),
            ("9", "9", CYAN, 1, 2, 1, 1),      ("-", "-", YELLOW, 1, 3, 1, 1),
            ("4", "4", CYAN, 2, 0, 1, 1),      ("5", "5", CYAN, 2, 1, 1, 1),
            ("6", "6", CYAN, 2, 2, 1, 1),      ("+", "+", YELLOW, 2, 3, 1, 1),
            ("1", "1", CYAN, 3, 0, 1, 1),      ("2", "2", CYAN, 3, 1, 1, 1),
            ("3", "3", CYAN, 3, 2, 1, 1),      ("=", "=", GREEN, 3, 3, 2, 1),
            ("0", "0", CYAN, 4, 0, 1, 2),      (".", ".", CYAN, 4, 2, 1, 1),
        ]
        for label, key, color, r, c, rs, cs in layout:
            self._make_key(grid, label, key, color, r, c, rs, cs)

    def _make_key(self, parent, label, key, color, r, c, rs, cs):
        """A key = neon border frame + label (Label, not Button, so colours work on every OS)."""
        border = tk.Frame(parent, bg=color, padx=2, pady=2)
        border.grid(row=r, column=c, rowspan=rs, columnspan=cs, sticky="nsew", padx=3, pady=3)
        lbl = tk.Label(border, text=label, bg=KEY_BG, fg=color, font=self._font(18, True),
                       cursor="hand2")
        lbl.pack(fill="both", expand=True)
        self.keys[key] = (lbl, color)

        # Press -> invert colours (physical "click"); release -> restore + execute
        lbl.bind("<ButtonPress-1>", lambda e, k=key: self._press_visual(k, True))
        lbl.bind("<ButtonRelease-1>", lambda e, k=key: self._release(k, e))
        lbl.bind("<Enter>", lambda e, w=lbl: w.configure(bg=KEY_HOVER))
        lbl.bind("<Leave>", lambda e, w=lbl: w.configure(bg=KEY_BG))

    def _build_hud(self, parent):
        outer, inner = self._panel(parent, "BASE CONVERSION HUD", CYAN)
        outer.pack(fill="x", pady=(0, 8))
        row = tk.Frame(inner, bg=PANEL)
        row.pack(fill="x", padx=10, pady=(4, 2))
        tk.Label(row, text="HEX", bg=PANEL, fg=CYAN, width=4, anchor="w",
                 font=self._font(11, True)).pack(side="left")
        self.hex_lbl = tk.Label(row, text="0x0", bg=PANEL, fg=GREEN, anchor="w",
                                font=self._font(13, True))
        self.hex_lbl.pack(side="left", fill="x")

        row = tk.Frame(inner, bg=PANEL)
        row.pack(fill="x", padx=10, pady=2)
        tk.Label(row, text="BIN", bg=PANEL, fg=CYAN, width=4, anchor="nw",
                 font=self._font(11, True)).pack(side="left", anchor="n")
        self.bin_lbl = tk.Label(row, text="0b0000", bg=PANEL, fg=GREEN, anchor="w",
                                justify="left", wraplength=380, font=self._font(11))
        self.bin_lbl.pack(side="left", fill="x")

        self.hud_note = tk.Label(inner, text="", bg=PANEL, fg=DIM, anchor="w",
                                 font=self._font(8))
        self.hud_note.pack(fill="x", padx=10, pady=(0, 6))

    def _build_feed(self, parent):
        outer, inner = self._panel(parent, "TERMINAL AUDIT FEED")
        outer.pack(fill="both", expand=True)
        self.feed = tk.Text(inner, bg=PANEL, fg=GREEN, bd=0, highlightthickness=0,
                            wrap="word", font=self._font(10), padx=8, pady=4,
                            state="disabled", cursor="arrow", height=10)
        self.feed.pack(fill="both", expand=True, padx=2, pady=(0, 4))
        # Colour tags per log type
        self.feed.tag_configure("ts", foreground=DIM)
        self.feed.tag_configure("+", foreground=CYAN)
        self.feed.tag_configure(">", foreground=YELLOW)
        self.feed.tag_configure("✓", foreground=GREEN, font=self._font(10, True))
        self.feed.tag_configure("!", foreground=RED, font=self._font(10, True))
        self.feed.tag_configure("~", foreground=MAGENTA)

    # ═══════════════════════════ AUDIT FEED ═══════════════════════════
    def log(self, tag, msg):
        """Append a timestamped line to the terminal feed (auto-scroll, capped length)."""
        f = self.feed
        f.configure(state="normal")
        f.insert("end", time.strftime("%H:%M:%S "), "ts")
        f.insert("end", f"[{tag}] {msg}\n", tag)
        if int(f.index("end-1c").split(".")[0]) > 200:  # keep the feed light
            f.delete("1.0", "20.0")
        f.see("end")
        f.configure(state="disabled")

    def _boot_sequence(self):
        for tag, msg in [("~", "KERNEL BOOT ........... OK"),
                         ("~", "ALU MODULE LOADED (+ - * /)"),
                         ("✓", "SYSTEM READY. AWAITING INPUT")]:
            self.log(tag, msg)

    # ═══════════════════════════ KEY FEEDBACK ═══════════════════════════
    def _press_visual(self, key, hold=False):
        lbl, color = self.keys[key]
        lbl.configure(bg=color, fg=VOID)  # inverted = "lit up"
        if not hold:                       # keyboard presses auto-release
            self.root.after(FLASH_MS, lambda: self._restore(key))

    def _restore(self, key):
        lbl, color = self.keys[key]
        lbl.configure(bg=KEY_BG, fg=color)

    def _release(self, key, event):
        self._restore(key)
        # Only fire if the pointer is still over the key (allows "drag off" cancel)
        w = event.widget
        if 0 <= event.x < w.winfo_width() and 0 <= event.y < w.winfo_height():
            self.dispatch(key)

    def _breach_flash(self, n=6):
        """Flash the window border red/green to signal a system breach."""
        self.shell.configure(bg=RED if n % 2 == 0 else VOID)
        if n > 0:
            self.root.after(120, lambda: self._breach_flash(n - 1))
        else:
            self.shell.configure(bg=GREEN)

    # ═══════════════════════════ INPUT HANDLING ═══════════════════════════
    def _bind_keyboard(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, e):
        ch, ks = e.char, e.keysym
        key = None
        if ch and ch in "0123456789":
            key = ch
        elif ch == "." or ks in ("period", "KP_Decimal"):
            key = "."
        elif ch and ch in "+-*/":
            key = ch
        elif ks in ("Return", "KP_Enter") or ch == "=":
            key = "="
        elif ks == "BackSpace":
            key = "BK"
        elif ks == "Escape":
            key = "AC"
        elif ch in ("c", "C") or ks == "Delete":
            key = "C"
        if key:
            self._press_visual("C" if key == "BK" else key)  # flash the matching key
            self.dispatch(key)

    def dispatch(self, key):
        if key.isdigit():
            self.press_digit(key)
        elif key == ".":
            self.press_dot()
        elif key in "+-*/":
            self.press_op(key)
        elif key == "=":
            self.press_equals()
        elif key == "C":
            self.press_clear()
        elif key == "AC":
            self.press_all_clear()
        elif key == "BK":
            self.press_backspace()
        self.refresh()

    # ═══════════════════════════ CALCULATOR LOGIC ═══════════════════════════
    def _fresh_if_needed(self):
        """Typing a number after a result or an error starts a new calculation."""
        if self.error or self.just_evaluated:
            self.acc, self.op = None, None
            self.entry, self.new_entry = "0", True
            self.error = self.just_evaluated = False
            self.expr_text = ""

    def press_digit(self, d):
        self._fresh_if_needed()
        if self.new_entry:
            self.entry, self.new_entry = d, False
        elif self.entry in ("0", "-0"):
            self.entry = d
        elif len(self.entry.replace("-", "").replace(".", "")) < MAX_DIGITS:
            self.entry += d
        else:
            self.log("!", "REGISTER FULL: INPUT REJECTED")
            return
        self.log("+", f"INPUT: {self.entry}")

    def press_dot(self):
        self._fresh_if_needed()
        if self.new_entry:
            self.entry, self.new_entry = "0.", False
        elif "." not in self.entry:
            self.entry += "."
        self.log("+", f"INPUT: {self.entry}")

    def press_backspace(self):
        if self.error:
            return self.press_all_clear()
        if self.new_entry:
            return
        self.entry = self.entry[:-1]
        if self.entry in ("", "-"):
            self.entry = "0"
        self.log("~", f"BACKSPACE: {self.entry}")

    def press_op(self, op):
        if self.error:
            return
        cur = Decimal(self.entry)
        if self.just_evaluated:                       # chain off the previous result
            self.acc, self.just_evaluated = cur, False
        elif self.op is not None and not self.new_entry:   # chained: 1 + 2 + ...
            self.log(">", f"EXEC: {fmt(self.acc)} {self.op} {fmt(cur)}")
            res = self._evaluate(self.acc, self.op, cur)
            if res is None:
                return
            self.acc = res
            self.log("✓", f"SYSTEM OUTPUT: {fmt(res)}")
        elif self.op is None:
            self.acc = cur
        # (else: operator pressed twice -> simply swap the operator)
        self.op = op
        self.entry = fmt(self.acc)
        self.new_entry = True
        self.expr_text = f"{fmt(self.acc)} {op}"
        self.log(">", f"QUEUED: {self.expr_text}")

    def press_equals(self):
        if self.error:
            return
        if self.op is None:
            self.log("~", "NO OPERATION QUEUED")
            return
        b = Decimal(self.entry)
        a, op = self.acc, self.op
        self.log(">", f"EXEC: {fmt(a)} {op} {fmt(b)}")
        res = self._evaluate(a, op, b)
        if res is None:
            return
        self.expr_text = f"{fmt(a)} {op} {fmt(b)} ="
        self.entry = fmt(res)
        self.acc, self.op = None, None
        self.new_entry = True
        self.just_evaluated = True
        self.log("✓", f"SYSTEM OUTPUT: {self.entry}")

    def _evaluate(self, a, op, b):
        """Run the ALU. Returns a Decimal, or None after raising a breach alert."""
        try:
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if op == "/":
                if b == 0:
                    raise ZeroDivisionError
                return a / b
        except ZeroDivisionError:
            self._breach("OVERFLOW / DIVISION BY ZERO")
        except InvalidOperation:
            self._breach("ARITHMETIC OVERFLOW")
        return None

    def _breach(self, message):
        self.error = True
        self.entry = message
        self.acc, self.op = None, None
        self.new_entry = True
        self.expr_text = "!! SYSTEM BREACH !!"
        self.log("!", f"BREACH DETECTED: {message}")
        self.log("!", "ALU LOCKED. PRESS AC / ESC TO REBOOT")
        self._breach_flash()

    def press_clear(self):
        """C: wipe the current entry only (or clear the error / result)."""
        if self.error or self.just_evaluated:
            return self.press_all_clear()
        self.entry, self.new_entry = "0", True
        self.log("~", "ENTRY REGISTER CLEARED")

    def press_all_clear(self):
        """AC: reset every register."""
        self.acc = self.op = None
        self.entry, self.new_entry = "0", True
        self.error = self.just_evaluated = False
        self.expr_text = ""
        self.log("~", "ALL REGISTERS PURGED")

    # ═══════════════════════════ DISPLAY / HUD ═══════════════════════════
    def refresh(self):
        # --- main display ---
        self._draw_display()
        self.expr_lbl.configure(text=self.expr_text, fg=RED if self.error else YELLOW)

        # --- base conversion HUD ---
        if self.error:
            self.hex_lbl.configure(text="-- NULL --", fg=RED)
            self.bin_lbl.configure(text="-- NULL --", fg=RED)
            self.hud_note.configure(text="HUD OFFLINE: ALU IN BREACH STATE", fg=RED)
            return
        val = Decimal(self.entry)
        n = int(val)  # truncate toward zero for the integer-only bases
        sign = "-" if n < 0 else ""
        mag = abs(n)
        bits = bin(mag)[2:]
        bits = bits.zfill((len(bits) + 3) // 4 * 4)                  # pad to nibbles
        grouped = " ".join(bits[i:i + 4] for i in range(0, len(bits), 4))
        self.hex_lbl.configure(text=f"{sign}0x{mag:X}", fg=GREEN)
        self.bin_lbl.configure(text=f"{sign}0b {grouped}", fg=GREEN)
        note = f"BIT-LENGTH: {max(mag.bit_length(), 1)}"
        if val != n:
            note += "   //   FRACTION TRUNCATED FOR HEX/BIN"
        self.hud_note.configure(text=note, fg=DIM)

    def _draw_display(self):
        text = self.entry
        if self.error:
            color, size = RED, 16
        else:
            color = GREEN
            if len(text) > 20:                        # too wide: use scientific notation
                text = format(Decimal(text), ".10e")
            size = 32 if len(text) <= 11 else 24 if len(text) <= 16 else 18
        cursor = "▌" if (self.cursor_on and not self.error) else " "
        self.disp_lbl.configure(text=text + cursor, fg=color, font=self._font(size, True))

    def _blink(self):
        """Blinking terminal cursor."""
        self.cursor_on = not self.cursor_on
        self._draw_display()
        self.root.after(520, self._blink)


def main():
    root = tk.Tk()
    CyberCalc(root)
    root.mainloop()


if __name__ == "__main__":
    main()