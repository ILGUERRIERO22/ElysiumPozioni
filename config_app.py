# config_app.py

import os
import shutil

APP_NAME = "Elysium Pozioni"
APP_DIRNAME = "ElysiumPozioni"
APP_VERSION = "2.5.0"
APP_AUTHOR = "ILGUERRIERO22"

def get_data_dir():
    base = os.getenv("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, APP_DIRNAME)
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR = get_data_dir()

# Migrazione file legacy (come prima)
for legacy_name in ("config.json", "profiles.json"):
    legacy_src = os.path.join(os.getcwd(), legacy_name)
    legacy_dst = os.path.join(DATA_DIR, legacy_name)
    try:
        if os.path.exists(legacy_src) and not os.path.exists(legacy_dst):
            shutil.move(legacy_src, legacy_dst)
    except Exception as e:
        print("Migrazione legacy fallita:", e)

try:
    os.chdir(DATA_DIR)
except Exception as e:
    print("Impossibile cambiare working dir:", e)

CONFIG_FILE   = "config.json"
PROFILES_FILE = "profiles.json"

# === Tema / colori ===

BG_MAIN   = "#1e1e1e"
BG_PANEL  = "#2a2a2a"
BG_CARD   = "#252525"
BG_RESULT = "#111111"
BG_INPUT  = "#333333"
FG_TEXT   = "#eaeaea"
FG_SUBTLE = "#9e9e9e"
FG_BRIGHT = "#ffffff"
ACCENT    = "#6a5dfd"
ACCENT_HOVER = "#8a7dff"
ACCENT_LIGHT = "#9a8dff"
ACCENT_GLOW  = "#7a6dfe"
SECONDARY = "#4a4a4a"
SECONDARY_HOVER = "#5a5a5a"
SUCCESS = "#2e7d32"
SUCCESS_HOVER = "#3e9d42"
DANGER_BG = "#742e2e"
DANGER_BG_HOVER = "#8a3e3e"
DANGER_BG_ACTIVE = "#993737"
GOLD = "#ffd700"
GOLD_HOVER = "#ffe44d"
BORDER_SUBTLE = "#3a3a3a"
BORDER_ACCENT = "#6a5dfd"
TAB_SELECTED = "#6a5dfd"
TAB_HOVER = "#4a4a4a"

TITLE_FONT   = ("Segoe UI", 15, "bold")
SECTION_FONT = ("Segoe UI", 11, "bold")
LABEL_FONT   = ("Segoe UI", 10)
BUTTON_FONT  = ("Segoe UI", 11, "bold")
RESULT_FONT  = ("Consolas", 11)
SMALL_FONT   = ("Segoe UI", 9)
PREVIEW_FONT = ("Segoe UI", 10)

BUTTON_PADX = 20
BUTTON_PADY = 8
PANEL_PADX  = 20
PANEL_PADY  = 15
ENTRY_WIDTH = 12
