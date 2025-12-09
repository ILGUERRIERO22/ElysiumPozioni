# calcolo_antidoti.py
from typing import Optional, Dict, Any

def calcola_antidoti(
    num: int,
    tipo: str,                 # "Terracotta" o "Ferro"
    prezzo_carbone: float,
    boccette_per_1b: int,
    vasetti_per_1b: int,
    verdure_per_1b: int,
    prezzo_brim: float,
    prezzo_rotten: float,
    prezzo_revival: float,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Antidoti (ricette corrette):

    TERRACOTTA:
        1 Brim powder + 1 Carne marcia + 1 Carbonella + 1 Boccetta = 1 antidoto

    FERRO:
        1 Resina + 1 Revival star + 2 Carbonella + 2 Boccette = 2 antidoti

    La resina NON ha un prezzo diretto:
    il suo costo unitario è ricavato dai parametri delle pozioni:
        costo_resina_unit = (2*verdura_unit + vasetto_unit) / 2
    """

    if num <= 0:
        raise ValueError("Numero antidoti deve essere > 0")

    # --- COSTI UNITARI DERIVATI GLOBALI ---
    costo_boccetta_unit = 1.0 / boccette_per_1b
    costo_vasetto_unit  = 1.0 / vasetti_per_1b
    costo_verdura_unit  = 1.0 / verdure_per_1b
    costo_resina_unit   = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0
    costo_carbonella_unit = prezzo_carbone / 12.0  # 1 blocco = 12 carbonella

    # quantità materiali
    q_brim = q_rotten = q_resina = q_revival = 0.0
    q_carbonella = q_boccette = 0.0

    # --- RICETTE ANTIDOTO ---
    # Terracotta: brim + carne marcia + 1 carbonella + 1 boccetta  -> 1 antidoto
    # Ferro:      resina + revival star + 2 carbonella + 2 boccette -> 2 antidoti
    if tipo == "Terracotta":
        # 1 batch = 1 antidoto
        q_brim       = num * 1.0
        q_rotten     = num * 1.0
        q_resina     = 0.0
        q_revival    = 0.0
        q_carbonella = num * 1.0
        q_boccette   = num * 1.0
    elif tipo == "Ferro":
        # 1 batch = 2 antidoti
        batch        = num / 2.0
        q_brim       = 0.0
        q_rotten     = 0.0
        q_resina     = batch * 1.0
        q_revival    = batch * 1.0
        q_carbonella = batch * 2.0
        q_boccette   = batch * 2.0
    else:
        raise ValueError("Tipo calderone antidoti non valido (usa 'Terracotta' o 'Ferro')")

    # --- COSTI PARZIALI ---
    costo_brim       = q_brim       * prezzo_brim
    costo_rotten     = q_rotten     * prezzo_rotten
    costo_resina     = q_resina     * costo_resina_unit
    costo_revival    = q_revival    * prezzo_revival
    costo_carbonella = q_carbonella * costo_carbonella_unit
    costo_boccette   = q_boccette   * costo_boccetta_unit

    costo_tot = (
        costo_brim
        + costo_rotten
        + costo_resina
        + costo_revival
        + costo_carbonella
        + costo_boccette
    )

    costo_unit = costo_tot / num if num else 0.0

    # --- PROFITTO (facoltativo) ---
    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo = prezzo_vendita * num
        guadagno = ricavo - costo_tot
        margine_unit = guadagno / num if num else 0.0
        ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0

        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Costo/ant: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per antidoto: {costo_unit:.2f} b"
        )

    lines = [
        f"Calderone antidoti:       {tipo}",
        f"Antidoti totali richiesti:{num:.2f}",
        "",
        f"COSTO TOTALE:             {costo_tot:.2f} b",
        f"Costo per antidoto:       {costo_unit:.2f} b",
        "",
        "Materiali richiesti:",
        f" • Brim powder:           {q_brim:.2f}",
        f" • Carne marcia:          {q_rotten:.2f}",
        f" • Resina (equivalente):  {q_resina:.2f}",
        f" • Revival star:          {q_revival:.2f}",
        f" • Carbonella:            {q_carbonella:.2f}",
        f" • Boccette:              {q_boccette:.2f}",
        "",
        "Costi parziali:",
        f" • Brim powder:           {costo_brim:.2f} b",
        f" • Carne marcia:          {costo_rotten:.2f} b",
        f" • Resina (da verdure):   {costo_resina:.2f} b",
        f" • Revival star:          {costo_revival:.2f} b",
        f" • Carbonella:            {costo_carbonella:.2f} b",
        f" • Boccette:              {costo_boccette:.2f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/antidoto:       {prezzo_vendita:.2f} b",
            f" • Ricavo totale:         {ricavo:.2f} b",
            f" • Guadagno totale:       {guadagno:.2f} b",
            f" • Margine per antidoto:  {margine_unit:.2f} b",
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
