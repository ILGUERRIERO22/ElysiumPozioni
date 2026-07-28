# calcolo_revivify.py
from typing import Optional, Dict, Any, List
from ricette import (
    CARBONELLA_PER_BLOCCO,
    REVIVIFY,
    get_ricetta_supportive,
    get_catalyst_per_reagente,
)


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


def calcola_supportive_revivify(
    num: int,
    calderone: str,            # "Oro" oppure "Smeraldo"
    prezzo_core: float,
    prezzo_carbone: float,
    boccette_per_1b: int,
    prezzo_revival: float,
    prezzo_reagente: float = 0.0,
    tier_reagente: str = "T1",
    prezzo_demonic_slab: float = 0.0,
    prezzo_end_shard: float = 0.0,
    prezzo_vendita: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Supportive Revivify. Due ricette alternative, da recipes.json.

    Oro:      1 Healing catalyst + 1 Core + 2 Carbonella + 1 Revivify base
              = 1 Supportive
    Smeraldo: 1 Demonic slab + 1 End shard + 1 Core + 3 Carbonella
              + 1 Revivify base = 2 Supportive

    In entrambe la Revivify base fa da contenitore, al posto delle boccette.
    L'healing catalyst e' quello che si ricava dai reagenti: il suo costo
    dipende dal prezzo del reagente e dal tier scelto (un T2 ne da' 2, un T3
    ne da' 3), non da un prezzo a se'.
    """

    if num <= 0:
        raise ValueError("Numero Supportive Revivify deve essere > 0")

    rec = get_ricetta_supportive(calderone)
    p = rec["per_batch"]
    per_batch = rec["supportive_per_batch"]
    batch = num / per_batch

    costo_carbonella_unit = prezzo_carbone / CARBONELLA_PER_BLOCCO

    # La Revivify base viene prodotta, non comprata: ne riusiamo il costo
    base = calcola_revivify(
        num=1, prezzo_core=prezzo_core, prezzo_carbone=prezzo_carbone,
        boccette_per_1b=boccette_per_1b, prezzo_revival=prezzo_revival,
    )
    costo_revivify_unit = base["costo_unit"]

    # Healing catalyst: quanti se ne ricavano da un reagente del tier scelto
    cat_per_reagente = get_catalyst_per_reagente(tier_reagente)
    costo_catalyst_unit = prezzo_reagente / cat_per_reagente if cat_per_reagente else 0.0

    q = {k: batch * v for k, v in p.items()}
    costi = {
        "core":         q.get("core", 0) * prezzo_core,
        "carbonella":   q.get("carbonella", 0) * costo_carbonella_unit,
        "revivify_base": q.get("revivify_base", 0) * costo_revivify_unit,
    }
    if "healing_catalyst" in q:
        costi["healing_catalyst"] = q["healing_catalyst"] * costo_catalyst_unit
    if "demonic_slab" in q:
        costi["demonic_slab"] = q["demonic_slab"] * prezzo_demonic_slab
    if "end_shard" in q:
        costi["end_shard"] = q["end_shard"] * prezzo_end_shard

    costo_tot  = sum(costi.values())
    costo_unit = costo_tot / num if num else 0.0

    ricavo = guadagno = margine_unit = ricarico_pct = None
    if prezzo_vendita is not None:
        ricavo       = prezzo_vendita * num
        guadagno     = ricavo - costo_tot
        margine_unit = guadagno / num if num else 0.0
        ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0

        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Costo/Supp: {costo_unit:.2f} b    •    "
            f"Guadagno: {guadagno:.2f} b"
        )
    else:
        preview = (
            f"Totale: {costo_tot:.2f} b    •    "
            f"Per Supportive: {costo_unit:.2f} b"
        )

    ETICHETTE = {
        "healing_catalyst": "Healing catalyst",
        "demonic_slab":     "Demonic slab",
        "end_shard":        "End shard",
        "core":             "Core fragment",
        "carbonella":       "Carbonella",
        "revivify_base":    "Revivify base",
    }

    lines = [
        f"--- SUPPORTIVE REVIVIFY (Calderone {calderone}) ---",
        f"Supportive richieste:    {num}",
        f"Preparazioni:            {batch:.2f}  ({per_batch} per preparazione)",
        "",
        f"COSTO TOTALE:            {costo_tot:.2f} b",
        f"Costo per Supportive:    {costo_unit:.2f} b",
        "",
        f"Ricetta ({per_batch} Supportive per preparazione):",
    ]
    lines += [f" • {v} {ETICHETTE[k]}" for k, v in p.items()]
    lines += ["", "Materiali richiesti:"]
    lines += [f" • {ETICHETTE[k]:22} {v:.2f}" for k, v in q.items()]
    lines += ["", "Costi parziali:"]
    lines += [f" • {ETICHETTE[k]:22} {v:.2f} b" for k, v in costi.items()]
    lines += [
        "",
        "Costi unitari usati:",
        f" • Revivify base:        {costo_revivify_unit:.4f} b  (prodotta, non comprata)",
    ]
    if "healing_catalyst" in q:
        lines.append(
            f" • Healing catalyst:     {costo_catalyst_unit:.4f} b  "
            f"(reagente {tier_reagente} diviso {cat_per_reagente})")

    if prezzo_vendita is not None:
        lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo/Supp:          {prezzo_vendita:.2f} b",
            f" • Ricavo totale:        {ricavo:.2f} b",
            f" • Guadagno totale:      {guadagno:.2f} b",
            f" • Margine per Supp:     {margine_unit:.2f} b",
            f" • Ricarico %:           {ricarico_pct:.1f} %",
        ]

    return {
        "preview_text": preview,
        "output_lines": lines,
        "costo_tot": costo_tot,
        "costo_unit": costo_unit,
        "costo_revivify_base": costo_revivify_unit,
        "ricavo": ricavo,
        "guadagno": guadagno,
        "margine_unit": margine_unit,
        "ricarico_pct": ricarico_pct,
    }
