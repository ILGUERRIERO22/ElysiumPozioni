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
BG_RESULT = "#111111"
FG_TEXT   = "#eaeaea"
FG_SUBTLE = "#9e9e9e"
ACCENT    = "#6a5dfd"
DANGER_BG = "#742e2e"
DANGER_BG_ACTIVE = "#993737"
DANGER_BG = "#742e2e"
DANGER_BG_ACTIVE = "#993737"


TITLE_FONT   = ("Segoe UI", 15, "bold")
SECTION_FONT = ("Segoe UI", 11, "bold")
LABEL_FONT   = ("Segoe UI", 10)
BUTTON_FONT  = ("Segoe UI", 11, "bold")
RESULT_FONT  = ("Consolas", 11)
