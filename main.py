import pyperclip
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import time
from collections import defaultdict
import threading
import queue

# Configuration
GROUPS = {
    "footstep-barefoot": ["footstep-barefoot-grass-walk", "footstep-barefoot-forest-walk", "footstep-barefoot-sand-walk", "footstep-barefoot-dirt-walk", "footstep-barefoot-gravel-walk", "footstep-barefoot-concrete-walk", "footstep-barefoot-concrete-jump-land", "footstep-barefoot-wood-walk", "footstep-barefoot-metal-jump-land", "footstep-barefoot-dirt-jump-land", "footstep-barefoot-metal-walk", "footstep-barefoot-grass-jump-land", "footstep-barefoot-sand-jump-land"],
    "boar-footstep": ["boar-footstep-dirt", "boar-footstep-grass"]
    # Add more groups as needed
}
ICONS = {
    "footstep-barefoot": "footstep-barefoot.png",
    "boar-footstep": "boar-footstep.png",
    # Add more mappings as needed
}

IMAGE_SIZE = (75, 75)  # Resize images to 30x30 pixels
PADDING_LEFT = 0.1  # 10% padding on the left

active_groups = {group: True for group in GROUPS}
active_items = {item: True for group in GROUPS for item in GROUPS[group]}
update_queue = queue.Queue()

class ItemSelectorApp:
    def __init__(self, group, items):
        self.window = tk.Toplevel()
        self.window.title(f"Select Items for {group}")

        self.item_vars = {}
        for item in items:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(self.window, text=item, variable=var, command=lambda i=item: self.toggle_item(i))
            chk.pack(anchor="w")
            self.item_vars[item] = var

    def toggle_item(self, item):
        active_items[item] = self.item_vars[item].get()

class ImageFlasherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group and Item Selector")

        self.group_vars = {}

        for group, items in GROUPS.items():
            frame = tk.Frame(root)
            frame.pack(anchor="w")

            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(frame, text=group, variable=var, command=lambda g=group: self.toggle_group(g))
            chk.pack(side="left")
            self.group_vars[group] = var

            btn = tk.Button(frame, text="Select Items", command=lambda g=group, i=items: self.open_item_selector(g, i))
            btn.pack(side="left")

        self.clear_clipboard_var = tk.BooleanVar(value=False)
        self.clear_clipboard_chk = tk.Checkbutton(root, text="Clear Clipboard after displaying", variable=self.clear_clipboard_var)
        self.clear_clipboard_chk.pack(anchor="w")

        self.start_btn = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_btn.pack(pady=10)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        root.after(100, self.process_queue)

    def toggle_group(self, group):
        active_groups[group] = self.group_vars[group].get()
        for item in GROUPS[group]:
            active_items[item] = active_groups[group]

    def open_item_selector(self, group, items):
        ItemSelectorApp(group, items)

    def process_queue(self):
        try:
            while True:
                task = update_queue.get_nowait()
                self.root.after(0, task)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def start_monitoring(self):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=monitor_clipboard, args=(self,))
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()

    def flash_icons(self, icons):
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.attributes("-alpha", 1.0)  # Start fully opaque

        # Set the window background to be transparent
        overlay.config(bg='white')
        overlay.attributes("-transparentcolor", 'white')

        frame = tk.Frame(overlay, bg='white')
        frame.pack()

        self.images = []  # Persistent reference to images

        for icon_file in icons:
            print(f"Loading icon: {icon_file}")  # Debug statement
            try:
                icon = Image.open(icon_file)
                icon = icon.resize(IMAGE_SIZE, Image.ANTIALIAS)  # Resize image
                icon = ImageTk.PhotoImage(icon)
                self.images.append(icon)  # Keep a reference to avoid garbage collection
                icon_label = tk.Label(frame, image=icon, bg='white')
                icon_label.pack(side="top", pady=5, padx=int(PADDING_LEFT * overlay.winfo_screenwidth()))  # Add padding
            except Exception as e:
                print(f"Error loading icon {icon_file}: {e}")  # Debug statement

        overlay.update_idletasks()
        overlay.attributes("-alpha", 1.0)

        def close_after_delay():
            fade_out(overlay)
            if self.clear_clipboard_var.get():
                pyperclip.copy('')  # Clear the clipboard

        overlay.after(500, close_after_delay)

    def on_closing(self):
        self.stop_monitoring()
        self.root.destroy()

def fade_out(root, duration=500, steps=20):
    alpha_values = [inverse_sigmoid(x) for x in np.linspace(-6, 6, steps)]
    interval = duration // steps

    def update_alpha(step=0):
        if step < len(alpha_values):
            root.attributes("-alpha", alpha_values[step])
            root.after(interval, update_alpha, step + 1)
        else:
            root.destroy()

    update_alpha()

def read_clipboard():
    data = pyperclip.paste()
    return data.strip().split("\n")

def parse_data(data):
    items = defaultdict(int)
    for line in data:
        if line:
            key, value = line.split(":")
            items[key.strip()] += int(value.strip())
    return items

def aggregate_items(items):
    aggregated = defaultdict(int)
    for group, keys in GROUPS.items():
        if active_groups[group]:
            for key in keys:
                if active_items[key]:
                    aggregated[group] += items[key]
    for key, value in items.items():
        if key not in {k for keys in GROUPS.values() for k in keys}:
            aggregated[key] = value
    return aggregated

def determine_icon(items):
    active_items = [ICONS[key] for key, value in items.items() if value > 0 and key in ICONS]
    return active_items

def inverse_sigmoid(x):
    return 1 - (1 / (1 + np.exp(-x)))

def flash_icons(icons):
    update_queue.put(lambda: app.flash_icons(icons))

def monitor_clipboard(app):
    last_text = ""
    while app.monitoring:
        try:
            current_text = pyperclip.paste()
            if current_text != last_text:
                last_text = current_text
                clipboard_data = read_clipboard()
                try:
                    parsed_items = parse_data(clipboard_data)
                    aggregated_items = aggregate_items(parsed_items)
                    icons_to_flash = determine_icon(aggregated_items)
                    if icons_to_flash:
                        flash_icons(icons_to_flash)
                except ValueError:
                    # Handle improperly formatted clipboard data
                    pass
            time.sleep(0.01)
        except KeyboardInterrupt:
            break

def create_gui():
    root = tk.Tk()
    global app
    app = ImageFlasherApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
