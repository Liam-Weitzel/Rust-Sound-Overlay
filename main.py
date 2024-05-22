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
    "metal-detector": ["metal-detector-deploy", "metal-detector-lower", "metal-detector-swing", "metal-detector-raise"],
    "c4": ["c4-explosion", "c4-beep-loop", "c4-deploy"],
    "survey-charge": ["survey-charge-deploy", "survey-charge-fuse-loop", "survey-charge-stick"],
    "flare": ["flare-deploy", "flare-ignite", "flare-throw", "flare-burn-loop"],
    #Weapons
    "bow": ["bow-arrow-flight", "bow-deploy", "bow-draw", "bow-attack"],
    "compound-bow": ["compound-bow-deploy", "compound-bow-reload-start", "compound-bow-place-arrow", "compound-bow-initial-pullback", "compound-bow-charge-up", "compound-bow-charge-up-complete", "compound-bow-held-stress-loop", "compound-bow-attack"],
    "machete": ["machete-deploy", "machete-attack", "machete-strike-soft"],
    "military-flamethrower": ["military-flamethrower-deploy", "military-flamethrower-attack-start", "military-flamethrower-attack-loop", "military-flamethrower-attack-stop"],
    "flamethrower": ["flamethrower-pilot-loop", "flamethrower-deploy", "flamethrower-valve_open", "flamethrower-fire-start", "flamethrower-fire-loop", "flamethrower-fire-stop"],
    "minigun": ["minigun-deploy", "minigun-motor-loop-unpitched", "minigun-motor-start", "minigun-motor-loop-pitched", "minigun-gunshot-body-loop", "minigun-gunshot-body-start", "minigun-gunshot-LFE-loop", "minigun-gunshot-LFE-start", "minigun-gunshot-mech-loop", "minigun-gunshot-body-tail", "minigun-gunshot-LFE-tail", "minigun-gunshot-mech-tail", "minigun-motor-release"],
    "molotov": ["molotov-cocktail-deploy", "molotov-cocktail-ignite", "molotov-cocktail-ignite-finish", "molotov-cocktail-throw", "molotov-cocktail-explosion", "molotov-cocktail-fireball-burn-loop"],
    "mp5": ["mp5-gunshot-body-suppressed", "mp5-gunshot-mech-suppressed", "mp5-deploy", "mp5-bolt-back", "mp5-bolt-shut", "mp5-gunshot-body", "mp5-gunshot-LFE", "mp5-gunshot-mech", "mp5-gunshot-tail-outdoor"],
    "grenade-launcher": ["grenade-launcher-deploy", "grenade-launcher-reload-start", "grenade-launcher-reload-single-start", "grenade-launcher-reload-single-spin", "grenade-launcher-reload-single-insert", "grenade-launcher-reload-end", "grenade-launcher-attack", "grenade-launcher-explosion"],
    "spas12": ["spas12-gunshot-body-suppressed", "spas12-deploy", "spas12-pump_back", "spas12-pump_forward", "spas12-gunshot-body", "spas12-gunshot-LFE", "spas12-gunshot-mech", "spas12-gunshot-tail-outdoor"],
    "lr300": ["lr300-deploy", "lr300-charging-handle-back", "lr300-charging-handle-shut", "lr300-gunshot-body", "lr300-gunshot-LFE", "lr300-gunshot-mech", "lr300-gunshot-tail-outdoor"],
    "ak47": ["ak74u-deploy", "ak74u-bolt-back", "ak74u-bolt-forward", "ak47-gunshot-body", "ak47-gunshot-tail-outdoor", "ak47-gunshot-LFE", "ak47-gunshot-mech", "ak47-gunshot-body-suppressed"],
    "m249": ["m249-gunshot-body-suppressed", "m249-deploy", "m249-chainbelt", "m249-gunshot-body", "m249-gunshot-LFE", "m249-gunshot-mech", "m249-gunshot-tail-outdoor"],
    "m39": ["m39-gunshot-body-suppressed", "m39-deploy", "m39-gunshot-body", "m39-gunshot-LFE", "m39-gunshot-mech", "m39-gunshot-tail-outdoor"],
    "m4": ["m4-shotgun-gunshot-LFE-suppressed", "m4-shotgun-deploy", "m4-shotgun-gunshot-body", "m4-shotgun-gunshot-LFE", "m4-shotgun-gunshot-mech", "m4-shotgun-gunshot-tail-outdoor"],
    "m92": ["m92-gunshot-body-suppressed", "m92-deploy", "m92-safety-off", "m92-gunshot-body", "m92-gunshot-LFE", "m92-gunshot-mech", "m92-gunshot-tail-outdoor"],
    "2handed-mace": ["2handed-mace-deploy", "2handed-mace-attack", "2handed-mace-strike"],
    "hmlmg": ["hmlmg-gunshot-body-suppressed", "hmlmg-deploy-02-start-01", "hmlmg-deploy-02-finish-01", "hmlmg-gunshot-body", "hmlmg-gunshot-tail-outdoor", "hmlmg-gunshot-mech", "hmlmg-gunshot-LFE"],
    "homing-missile-launcher": ["homing-missile-launcher-deploy-start", "homing-missile-launcher-deploy-camera", "homing-missile-launcher-deploy-finish", "homing-missile-launcher-reload-start", "homing-missile-launcher-reload-insert-rocket", "homing-missile-launcher-reload-finish"],
    "2handed-sword": ["2handed-sword-deploy", "2handed-sword-attack", "2handed-sword-strike-soft", "2handed-sword-strike"],
    "l96": ["l96-gunshot-LFE-suppressed", "l96-gunshot-body-suppressed", "l96-deploy", "l96-gunshot-body", "l96-gunshot-LFE", "l96-gunshot-mech", "l96-gunshot-tail-outdoor", "l96-bolt-start", "l96-bolt-grab", "l96-bolt-action", "l96-bolt-finish"],
    "crossbow": ["crossbow-reload", "crossbow-attack"],
    "custom-smg": ["smg-deploy", "smg-bolt_back", "smg-bolt_shut", "custom-smg-gunshot-body-suppressed", "custom-smg-gunshot-body", "custom-smg-gunshot-tail-outdoor", "custom-smg-gunshot-LFE", "custom-smg-gunshot-mech"],
    "double-shotgun": ["doubleshotgun-deploy", "double-shotgun-gunshot-body", "double-shotgun-gunshot-LFE", "double-shotgun-gunshot-mech", "double-shotgun-gunshot-tail-outdoor"],
    "eoka-pistol": ["eoka-pistol-deploy", "eoka-pistol-flint-strike", "eoka-pistol-gunshot-body", "eoka-pistol-gunshot-LFE", "eoka-pistol-gunshot-mech", "eoka-pistol-gunshot-tail-outdoor"],
    "f1-grenade": ["f1-grenade-deploy", "f1-grenade-pull-pin", "f1-grenade-explosion"],
    "nailgun": ["nailgun-deploy", "nailgun-attack"],
    "paddle": ["paddle-deploy", "paddle-attack-start", "paddle-attack-whoosh", "paddle-strike-soft", "paddle-strike"],
    "spear": ["spear-2hand-deploy", "spear-attack", "spear-strike-soft", "spear-strike"],
    "glock": ["glock-gunshot-body-suppressed", "glock-deploy", "glock-gunshot-body", "glock-gunshot-LFE", "glock-gunshot-mech", "glock-gunshot-tail-outdoor"],
    "sawnoff-shotgun": ["sawnoff-shotgun-gunshot-body-suppressed", "sawnoff-shotgun-deploy", "sawnoff-shotgun-gunshot-body", "sawnoff-shotgun-gunshot-LFE", "sawnoff-shotgun-gunshot-mech", "sawnoff-shotgun-gunshot-tail-outdoor", "sawnoff-shotgun-pumpaction"],
    "python": ["python-deploy", "python-gunshot-body", "python-gunshot-LFE", "python-gunshot-mech", "python-gunshot-tail-outdoor"],
    "waterpipe": ["waterpipe-shotgun-deploy", "waterpipe-shotgun-gunshot-body", "waterpipe-shotgun-gunshot-LFE", "waterpipe-shotgun-gunshot-mech", "waterpipe-shotgun-gunshot-tail-outdoor"],
    "thompson": ["thompson-gunshot-body-suppressed", "thompson-deploy", "thompson-safety-off", "thompson-gunshot-body", "thompson-gunshot-LFE", "thompson-gunshot-mech", "thompson-gunshot-tail-outdoor", "thompson-dryfire"],
    "revolver": ["revolver-gunshot-body-suppressed", "revolver-deploy", "revolver-dryfire", "revolver-gunshot-body", "revolver-gunshot-LFE", "revolver-gunshot-mech", "revolver-gunshot-tail-outdoor"],
    "semi-auto-pistol": ["semi-auto-pistol-gunshot-body-suppressed", "semi-auto-pistol-gunshot-body", "semi-auto-pistol-gunshot-LFE", "semi-auto-pistol-gunshot-mech", "semi-auto-pistol-gunshot-tail-outdoor"],
    "semi-auto-rifle": ["semi-auto-rifle-gunshot-body-suppressed", "sar-deploy", "sar-deploy_grab_forearm", "semi-auto-rifle-gunshot-body", "semi-auto-rifle-gunshot-LFE", "semi-auto-rifle-gunshot-mech", "semi-auto-rifle-gunshot-tail-outdoor"],
    "2handed-cleaver": ["2handed-cleaver-deploy", "2handed-cleaver-attack", "2handed-cleaver-strike-soft"],
    "sword": ["sword-deploy", "sword-attack", "sword-strike-soft"],
    "rocket-launcher": ["rocket-launcher-deploy", "rocket-launcher-reload-start", "rocket-launcher-reload-open-hatch", "rocket-launcher-reload-insert-rocket", "rocket-launcher-reload-close-hatch", "rocket-launcher-reload-finish", "rocketlauncher_attack", "rocket_engine"],
    "bolt-rifle": ["bolt-rifle-gunshot-body-suppressed", "bolt-rifle-deploy", "bolt-rifle-gunshot-body", "bolt-rifle-gunshot-LFE", "bolt-rifle-gunshot-tail-outdoor", "bolt-rifle-bolt-jack", "bolt-rifle-eject-shell", "bolt-rifle-bolt-forward"],
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
    "metal-detector": "metal-detector.png",
    "c4": "c4.png",
    "survey-charge": "survey-charge.png",
    "flare": "flare.png",
    #Weapons
    "bow": "bow.png",
    "compound-bow": "compound-bow.png",
    "machete": "machete.png",
    "military-flamethrower": "military-flamethrower.png",
    "flamethrower": "flamethrower.png",
    "minigun": "minigun.png",
    "molotov": "molotov.png",
    "mp5": "mp5.png",
    "grenade-launcher": "grenade-launcher.png",
    "spas12": "spas12.png",
    "lr300": "lr300.png",
    "m249": "m249.png",
    "m39": "m39.png",
    "m4": "m4.png",
    "m92": "m92.png",
    "2handed-mace": "2handed-mace.png",
    "hmlmg": "hmlmg.png",
    "homing-missile-launcher": "homing-missile-launcher.png",
    "2handed-sword": "2handed-sword.png",
    "l96": "l96.png",
    "crossbow": "crossbow.png",
    "custom-smg": "custom-smg.png",
    "double-shotgun": "double-shotgun.png",
    "eoka-pistol": "eoka-pistol.png",
    "f1-grenade": "f1-grenade.png",
    "nailgun": "nailgun.png",
    "paddle": "paddle.png",
    "spear": "spear.png",
    "glock": "glock.png",
    "sawnoff-shotgun": "sawnoff-shotgun.png",
    "python": "python.png",
    "waterpipe": "waterpipe.png",
    "thompson": "thompson.png",
    "revolver": "revolver.png",
    "semi-auto-pistol": "semi-auto-pistol",
    "semi-auto-rifle": "semi-auto-rifle.png",
    "2handed-cleaver": "2handed-cleaver.png",
    "sword": "sword.png",
    "rocket-launcher": "rocket-launcher.png",
    "bolt-rifle": "bolt-rifle.png",
    "ak47": "ak47.png"
}

IMAGE_SIZE = (75, 75)
PADDING_LEFT = 0.1
MAX_ITEMS_PER_COLUMN = 10

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

        row, column = 0, 0
        for group, items in GROUPS.items():
            if row >= MAX_ITEMS_PER_COLUMN:
                row = 0
                column += 1
            
            frame = tk.Frame(root)
            frame.grid(row=row, column=column, padx=5, pady=5, sticky="w")

            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(frame, text=group, variable=var, command=lambda g=group: self.toggle_group(g))
            chk.pack(side="left")
            self.group_vars[group] = var

            btn = tk.Button(frame, text="Select Items", command=lambda g=group, i=items: self.open_item_selector(g, i))
            btn.pack(side="left")
            row += 1

        self.clear_clipboard_var = tk.BooleanVar(value=False)
        self.clear_clipboard_chk = tk.Checkbutton(root, text="Clear Clipboard after displaying", variable=self.clear_clipboard_var)
        self.clear_clipboard_chk.grid(row=row, column=0, columnspan=2, pady=10, sticky="w")

        self.start_btn = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.grid(row=row + 1, column=0, columnspan=2, pady=10)

        self.stop_btn = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_btn.grid(row=row + 2, column=0, columnspan=2, pady=10)

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
