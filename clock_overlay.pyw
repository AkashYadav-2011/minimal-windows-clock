"""
Ultra-Minimalist Clock Overlay
- Hours and Minutes only (Solid colon, no blinking, no AM/PM, no date)
"""

import tkinter as tk
from tkinter import colorchooser
import time
import threading
import math
import ctypes
import pystray
from PIL import Image, ImageDraw

BG         = '#010101'
TIME_FG    = '#00D4FF'
MENU_BG    = '#0D1117'
MENU_FG    = '#C9D1D9'
MENU_SEL   = '#00D4FF'
MENU_SELF  = '#000000'

def _make_tray_icon(color: str = '#00D4FF') -> Image.Image:
    size = 64
    img  = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = size // 2 - 4
    cr, cg, cb = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    rgba = (cr, cg, cb, 255)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=rgba, width=4)
    for angle, length, width in [(-60, r * 0.50, 4), (60, r * 0.70, 3)]:
        rad = math.radians(angle)
        x2  = cx + length * math.sin(rad)
        y2  = cy - length * math.cos(rad)
        draw.line([cx, cy, x2, y2], fill=rgba, width=width)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=rgba)
    return img

class ClockOverlay:
    def __init__(self):
        self.root          = tk.Tk()
        self._dx           = 0
        self._dy           = 0
        self._time_color   = TIME_FG
        self._tray         = None

        self._setup_window()
        self._build_ui()
        self._tick()
        self._start_tray()
        self.root.mainloop()

    def _setup_window(self):
        r = self.root
        r.overrideredirect(True)
        r.configure(bg=BG)
        r.attributes('-transparentcolor', BG)
        r.update_idletasks()
        sw = r.winfo_screenwidth()
        r.geometry(f'+{sw - 260}+30')
        
        r.update()
        hwnd = ctypes.windll.user32.GetParent(r.winfo_id())
        ctypes.windll.user32.SetWindowPos(hwnd, 1, 0, 0, 0, 0, 0x0010 | 0x0002 | 0x0001)

    def _build_ui(self):
        outer    = tk.Frame(self.root, bg=BG)
        outer.pack(padx=12, pady=6)
        time_row = tk.Frame(outer, bg=BG)
        time_row.pack()

        c = self._time_color

        # Only Hours, Colon, and Minutes (Solid colon, no AM/PM)
        self.lbl_hh = tk.Label(time_row, text='00', font=('Segoe UI Light', 58), fg=c, bg=BG)
        self.lbl_c1 = tk.Label(time_row, text=':',  font=('Segoe UI Light', 50), fg=c, bg=BG)
        self.lbl_mm = tk.Label(time_row, text='00', font=('Segoe UI Light', 58), fg=c, bg=BG)

        self.lbl_hh.pack(side='left')
        self.lbl_c1.pack(side='left')
        self.lbl_mm.pack(side='left')

        for widget in self.root.winfo_children():
            self._bind_all(widget)

    def _bind_all(self, widget):
        widget.bind('<ButtonPress-1>', self._on_press)
        widget.bind('<B1-Motion>',     self._on_drag)
        widget.bind('<Button-3>',      self._show_menu)
        for child in widget.winfo_children():
            self._bind_all(child)

    def _tick(self):
        now = time.localtime()
        # 24-hour format (change to 12-hour if you prefer by using now.tm_hour % 12 or 12)
        h24 = now.tm_hour

        self.lbl_hh.config(text=f'{h24:02d}')
        self.lbl_mm.config(text=f'{now.tm_min:02d}')

        self.root.after(1000, self._tick)

    def _apply_color(self, color: str):
        self._time_color = color
        self.lbl_hh.config(fg=color)
        self.lbl_c1.config(fg=color)
        self.lbl_mm.config(fg=color)
        if self._tray:
            self._tray.icon = _make_tray_icon(color)

    def _pick_color_dialog(self):
        result = colorchooser.askcolor(color=self._time_color, title='Choose Clock Color', parent=self.root)
        if result and result[1]:
            self._apply_color(result[1])

    def _on_press(self, event):
        self._dx = event.x_root - self.root.winfo_x()
        self._dy = event.y_root - self.root.winfo_y()

    def _on_drag(self, event):
        self.root.geometry(f'+{event.x_root - self._dx}+{event.y_root - self._dy}')

    def _show_menu(self, event):
        m = tk.Menu(self.root, tearoff=0, bg=MENU_BG, fg=MENU_FG, activebackground=MENU_SEL, activeforeground=MENU_SELF, relief='flat', bd=1)
        m.add_command(label='  Color  ●  Cyan',          command=lambda: self._apply_color('#00D4FF'))
        m.add_command(label='  Color  ●  White',         command=lambda: self._apply_color('#FFFFFF'))
        m.add_command(label='  Color  ●  Soft Green',    command=lambda: self._apply_color('#00FF99'))
        m.add_command(label='  Color  ●  Warm Orange',   command=lambda: self._apply_color('#FF8C42'))
        m.add_command(label='  Color  ●  Purple',        command=lambda: self._apply_color('#CC88FF'))
        m.add_command(label='  Color  ●  Pink',          command=lambda: self._apply_color('#FF6EB4'))
        m.add_command(label='  Color  ⊕  Custom...',     command=self._pick_color_dialog)
        m.add_separator()
        m.add_command(label='  ✕  Exit Clock', command=self._exit)
        m.tk_popup(event.x_root, event.y_root)

    def _start_tray(self):
        def _set(c):
            return lambda icon, item: self.root.after(0, lambda: self._apply_color(c))
        def _custom(icon, item):
            self.root.after(0, self._pick_color_dialog)
        def _exit(icon, item):
            icon.stop()
            self.root.after(0, self.root.destroy)

        menu = pystray.Menu(
            pystray.MenuItem('Color', pystray.Menu(
                pystray.MenuItem('Cyan',         _set('#00D4FF')),
                pystray.MenuItem('White',        _set('#FFFFFF')),
                pystray.MenuItem('Soft Green',   _set('#00FF99')),
                pystray.MenuItem('Warm Orange',  _set('#FF8C42')),
                pystray.MenuItem('Purple',       _set('#CC88FF')),
                pystray.MenuItem('Pink',         _set('#FF6EB4')),
                pystray.MenuItem('Custom...',    _custom),
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', _exit, default=True),
        )

        def _run():
            self._tray = pystray.Icon('clock_overlay', _make_tray_icon(self._time_color), 'Clock Overlay', menu)
            self._tray.run()

        threading.Thread(target=_run, daemon=True).start()

    def _exit(self):
        if self._tray:
            self._tray.stop()
        self.root.destroy()

if __name__ == '__main__':
    ClockOverlay()
