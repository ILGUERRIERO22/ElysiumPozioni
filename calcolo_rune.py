# calcolo_rune.py
from typing import Dict, List, Any
from ricette import RESA_PEPITA_NET, METALLI_ORDINE

"""
Calcolo delle rune ottenibili a partire da un certo numero di pepite.
Rese per tipo di rune caricate da recipes.json.
"""


def calcola_rune_diretto(tipo_rune: str, q_pepite: Dict[str, float]) -> Dict[str, Any]:
    """
    Calcola quante rune si ottengono in totale (e i dettagli per metallo)
    in base al tipo di rune ("Maghi" o "Bardi") e a un dizionario
    'q_pepite' con le quantità di pepite per ciascun metallo.
    """

    tipo_rune = tipo_rune.strip()
    if tipo_rune not in RESA_PEPITA_NET:
        raise ValueError("Tipo di rune non valido. Usa 'Maghi' o 'Bardi'.")

    resa = RESA_PEPITA_NET[tipo_rune]
    totale_rune = 0.0
    dettagli = []

    for metallo in METALLI_ORDINE:
        quant_pepite = float(q_pepite.get(metallo, 0) or 0)
        if quant_pepite <= 0:
            continue

        resa_per_pepite = float(resa.get(metallo, 0))
        r_tot = quant_pepite * resa_per_pepite
        totale_rune += r_tot

        dettagli.append(
            f"{metallo}: {quant_pepite:.0f} pepite → "
            f"{r_tot:.0f} rune (resa {resa_per_pepite:.0f}/pep)"
        )

    if totale_rune <= 0:
        preview = "Nessuna pepita valida o resa nulla."
        output_lines = [
            "--- CALCOLO RUNE ---",
            f"Tipo di rune: {tipo_rune}",
            "",
            "Nessuna pepita inserita o rese tutte a 0.",
        ]
    else:
        preview = f"Totale rune: {totale_rune:.0f}"
        output_lines = [
            "--- CALCOLO RUNE ---",
            f"Tipo di rune: {tipo_rune}",
            "",
        ]
        output_lines.extend(dettagli)
        output_lines.append("")
        output_lines.append(f"Totale rune ottenute: {totale_rune:.0f}")

    return {
        "preview_text": preview,
        "output_lines": output_lines,
        "tot_rune": totale_rune,
        "dettagli_per_metallo": dettagli,
    }


def calcola_rune_inverso(tipo_rune: str, num_rune_desiderate: int) -> Dict[str, Any]:
    """
    Per compatibilità con l'import nella GUI.
    Al momento NON implementa ancora il calcolo inverso.
    """
    raise NotImplementedError(
        "calcola_rune_inverso non è ancora implementato."
    )
