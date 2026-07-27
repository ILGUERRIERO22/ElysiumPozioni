# Elysium Pozioni

Calcolatore desktop (Python + Tkinter) di costi, materiali e margini per le
pozioni del server Minecraft *Elysium*. GUI a tab, tema scuro, profili di
mercato multipli. Distribuito come EXE Windows via PyInstaller.

Interfaccia, commenti e messaggi di commit sono **in italiano**.

## Architettura

```
main.py                 avvio, chiama run_app()
gui_main.py             classe ElysiumPozioniApp: stato, handler, persistenza
  tabs/tab_*.py         costruzione UI delle 11 tab: build(app)
  calcolo_*.py          logica pura di calcolo (11 moduli), nessun Tkinter
  ricette.py            loader di recipes.json
  recipes.json          ricette del gioco (fonte unica di verita)
  config_app.py         tema, font, palette, percorsi dati
  animations.py         effetti fade/slide
```

Le 11 tab: Pozioni di cura, Antidoti, Revivify, Extinguish, Danno, Rune,
Elisir, Velocita, Riduzione, Multi-Prodotto, Lista della spesa. Le ultime due
sono aggregatori: combinano piu' prodotti in un unico calcolo.

Tre regole che reggono l'impianto — romperle e' il modo piu' rapido di fare
danni:

1. **`recipes.json` e' la fonte unica di verita' delle ricette.** Se cambia un
   bilanciamento del gioco si modifica il JSON, mai i valori nel codice.
2. **I moduli `calcolo_*.py` non importano Tkinter.** Ricevono numeri,
   restituiscono un dict con `preview_text` (riga di riepilogo),
   `output_lines` (dettaglio) e i valori numerici. Nessun widget, nessun
   messagebox: sono eseguibili e testabili senza display. Fanno eccezione i
   due aggregatori, `calcolo_multi_prodotto.py` e `calcolo_spesa.py`, che
   restituiscono dati grezzi formattati poi da `gui_main.py`.
3. **La UI di una tab si costruisce nel suo modulo `tabs/`**, tramite
   `build(app)` che riceve l'istanza dell'app e vi aggancia i widget come
   attributi (`app.entry_core`, ...). `gui_main.py` contiene gli handler
   `do_calcola_*`, non il layout.

### Aggiungere un nuovo prodotto

1. Ricetta in `recipes.json` + accessore in `ricette.py`.
2. `calcolo_<nome>.py` con la logica pura.
3. `tabs/tab_<nome>.py` con `build(app)`.
4. In `gui_main.py`: frame + `notebook.add()` in `_build_main_layout`, voce in
   `_setup_tab_tooltips`, `build` in `_build_tabs`, handler `do_calcola_*`,
   campi in `save_config`/`load_config`.

## Comandi

Avvio:

```bash
python main.py
```

Build dell'EXE:

```bash
pyinstaller ElysiumPozioni.spec
```

Lo `.spec` impacchetta `icon/` e `recipes.json` via `datas`: una nuova risorsa
a runtime va aggiunta li', altrimenti l'EXE non la trova.

**L'EXE si distribuisce via GitHub Release, mai committandolo.** `dist/` e'
ignorato dal repo. Dopo il build, verificare che l'app si avvii e che il titolo
della finestra riporti la versione attesa, poi pubblicare:

```bash
gh release create vX.Y.Z "dist/ElysiumPozioni.exe" --title "ElysiumPozioni vX.Y.Z" --notes "..."
```

Per allegarlo a una release esistente: `gh release upload vX.Y.Z "dist/ElysiumPozioni.exe" --clobber`.
Prima di rilasciare vanno allineati `APP_VERSION` e la sezione "Non rilasciato"
del changelog.

## Trappole note

**`config_app.py` fa `os.chdir()` all'import.** Sposta la working directory in
`%APPDATA%\ElysiumPozioni`, quindi un `import gui_main` da riga di comando
fallisce sui moduli locali. Per test e script:

```python
import sys; sys.path.insert(0, r"C:\Users\dbait\Documents\ElysiumPozioni")
```

**La console Windows e' cp1252.** Qualsiasi script che stampi emoji va lanciato
con `PYTHONIOENCODING=utf-8`, altrimenti muore con `UnicodeEncodeError`.

**`calcolo_multi_prodotto.py` legge le ricette da `ricette.py`**, tramite
cinque funzioni e le tabelle di dispatch in cima al modulo: pozioni di cura
(`_materiali_pozione_cura`), prodotti a step singolo (`RICETTE_SEMPLICI`),
prodotti a due step dove il livello II consuma un'unita' del livello I
(`RICETTE_DUE_STEP`), elisir (`ELISIR_PER_TIPO`) e rune (`RUNE_PER_TIPO`). Un
nuovo prodotto si aggiunge inserendolo nella tabella giusta, senza scrivere
quantita' a mano.

Le **rune** non sono una ricetta ma una scelta: `_materiali_rune` valuta ogni
metallo e marca con `[BEST]` l'opzione piu' economica, che e' l'unica a entrare
nei costi (le altre restano visibili come alternative). I metalli a resa 0 — il
Tin per i Maghi — sono esclusi, altrimenti si dividerebbe per zero.

Le etichette dei materiali vengono dai nomi in `recipes.json`: aggiungendo un
ingrediente vanno estese `INGREDIENTI` o `ETICHETTA_EXTRA_PREZZO`, che mappano
la chiave di ricetta sull'etichetta mostrata e sulla chiave prezzo.

**Il tier del reagente e' indipendente dal calderone.** Un reagente T2 produce
2 catalyst e un T3 ne produce 3 (`catalyst_per_reagente`), quindi salendo di
tier servono meno reagenti per le stesse pozioni. Usare un T1 in un calderone
Diamante e' legittimo. Sia la tab Pozioni sia la tab Multi-Prodotto lasciano
scegliere il tier: non dedurlo mai dal calderone.

**Il prezzo del combustibile va normalizzato.** L'utente sceglie tra Carbone
(12 carbonella/blocco), Anthracite (24) e Firestone (36), ma tutti i moduli
dividono per `CARBONELLA_PER_BLOCCO`. Passare sempre
`self._get_prezzo_carbone_norm()`, mai `float(self.entry_carbone.get())`.

**I campi prezzo possono essere vuoti.** Diversi campi nascono vuoti (es. i
prezzi dei lingotti): `float()` diretto solleva `ValueError` e fa fallire il
calcolo. In `do_calcola_multi` c'e' gia' l'helper `prezzo(nome_entry, default)`
che tratta il vuoto come `0` — usarlo invece di riscrivere la conversione. Per
i campi "per 1 b", che sono divisori, il default e' il valore di ricetta
(14 / 3 / 15) e mai `0`, altrimenti si scambia un `ValueError` con una
`ZeroDivisionError`.

**Verificare avviando la GUI, non solo compilando.** Piu' di un bug qui vive
nel percorso di esecuzione e passa indenne un controllo di sintassi:

```python
root = tk.Tk(); root.withdraw()
app = ElysiumPozioniApp(root)
app.do_calcola_pozioni()
```

## Aspetto

Palette e font stanno **solo** in `config_app.py`: nessun colore va scritto a
mano nei moduli GUI. Tema "alchimia": fondali di pietra scura, `ACCENT` verde
pozione per le azioni primarie, `MAGIC` viola per gli elementi magici, `GOLD`
per i valori monetari.

Le tab del notebook usano **etichette testuali**, non emoji: Tk su Windows le
rende in monocromia e diventano indistinguibili. Per lo stesso motivo il
padding orizzontale delle tab e' contenuto (11 px) — undici etichette devono
stare su una riga sola.

La finestra parte a 980x760 con minimo 950x620: sotto i ~950 px la riga di
pulsanti dei profili viene tagliata dal bordo.

Ogni tab e' divisa in due colonne da `make_split(outer)`, che ritorna
`(container, col_out)`: gli input vanno in `container`, i risultati in
`col_out`, cosi restano visibili mentre si compilano i campi. Header
informativi e pannelli con molti pulsanti in riga (la gestione profili) vanno
invece agganciati a `outer`, a tutta larghezza: nella colonna stretta
verrebbero tagliati.

## Dati utente

`config.json` e `profiles.json` stanno in `%APPDATA%\ElysiumPozioni`, non nel
repo (`config_app.py` migra automaticamente i file legacy). `load_config` legge
per chiave, quindi rimuovere un campo non rompe le configurazioni esistenti.

## Dipendenze

Tkinter (stdlib) e **Pillow**, usata in `gui_main.py` per le icone dei
materiali. Entrambe in `Requirements.txt`; PyInstaller serve solo per il build
ed e' elencato come commento.

## Versionamento

`APP_VERSION` in `config_app.py`, changelog in `CHANGELOG.md` (formato Keep a
Changelog, in italiano). Il lavoro non ancora rilasciato si accumula nella
sezione **"Non rilasciato"** in cima al changelog: al rilascio va rinominata
con il numero di versione e `APP_VERSION` allineato.

Sono volutamente fuori dal repo: artefatti di build (`__pycache__/`, `build/`),
dati utente (`config.json`, `profiles.json`) e la configurazione locale di
Claude Code (`.claude/`). `dist/ElysiumPozioni.exe` e' invece tracciato.

Il file di ignore e' `.gitignore` — fino al 2026-07-27 si chiamava
`.gitignore.txt` e quindi non veniva letto da Git.
