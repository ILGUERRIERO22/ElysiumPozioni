# calcolo_multi_prodotto.py
# Modulo per calcolare materiali aggregati per produzioni multiple

from ricette import (
    CARBONELLA_PER_BLOCCO,
    PEPITE_PER_LINGOTTO,
    POZIONI_CURA,
    RESINA,
    ANTIDOTI,
    REVIVIFY,
    EXTINGUISH,
    DANNO,
    RIDUZIONE,
    VELOCITA,
    RESA_PEPITA_NET,
    METALLI_ORDINE,
    get_calderone_pozioni,
    get_catalyst_per_reagente,
    get_ricetta_elisir,
)


def calcola_multi_prodotto(prodotti_lista, prezzi_base):
    """
    Calcola materiali aggregati e costi per produzioni multiple.
    
    Args:
        prodotti_lista: Lista di dict con struttura:
            [
                {
                    'tipo': 'danno_i',
                    'quantita': 10,
                    'prezzo_vendita': 5.0  # opzionale
                },
                {
                    'tipo': 'antidoto_ferro',
                    'quantita': 20,
                    'prezzo_vendita': 3.0
                },
                ...
            ]
        
        prezzi_base: Dict con tutti i prezzi necessari:
            {
                'core': 1.0,
                'reagente': 1.5,
                'carbone': 1.5,   # normalizzato a equivalente Carbone (12 carbonella/blocco)
                'boccette_per_1b': 14,
                'spidereye': 1.5,
                'withering_dust': 2.0,
                'brim': 1.0,
                'rotten': 1.0,
                'revival': 2.0,
                'verdure_per_1b': 3,
                'vasetti_per_1b': 15,
                # ... altri prezzi
            }
    
    Returns:
        Dict con:
            - materiali_aggregati: Dict {nome_materiale: quantita}
            - costi_materiali: Dict {nome_materiale: costo_totale}
            - costo_totale: float
            - ricavo_totale: float (se prezzi vendita forniti)
            - profitto_netto: float (se prezzi vendita forniti)
            - dettaglio_prodotti: Lista con breakdown per prodotto
    """
    
    # Dizionario per aggregare materiali
    materiali = {}
    costi = {}
    
    # Lista dettagli per ogni prodotto
    dettagli = []
    
    costo_totale = 0.0
    ricavo_totale = 0.0
    
    # Calcola costi base comuni
    # 'carbone' arriva gia normalizzato a equivalente Carbone (vedi _get_prezzo_carbone_norm)
    costo_carbonella = prezzi_base.get('carbone', 1.5) / CARBONELLA_PER_BLOCCO
    costo_boccetta = 1.0 / prezzi_base.get('boccette_per_1b', 14)
    costo_resina = calcola_resina(
        prezzi_base.get('verdure_per_1b', 3),
        prezzi_base.get('vasetti_per_1b', 15)
    )
    
    # Processa ogni prodotto
    for prod in prodotti_lista:
        tipo = prod['tipo']
        qty = prod['quantita']
        prezzo_vendita = prod.get('prezzo_vendita', None)
        
        # Calcola materiali e costi per questo prodotto
        mat_prod, costo_prod = calcola_materiali_prodotto(
            tipo, qty, prezzi_base, costo_carbonella, costo_boccetta, costo_resina,
            tier=prod.get('tier', 'T1')
        )
        
        # Aggrega materiali
        for mat, qty_mat in mat_prod.items():
            materiali[mat] = materiali.get(mat, 0) + qty_mat
        
        # Aggrega costi
        for mat, costo_mat in costo_prod.items():
            costi[mat] = costi.get(mat, 0) + costo_mat
        
        # Somma costo totale
        costo_prodotto = sum(costo_prod.values())
        costo_totale += costo_prodotto
        
        # Calcola ricavo se prezzo vendita fornito
        ricavo_prod = 0.0
        if prezzo_vendita:
            ricavo_prod = prezzo_vendita * qty
            ricavo_totale += ricavo_prod
        
        # Salva dettaglio
        dettagli.append({
            'tipo': tipo,
            'nome': get_nome_prodotto(tipo),
            'quantita': qty,
            'costo': costo_prodotto,
            'costo_unitario': costo_prodotto / qty if qty > 0 else 0,
            'prezzo_vendita': prezzo_vendita,
            'ricavo': ricavo_prod,
            'profitto': ricavo_prod - costo_prodotto if prezzo_vendita else None
        })
    
    profitto_netto = ricavo_totale - costo_totale if ricavo_totale > 0 else None
    
    return {
        'materiali_aggregati': materiali,
        'costi_materiali': costi,
        'costo_totale': costo_totale,
        'ricavo_totale': ricavo_totale if ricavo_totale > 0 else None,
        'profitto_netto': profitto_netto,
        'dettaglio_prodotti': dettagli
    }


def calcola_resina(verdure_per_1b, vasetti_per_1b):
    """Calcola costo resina da verdure e vasetti"""
    if verdure_per_1b <= 0 or vasetti_per_1b <= 0:
        return 0.0
    costo_verdura = 1.0 / verdure_per_1b
    costo_vasetto = 1.0 / vasetti_per_1b
    return (2.0 * costo_verdura + costo_vasetto) / 2.0


CALDERONE_PER_TIPO = {
    'cura_terracotta': 'Terracotta',
    'cura_rame':       'Rame',
    'cura_ferro':      'Ferro',
    'cura_oro':        'Oro',
    'cura_diamante':   'Diamante',
    'cura_smeraldo':   'Smeraldo',
}


def _materiali_pozione_cura(calderone, tier, qty, prezzi, costo_carb, costo_bocc):
    """Materiali e costi per qty pozioni di cura, secondo recipes.json.

    Il tier del reagente e' indipendente dal calderone: un reagente T2 produce
    2 catalyst e un T3 ne produce 3, quindi a parita' di pozioni servono meno
    reagenti salendo di tier.
    """
    cal = get_calderone_pozioni(calderone)
    cat_per_rea = get_catalyst_per_reagente(tier)

    catalyst   = qty / cal['pozioni_per_catalyst']
    reagenti   = catalyst / cat_per_rea
    core       = reagenti * POZIONI_CURA['core_per_reagente']
    resine     = reagenti * POZIONI_CURA['resine_per_reagente']
    carbonella = qty / cal['pozioni_per_carbonella']
    boccette   = qty * POZIONI_CURA['boccette_per_pozione']

    # 1 resina = (verdure_per_batch verdure + vasetti_per_batch vasetti) / output
    verdure = resine * RESINA['verdure_per_batch'] / RESINA['output_per_batch']
    vasetti = resine * RESINA['vasetti_per_batch'] / RESINA['output_per_batch']

    materiali = {
        'Reagente':      reagenti,
        'Core fragment': core,
        'Verdura':       verdure,
        'Vasetto':       vasetti,
        'Carbonella':    carbonella,
        'Boccetta':      boccette,
    }
    costi = {
        'Reagente':      reagenti * prezzi.get('reagente', 1.5),
        'Core fragment': core * prezzi.get('core', 1.0),
        'Verdura':       verdure / prezzi.get('verdure_per_1b', 3),
        'Vasetto':       vasetti / prezzi.get('vasetti_per_1b', 15),
        'Carbonella':    carbonella * costo_carb,
        'Boccetta':      boccette * costo_bocc,
    }
    return materiali, costi


# Mappa ingrediente di ricetta -> (etichetta mostrata, chiave prezzo).
# La chiave "resina" e "carbonella" e "boccette" sono trattate a parte perche'
# il loro costo unitario e' gia' calcolato a monte.
INGREDIENTI = {
    'occhio_ragno':   ('Occhio di ragno', 'spidereye'),
    'withering_dust': ('Withering dust',  'withering_dust'),
    'fungo_marrone':  ('Fungo marrone',   'fungo_marrone'),
    'slimeball':      ('Slimeball',       'slime'),
    'core':           ('Core fragment',   'core'),
    'brim':           ('Brim powder',     'brim'),
    'carne_marcia':   ('Carne marcia',    'rotten'),
    'revival_star':   ('Revival star',    'revival'),
    'quarzo':         ('Quarzo',          'quartz'),
    'lapis':          ('Lapis',           'lapis'),
    'zucchero':       ('Zucchero',        'zucchero'),
    'blaze':          ('Blaze',           'blaze'),
}

# Prodotti a step singolo: (sezione di recipes.json, chiave ricetta, campo)
RICETTE_SEMPLICI = {
    'danno_i':             (DANNO,      'Danno I',      'per_pozione'),
    'riduzione_i':         (RIDUZIONE,  'Riduzione I',  'per_pozione'),
    'velocita_i':          (VELOCITA,   'Velocita I',   'per_pozione'),
    'revivify':            (REVIVIFY,   None,           'per_revivify'),
    'extinguish':          (EXTINGUISH, None,           'per_extinguish'),
    'antidoto_terracotta': (ANTIDOTI,   'Terracotta',   'per_antidoto'),
    'antidoto_ferro':      (ANTIDOTI,   'Ferro',        'per_batch'),
}

# Prodotti a due step: il livello II include un'unita' del livello I.
RICETTE_DUE_STEP = {
    'danno_ii':     (DANNO,     'Danno I',     'Danno II'),
    'riduzione_ii': (RIDUZIONE, 'Riduzione I', 'Riduzione II'),
    'velocita_ii':  (VELOCITA,  'Velocita I',  'Velocita II'),
}

ELISIR_PER_TIPO = {
    'elisir_minor':    'Minor mending',
    'elisir_inferior': 'Inferior mending',
    'elisir_lesser':   'Lesser mending',
    'elisir_medium':   'Medium mending',
    'elisir_greater':  'Greater mending',
}

# Etichette delle pepite e chiave prezzo del lingotto corrispondente
PEPITE_PREZZO = {
    'Tin': 'tin', 'Rame': 'copper', 'Ferro': 'iron',
    'Oro': 'gold', 'Diamante': 'diamond',
}


def _applica_ricetta(per_unita, n, materiali, costi, prezzi, costo_carb,
                     costo_bocc, costo_resina):
    """Somma in materiali/costi gli ingredienti di una ricetta, per n unita'."""
    for ing, quanti in per_unita.items():
        tot = n * quanti
        if ing == 'carbonella':
            etichetta, costo_unit = 'Carbonella', costo_carb
        elif ing == 'boccette':
            etichetta, costo_unit = 'Boccetta', costo_bocc
        elif ing == 'resina':
            etichetta, costo_unit = 'Resina', costo_resina
        else:
            etichetta, chiave = INGREDIENTI[ing]
            costo_unit = prezzi.get(chiave, 1.0)
        materiali[etichetta] = materiali.get(etichetta, 0.0) + tot
        costi[etichetta] = costi.get(etichetta, 0.0) + tot * costo_unit
    return materiali, costi


def _materiali_semplice(tipo, qty, prezzi, costo_carb, costo_bocc, costo_resina):
    """Prodotto con una sola fase di preparazione."""
    sezione, chiave, campo = RICETTE_SEMPLICI[tipo]
    ricetta = sezione[chiave] if chiave else sezione
    # Le ricette a lotto (es. antidoto Ferro: 2 per batch) vanno divise
    per_batch = ricetta.get('antidoti_per_batch', 1)
    return _applica_ricetta(ricetta[campo], qty / per_batch, {}, {}, prezzi,
                            costo_carb, costo_bocc, costo_resina)


def _materiali_due_step(tipo, qty, prezzi, costo_carb, costo_bocc):
    """Prodotto di livello II: consuma un'unita' del livello I piu' l'upgrade."""
    sezione, chiave_base, chiave_up = RICETTE_DUE_STEP[tipo]
    materiali, costi = _applica_ricetta(
        sezione[chiave_base]['per_pozione'], qty, {}, {}, prezzi,
        costo_carb, costo_bocc, 0.0)
    return _applica_ricetta(
        sezione[chiave_up]['step_aggiuntivo_per_pozione'], qty, materiali, costi,
        prezzi, costo_carb, costo_bocc, 0.0)


def _materiali_elisir(nome, qty, prezzi, costo_carb, costo_bocc, costo_resina):
    """Elisir: ricetta comune + pepita del metallo e ingrediente extra."""
    ricetta = get_ricetta_elisir(nome)
    per_el = ricetta['per_elisir']
    metallo = ricetta['metallo_pepita']

    materiali, costi = {}, {}
    for ing in ('resina', 'core', 'boccette'):
        _applica_ricetta({ing: per_el[ing]}, qty, materiali, costi, prezzi,
                         costo_carb, costo_bocc, costo_resina)

    # Carbonella: quantita' specifica dell'elisir, non in per_elisir
    _applica_ricetta({'carbonella': ricetta['carbonella_per_elisir']}, qty,
                     materiali, costi, prezzi, costo_carb, costo_bocc, costo_resina)

    n_pepite = qty * per_el['pepite']
    materiali[f'Pepita {metallo}'] = n_pepite
    costi[f'Pepita {metallo}'] = n_pepite * (
        prezzi.get(PEPITE_PREZZO[metallo], 0.0) / PEPITE_PER_LINGOTTO)

    extra = ricetta['ingrediente_extra']
    chiave_extra = ETICHETTA_EXTRA_PREZZO[extra]
    n_extra = qty * per_el['extra']
    materiali[extra] = n_extra
    costi[extra] = n_extra * prezzi.get(chiave_extra, 1.0)

    return materiali, costi


RUNE_PER_TIPO = {
    'rune_maghi': 'Maghi',
    'rune_bardi': 'Bardi',
}

# Metallo delle rune -> chiave prezzo del lingotto.
# L'argento non ha un campo prezzo dedicato: la GUI gli passa quello del diamante.
METALLO_RUNE_PREZZO = {
    'Tin': 'tin', 'Rame': 'copper', 'Ferro': 'iron',
    'Oro': 'gold', 'Argento': 'silver',
}


def _materiali_rune(tipo_rune, qty, prezzi):
    """Rune: confronta i metalli e segnala l'opzione piu' economica.

    Non e' una ricetta a quantita' fisse: per ogni metallo si valuta quante
    pepite servono per qty rune, arrotondate per difetto e per eccesso, e si
    marca con [BEST] la combinazione che costa meno. Solo quella entra nei
    costi, le altre restano visibili come alternative.

    Le rese vengono da recipes.json; i metalli a resa 0 (il Tin per i Maghi)
    non sono utilizzabili e vengono esclusi.
    """
    resa_per_metallo = RESA_PEPITA_NET[tipo_rune]

    opzioni = []
    for metallo in METALLI_ORDINE:
        resa = resa_per_metallo.get(metallo, 0)
        if not resa:
            continue

        pepite_necessarie = qty / resa
        pepite_int_basso = int(pepite_necessarie)
        pepite_int_alto = pepite_int_basso + 1

        prezzo_pepita = prezzi.get(METALLO_RUNE_PREZZO[metallo], 0.0) / PEPITE_PER_LINGOTTO

        if abs(pepite_necessarie - pepite_int_basso) > 0.001:
            for n_pepite in (pepite_int_basso, pepite_int_alto):
                opzioni.append({
                    'pepite': n_pepite,
                    'rune': n_pepite * resa,
                    'costo': n_pepite * prezzo_pepita,
                    'label': f'{metallo}: {n_pepite} pep',
                })
        else:
            opzioni.append({
                'pepite': pepite_necessarie,
                'rune': qty,
                'costo': pepite_necessarie * prezzo_pepita,
                'label': f'{metallo}',
            })

    materiali, costi = {}, {}
    if opzioni:
        migliore = min(opzioni, key=lambda x: x['costo'])
        for opz in opzioni:
            etichetta = f"{opz['label']} -> {opz['rune']:.0f} rune"
            if opz is migliore:
                # Solo la migliore entra nei costi, per non gonfiare il totale
                etichetta = f"[BEST] {etichetta}"
                costi[etichetta] = opz['costo']
            materiali[etichetta] = opz['pepite']

    return materiali, costi


# Ingrediente extra dell'elisir -> chiave prezzo
ETICHETTA_EXTRA_PREZZO = {
    'Brim powder':          'brim',
    'Occhio di ragno':      'spidereye',
    'Membrana di Phantom':  'membrana',
    'Slimeball':            'slime',
    'Lost soul':            'lost_soul',
}


def calcola_materiali_prodotto(tipo, qty, prezzi, costo_carb, costo_bocc,
                               costo_resina, tier='T1'):
    """
    Calcola materiali e costi per un singolo tipo di prodotto.

    tier: tier del reagente per le pozioni di cura ("T1"/"T2"/"T3"), ignorato
          dagli altri prodotti.

    Returns:
        (materiali_dict, costi_dict)
    """
    materiali = {}
    costi = {}

    # POZIONI DI CURA: ricette e rese dei calderoni da recipes.json
    if tipo in CALDERONE_PER_TIPO:
        return _materiali_pozione_cura(
            CALDERONE_PER_TIPO[tipo], tier, qty, prezzi, costo_carb, costo_bocc)

    # --- Prodotti a step singolo e a due step, da recipes.json ---
    if tipo in RICETTE_SEMPLICI:
        return _materiali_semplice(tipo, qty, prezzi, costo_carb, costo_bocc,
                                   costo_resina)

    if tipo in RICETTE_DUE_STEP:
        return _materiali_due_step(tipo, qty, prezzi, costo_carb, costo_bocc)

    if tipo in ELISIR_PER_TIPO:
        return _materiali_elisir(ELISIR_PER_TIPO[tipo], qty, prezzi, costo_carb,
                                 costo_bocc, costo_resina)

    # === RUNE ===
    # Non e' una ricetta ma una scelta: per ogni metallo si valuta quante pepite
    # servono e si evidenzia l'opzione piu' economica. Rese da recipes.json.
    if tipo in RUNE_PER_TIPO:
        return _materiali_rune(RUNE_PER_TIPO[tipo], qty, prezzi)

    return materiali, costi


def get_nome_prodotto(tipo):
    """Restituisce nome leggibile del prodotto"""
    nomi = {
        'cura_terracotta': 'Pozione Cura T1 (Terracotta)',
        'cura_rame': 'Pozione Cura T1 (Rame)',
        'cura_ferro': 'Pozione Cura T2 (Ferro)',
        'cura_oro': 'Pozione Cura T2 (Oro)',
        'cura_diamante': 'Pozione Cura T3 (Diamante)',
        'cura_smeraldo': 'Pozione Cura T3 (Smeraldo)',
        'danno_i': 'Pozione Danno I',
        'danno_ii': 'Pozione Danno II (Avvizzimento)',
        'antidoto_terracotta': 'Antidoto (Terracotta)',
        'antidoto_ferro': 'Antidoto (Ferro)',
        'revivify': 'Revivify',
        'extinguish': 'Extinguish',
        'velocita_i': 'Velocità I',
        'velocita_ii': 'Velocità II',
        'riduzione_i': 'Riduzione I',
        'riduzione_ii': 'Riduzione II',
        'elisir_minor': 'Elisir Minor Mending (Terracotta)',
        'elisir_inferior': 'Elisir Inferior Mending (Rame)',
        'elisir_lesser': 'Elisir Lesser Mending (Ferro)',
        'elisir_medium': 'Elisir Medium Mending (Oro)',
        'elisir_greater': 'Elisir Greater Mending (Diamante)',
        'rune_maghi': 'Rune Maghi',
        'rune_bardi': 'Rune Bardi',
    }
    return nomi.get(tipo, tipo)


def get_tipi_prodotti_disponibili():
    """Restituisce lista di tutti i prodotti disponibili"""
    return [
        # Pozioni di cura (6 calderoni)
        ('cura_terracotta', 'Pozione Cura T1 (Terracotta)'),
        ('cura_rame', 'Pozione Cura T1 (Rame)'),
        ('cura_ferro', 'Pozione Cura T2 (Ferro)'),
        ('cura_oro', 'Pozione Cura T2 (Oro)'),
        ('cura_diamante', 'Pozione Cura T3 (Diamante)'),
        ('cura_smeraldo', 'Pozione Cura T3 (Smeraldo)'),
        # Altri prodotti
        ('danno_i', 'Pozione Danno I'),
        ('danno_ii', 'Pozione Danno II (Avvizzimento)'),
        ('antidoto_terracotta', 'Antidoto (Terracotta)'),
        ('antidoto_ferro', 'Antidoto (Ferro)'),
        ('revivify', 'Revivify'),
        ('extinguish', 'Extinguish'),
        ('velocita_i', 'Velocità I'),
        ('velocita_ii', 'Velocità II'),
        ('riduzione_i', 'Riduzione I'),
        ('riduzione_ii', 'Riduzione II'),
        # Elisir
        ('elisir_minor', 'Elisir Minor Mending (Terracotta)'),
        ('elisir_inferior', 'Elisir Inferior Mending (Rame)'),
        ('elisir_lesser', 'Elisir Lesser Mending (Ferro)'),
        ('elisir_medium', 'Elisir Medium Mending (Oro)'),
        ('elisir_greater', 'Elisir Greater Mending (Diamante)'),
        # Rune
        ('rune_maghi', 'Rune Maghi'),
        ('rune_bardi', 'Rune Bardi'),
    ]
