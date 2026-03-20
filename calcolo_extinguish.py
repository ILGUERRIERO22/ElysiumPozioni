# calcolo_extinguish.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, EXTINGUISH


def calcola_extinguish(
    num: int,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_quartz: float,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Ricetta da recipes.json:
      1 Quarzo + 1 Core fragment + 1 Carbonella + 1 Boccetta = 1 Extinguish
    """

    if num <= 0:
        raise ValueError("Numero Extinguish deve essere > 0")

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    p = EXTINGUISH["per_extinguish"]
    costo_unit = (
        p["quarzo"]       * prezzo_quartz
        + p["core"]       * prezzo_core
        + p["carbonella"] * costo_carbonella_unit
        + p["boccette"]   * costo_boccetta_unit
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
            f"Costo/Ext: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per Extinguish: {costo_unit:.2f} b"
        )

    lines = [
        "--- CALCOLO EXTINGUISH (Calderone Rame) ---",
        f"Numero Extinguish:       {num}",
        "",
        f"COSTO TOTALE:            {costo_tot:.2f} b",
        f"Costo per Extinguish:    {costo_unit:.2f} b",
        "",
        "Materiali per 1 Extinguish:",
        " • 1 Quarzo",
        " • 1 Core fragment",
        " • 1 Carbonella",
        " • 1 Boccetta",
        "",
        "Costi unitari usati:",
        f" • Quarzo:               {prezzo_quartz:.2f} b",
        f" • Core fragment:        {prezzo_core:.2f} b",
        f" • Carbonella:           {costo_carbonella_unit:.4f} b",
        f" • Boccetta:             {costo_boccetta_unit:.4f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/Ext:           {prezzo_vendita:.2f} b",
            f" • Ricavo totale:        {ricavo:.2f} b",
            f" • Guadagno totale:      {guadagno:.2f} b",
            f" • Margine per Ext:      {margine_unit:.2f} b",
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
