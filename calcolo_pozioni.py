# calcolo_pozioni.py

"""
Modulo di sola logica per il calcolo delle pozioni di cura.

Nessuna dipendenza da Tkinter o GUI.
Può essere usato sia dal programma principale che da eventuali test.
"""

APP_NAME = "Elysium Pozioni"
APP_VERSION = "2.1.0"
APP_AUTHOR = "ILGUERRIERO22"


def calcola_pozioni(
    num_pozioni: float,
    tier_reagente: str,           # "T1" / "T2" / "T3"
    tipo_calderone: str,          # "Terracotta" / "Rame" / "Ferro" / "Oro" / "Diamante"
    prezzo_reagente: float,
    prezzo_core: float,
    prezzo_carbone: float,
    verdure_per_1b: float,
    vasetti_per_1b: float,
    boccette_per_1b: float,
    prezzo_vendita: float | None = None,
    profilo_attivo: str | None = None,
    app_name: str = APP_NAME,
    app_version: str = APP_VERSION,
    app_author: str = APP_AUTHOR,
) -> dict:
    """
    Esegue tutti i calcoli che prima stavano in calcola() dentro la GUI.

    Ritorna un dizionario con:
      - preview_text: stringa breve per la label in alto
      - output_lines: lista di righe di testo per il box dettagliato
      - vari valori numerici (costo_totale, guadagno, ecc.)

    NON usa Tkinter: nessun widget, nessun messagebox.
    """

    if num_pozioni <= 0:
        raise ValueError("num_pozioni deve essere > 0")

    # --- PACCHETTI (quante unità per 1b) ---
    costo_verdura_unit = 1.0 / verdure_per_1b      # b per 1 verdura
    costo_vasetto_unit = 1.0 / vasetti_per_1b      # b per 1 vasetto
    costo_boccetta_unit = 1.0 / boccette_per_1b    # b per 1 boccetta

    # Resina: 2 verdure + 1 vasetto -> 2 resine
    costo_resina_unit = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0

    # Carbonella: 1 carbone = 12 carbonella
    costo_carbonella_unit = prezzo_carbone / 12.0

    # ======================================================
    # LOGICA CALDERONI
    # ======================================================

    if tipo_calderone == "Terracotta":
        pozioni_per_catalyst = 2.0
        pozioni_per_carbonella = 2.0
        tier_pozione_prodotta = "T1"

    elif tipo_calderone == "Rame":
        pozioni_per_catalyst = 3.0
        pozioni_per_carbonella = 3.0
        tier_pozione_prodotta = "T1"

    elif tipo_calderone == "Ferro":
        pozioni_per_catalyst = 1.0
        pozioni_per_carbonella = 1.0 / 2.0
        tier_pozione_prodotta = "T2"

    elif tipo_calderone == "Oro":
        pozioni_per_catalyst = 1.5
        pozioni_per_carbonella = 1.5
        tier_pozione_prodotta = "T2"

    elif tipo_calderone == "Diamante":
        pozioni_per_catalyst = (2.0 / 3.0)
        pozioni_per_carbonella = (2.0 / 3.0)
        tier_pozione_prodotta = "T3"

    else:
        raise ValueError("Tipo calderone non valido")

    # catalyst necessari:
    catalyst_necessari = num_pozioni / pozioni_per_catalyst
    # carbonella necessaria:
    carbonella_tot = num_pozioni / pozioni_per_carbonella

    # efficienze per output leggibile
    catalyst_per_pozione = 1.0 / pozioni_per_catalyst
    carbonella_per_pozione = 1.0 / pozioni_per_carbonella

    # =========================
    # REAGENTI / CORE / RESINE
    # =========================
    catalyst_per_reagente = {"T1": 1.0, "T2": 2.0, "T3": 3.0}
    if tier_reagente not in catalyst_per_reagente:
        raise ValueError("Tier reagente non valido")

    reagenti_usati = catalyst_necessari / catalyst_per_reagente[tier_reagente]

    # Ogni reagente batch usa 1 core e 1 resina
    core_usati = reagenti_usati
    resine_usate = reagenti_usati

    # Boccette: 1 per pozione
    boccette_tot = num_pozioni * 1.0

    # =========================
    # COSTI PARZIALI
    # =========================
    costo_reagenti = reagenti_usati * prezzo_reagente
    costo_core = core_usati * prezzo_core
    costo_resine = resine_usate * costo_resina_unit
    costo_carbonella = carbonella_tot * costo_carbonella_unit
    costo_boccette = boccette_tot * costo_boccetta_unit

    costo_totale = (
        costo_reagenti
        + costo_core
        + costo_resine
        + costo_carbonella
        + costo_boccette
    )

    costo_per_pozione = costo_totale / num_pozioni if num_pozioni != 0 else 0.0

    # =========================
    # PROFITTO / MARGINE
    # =========================
    if prezzo_vendita is not None:
        ricavo_lotto = prezzo_vendita * num_pozioni
        guadagno = ricavo_lotto - costo_totale
        margine_per_pozione = guadagno / num_pozioni if num_pozioni else 0.0
        ricarico_percent = (
            (margine_per_pozione / costo_per_pozione * 100.0)
            if costo_per_pozione > 0 else 0.0
        )
        prezzo_break_even = costo_per_pozione
    else:
        ricavo_lotto = None
        guadagno = None
        margine_per_pozione = None
        ricarico_percent = None
        prezzo_break_even = None

    # =========================
    # TESTO PREVIEW
    # =========================
    if prezzo_vendita is not None:
        preview_text = (
            f"Totale: {costo_totale:.2f} b    •    "
            f"Costo/poz: {costo_per_pozione:.2f} b    •    "
            f"Guadagno eff.: {guadagno:.2f} b"
        )
    else:
        preview_text = (
            f"Totale: {costo_totale:.2f} b    •    "
            f"Per pozione: {costo_per_pozione:.2f} b"
        )

    # =========================
    # OUTPUT DETTAGLIATO (righe testo)
    # =========================
    profilo_label = profilo_attivo or "(non salvato)"

    output_lines = [
        f"Profilo prezzi attivo:    {profilo_label}",
        f"Calderone:                {tipo_calderone}",
        f"Pozione prodotta:         {tier_pozione_prodotta}",
        f"Pozioni totali richieste: {num_pozioni:.2f}",
        f"Tipo reagente usato:      {tier_reagente}",
        "",
        f"COSTO TOTALE:             {costo_totale:.2f} b",
        f"Costo per pozione:        {costo_per_pozione:.2f} b",
    ]

    if prezzo_vendita is not None:
        output_lines += [
            "",
            "Vendita & Profitto:",
            f" • Prezzo per pozione:        {prezzo_vendita:.2f} b",
            f" • Ricavo totale lotto:        {ricavo_lotto:.2f} b",
            f" • Guadagno netto lotto:       {guadagno:.2f} b",
            f" • Margine per pozione:        {margine_per_pozione:.2f} b",
            f" • Ricarico percentuale:       {ricarico_percent:.1f} %",
            f" • Prezzo di pareggio:         {prezzo_break_even:.2f} b/poz",
        ]

    output_lines += [
        "",
        "Efficienza calderone:",
        f" • Catalyst per pozione:    {catalyst_per_pozione:.4f}",
        f" • Carbonella per pozione:  {carbonella_per_pozione:.4f}",
        "",
        "Materiali richiesti:",
        f" • Catalyst totali:         {catalyst_necessari:.2f}",
        f" • Reagenti usati:          {reagenti_usati:.2f}",
        f" • Core frammenti:          {core_usati:.2f}",
        f" • Resine:                  {resine_usate:.2f}",
        f" • Carbonella totale:       {carbonella_tot:.2f}",
        f" • Boccette:                {boccette_tot:.2f}",
        "",
        "Costi parziali:",
        f" • Reagenti:                {costo_reagenti:.2f} b",
        f" • Core:                    {costo_core:.2f} b",
        f" • Resine:                  {costo_resine:.2f} b",
        f" • Carbonella:              {costo_carbonella:.2f} b",
        f" • Boccette:                {costo_boccette:.2f} b",
        "",
        f"{app_name} v{app_version} — {app_author}",
        "Profili multipli, salvataggio automatico e analisi margine.",
    ]

    return {
        "preview_text": preview_text,
        "output_lines": output_lines,
        "tier_pozione_prodotta": tier_pozione_prodotta,
        "costo_totale": costo_totale,
        "costo_per_pozione": costo_per_pozione,
        "catalyst_necessari": catalyst_necessari,
        "carbonella_tot": carbonella_tot,
        "reagenti_usati": reagenti_usati,
        "core_usati": core_usati,
        "resine_usate": resine_usate,
        "boccette_tot": boccette_tot,
        "ricavo_lotto": ricavo_lotto,
        "guadagno": guadagno,
        "margine_per_pozione": margine_per_pozione,
        "ricarico_percent": ricarico_percent,
        "prezzo_break_even": prezzo_break_even,
    }
