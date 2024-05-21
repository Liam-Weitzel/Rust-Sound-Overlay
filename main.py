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
    #Footsteps
    "footstep-barefoot": ["footstep-barefoot-sand-walk", "footstep-barefoot-grass-walk", "footstep-barefoot-grass-jump-start", "footstep-barefoot-grass-jump-land", "footstep-barefoot-sand-jump-start", "footstep-barefoot-wood-jump-land", "footstep-barefoot-wood-walk", "footstep-barefoot-metal-jump-land", "footstep-barefoot-metal-walk", "footstep-barefoot-metal-jump-start", "footstep-barefoot-sand-jump-land", "footstep-barefoot-concrete-walk", "footstep-barefoot-wood-jump-start", "footstep-barefoot-concrete-jump-land", "footstep-barefoot-concrete-jump-start", "footstep-barefoot-stones-jump-start", "footstep-barefoot-stones-walk", "footstep-barefoot-stones-jump-land", "footstep-barefoot-gravel-jump-land", "footstep-barefoot-cloth-jump-start"],
    "footstep-hide": ["footstep-hide-wood-walk", "footstep-hide-wood-jump-start", "footstep-hide-wood-jump-land", "footstep-hide-metal-walk", "footstep-hide-metal-jump-start", "footstep-hide-metal-jump-land", "footstep-hide-concrete-jump-start", "footstep-hide-concrete-walk", "footstep-hide-concrete-jump-land", "footstep-hide-grass-walk", "footstep-hide-sand-walk", "footstep-hide-grass-jump-start", "footstep-hide-grass-jump-land", "footstep-hide-sand-jump-land", "footstep-hide-sand-jump-start", "footstep-hide-gravel-walk", "footstep-hide-stones-jump-land", "footstep-hide-stones-jump-start"],
    "footstep-boots": ["footstep-boots-metal-walk", "footstep-boots-metal-jump-start", "footstep-boots-metal-jump-land", "footstep-boots-concrete-walk", "footstep-boots-concrete-jump-start", "footstep-boots-concrete-jump-land", "footstep-boots-wood-walk", "footstep-boots-wood-jump-start", "footstep-boots-wood-jump-land", "footstep-boots-sand-walk", "footstep-boots-grass-walk", "footstep-boots-grass-jump-land", "footstep-boots-grass-jump-start", "footstep-boots-sand-jump-land", "footstep-boots-sand-jump-start", "footstep-boots-stones-jump-land", "footstep-boots-stones-walk", "footstep-boots-stones-jump-start", "footstep-boots-gravel-jump-land", "footstep-boots-gravel-jump-start"],
    "footstep-burlap": ["footstep-burlap-wood-walk", "footstep-burlap-wood-jump-start", "footstep-burlap-wood-jump-land", "footstep-burlap-metal-walk", "footstep-burlap-metal-jump-start", "footstep-burlap-metal-jump-land", "footstep-burlap-concrete-jump-start", "footstep-burlap-concrete-jump-land", "footstep-burlap-concrete-walk", "footstep-burlap-grass-walk", "footstep-burlap-sand-walk", "footstep-burlap-grass-jump-land", "footstep-burlap-grass-jump-start", "footstep-burlap-sand-jump-land", "footstep-burlap-sand-jump-start", "footstep-burlap-stones-walk", "footstep-burlap-gravel-walk", "footstep-burlap-stones-jump-land", "footstep-burlap-stones-jump-start"],
    "footstep-rubber": ["footstep-rubber-boots-metal-walk", "footstep-rubber-boots-metal-jump-land", "footstep-rubber-boots-metal-jump-start", "footstep-rubber-boots-concrete-jump-land", "footstep-rubber-boots-concrete-walk", "footstep-rubber-boots-concrete-jump-start", "footstep-rubber-boots-wood-walk", "footstep-rubber-boots-wood-jump-start", "footstep-rubber-boots-wood-jump-land", "footstep-rubber-boots-sand-walk", "footstep-rubber-boots-grass-walk", "footstep-rubber-boots-grass-jump-land", "footstep-rubber-boots-grass-jump-start", "footstep-rubber-boots-sand-jump-land", "footstep-rubber-boots-sand-jump-start", "footstep-rubber-boots-stones-jump-land", "footstep-rubber-boots-stones-walk", "footstep-rubber-boots-gravel-walk", "footstep-rubber-boots-gravel-jump-start", "footstep-rubber-boots-stones-jump-start"],
    #Tools
    "hatchet": ["hatchet-deploy", "hatchet-attack", "lumberjack-axe-attack", "lumberjack-axe-impact"],
    "hatchet-stone": ["concrete-axe-attack", "concrete-axe-impact", "hatchet-stone-strike-soft", "hatchet-stone-strike"],
    "pickaxe": ["concrete-pick-impact", "lumberjack-pick-attack, lumberjack-pick-impact", "pickaxe-deploy", "pickaxe-attack", "pickaxe-strike", "diver-pickaxe-deploy", "diver-pickaxe-attack"],
    "salvaged-axe": ["salvaged-axe-deploy", "salvaged-axe-attack", "salvaged-axe-strike"],
    "salvaged-icepick": ["salvaged-icepick-deploy", "salvaged-icepick-hand-tap", "salvaged-icepick-attack", "salvaged-icepick-strike"],
    "torch": ["skull-torch-burn-loop", "skull-torch-deploy", "skull-torch-attack", "skull-torch-strike", "torch-strike", "diver-torch-deploy", "diver-torch-attack", "diver-torch-strike"],
    "chainsaw": ["chainsaw-pull-chain", "chainsaw-unscrew-gascap", "chainsaw-fill-gas", "chainsaw-idle", "chainsaw-hit-metal", "chainsaw-rev-up", "chainsaw-active", "chainsaw-rev-down", "chainsaw-engine-off"],
    "salvaged-hammer": ["salvaged-hammer-deploy", "salvaged-hammer-attack", "salvaged-hammer-strike"],
    "shovel": ["shovel-deploy", "shovel-strike"],
    "paddle": ["paddle-strike"],
    "metal-detector": ["metal-detector-deploy", "metal-detector-lower", "metal-detector-swing", "metal-detector-raise"],
    "c4": ["c4-explosion", "c4-beep-loop", "c4-deploy"],
    "survey-charge": ["survey-charge-deploy", "survey-charge-fuse-loop", "survey-charge-stick"],
    "flare": ["flare-deploy", "flare-ignite", "flare-throw", "flare-burn-loop"],
    #Generic sounds
    "fire": ["campfire-burning", "mlrs-damaged-fire-loop", "large-fire-loop", "ignite"],
    "phys-impact": ["phys-impact-wood", "phys-impact-tool", "phys-impact-metal-medium-rattley", "phys-impact-plastic", "phys-impact-bone"],
    "throw-item": ["throw-item-small"],
    #Interactable objects
    "recycle": ["grinding_loop", "recycler-open", "recycle-start", "recycler-close", "recycle-stop"],
}
ICONS = {
    #Footsteps
    "footstep-barefoot": "footstep-barefoot.png",
    "footstep-hide": "footstep-hide.png",
    "footstep-boots": "footstep-boots.png",
    "footstep-burlap": "footstep-burlap.png",
    "footstep-rubber": "footstep-rubber.png",
    #Tools
    "hatchet": "hatchet.png",
    "hatchet-stone": "hatchet-stone.png",
    "pickaxe": "pickaxe.png",
    "salvaged-axe": "salvaged-axe.png",
    "salvaged-icepick": "salvaged-icepick.png",
    "torch": "torch.png",
    "chainsaw": "chainsaw.png",
    "salvaged-hammer": "salvaged-hammer.png",
    "shovel": "shovel.png",
    "paddle": "paddle.png",
    "metal-detector": "metal-detector.png",
    "c4": "c4.png",
    "survey-charge": "survey-charge.png",
    "flare": "flare.png",
    #Generic sounds
    "fire": "fire.png",
    "phys-impact": "phys-impact.png",
    "throw-item": "throw-item.png",
    #Interactable objects
    "recycle": "recycle.png",
}

IMAGE_SIZE = (75, 75)
PADDING_LEFT = 0.1

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
        overlay.attributes("-alpha", 1.0)

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
                icon = icon.resize(IMAGE_SIZE, Image.ANTIALIAS)
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
