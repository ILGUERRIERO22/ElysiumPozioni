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

# === Tema / colori - Palette "alchimia" ispirata a Minecraft ===
# Fondali di pietra scura, accento verde pozione, viola per gli elementi magici.

# Backgrounds - grigi di pietra con una punta di blu
BG_MAIN   = "#12131a"      # pietra scura, sfondo finestra
BG_PANEL  = "#191b24"      # pannelli
BG_CARD   = "#1e212c"      # card sopra i pannelli
BG_RESULT = "#0c0d12"      # box risultati, il piu' scuro
BG_INPUT  = "#252936"      # campi di input, staccati dalle card

# Foreground - testi
FG_TEXT   = "#e6e8f0"      # testo normale
FG_SUBTLE = "#8d93a6"      # etichette secondarie e suggerimenti
FG_BRIGHT = "#ffffff"      # testo sui pulsanti

# Accent - verde smeraldo, il colore delle pozioni
ACCENT       = "#2ea86a"   # accento primario
ACCENT_HOVER = "#3dc47f"   # hover
ACCENT_LIGHT = "#6ee7a8"   # titoli e valori evidenziati
ACCENT_GLOW  = "#25925c"   # verde profondo, per il lampeggio dei risultati

# Secondary - grigi di pietra per le azioni neutre
SECONDARY = "#39404f"
SECONDARY_HOVER = "#4a5263"

# Status
SUCCESS = "#2ea86a"        # come l'accento: l'azione principale e' "calcola"
SUCCESS_HOVER = "#3dc47f"
DANGER_BG = "#c0392b"      # rosso mattone, meno acceso del precedente
DANGER_BG_HOVER = "#d94f3d"
DANGER_BG_ACTIVE = "#a32e22"

# Special
GOLD = "#e0a63c"           # oro, per i valori monetari
GOLD_HOVER = "#f0bd5c"
MAGIC = "#8b5cf6"          # viola incantesimo, per gli elementi magici
MAGIC_LIGHT = "#a78bfa"

# Borders
BORDER_SUBTLE = "#2b303d"  # bordo delle card
BORDER_ACCENT = "#2ea86a"
INPUT_ERROR = "#a33a2f"    # bordo campo numerico non valido
LOSS_BG     = "#2a0f0d"    # sfondo preview vendita in perdita
LOSS_FG     = "#ff8a7a"    # testo preview vendita in perdita

# Tab
TAB_SELECTED = "#2ea86a"   # tab attiva
TAB_HOVER = "#39404f"

# Fonts - Leggermente più grandi e spaziati
TITLE_FONT   = ("Segoe UI", 16, "bold")    # Più grande per titoli
SECTION_FONT = ("Segoe UI", 12, "bold")    # Più leggibile
LABEL_FONT   = ("Segoe UI", 10)
BUTTON_FONT  = ("Segoe UI", 11, "bold")
RESULT_FONT  = ("Consolas", 10)            # Leggermente più piccolo per risultati
SMALL_FONT   = ("Segoe UI", 9)
PREVIEW_FONT = ("Segoe UI", 11)            # Più grande per preview

# Spacing
BUTTON_PADX = 16     # contenuto: piu' pulsanti devono stare sulla stessa riga
BUTTON_PADY = 8
PANEL_PADX  = 24
PANEL_PADY  = 18
ENTRY_WIDTH = 14
