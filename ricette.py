# ricette.py
"""
Loader centralizzato per recipes.json.
Tutti i moduli calcolo_*.py importano da qui invece di avere valori hardcoded.
"""

import json
import os

def _get_recipes_path() -> str:
    """Trova recipes.json sia in modalità sviluppo che come EXE PyInstaller."""
    import sys
    if getattr(sys, "frozen", False):
        # EXE PyInstaller: usa la cartella temporanea dell'eseguibile
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "recipes.json")

_RECIPES_PATH = _get_recipes_path()

def _load() -> dict:
    with open(_RECIPES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_data = _load()

# === GLOBALI ===
CARBONELLA_PER_BLOCCO: int = _data["globali"]["carbonella_per_blocco"]
PEPITE_PER_LINGOTTO: int   = _data["globali"]["pepite_per_lingotto"]
RESINA: dict               = _data["globali"]["resina"]

# === COMBUSTIBILI ===
COMBUSTIBILI: dict = _data["combustibili"]

# === POZIONI CURA ===
POZIONI_CURA: dict = _data["pozioni_cura"]

def get_calderone_pozioni(tipo: str) -> dict:
    """Ritorna la configurazione di un calderone per le pozioni di cura."""
    calderoni = POZIONI_CURA["calderoni"]
    if tipo not in calderoni:
        raise ValueError(f"Calderone non valido: {tipo!r}")
    return calderoni[tipo]

def get_catalyst_per_reagente(tier: str) -> int:
    """Ritorna quanti catalyst servono per 1 reagente del tier dato."""
    mapping = POZIONI_CURA["catalyst_per_reagente"]
    if tier not in mapping:
        raise ValueError(f"Tier reagente non valido: {tier!r}")
    return mapping[tier]

# === ANTIDOTI ===
ANTIDOTI: dict = _data["antidoti"]

def get_ricetta_antidoto(tipo: str) -> dict:
    if tipo not in ANTIDOTI:
        raise ValueError(f"Tipo antidoto non valido: {tipo!r}")
    return ANTIDOTI[tipo]

# === REVIVIFY ===
REVIVIFY: dict = _data["revivify"]
SUPPORTIVE: dict = REVIVIFY["supportive"]

def get_ricetta_supportive(calderone: str) -> dict:
    """Ricetta della Supportive Revivify per il calderone dato (Oro o Smeraldo)."""
    if calderone not in SUPPORTIVE:
        raise ValueError(f"Calderone supportive non valido: {calderone!r}")
    return SUPPORTIVE[calderone]

# === EXTINGUISH ===
EXTINGUISH: dict = _data["extinguish"]

# === ELISIR ===
ELISIR: dict = _data["elisir"]

def get_ricetta_elisir(tipo: str) -> dict:
    if tipo not in ELISIR:
        raise ValueError(f"Tipo elisir non valido: {tipo!r}")
    return ELISIR[tipo]

# === RUNE ===
RUNE: dict = _data["rune"]
RESA_PEPITA_NET: dict  = RUNE["resa_per_pepita"]
METALLI_ORDINE: list   = RUNE["ordine_metalli"]

# === VELOCITA ===
VELOCITA: dict = _data["velocita"]

def get_ricetta_velocita(tipo: str) -> dict:
    if tipo not in VELOCITA:
        raise ValueError(f"Tipo velocita non valido: {tipo!r}")
    return VELOCITA[tipo]

# === DANNO ===
DANNO: dict = _data["danno"]

def get_ricetta_danno(tipo: str) -> dict:
    if tipo not in DANNO:
        raise ValueError(f"Tipo danno non valido: {tipo!r}")
    return DANNO[tipo]

# === FORZA ===
FORZA: dict = _data["forza"]

def get_ricetta_forza(tipo: str) -> dict:
    if tipo not in FORZA:
        raise ValueError(f"Tipo forza non valido: {tipo!r}")
    return FORZA[tipo]

# === RIDUZIONE ===
RIDUZIONE: dict = _data["riduzione"]

def get_ricetta_riduzione(tipo: str) -> dict:
    if tipo not in RIDUZIONE:
        raise ValueError(f"Tipo riduzione non valido: {tipo!r}")
    return RIDUZIONE[tipo]
