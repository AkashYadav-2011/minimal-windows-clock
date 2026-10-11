# Minimalist Windows Desktop Clock Overlay

A lightweight, clean, transparent desktop clock for Windows built with Python and Tkinter. Stays locked to the desktop background layer behind other windows and includes a system tray menu for easy color customization.

## Features
- **Hours & Minutes Only**: No clutter, seconds, AM/PM, or dates—just a clean, minimal look.
- **Desktop Layering**: Stays tucked neatly behind your active windows.
- **Easy Color Customizer**: Change the clock color instantly by using its **system tray icon** (found down in the Windows taskbar, often hidden inside the "Show hidden icons" pop-up arrow `^`).
- **Draggable**: Click and drag the clock anywhere you want on your screen.

## Requirements
Make sure you have Python installed along with the required libraries:

pip install pystray pillow

## Step-by-Step: Pin Your .pyw Clock Overlay

- **1. Create a new shortcut: Right-click empty space on your desktop, hover over New, and select Shortcut.
- **2. Enter the Target path: Paste the following path structure into the location box, adjusting it to match where Python and your clock file are located:text
C:\Windows\System32\cmd.exe /c start /b pythonw.exe "C:\Path\To\Your\clockoverlay.pyw"
Use code with caution.
(Note: Prepending cmd.exe /c start /b ensures it starts completely silently in the background using pythonw.exe, hiding any trailing command prompt windows).
- **3. Name the shortcut: Type Clock Overlay (or your preferred name) and click Finish.
- **4. Give it an icon (Optional):
	• Right-click your new desktop shortcut and select Properties.
	• Click Change Icon....
	• Browse for a clock icon or select an existing one from Windows' system files, then click OK -> Apply.
- **5. Pin to taskbar: Right-click your finished desktop shortcut and choose Pin to taskbar.
- '''bash
- 
