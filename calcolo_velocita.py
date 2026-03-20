# calcolo_velocita.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, get_ricetta_velocita


def calcola_pozione_velocita(
    num: int,
    tipo: str,              # "Velocità I" oppure "Velocità II"
    prezzo_lapis: float,
    prezzo_zucchero: float,
    prezzo_blaze: float,
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Pozione di Velocità. Ricette da recipes.json.

    Velocità I (Calderone in terracotta):
        1 Lapis + 1 Zucchero + 1 Carbonella + 1 Boccetta = 1 pozione

    Velocità II (Calderone in ferro):
        1 Blaze + 1 Core fragment + 2 Carbonella + 1 Pozione Velocità I
    """

    if num <= 0:
        raise ValueError("Numero pozioni deve essere > 0")

    # Usa chiavi senza accento per il lookup nel JSON
    tipo_key = tipo.replace("à", "a")  # "Velocità I" -> "Velocita I"

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    rec1 = get_ricetta_velocita("Velocita I")
    p1   = rec1["per_pozione"]
    costo_vel1_unit = (
        p1["lapis"]     * prezzo_lapis
        + p1["zucchero"] * prezzo_zucchero
        + p1["carbonella"] * costo_carbonella_unit
        + p1["boccette"] * costo_boccetta_unit
    )

    if tipo_key == "Velocita I":
        calderone_txt = rec1["calderone"]
        costo_unit    = costo_vel1_unit

    elif tipo_key == "Velocita II":
        rec2  = get_ricetta_velocita("Velocita II")
        calderone_txt = rec2["calderone"]
        p2    = rec2["step_aggiuntivo_per_pozione"]
        costo_extra = (
            p2["blaze"]      * prezzo_blaze
            + p2["core"]     * prezzo_core
            + p2["carbonella"] * costo_carbonella_unit
        )
        costo_unit = costo_vel1_unit + costo_extra
    else:
        raise ValueError("Tipo pozione velocità non valido.")

    costo_tot = costo_unit * num

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
        "--- POZIONE DI VELOCITÀ ---",
        f"Tipo:                     {tipo}",
        f"Calderone:                {calderone_txt}",
        f"Pozioni richieste:        {num}",
        "",
        f"COSTO TOTALE:             {costo_tot:.2f} b",
        f"Costo per pozione:        {costo_unit:.2f} b",
        "",
        "Ricetta base Velocità I:",
        " • 1 Lapis",
        " • 1 Zucchero",
        " • 1 Carbonella",
        " • 1 Boccetta",
        "",
        f"Costo Velocità I (solo step 1): {costo_vel1_unit:.2f} b/poz",
    ]

    if tipo_key == "Velocita II":
        lines += [
            "",
            "Step aggiuntivo Velocità II:",
            " • 1 Blaze",
            " • 1 Core fragment",
            " • 2 Carbonella",
        ]

    lines += [
        "",
        "Costi unitari:",
        f" • Lapis:                 {prezzo_lapis:.2f} b",
        f" • Zucchero:              {prezzo_zucchero:.2f} b",
        f" • Blaze:                 {prezzo_blaze:.2f} b",
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
