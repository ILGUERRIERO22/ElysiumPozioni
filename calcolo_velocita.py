# calcolo_velocita.py

def calcola_pozione_velocita(
    num,
    tipo,              # "Velocità I" oppure "Velocità II"
    prezzo_lapis,
    prezzo_zucchero,
    prezzo_blaze,
    prezzo_core,
    prezzo_carbone,
    boccette_per_1b,
    prezzo_vendita=None,
):
    """
    Pozione di Velocità

    Velocità I (Calderone in terracotta):
        1 Lapis + 1 Zucchero + 1 Carbonella + 1 Boccetta = 1 pozione

    Velocità II (Calderone in ferro):
        1 Blaze + 1 Core fragment + 2 Carbonella + 1 Pozione Velocità I

    NB: per Velocità II il costo totale è:
        costo(Vel I) + Blaze + Core + 2 Carbonella aggiuntive
    """

    if num <= 0:
        raise ValueError("Numero pozioni deve essere > 0")

    # costi unitari derivati
    costo_carbonella_unit = prezzo_carbone / 12.0   # 1 blocco = 12 carbonella
    costo_boccetta_unit   = 1.0 / boccette_per_1b

    # costo base di 1 Velocità I
    costo_vel1_unit = (
        prezzo_lapis
        + prezzo_zucchero
        + costo_carbonella_unit
        + costo_boccetta_unit
    )

    if tipo == "Velocità I":
        calderone_txt = "Terracotta"
        costo_unit = costo_vel1_unit

    elif tipo == "Velocità II":
        calderone_txt = "Ferro"

        # costo extra per trasformare 1 Vel I in Vel II
        costo_extra = (
            prezzo_blaze           # 1 blaze
            + prezzo_core          # 1 core fragment
            + 2 * costo_carbonella_unit  # 2 carbonella nel secondo step
        )
        costo_unit = costo_vel1_unit + costo_extra
    else:
        raise ValueError("Tipo pozione velocità non valido.")

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

    if tipo == "Velocità II":
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
