# calcolo_elisir.py
from typing import Optional, Dict, Any
from ricette import CARBONELLA_PER_BLOCCO, PEPITE_PER_LINGOTTO, RESINA, get_ricetta_elisir


def calcola_elisir(
    num: int,
    tipo: str,                   # "Minor mending" / "Inferior mending" / ...
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    vasetti_per_1b: int,
    verdure_per_1b: int,
    prezzo_brim: float,
    prezzo_spidereye: float,
    prezzo_membrana: float,
    prezzo_slime: float,
    prezzo_lost_soul: float,
    price_tin: float,
    price_cu: float,
    price_fe: float,
    price_au: float,
    price_dia: float,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Calcolo costo elisir di cura. Ricette da recipes.json.
    """

    if num <= 0:
        raise ValueError("Il numero di elisir deve essere > 0")

    # --- Derivati globali ---
    costo_boccetta_unit   = 1.0 / boccette_per_1b
    costo_vasetto_unit    = 1.0 / vasetti_per_1b
    costo_verdura_unit    = 1.0 / verdure_per_1b
    r = RESINA
    costo_resina_unit     = (
        r["verdure_per_batch"] * costo_verdura_unit + r["vasetti_per_batch"] * costo_vasetto_unit
    ) / r["output_per_batch"]
    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO

    # --- Prezzi lingotti -> pepite ---
    prezzi_lingotti = {
        "Tin": price_tin, "Rame": price_cu, "Ferro": price_fe,
        "Oro": price_au,  "Diamante": price_dia,
    }
    pepita_price = {
        k: (v / PEPITE_PER_LINGOTTO if v > 0 else 0.0)
        for k, v in prezzi_lingotti.items()
    }

    # --- Prezzi ingredienti speciali ---
    prezzi_extra = {
        "Brim powder":         float(prezzo_brim),
        "Occhio di ragno":     float(prezzo_spidereye),
        "Membrana di Phantom": float(prezzo_membrana),
        "Slimeball":           float(prezzo_slime),
        "Lost soul":           float(prezzo_lost_soul),
    }

    # --- Ricetta da recipes.json ---
    rec = get_ricetta_elisir(tipo)
    metallo      = rec["metallo_pepita"]
    extra_nome   = rec["ingrediente_extra"]
    carb_per_el  = rec["carbonella_per_elisir"]
    calderone_txt = rec["calderone"]
    p            = rec["per_elisir"]

    extra_prezzo = prezzi_extra.get(extra_nome, 0.0)

    q_resina     = num * p["resina"]
    q_core       = num * p["core"]
    q_pepite     = num * p["pepite"]
    q_extra      = num * p["extra"]
    q_carbonella = num * float(carb_per_el)
    q_boccette   = num * p["boccette"]

    # --- Costi parziali ---
    costo_resina     = q_resina     * costo_resina_unit
    costo_core       = q_core       * prezzo_core
    costo_pepite     = q_pepite     * pepita_price[metallo]
    costo_extra      = q_extra      * extra_prezzo
    costo_carbonella = q_carbonella * costo_carbonella_unit
    costo_boccette   = q_boccette   * costo_boccetta_unit

    costo_tot = (
        costo_resina + costo_core + costo_pepite
        + costo_extra + costo_carbonella + costo_boccette
    )
    costo_unit = costo_tot / num if num else 0.0

    # --- Prezzo vendita / profitto ---
    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo       = prezzo_vendita * num
        guadagno     = ricavo - costo_tot
        margine_unit = guadagno / num if num else 0.0
        ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0

        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Costo/elisir: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per elisir: {costo_unit:.2f} b"
        )

    lines = [
        f"Tipo elisir:              {tipo}",
        f"Calderone:                {calderone_txt}",
        f"Elisir totali richiesti:  {num:.2f}",
        "",
        f"COSTO TOTALE:             {costo_tot:.2f} b",
        f"Costo per elisir:         {costo_unit:.2f} b",
        "",
        "Materiali richiesti:",
        f" • Resina:                {q_resina:.2f}",
        f" • Core fragment:         {q_core:.2f}",
        f" • Pepite in {metallo}:   {q_pepite:.2f}",
        f" • {extra_nome}:          {q_extra:.2f}",
        f" • Carbonella:            {q_carbonella:.2f}",
        f" • Boccette:              {q_boccette:.2f}",
        "",
        "Costi parziali:",
        f" • Resina:                {costo_resina:.2f} b",
        f" • Core:                  {costo_core:.2f} b",
        f" • Pepite {metallo}:      {costo_pepite:.2f} b",
        f" • {extra_nome}:          {costo_extra:.2f} b",
        f" • Carbonella:            {costo_carbonella:.2f} b",
        f" • Boccette:              {costo_boccette:.2f} b",
    ]

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/elisir:         {prezzo_vendita:.2f} b",
            f" • Ricavo totale:         {ricavo:.2f} b",
            f" • Guadagno totale:       {guadagno:.2f} b",
            f" • Margine per elisir:    {margine_unit:.2f} b",
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
