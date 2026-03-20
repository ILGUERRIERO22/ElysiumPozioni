# calcolo_antidoti.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, RESINA, get_ricetta_antidoto


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
    Antidoti (ricette da recipes.json):

    TERRACOTTA:
        1 Brim powder + 1 Carne marcia + 1 Carbonella + 1 Boccetta = 1 antidoto

    FERRO:
        1 Resina + 1 Revival star + 2 Carbonella + 2 Boccette = 2 antidoti
    """

    if num <= 0:
        raise ValueError("Numero antidoti deve essere > 0")

    # --- COSTI UNITARI DERIVATI ---
    costo_boccetta_unit   = 1.0 / boccette_per_1b
    costo_vasetto_unit    = 1.0 / vasetti_per_1b
    costo_verdura_unit    = 1.0 / verdure_per_1b
    r = RESINA
    costo_resina_unit     = (
        r["verdure_per_batch"] * costo_verdura_unit + r["vasetti_per_batch"] * costo_vasetto_unit
    ) / r["output_per_batch"]
    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO

    # --- RICETTA DA recipes.json ---
    ricetta = get_ricetta_antidoto(tipo)
    q_brim = q_rotten = q_resina = q_revival = q_carbonella = q_boccette = 0.0

    if tipo == "Terracotta":
        p = ricetta["per_antidoto"]
        antidoti_per_batch = ricetta["antidoti_per_batch"]
        batch = num / antidoti_per_batch
        q_brim       = batch * p["brim"]
        q_rotten     = batch * p["carne_marcia"]
        q_carbonella = batch * p["carbonella"]
        q_boccette   = batch * p["boccette"]
    elif tipo == "Ferro":
        p = ricetta["per_batch"]
        antidoti_per_batch = ricetta["antidoti_per_batch"]
        batch = num / antidoti_per_batch
        q_resina     = batch * p["resina"]
        q_revival    = batch * p["revival_star"]
        q_carbonella = batch * p["carbonella"]
        q_boccette   = batch * p["boccette"]

    # --- COSTI PARZIALI ---
    costo_brim       = q_brim       * prezzo_brim
    costo_rotten     = q_rotten     * prezzo_rotten
    costo_resina     = q_resina     * costo_resina_unit
    costo_revival    = q_revival    * prezzo_revival
    costo_carbonella = q_carbonella * costo_carbonella_unit
    costo_boccette   = q_boccette   * costo_boccetta_unit

    costo_tot = (
        costo_brim + costo_rotten + costo_resina
        + costo_revival + costo_carbonella + costo_boccette
    )
    costo_unit = costo_tot / num if num else 0.0

    # --- PROFITTO (facoltativo) ---
    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo       = prezzo_vendita * num
        guadagno     = ricavo - costo_tot
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
