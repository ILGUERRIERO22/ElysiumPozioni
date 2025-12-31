# calcolo_riduzione.py
from typing import Optional, Dict, Any

def calcola_pozione_riduzione(
    num: int,
    tipo: str,              # "Riduzione I" oppure "Riduzione II"
    prezzo_fungo_marrone: float,
    prezzo_slimeball: float,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Pozione di Riduzione

    Riduzione I (Calderone in rame):
        1 Fungo marrone + 1 Core fragment + 1 Boccetta + 1 Carbonella = 1 pozione

    Riduzione II (Calderone in oro):
        1 Slimeball + 1 Core fragment + 2 Carbonella + 1 Pozione Riduzione I

    NB: per Riduzione II il costo totale è:
        costo(Rid I) + Slimeball + Core + 2 Carbonella aggiuntive
    """

    if num <= 0:
        raise ValueError("Numero pozioni deve essere > 0")

    # costi unitari derivati
    costo_carbonella_unit = prezzo_carbone / 12.0   # 1 blocco = 12 carbonella
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    # costo base di 1 Riduzione I
    costo_rid1_unit = (
        prezzo_fungo_marrone
        + prezzo_core
        + costo_carbonella_unit
        + costo_boccetta_unit
    )

    if tipo == "Riduzione I":
        calderone_txt = "Rame"
        costo_unit = costo_rid1_unit

    elif tipo == "Riduzione II":
        calderone_txt = "Oro"

        # costo extra per trasformare 1 Rid I in Rid II
        costo_extra = (
            prezzo_slimeball           # 1 slimeball
            + prezzo_core              # 1 core fragment
            + 2 * costo_carbonella_unit  # 2 carbonella nel secondo step
        )
        costo_unit = costo_rid1_unit + costo_extra
    else:
        raise ValueError("Tipo pozione riduzione non valido.")

    costo_tot = costo_unit * num

    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo = prezzo_vendita * num
        guadagno = ricavo - costo_tot
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
        "--- POZIONE DI RIDUZIONE ---",
        f"Tipo:                     {tipo}",
        f"Calderone:                {calderone_txt}",
        f"Pozioni richieste:        {num}",
        "",
        f"COSTO TOTALE:             {costo_tot:.2f} b",
        f"Costo per pozione:        {costo_unit:.2f} b",
        "",
        "Ricetta base Riduzione I:",
        " • 1 Fungo marrone",
        " • 1 Core fragment",
        " • 1 Carbonella",
        " • 1 Boccetta",
        "",
        f"Costo Riduzione I (solo step 1): {costo_rid1_unit:.2f} b/poz",
    ]

    if tipo == "Riduzione II":
        lines += [
            "",
            "Step aggiuntivo Riduzione II:",
            " • 1 Slimeball",
            " • 1 Core fragment",
            " • 2 Carbonella",
        ]

    lines += [
        "",
        "Costi unitari:",
        f" • Fungo marrone:         {prezzo_fungo_marrone:.2f} b",
        f" • Slimeball:             {prezzo_slimeball:.2f} b",
        f" • Core fragment:         {prezzo_core:.2f} b",
        f" • Carbonella:            {costo_carbonella_unit:.4f} b",
        f" • Boccetta:              {costo_boccetta_unit:.4f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/poz:            {prezzo_vendita:.2f} b",
            f" • Ricavo totale:         {ricavo:.2f} b",
            f" • Guadagno totale:       {guadagno:.2f} b",
            f" • Margine unitario:      {margine_unit:.2f} b",
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
