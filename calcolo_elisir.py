# calcolo_elisir.py
from typing import Optional, Dict, Any

def calcola_elisir(
    num: int,
    tipo: str,                   # "Minor mending", "Inferior mending", "Lesser mending", "Medium mending", "Greater mending"
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
    Calcolo costo elisir di cura.

    Ricette per 1 elisir:

      Minor mending (Terracotta):
        1 Resina + 1 Core + 1 pepita Tin + 1 Brim + 1 Carbonella + 1 Boccetta

      Inferior mending (Rame):
        1 Resina + 1 Core + 1 pepita Rame + 1 Occhio di ragno + 1 Carbonella + 1 Boccetta

      Lesser mending (Ferro):
        1 Resina + 1 Core + 1 pepita Ferro + 1 Membrana Phantom + 2 Carbonella + 1 Boccetta

      Medium mending (Oro):
        1 Resina + 1 Core + 1 pepita Oro + 1 Slimeball + 2 Carbonella + 1 Boccetta

      Greater mending (Diamante):
        1 Resina + 1 Core + 1 pepita Diamante + 1 Lost soul + 3 Carbonella + 1 Boccetta

    La resina è derivata da verdure/vasetti:
        costo_resina_unit = (2*costo_verdura + costo_vasetto) / 2
    """

    if num <= 0:
        raise ValueError("Il numero di elisir deve essere > 0")

    # --- Derivati globali (come nelle pozioni) ---
    costo_boccetta_unit   = 1.0 / boccette_per_1b
    costo_vasetto_unit    = 1.0 / vasetti_per_1b
    costo_verdura_unit    = 1.0 / verdure_per_1b
    costo_resina_unit     = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0
    costo_carbonella_unit = prezzo_carbone / 12.0  # 1 blocco = 12 carbonella

    # --- Prezzi ingredienti speciali (passati dalla GUI) ---
    prezzo_brim        = float(prezzo_brim)
    prezzo_spidereye   = float(prezzo_spidereye)
    prezzo_membrana    = float(prezzo_membrana)
    prezzo_slime       = float(prezzo_slime)
    prezzo_lost_soul   = float(prezzo_lost_soul)

    # --- Prezzi lingotti -> pepite (1 lingotto = 9 pepite) ---
    pepita_price = {
        "Tin":      (price_tin / 9.0) if price_tin > 0 else 0.0,
        "Rame":     (price_cu  / 9.0) if price_cu  > 0 else 0.0,
        "Ferro":    (price_fe  / 9.0) if price_fe  > 0 else 0.0,
        "Oro":      (price_au  / 9.0) if price_au  > 0 else 0.0,
        "Diamante": (price_dia / 9.0) if price_dia > 0 else 0.0,
    }

    # (metallo pepita, nome extra, prezzo extra, carbonella per elisir, calderone label)
    REC = {
        "Minor mending":    ("Tin",      "Brim powder",         prezzo_brim,       1, "Terracotta"),
        "Inferior mending": ("Rame",     "Occhio di ragno",     prezzo_spidereye,  1, "Rame"),
        "Lesser mending":   ("Ferro",    "Membrana di Phantom", prezzo_membrana,   2, "Ferro"),
        "Medium mending":   ("Oro",      "Slimeball",           prezzo_slime,      2, "Oro"),
        "Greater mending":  ("Diamante", "Lost soul",           prezzo_lost_soul,  3, "Diamante"),
    }

    if tipo not in REC:
        raise ValueError("Tipo elisir non valido")

    metallo, extra_nome, extra_prezzo, carb_per_el, calderone_txt = REC[tipo]

    # --- Quantità materiali per tutti gli elisir ---
    q_resina     = num * 1.0
    q_core       = num * 1.0
    q_pepite     = num * 1.0
    q_extra      = num * 1.0
    q_carbonella = num * float(carb_per_el)
    q_boccette   = num * 1.0

    # --- Costi parziali ---
    costo_resina     = q_resina     * costo_resina_unit
    costo_core       = q_core       * prezzo_core
    costo_pepite     = q_pepite     * pepita_price[metallo]
    costo_extra      = q_extra      * extra_prezzo
    costo_carbonella = q_carbonella * costo_carbonella_unit
    costo_boccette   = q_boccette   * costo_boccetta_unit

    costo_tot = (
        costo_resina
        + costo_core
        + costo_pepite
        + costo_extra
        + costo_carbonella
        + costo_boccette
    )
    costo_unit = costo_tot / num if num else 0.0

    # --- Prezzo vendita / profitto ---
    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo = prezzo_vendita * num
        guadagno = ricavo - costo_tot
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
