# calcolo_spesa.py
"""
Calcolo degli ingredienti grezzi per un mix di prodotti.
Non dipende da Tkinter. Usa ricette da recipes.json tramite ricette.py.
"""
import math
from collections import defaultdict
from ricette import (
    CARBONELLA_PER_BLOCCO, RESINA, POZIONI_CURA, REVIVIFY, EXTINGUISH,
    COMBUSTIBILI,
    get_calderone_pozioni, get_catalyst_per_reagente,
    get_ricetta_antidoto, get_ricetta_elisir,
    get_ricetta_velocita, get_ricetta_danno, get_ricetta_riduzione,
)


def _resina_to_raw(n_resina: float) -> dict:
    """Decompone n_resina in verdure + vasetti grezzi."""
    r = RESINA
    n_batch = n_resina / r["output_per_batch"]
    return {
        "Verdure":  n_batch * r["verdure_per_batch"],
        "Vasetti":  n_batch * r["vasetti_per_batch"],
    }


def reagente_dettaglio(qty: float, tier: str, calderone: str) -> dict:
    """
    Calcola, per le pozioni di cura, quanti reagenti comprare e quanti HC avanzano.

    Ritorna:
        tier          → tier del reagente
        n_reagenti    → reagenti da comprare (intero)
        hc_needed     → HC necessari (intero, ceil)
        hc_produced   → HC prodotti comprando n_reagenti (intero)
        hc_avanzo     → HC in avanzo (intero >= 0)
    """
    cal         = get_calderone_pozioni(calderone)
    cat_per_rea = get_catalyst_per_reagente(tier)
    poz_per_cat = cal["pozioni_per_catalyst"]

    hc_needed   = math.ceil(qty / poz_per_cat)          # HC servono (intero)
    n_reagenti  = math.ceil(hc_needed / cat_per_rea)    # reagenti da comprare
    hc_produced = n_reagenti * cat_per_rea              # HC ottenuti
    hc_avanzo   = hc_produced - hc_needed               # HC in avanzo

    return {
        "tier":        tier,
        "n_reagenti":  n_reagenti,
        "hc_needed":   hc_needed,
        "hc_produced": hc_produced,
        "hc_avanzo":   hc_avanzo,
    }


def ingredienti_pozione_cura(qty: float, tier: str, calderone: str) -> dict:
    """
    Ingredienti grezzi per qty pozioni di cura.
    Usa ceil per gli interi (reagenti, core, carbonella, boccette).
    Verdure/vasetti possono essere frazionari (da arrotondare nel display).
    """
    cal         = get_calderone_pozioni(calderone)
    cat_per_rea = get_catalyst_per_reagente(tier)
    poz_per_cat = cal["pozioni_per_catalyst"]
    poz_per_cbn = cal["pozioni_per_carbonella"]

    # Ceil sugli interi sin dalla fonte
    hc_needed   = math.ceil(qty / poz_per_cat)
    n_reagenti  = math.ceil(hc_needed / cat_per_rea)
    n_core      = n_reagenti * POZIONI_CURA["core_per_reagente"]
    n_resina    = n_reagenti * POZIONI_CURA["resine_per_reagente"]
    n_boccette  = int(qty * POZIONI_CURA["boccette_per_pozione"])
    n_carbonella = math.ceil(qty / poz_per_cbn)

    raw = defaultdict(float)
    raw[f"Reagente {tier}"] += n_reagenti
    raw["Core fragment"]    += n_core
    raw["Boccette"]         += n_boccette
    raw["Carbonella"]       += n_carbonella
    for k, v in _resina_to_raw(n_resina).items():
        raw[k] += v
    return dict(raw)


def ingredienti_antidoto(qty: float, tipo: str) -> dict:
    ricetta = get_ricetta_antidoto(tipo)
    raw = defaultdict(float)
    n = ricetta["antidoti_per_batch"]
    batch = qty / n

    if tipo == "Terracotta":
        p = ricetta["per_antidoto"]
        raw["Brim powder"]  += batch * p["brim"]
        raw["Carne marcia"] += batch * p["carne_marcia"]
        raw["Carbonella"]   += batch * p["carbonella"]
        raw["Boccette"]     += batch * p["boccette"]
    elif tipo == "Ferro":
        p = ricetta["per_batch"]
        n_resina = batch * p["resina"]
        for k, v in _resina_to_raw(n_resina).items():
            raw[k] += v
        raw["Revival star"] += batch * p["revival_star"]
        raw["Carbonella"]   += batch * p["carbonella"]
        raw["Boccette"]     += batch * p["boccette"]
    return dict(raw)


def ingredienti_revivify(qty: float) -> dict:
    p = REVIVIFY["per_revivify"]
    return {
        "Revival star":  qty * p["revival_star"],
        "Core fragment": qty * p["core"],
        "Carbonella":    qty * p["carbonella"],
        "Boccette":      qty * p["boccette"],
    }


def ingredienti_extinguish(qty: float) -> dict:
    p = EXTINGUISH["per_extinguish"]
    return {
        "Quarzo":        qty * p["quarzo"],
        "Core fragment": qty * p["core"],
        "Carbonella":    qty * p["carbonella"],
        "Boccette":      qty * p["boccette"],
    }


def ingredienti_velocita(qty: float, tipo: str) -> dict:
    tipo_key = tipo.replace("à", "a")
    raw = defaultdict(float)

    rec1 = get_ricetta_velocita("Velocita I")
    p1   = rec1["per_pozione"]
    raw["Lapis"]    += qty * p1["lapis"]
    raw["Zucchero"] += qty * p1["zucchero"]
    raw["Carbonella"] += qty * p1["carbonella"]
    raw["Boccette"] += qty * p1["boccette"]

    if tipo_key == "Velocita II":
        rec2 = get_ricetta_velocita("Velocita II")
        p2   = rec2["step_aggiuntivo_per_pozione"]
        raw["Blaze powder"]  += qty * p2["blaze"]
        raw["Core fragment"] += qty * p2["core"]
        raw["Carbonella"]    += qty * p2["carbonella"]
    return dict(raw)


def ingredienti_danno(qty: float, tipo: str) -> dict:
    raw = defaultdict(float)
    rec1 = get_ricetta_danno("Danno I")
    p1   = rec1["per_pozione"]

    # Danno I è sempre il base (anche per Danno II)
    raw["Occhio di ragno"] += qty * p1["occhio_ragno"]
    raw["Core fragment"]   += qty * p1["core"]
    raw["Carbonella"]      += qty * p1["carbonella"]
    raw["Boccette"]        += qty * p1["boccette"]

    if tipo == "Danno II":
        rec2 = get_ricetta_danno("Danno II")
        p2   = rec2["step_aggiuntivo_per_pozione"]
        raw["Withering dust"] += qty * p2["withering_dust"]
        raw["Core fragment"]  += qty * p2["core"]
        raw["Carbonella"]     += qty * p2["carbonella"]
    return dict(raw)


def ingredienti_riduzione(qty: float, tipo: str) -> dict:
    raw = defaultdict(float)
    rec1 = get_ricetta_riduzione("Riduzione I")
    p1   = rec1["per_pozione"]

    raw["Fungo marrone"] += qty * p1["fungo_marrone"]
    raw["Core fragment"] += qty * p1["core"]
    raw["Carbonella"]    += qty * p1["carbonella"]
    raw["Boccette"]      += qty * p1["boccette"]

    if tipo == "Riduzione II":
        rec2 = get_ricetta_riduzione("Riduzione II")
        p2   = rec2["step_aggiuntivo_per_pozione"]
        raw["Slimeball"]     += qty * p2["slimeball"]
        raw["Core fragment"] += qty * p2["core"]
        raw["Carbonella"]    += qty * p2["carbonella"]
    return dict(raw)


def ingredienti_elisir(qty: float, tipo: str) -> dict:
    rec          = get_ricetta_elisir(tipo)
    metallo      = rec["metallo_pepita"]
    extra_nome   = rec["ingrediente_extra"]
    carb_per_el  = rec["carbonella_per_elisir"]
    p            = rec["per_elisir"]

    raw = defaultdict(float)
    n_resina = qty * p["resina"]
    for k, v in _resina_to_raw(n_resina).items():
        raw[k] += v
    raw["Core fragment"]         += qty * p["core"]
    raw[f"Pepite {metallo}"]     += qty * p["pepite"]
    raw[extra_nome]              += qty * p["extra"]
    raw["Carbonella"]            += qty * float(carb_per_el)
    raw["Boccette"]              += qty * p["boccette"]
    return dict(raw)


# Ingredienti "generici" (non specifici di un solo prodotto)
_GENERICI = {"Boccette", "Verdure", "Vasetti", "Core fragment", "Carbonella"}


def genera_lista_spesa(selezioni: list, tipo_combustibile: str = "Carbone") -> tuple:
    """
    Aggrega gli ingredienti per tutte le selezioni.

    selezioni: lista di dict con chiavi:
        tipo     → "poz_cura"|"antidoto"|"revivify"|"extinguish"|
                   "velocita"|"danno"|"riduzione"|"elisir"
        qty      → float > 0
        params   → dict con parametri specifici (tier, calderone, tipo_prodotto...)
        label    → str descrittiva per l'output

    Ritorna (totale: dict, blocchi_necessari: float)
    """
    totale = defaultdict(float)

    for sel in selezioni:
        t    = sel["tipo"]
        qty  = sel["qty"]
        p    = sel.get("params", {})

        if t == "poz_cura":
            ing = ingredienti_pozione_cura(qty, **p)
        elif t == "antidoto":
            ing = ingredienti_antidoto(qty, **p)
        elif t == "revivify":
            ing = ingredienti_revivify(qty)
        elif t == "extinguish":
            ing = ingredienti_extinguish(qty)
        elif t == "velocita":
            ing = ingredienti_velocita(qty, **p)
        elif t == "danno":
            ing = ingredienti_danno(qty, **p)
        elif t == "riduzione":
            ing = ingredienti_riduzione(qty, **p)
        elif t == "elisir":
            ing = ingredienti_elisir(qty, **p)
        else:
            continue

        for k, v in ing.items():
            totale[k] += v

    # Converti carbonella in blocchi del combustibile scelto
    carbonella_tot   = totale.get("Carbonella", 0.0)
    cbn_per_blocco   = COMBUSTIBILI.get(tipo_combustibile, {}).get("carbonella", CARBONELLA_PER_BLOCCO)
    blocchi_necessari = carbonella_tot / cbn_per_blocco if cbn_per_blocco else 0.0

    return dict(totale), blocchi_necessari
