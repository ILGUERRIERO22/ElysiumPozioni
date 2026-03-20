# calcolo_revivify.py
from typing import Optional, Dict, Any, List
from ricette import CARBONELLA_PER_BLOCCO, REVIVIFY


def calcola_revivify(
    num: int,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_revival: float,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Ricetta da recipes.json:
      1 Revival star + 1 Core fragment + 1 Carbonella + 1 Boccetta = 1 Revivify
    """

    if num <= 0:
        raise ValueError("Numero Revivify deve essere > 0")

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    p = REVIVIFY["per_revivify"]
    costo_unit = (
        p["revival_star"]  * prezzo_revival
        + p["core"]        * prezzo_core
        + p["carbonella"]  * costo_carbonella_unit
        + p["boccette"]    * costo_boccetta_unit
    )

    costo_tot = costo_unit * num

    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo       = prezzo_vendita * num
        guadagno     = ricavo - costo_tot
        margine_unit = guadagno / num if num else 0.0
        ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0

        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Costo/Rev: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per Revivify: {costo_unit:.2f} b"
        )

    lines = [
        "--- CALCOLO REVIVIFY (Calderone Rame) ---",
        f"Numero Revivify:         {num}",
        "",
        f"COSTO TOTALE:            {costo_tot:.2f} b",
        f"Costo per Revivify:      {costo_unit:.2f} b",
        "",
        "Materiali per 1 Revivify:",
        " • 1 Revival star",
        " • 1 Core fragment",
        " • 1 Carbonella",
        " • 1 Boccetta",
        "",
        "Costi unitari usati:",
        f" • Revival star:         {prezzo_revival:.2f} b",
        f" • Core fragment:        {prezzo_core:.2f} b",
        f" • Carbonella:           {costo_carbonella_unit:.4f} b",
        f" • Boccetta:             {costo_boccetta_unit:.4f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/Rev:           {prezzo_vendita:.2f} b",
            f" • Ricavo totale:        {ricavo:.2f} b",
            f" • Guadagno totale:      {guadagno:.2f} b",
            f" • Margine per Rev:      {margine_unit:.2f} b",
            f" • Ricarico %:           {ricarico_pct:.1f} %",
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
