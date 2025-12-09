# calcolo_rune.py
from typing import Dict, List, Any

"""
Calcolo delle rune ottenibili a partire da un certo numero di pepite
(Tin, Rame, Ferro, Oro, Argento), con due tipologie di rune:
- Maghi
- Bardi

Tutte le rese sono espresse in "rune per 1 pepita".
"""

# Resa in rune per 1 pepita, per tipo di rune
RESA_PEPITA_NET: Dict[str, Dict[str, int]] = {
    "Maghi": {
        "Tin":      0,   # N/D -> lo trattiamo come 0
        "Rame":    11,
        "Ferro":   23,
        "Oro":     35,
        "Argento": 47,
    },
    "Bardi": {
        "Tin":     23,
        "Rame":    23,
        "Ferro":   23,
        "Oro":     35,
        "Argento": 47,
    },
}

METALLI_ORDINE: List[str] = ["Tin", "Rame", "Ferro", "Oro", "Argento"]


def calcola_rune_diretto(tipo_rune: str, q_pepite: Dict[str, float]) -> Dict[str, Any]:
    """
    Calcola quante rune si ottengono in totale (e i dettagli per metallo)
    in base al tipo di rune ("Maghi" o "Bardi") e a un dizionario
    'q_pepite' con le quantità di pepite per ciascun metallo, es:

        {
            "Tin": 0,
            "Rame": 2,
            "Ferro": 0,
            "Oro": 0,
            "Argento": 0,
        }

    Ritorna un dizionario con:
    {
        "preview_text": str,
        "output_lines": [ ... ],
        "tot_rune": float,
        "dettagli_per_metallo": [str, ...]
    }
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
    Al momento NON implementa ancora il calcolo inverso
    (dato un target di rune, calcolare quante pepite servono).

    Potremo implementarlo in seguito se ti serve.
    """
    raise NotImplementedError(
        "calcola_rune_inverso non è ancora implementato."
    )
