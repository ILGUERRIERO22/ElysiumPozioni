# test_multi_prodotto.py
# Test del modulo calcolo_multi_prodotto

from calcolo_multi_prodotto import calcola_multi_prodotto

print("=" * 60)
print("TEST CALCOLATRICE MULTI-PRODOTTO")
print("=" * 60)

# Prezzi base di esempio
prezzi_base = {
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
    'quartz': 1.0,
    'lapis': 1.0,
    'zucchero': 1.0,
    'blaze': 1.5,
}

# Lista prodotti da produrre
prodotti = [
    {
        'tipo': 'danno_ii',
        'quantita': 10,
        'prezzo_vendita': 8.0
    },
    {
        'tipo': 'antidoto_ferro',
        'quantita': 20,
        'prezzo_vendita': 3.0
    },
    {
        'tipo': 'velocita_i',
        'quantita': 15,
        'prezzo_vendita': 4.0
    }
]

print("\n📦 PRODOTTI DA PRODURRE:")
for p in prodotti:
    print(f"  • {p['quantita']}x {p['tipo']} (vendita: {p.get('prezzo_vendita', '-')}b)")

# Calcola
risultato = calcola_multi_prodotto(prodotti, prezzi_base)

print("\n" + "=" * 60)
print("💰 MATERIALI NECESSARI (AGGREGATI)")
print("=" * 60)

for materiale, qty in sorted(risultato['materiali_aggregati'].items()):
    costo = risultato['costi_materiali'][materiale]
    print(f"  • {materiale}: {qty:.2f} unità ({costo:.2f}b)")

print("\n" + "=" * 60)
print("💵 RIEPILOGO FINANZIARIO")
print("=" * 60)

print(f"\nCosto totale materiali: {risultato['costo_totale']:.2f}b")
if risultato['ricavo_totale']:
    print(f"Ricavo totale vendita:  {risultato['ricavo_totale']:.2f}b")
    print(f"Profitto netto:         {risultato['profitto_netto']:.2f}b")
    margine_perc = (risultato['profitto_netto'] / risultato['costo_totale']) * 100
    print(f"Margine di profitto:    {margine_perc:.1f}%")

print("\n" + "=" * 60)
print("📋 DETTAGLIO PER PRODOTTO")
print("=" * 60)

for det in risultato['dettaglio_prodotti']:
    print(f"\n{det['nome']} (x{det['quantita']})")
    print(f"  Costo: {det['costo']:.2f}b (unit: {det['costo_unitario']:.2f}b)")
    if det['prezzo_vendita']:
        print(f"  Ricavo: {det['ricavo']:.2f}b")
        print(f"  Profitto: {det['profitto']:.2f}b")

print("\n" + "=" * 60)
print("✅ TEST COMPLETATO!")
print("=" * 60)
