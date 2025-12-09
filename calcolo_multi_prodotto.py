# calcolo_multi_prodotto.py
# Modulo per calcolare materiali aggregati per produzioni multiple

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
                'carbone': 1.5,
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
    costo_carbonella = prezzi_base.get('carbone', 1.5) / 12.0
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
            tipo, qty, prezzi_base, costo_carbonella, costo_boccetta, costo_resina
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


def calcola_materiali_prodotto(tipo, qty, prezzi, costo_carb, costo_bocc, costo_resina):
    """
    Calcola materiali e costi per un singolo tipo di prodotto.
    
    Returns:
        (materiali_dict, costi_dict)
    """
    materiali = {}
    costi = {}
    
    # POZIONI DI CURA (5 calderoni)
    # Catalyst = 1 reagente + 1 core + 1 resina
    # Resina: 2 verdure + 1 vasetto = 2 resine → 1 resina = 1 verdura + 0.5 vasetti
    # Terracotta: 1 catalyst + 1 carbonella + 2 boccette = 2 pozioni T1
    # Rame:       1 catalyst + 1 carbonella + 3 boccette = 3 pozioni T1
    # Ferro:      1 catalyst + 2 carbonella + 1 boccetta = 1 pozione T2
    # Oro:        2 catalyst + 2 carbonella + 3 boccette = 3 pozioni T2
    # Diamante:   3 catalyst + 3 carbonella + 2 boccette = 2 pozioni T3
    
    if tipo == 'cura_terracotta':
        # 1 catalyst + 1 carb + 2 bocc = 2 pozioni → per qty pozioni servono qty/2 ricette
        ricette = qty / 2.0
        # Catalyst: 1 reagente + 1 core + 1 resina (1 verdura + 0.5 vasetti)
        materiali['Reagente'] = ricette * 1
        materiali['Core fragment'] = ricette * 1
        materiali['Verdura'] = ricette * 1  # Per 1 resina
        materiali['Vasetto'] = ricette * 0.5  # Per 1 resina
        materiali['Carbonella'] = ricette * 1
        materiali['Boccetta'] = ricette * 2
        
        costi['Reagente'] = ricette * prezzi.get('reagente', 1.5)
        costi['Core fragment'] = ricette * prezzi.get('core', 1.0)
        costi['Verdura'] = ricette * 1 * (1.0 / prezzi.get('verdure_per_1b', 3))
        costi['Vasetto'] = ricette * 0.5 * (1.0 / prezzi.get('vasetti_per_1b', 15))
        costi['Carbonella'] = ricette * costo_carb
        costi['Boccetta'] = ricette * 2 * costo_bocc
    
    elif tipo == 'cura_rame':
        # 1 catalyst + 1 carb + 3 bocc = 3 pozioni → per qty pozioni servono qty/3 ricette
        ricette = qty / 3.0
        materiali['Reagente'] = ricette * 1
        materiali['Core fragment'] = ricette * 1
        materiali['Verdura'] = ricette * 1
        materiali['Vasetto'] = ricette * 0.5
        materiali['Carbonella'] = ricette * 1
        materiali['Boccetta'] = ricette * 3
        
        costi['Reagente'] = ricette * prezzi.get('reagente', 1.5)
        costi['Core fragment'] = ricette * prezzi.get('core', 1.0)
        costi['Verdura'] = ricette * 1 * (1.0 / prezzi.get('verdure_per_1b', 3))
        costi['Vasetto'] = ricette * 0.5 * (1.0 / prezzi.get('vasetti_per_1b', 15))
        costi['Carbonella'] = ricette * costo_carb
        costi['Boccetta'] = ricette * 3 * costo_bocc
    
    elif tipo == 'cura_ferro':
        # 1 catalyst + 2 carb + 1 bocc = 1 pozione → per qty pozioni servono qty ricette
        ricette = qty
        materiali['Reagente'] = ricette * 1
        materiali['Core fragment'] = ricette * 1
        materiali['Verdura'] = ricette * 1
        materiali['Vasetto'] = ricette * 0.5
        materiali['Carbonella'] = ricette * 2
        materiali['Boccetta'] = ricette * 1
        
        costi['Reagente'] = ricette * prezzi.get('reagente', 1.5)
        costi['Core fragment'] = ricette * prezzi.get('core', 1.0)
        costi['Verdura'] = ricette * 1 * (1.0 / prezzi.get('verdure_per_1b', 3))
        costi['Vasetto'] = ricette * 0.5 * (1.0 / prezzi.get('vasetti_per_1b', 15))
        costi['Carbonella'] = ricette * 2 * costo_carb
        costi['Boccetta'] = ricette * costo_bocc
    
    elif tipo == 'cura_oro':
        # 2 catalyst + 2 carb + 3 bocc = 3 pozioni → per qty pozioni servono qty/3 ricette
        ricette = qty / 3.0
        materiali['Reagente'] = ricette * 2
        materiali['Core fragment'] = ricette * 2
        materiali['Verdura'] = ricette * 2  # 2 catalyst × 1 verdura
        materiali['Vasetto'] = ricette * 1  # 2 catalyst × 0.5 vasetti
        materiali['Carbonella'] = ricette * 2
        materiali['Boccetta'] = ricette * 3
        
        costi['Reagente'] = ricette * 2 * prezzi.get('reagente', 1.5)
        costi['Core fragment'] = ricette * 2 * prezzi.get('core', 1.0)
        costi['Verdura'] = ricette * 2 * (1.0 / prezzi.get('verdure_per_1b', 3))
        costi['Vasetto'] = ricette * 1 * (1.0 / prezzi.get('vasetti_per_1b', 15))
        costi['Carbonella'] = ricette * 2 * costo_carb
        costi['Boccetta'] = ricette * 3 * costo_bocc
    
    elif tipo == 'cura_diamante':
        # 3 catalyst + 3 carb + 2 bocc = 2 pozioni → per qty pozioni servono qty/2 ricette
        ricette = qty / 2.0
        materiali['Reagente'] = ricette * 3
        materiali['Core fragment'] = ricette * 3
        materiali['Verdura'] = ricette * 3  # 3 catalyst × 1 verdura
        materiali['Vasetto'] = ricette * 1.5  # 3 catalyst × 0.5 vasetti
        materiali['Carbonella'] = ricette * 3
        materiali['Boccetta'] = ricette * 2
        
        costi['Reagente'] = ricette * 3 * prezzi.get('reagente', 1.5)
        costi['Core fragment'] = ricette * 3 * prezzi.get('core', 1.0)
        costi['Verdura'] = ricette * 3 * (1.0 / prezzi.get('verdure_per_1b', 3))
        costi['Vasetto'] = ricette * 1.5 * (1.0 / prezzi.get('vasetti_per_1b', 15))
        costi['Carbonella'] = ricette * 3 * costo_carb
        costi['Boccetta'] = ricette * 2 * costo_bocc
    
    elif tipo == 'danno_i':
        # 1 Occhio ragno + 1 Core + 1 Carbonella + 1 Boccetta
        materiali['Occhio di ragno'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1
        
        costi['Occhio di ragno'] = qty * prezzi.get('spidereye', 1.0)
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc
    
    elif tipo == 'danno_ii':
        # 1 Withering dust + 1 Core + 2 Carbonella + 1 Danno I
        materiali['Withering dust'] = qty * 1
        materiali['Core fragment'] = qty * 2  # 1 per Danno II + 1 per Danno I
        materiali['Carbonella'] = qty * 3  # 2 per Danno II + 1 per Danno I
        materiali['Boccetta'] = qty * 1  # Per Danno I
        materiali['Occhio di ragno'] = qty * 1  # Per Danno I
        
        costi['Withering dust'] = qty * prezzi.get('withering_dust', 2.0)
        costi['Core fragment'] = qty * 2 * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * 3 * costo_carb
        costi['Boccetta'] = qty * costo_bocc
        costi['Occhio di ragno'] = qty * prezzi.get('spidereye', 1.0)
    
    elif tipo == 'antidoto_terracotta':
        # 1 Brim + 1 Carne marcia + 1 Carbonella + 1 Boccetta
        materiali['Brim powder'] = qty * 1
        materiali['Carne marcia'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1
        
        costi['Brim powder'] = qty * prezzi.get('brim', 1.0)
        costi['Carne marcia'] = qty * prezzi.get('rotten', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc
    
    elif tipo == 'antidoto_ferro':
        # 1 Resina + 1 Revival star + 2 Carbonella + 2 Boccette = 2 antidoti
        # Quindi per qty antidoti servono: qty/2 ricette
        ricette_necessarie = qty / 2.0
        
        materiali['Resina'] = ricette_necessarie * 1
        materiali['Revival star'] = ricette_necessarie * 1
        materiali['Carbonella'] = ricette_necessarie * 2
        materiali['Boccetta'] = ricette_necessarie * 2
        
        costi['Resina'] = ricette_necessarie * costo_resina
        costi['Revival star'] = ricette_necessarie * prezzi.get('revival', 2.0)
        costi['Carbonella'] = ricette_necessarie * 2 * costo_carb
        costi['Boccetta'] = ricette_necessarie * 2 * costo_bocc
    
    elif tipo == 'revivify':
        # 1 Revival star + 1 Core + 1 Carbonella + 1 Boccetta
        materiali['Revival star'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1
        
        costi['Revival star'] = qty * prezzi.get('revival', 2.0)
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc
    
    elif tipo == 'extinguish':
        # 1 Quarzo + 1 Core + 1 Carbonella + 1 Boccetta
        materiali['Quarzo'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1
        
        costi['Quarzo'] = qty * prezzi.get('quartz', 1.0)
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc
    
    elif tipo == 'velocita_i':
        # 1 Lapis + 1 Zucchero + 1 Core + 1 Carbonella + 1 Boccetta
        materiali['Lapis'] = qty * 1
        materiali['Zucchero'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1
        
        costi['Lapis'] = qty * prezzi.get('lapis', 1.0)
        costi['Zucchero'] = qty * prezzi.get('zucchero', 1.0)
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc
    
    elif tipo == 'velocita_ii':
        # 1 Blaze + 1 Core + 2 Carbonella + 1 Velocità I
        # Velocità I = 1 Lapis + 1 Zucchero + 1 Core + 1 Carb + 1 Bocc
        materiali['Blaze'] = qty * 1
        materiali['Core fragment'] = qty * 2  # 1 per Vel II + 1 per Vel I
        materiali['Carbonella'] = qty * 3  # 2 per Vel II + 1 per Vel I
        materiali['Boccetta'] = qty * 1  # Per Vel I
        materiali['Lapis'] = qty * 1  # Per Vel I
        materiali['Zucchero'] = qty * 1  # Per Vel I

        costi['Blaze'] = qty * prezzi.get('blaze', 1.0)
        costi['Core fragment'] = qty * 2 * prezzi.get('core', 1.0)
        costi['Carbonella'] = qty * 3 * costo_carb
        costi['Boccetta'] = qty * costo_bocc
        costi['Lapis'] = qty * prezzi.get('lapis', 1.0)
        costi['Zucchero'] = qty * prezzi.get('zucchero', 1.0)

    # === ELISIR ===
    elif tipo == 'elisir_minor':
        # Minor mending (Terracotta): 1 Resina + 1 Core + 1 pepita Tin + 1 Brim + 1 Carbonella + 1 Boccetta
        materiali['Resina'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Pepita Tin'] = qty * 1
        materiali['Brim powder'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1

        costi['Resina'] = qty * costo_resina
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Pepita Tin'] = qty * (prezzi.get('tin', 0.0) / 9.0)
        costi['Brim powder'] = qty * prezzi.get('brim', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc

    elif tipo == 'elisir_inferior':
        # Inferior mending (Rame): 1 Resina + 1 Core + 1 pepita Rame + 1 Occhio di ragno + 1 Carbonella + 1 Boccetta
        materiali['Resina'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Pepita Rame'] = qty * 1
        materiali['Occhio di ragno'] = qty * 1
        materiali['Carbonella'] = qty * 1
        materiali['Boccetta'] = qty * 1

        costi['Resina'] = qty * costo_resina
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Pepita Rame'] = qty * (prezzi.get('copper', 0.0) / 9.0)
        costi['Occhio di ragno'] = qty * prezzi.get('spidereye', 1.0)
        costi['Carbonella'] = qty * costo_carb
        costi['Boccetta'] = qty * costo_bocc

    elif tipo == 'elisir_lesser':
        # Lesser mending (Ferro): 1 Resina + 1 Core + 1 pepita Ferro + 1 Membrana Phantom + 2 Carbonella + 1 Boccetta
        materiali['Resina'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Pepita Ferro'] = qty * 1
        materiali['Membrana Phantom'] = qty * 1
        materiali['Carbonella'] = qty * 2
        materiali['Boccetta'] = qty * 1

        costi['Resina'] = qty * costo_resina
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Pepita Ferro'] = qty * (prezzi.get('iron', 0.0) / 9.0)
        costi['Membrana Phantom'] = qty * prezzi.get('membrana', 1.0)
        costi['Carbonella'] = qty * 2 * costo_carb
        costi['Boccetta'] = qty * costo_bocc

    elif tipo == 'elisir_medium':
        # Medium mending (Oro): 1 Resina + 1 Core + 1 pepita Oro + 1 Slimeball + 2 Carbonella + 1 Boccetta
        materiali['Resina'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Pepita Oro'] = qty * 1
        materiali['Slimeball'] = qty * 1
        materiali['Carbonella'] = qty * 2
        materiali['Boccetta'] = qty * 1

        costi['Resina'] = qty * costo_resina
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Pepita Oro'] = qty * (prezzi.get('gold', 0.0) / 9.0)
        costi['Slimeball'] = qty * prezzi.get('slime', 1.0)
        costi['Carbonella'] = qty * 2 * costo_carb
        costi['Boccetta'] = qty * costo_bocc

    elif tipo == 'elisir_greater':
        # Greater mending (Diamante): 1 Resina + 1 Core + 1 pepita Diamante + 1 Lost soul + 3 Carbonella + 1 Boccetta
        materiali['Resina'] = qty * 1
        materiali['Core fragment'] = qty * 1
        materiali['Pepita Diamante'] = qty * 1
        materiali['Lost soul'] = qty * 1
        materiali['Carbonella'] = qty * 3
        materiali['Boccetta'] = qty * 1

        costi['Resina'] = qty * costo_resina
        costi['Core fragment'] = qty * prezzi.get('core', 1.0)
        costi['Pepita Diamante'] = qty * (prezzi.get('diamond', 0.0) / 9.0)
        costi['Lost soul'] = qty * prezzi.get('lost_soul', 1.0)
        costi['Carbonella'] = qty * 3 * costo_carb
        costi['Boccetta'] = qty * costo_bocc

    # === RUNE ===
    # Rese: rune per pepita
    # Maghi: Tin=0, Rame=11, Ferro=23, Oro=35, Argento=47
    # Bardi: Tin=23, Rame=23, Ferro=23, Oro=35, Argento=47

    elif tipo == 'rune_maghi':
        rese_maghi = [
            ('Rame', 'copper', 11),
            ('Ferro', 'iron', 23),
            ('Oro', 'gold', 35),
            ('Argento', 'silver', 47)
        ]

        # Calcola tutte le opzioni e trova la più economica
        opzioni = []
        for nome_metallo, key_prezzo, resa in rese_maghi:
            pepite_necessarie = qty / resa
            pepite_int_basso = int(pepite_necessarie)
            pepite_int_alto = pepite_int_basso + 1
            rune_ottenute_basso = pepite_int_basso * resa
            rune_ottenute_alto = pepite_int_alto * resa

            prezzo_pepita = prezzi.get(key_prezzo, 0.0) / 9.0
            costo_basso = pepite_int_basso * prezzo_pepita
            costo_alto = pepite_int_alto * prezzo_pepita

            # Aggiungi entrambe le opzioni (basso e alto)
            if abs(pepite_necessarie - pepite_int_basso) > 0.001:
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_int_basso,
                    'rune': rune_ottenute_basso,
                    'costo': costo_basso,
                    'label': f'{nome_metallo}: {pepite_int_basso} pep'
                })
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_int_alto,
                    'rune': rune_ottenute_alto,
                    'costo': costo_alto,
                    'label': f'{nome_metallo}: {pepite_int_alto} pep'
                })
            else:
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_necessarie,
                    'rune': qty,
                    'costo': pepite_necessarie * prezzo_pepita,
                    'label': f'{nome_metallo}'
                })

        # Trova l'opzione più economica
        if opzioni:
            opzione_migliore = min(opzioni, key=lambda x: x['costo'])

            # Mostra TUTTE le opzioni nei materiali, ma solo la migliore nei costi (per il totale)
            for opz in opzioni:
                if opz == opzione_migliore:
                    # Evidenzia la migliore - questa va nei costi per il totale
                    materiali[f"[BEST] {opz['label']} -> {opz['rune']:.0f} rune"] = opz['pepite']
                    costi[f"[BEST] {opz['label']} -> {opz['rune']:.0f} rune"] = opz['costo']
                else:
                    # Mostra le altre solo nei materiali, NON nei costi
                    materiali[f"{opz['label']} -> {opz['rune']:.0f} rune"] = opz['pepite']
                    # NON aggiungo ai costi per non sommare nel totale

    elif tipo == 'rune_bardi':
        rese_bardi = [
            ('Tin', 'tin', 23),
            ('Rame', 'copper', 23),
            ('Ferro', 'iron', 23),
            ('Oro', 'gold', 35),
            ('Argento', 'silver', 47)
        ]

        # Calcola tutte le opzioni e trova la più economica
        opzioni = []
        for nome_metallo, key_prezzo, resa in rese_bardi:
            pepite_necessarie = qty / resa
            pepite_int_basso = int(pepite_necessarie)
            pepite_int_alto = pepite_int_basso + 1
            rune_ottenute_basso = pepite_int_basso * resa
            rune_ottenute_alto = pepite_int_alto * resa

            prezzo_pepita = prezzi.get(key_prezzo, 0.0) / 9.0
            costo_basso = pepite_int_basso * prezzo_pepita
            costo_alto = pepite_int_alto * prezzo_pepita

            # Aggiungi entrambe le opzioni (basso e alto)
            if abs(pepite_necessarie - pepite_int_basso) > 0.001:
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_int_basso,
                    'rune': rune_ottenute_basso,
                    'costo': costo_basso,
                    'label': f'{nome_metallo}: {pepite_int_basso} pep'
                })
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_int_alto,
                    'rune': rune_ottenute_alto,
                    'costo': costo_alto,
                    'label': f'{nome_metallo}: {pepite_int_alto} pep'
                })
            else:
                opzioni.append({
                    'metallo': nome_metallo,
                    'pepite': pepite_necessarie,
                    'rune': qty,
                    'costo': pepite_necessarie * prezzo_pepita,
                    'label': f'{nome_metallo}'
                })

        # Trova l'opzione più economica
        if opzioni:
            opzione_migliore = min(opzioni, key=lambda x: x['costo'])

            # Mostra TUTTE le opzioni nei materiali, ma solo la migliore nei costi (per il totale)
            for opz in opzioni:
                if opz == opzione_migliore:
                    # Evidenzia la migliore - questa va nei costi per il totale
                    materiali[f"[BEST] {opz['label']} -> {opz['rune']:.0f} rune"] = opz['pepite']
                    costi[f"[BEST] {opz['label']} -> {opz['rune']:.0f} rune"] = opz['costo']
                else:
                    # Mostra le altre solo nei materiali, NON nei costi
                    materiali[f"{opz['label']} -> {opz['rune']:.0f} rune"] = opz['pepite']
                    # NON aggiungo ai costi per non sommare nel totale

    return materiali, costi


def get_nome_prodotto(tipo):
    """Restituisce nome leggibile del prodotto"""
    nomi = {
        'cura_terracotta': 'Pozione Cura T1 (Terracotta)',
        'cura_rame': 'Pozione Cura T1 (Rame)',
        'cura_ferro': 'Pozione Cura T2 (Ferro)',
        'cura_oro': 'Pozione Cura T2 (Oro)',
        'cura_diamante': 'Pozione Cura T3 (Diamante)',
        'danno_i': 'Pozione Danno I',
        'danno_ii': 'Pozione Danno II (Avvizzimento)',
        'antidoto_terracotta': 'Antidoto (Terracotta)',
        'antidoto_ferro': 'Antidoto (Ferro)',
        'revivify': 'Revivify',
        'extinguish': 'Extinguish',
        'velocita_i': 'Velocità I',
        'velocita_ii': 'Velocità II',
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
        # Pozioni di cura (5 calderoni)
        ('cura_terracotta', 'Pozione Cura T1 (Terracotta)'),
        ('cura_rame', 'Pozione Cura T1 (Rame)'),
        ('cura_ferro', 'Pozione Cura T2 (Ferro)'),
        ('cura_oro', 'Pozione Cura T2 (Oro)'),
        ('cura_diamante', 'Pozione Cura T3 (Diamante)'),
        # Altri prodotti
        ('danno_i', 'Pozione Danno I'),
        ('danno_ii', 'Pozione Danno II (Avvizzimento)'),
        ('antidoto_terracotta', 'Antidoto (Terracotta)'),
        ('antidoto_ferro', 'Antidoto (Ferro)'),
        ('revivify', 'Revivify'),
        ('extinguish', 'Extinguish'),
        ('velocita_i', 'Velocità I'),
        ('velocita_ii', 'Velocità II'),
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
