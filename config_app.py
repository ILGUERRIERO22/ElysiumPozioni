# config_app.py

import os
import shutil

APP_NAME = "Elysium Pozioni"
APP_DIRNAME = "ElysiumPozioni"
APP_VERSION = "4.1.0"
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

# === Tema / colori - Palette Moderna Migliorata ===

# Backgrounds - Gradiente più ricco e profondo
BG_MAIN   = "#0f0f1a"      # Blu scuro quasi nero per maggiore profondità
BG_PANEL  = "#1a1a2e"      # Blu scuro per pannelli
BG_CARD   = "#16213e"      # Blu medio per card
BG_RESULT = "#0a0a15"      # Nero bluastro per risultati
BG_INPUT  = "#1f2937"      # Grigio bluastro per input

# Foreground - Testi più leggibili
FG_TEXT   = "#e8eaf6"      # Bianco leggermente bluastro
FG_SUBTLE = "#9ca3af"      # Grigio chiaro per testo secondario
FG_BRIGHT = "#ffffff"      # Bianco puro per evidenziare

# Accent Colors - Viola/Blu più vivaci e moderni
ACCENT    = "#7c3aed"      # Viola intenso
ACCENT_HOVER = "#9d5cff"   # Viola chiaro hover
ACCENT_LIGHT = "#a78bfa"   # Viola pastello
ACCENT_GLOW  = "#8b5cf6"   # Viola luminoso per effetti glow

# Secondary Colors
SECONDARY = "#374151"      # Grigio scuro moderno
SECONDARY_HOVER = "#4b5563" # Grigio hover

# Status Colors - Più vivaci e distintivi
SUCCESS = "#10b981"        # Verde smeraldo moderno
SUCCESS_HOVER = "#34d399"  # Verde chiaro hover
DANGER_BG = "#ef4444"      # Rosso moderno
DANGER_BG_HOVER = "#f87171" # Rosso chiaro hover
DANGER_BG_ACTIVE = "#dc2626" # Rosso scuro active

# Special Colors
GOLD = "#fbbf24"           # Oro moderno
GOLD_HOVER = "#fcd34d"     # Oro chiaro

# Borders - Più sottili e definiti
BORDER_SUBTLE = "#2d3748"  # Grigio bluastro sottile
BORDER_ACCENT = "#7c3aed"  # Viola come accent
INPUT_ERROR = "#8B2222"   # rosso scuro per campo numerico non valido
LOSS_BG     = "#2d0808"   # sfondo preview vendita in perdita
LOSS_FG     = "#ff6b6b"   # testo preview vendita in perdita

# Tab Colors
TAB_SELECTED = "#7c3aed"   # Viola per tab selezionata
TAB_HOVER = "#374151"      # Grigio scuro hover

# Fonts - Leggermente più grandi e spaziati
TITLE_FONT   = ("Segoe UI", 16, "bold")    # Più grande per titoli
SECTION_FONT = ("Segoe UI", 12, "bold")    # Più leggibile
LABEL_FONT   = ("Segoe UI", 10)
BUTTON_FONT  = ("Segoe UI", 11, "bold")
RESULT_FONT  = ("Consolas", 10)            # Leggermente più piccolo per risultati
SMALL_FONT   = ("Segoe UI", 9)
PREVIEW_FONT = ("Segoe UI", 11)            # Più grande per preview

# Spacing - Più generoso per respiro visivo
BUTTON_PADX = 24     # Più padding orizzontale
BUTTON_PADY = 10     # Più padding verticale
PANEL_PADX  = 24     # Più spazio nei pannelli
PANEL_PADY  = 18     # Più spazio verticale
ENTRY_WIDTH = 14     # Input leggermente più larghi
