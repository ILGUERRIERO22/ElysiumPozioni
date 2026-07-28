# calcolo_forza.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, get_ricetta_forza


def calcola_pozione_forza(
    num: int,
    tipo: str,                 # "Forza II"
    prezzo_anthracite: float,
    prezzo_quarzo: float,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Pozione di Forza. Ricette da recipes.json.

    Forza II (Calderone in ferro):
        1 Anthracite + 1 Quarzo + 1 Core fragment + 2 Carbonella + 1 Boccetta

    Nota: qui l'Anthracite e' un ingrediente a se', non il combustibile del
    calderone. Le 2 carbonella vanno contate a parte, al prezzo del
    combustibile scelto nella tab Pozioni.
    """

    if num <= 0:
        raise ValueError("Numero pozioni deve essere > 0")

    rec = get_ricetta_forza(tipo)
    p = rec["per_pozione"]

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    q_anthracite = num * p["anthracite"]
    q_quarzo     = num * p["quarzo"]
    q_core       = num * p["core"]
    q_carbonella = num * p["carbonella"]
    q_boccette   = num * p["boccette"]

    costo_anthracite = q_anthracite * prezzo_anthracite
    costo_quarzo     = q_quarzo     * prezzo_quarzo
    costo_core       = q_core       * prezzo_core
    costo_carbonella = q_carbonella * costo_carbonella_unit
    costo_boccette   = q_boccette   * costo_boccetta_unit

    costo_tot = (
        costo_anthracite + costo_quarzo + costo_core
        + costo_carbonella + costo_boccette
    )
    costo_unit = costo_tot / num if num else 0.0

    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo       = prezzo_vendita * num
        guadagno     = ricavo - costo_tot
        margine_unit = guadagno / num if num else 0.0
        ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0

        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Costo/poz: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per pozione: {costo_unit:.2f} b"
        )

    lines = [
        "--- POZIONE DI FORZA ---",
        f"Tipo:                     {tipo}",
        f"Calderone:                {rec['calderone']}",
        f"Pozioni richieste:        {num}",
        "",
        f"COSTO TOTALE:             {costo_tot:.2f} b",
        f"Costo per pozione:        {costo_unit:.2f} b",
        "",
        f"Ricetta {tipo}:",
        f" • {p['anthracite']} Anthracite",
        f" • {p['quarzo']} Quarzo",
        f" • {p['core']} Core fragment",
        f" • {p['carbonella']} Carbonella",
        f" • {p['boccette']} Boccetta",
        "",
        "Materiali richiesti:",
        f" • Anthracite:             {q_anthracite:.2f}",
        f" • Quarzo:                 {q_quarzo:.2f}",
        f" • Core fragment:          {q_core:.2f}",
        f" • Carbonella:             {q_carbonella:.2f}",
        f" • Boccette:               {q_boccette:.2f}",
        "",
        "Costi parziali:",
        f" • Anthracite:             {costo_anthracite:.2f} b",
        f" • Quarzo:                 {costo_quarzo:.2f} b",
        f" • Core fragment:          {costo_core:.2f} b",
        f" • Carbonella:             {costo_carbonella:.2f} b",
        f" • Boccette:               {costo_boccette:.2f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/poz:            {prezzo_vendita:.2f} b",
            f" • Ricavo totale:         {ricavo:.2f} b",
            f" • Guadagno totale:       {guadagno:.2f} b",
            f" • Margine per pozione:   {margine_unit:.2f} b",
            f" • Ricarico %:            {ricarico_pct:.1f} %",
        ]

    return {
        "preview_text": preview,
        "output_lines": lines,
        "costo_tot": costo_tot,
        "costo_unit": costo_unit,
        "ricavo": ricavo,
        "guadagno": guadagno,
        "margine_unit": margine_unit,
        "ricarico_pct": ricarico_pct,
    }
