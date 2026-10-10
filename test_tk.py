# Run this from cmd: python test_tk.py
# Each test builds on the last — note which step fails

import tkinter as tk
import time

print("Step 1: importing tkinter — OK")

root = tk.Tk()
print("Step 2: tk.Tk() created — OK")

root.title("Clock Test")
root.geometry("300x100+200+200")
root.configure(bg="#1a1a2e")

label = tk.Label(root, text="If you see this, tkinter works!",
                 fg="white", bg="#1a1a2e", font=("Segoe UI", 14))
label.pack(expand=True)

print("Step 3: widgets built — OK")
print("Step 4: entering mainloop — window should appear now")

root.mainloop()

print("Step 5: mainloop exited (window was closed)")
