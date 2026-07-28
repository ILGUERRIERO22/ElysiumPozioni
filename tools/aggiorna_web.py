"""Allinea docs/recipes.json alla copia nella radice del progetto.

La pagina web deve poter leggere le ricette via fetch(), quindi il file
deve stare dentro docs/. Per non avere due fonti di verita' che divergono,
si modifica SEMPRE recipes.json nella radice e poi si lancia:

    python tools/aggiorna_web.py

Lo script esce con codice 1 se le due copie erano diverse, cosi puo' essere
usato anche come controllo prima di un rilascio.
"""
import filecmp
import shutil
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "recipes.json"
DESTINAZIONE = RADICE / "docs" / "recipes.json"


def main() -> int:
    if not SORGENTE.exists():
        print(f"ERRORE: {SORGENTE} non trovato")
        return 2

    DESTINAZIONE.parent.mkdir(exist_ok=True)

    if DESTINAZIONE.exists() and filecmp.cmp(SORGENTE, DESTINAZIONE, shallow=False):
        print("docs/recipes.json e' gia' allineato")
        return 0

    shutil.copyfile(SORGENTE, DESTINAZIONE)
    print("docs/recipes.json aggiornato da recipes.json")
    return 1


if __name__ == "__main__":
    sys.exit(main())
