# calcolo_danno.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, get_ricetta_danno


def calcola_pozione_danno(
    num: int,
    tipo: str,  # "Danno I" o "Danno II"
    prezzo_spidereye: float,
    prezzo_withering_dust: float,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Pozioni di Danno. Ricette da recipes.json.

    DANNO I (Calderone Rame):
        1 Occhio di ragno + 1 Core + 1 Carbonella + 1 Boccetta = 1 Pozione Danno I

    DANNO II / AVVIZZIMENTO (Calderone Oro):
        1 Withering dust + 1 Core + 2 Carbonella + 1 Pozione Danno I = 1 Pozione Danno II
    """

    if num <= 0:
        raise ValueError("Numero pozioni deve essere > 0")

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    rec1 = get_ricetta_danno("Danno I")
    p1   = rec1["per_pozione"]

    # Costo di 1 Danno I
    danno_i_costo_unit = (
        p1["occhio_ragno"]  * prezzo_spidereye
        + p1["core"]        * prezzo_core
        + p1["carbonella"]  * costo_carbonella_unit
        + p1["boccette"]    * costo_boccetta_unit
    )

    if tipo == "Danno I":
        calderone_info = rec1["calderone"]
        q_spidereye   = num * p1["occhio_ragno"]
        q_withering   = 0.0
        q_core        = num * p1["core"]
        q_carbonella  = num * p1["carbonella"]
        q_boccette    = num * p1["boccette"]
        q_danno_i     = 0.0
        costo_danno_i_ingrediente = 0.0

        costo_spidereye = q_spidereye * prezzo_spidereye
        costo_withering = 0.0
        costo_core_tot  = q_core * prezzo_core
        costo_carbonella = q_carbonella * costo_carbonella_unit
        costo_boccette  = q_boccette * costo_boccetta_unit

        costo_tot = costo_spidereye + costo_core_tot + costo_carbonella + costo_boccette

    elif tipo == "Danno II":
        rec2 = get_ricetta_danno("Danno II")
        calderone_info = rec2["calderone"]
        p2   = rec2["step_aggiuntivo_per_pozione"]

        q_danno_i     = num * 1.0
        costo_danno_i_ingrediente = q_danno_i * danno_i_costo_unit

        q_spidereye  = 0.0
        q_withering  = num * p2["withering_dust"]
        q_core       = num * p2["core"]
        q_carbonella = num * p2["carbonella"]
        q_boccette   = 0.0

        costo_spidereye = 0.0
        costo_withering = q_withering * prezzo_withering_dust
        costo_core_tot  = q_core * prezzo_core
        costo_carbonella = q_carbonella * costo_carbonella_unit
        costo_boccette  = 0.0

        costo_tot = costo_withering + costo_core_tot + costo_carbonella + costo_danno_i_ingrediente

    else:
        raise ValueError("Tipo pozione non valido. Usa 'Danno I' o 'Danno II'")

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
        f"--- CALCOLO POZIONI {tipo.upper()} (Calderone {calderone_info}) ---",
        f"Numero pozioni:          {num:.2f}",
        "",
        f"COSTO TOTALE:            {costo_tot:.2f} b",
        f"Costo per pozione:       {costo_unit:.2f} b",
        "",
    ]

    if tipo == "Danno I":
        lines += [
            "Materiali per 1 Pozione Danno I:",
            " • 1 Occhio di ragno",
            " • 1 Core fragment",
            " • 1 Carbonella",
            " • 1 Boccetta",
            "",
            "Costi unitari usati:",
            f" • Occhio di ragno:      {prezzo_spidereye:.2f} b",
            f" • Core fragment:        {prezzo_core:.2f} b",
            f" • Carbonella:           {costo_carbonella_unit:.4f} b",
            f" • Boccetta:             {costo_boccetta_unit:.4f} b",
        ]
    else:  # Danno II
        lines += [
            "Materiali per 1 Pozione Danno II (Avvizzimento):",
            " • 1 Withering dust",
            " • 1 Core fragment",
            " • 2 Carbonella",
            " • 1 Pozione Danno I",
            "",
            f"Pozioni Danno I necessarie: {q_danno_i:.2f}",
            f"Costo Danno I (ingrediente): {costo_danno_i_ingrediente:.2f} b",
            "",
            "Costi unitari usati:",
            f" • Withering dust:       {prezzo_withering_dust:.2f} b",
            f" • Core fragment:        {prezzo_core:.2f} b",
            f" • Carbonella (x2):      {costo_carbonella_unit:.4f} b/u",
            f" • Danno I (calcolato):  {danno_i_costo_unit:.4f} b",
        ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/pozione:       {prezzo_vendita:.2f} b",
            f" • Ricavo totale:        {ricavo:.2f} b",
            f" • Guadagno totale:      {guadagno:.2f} b",
            f" • Margine per pozione:  {margine_unit:.2f} b",
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
        "calderone": calderone_info,
    }
