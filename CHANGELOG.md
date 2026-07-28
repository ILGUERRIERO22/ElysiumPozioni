# 🧾 Elysium Pozioni — Changelog

Tutte le modifiche rilevanti a questo progetto verranno documentate in questo file.  
Il formato segue le linee guida di [Keep a Changelog](https://keepachangelog.com/it/1.0.0/).

---

## [v4.1] — 2026-07-28
### ⚗️ Tier del reagente nel Multi-Prodotto
- La tab **Multi-Prodotto** ora lascia scegliere il **tier del reagente**
  (T1/T2/T3) per le pozioni di cura, come già fa la tab Pozioni. Il selettore
  compare solo quando serve.
- **I costi delle pozioni T2 e T3 erano sovrastimati**: il calcolo contava un
  reagente per ogni catalyst, ignorando che un reagente T2 ne produce 2 e un T3
  ne produce 3. Con i tier naturali il costo scende del 45 % circa su Ferro e
  Oro e di oltre il 60 % su Diamante e Smeraldo. Le pozioni T1 non erano
  interessate.
- Le due tab ora restituiscono **numeri identici** a parità di parametri.

### 🐞 Correzioni
- **Pozioni di Velocità sovrastimate nel Multi-Prodotto**: il calcolo
  aggiungeva 1 Core fragment a Velocità I, che la ricetta non prevede. Il costo
  scende di conseguenza, anche per Velocità II che include la pozione base. La
  tab Velocità ha sempre dato il numero giusto.
- **Tab Multi-Prodotto: il prezzo del reagente veniva ignorato.** Il valore
  inserito nella tab Pozioni non arrivava al calcolo, che ripiegava sempre sul
  default `1.5 b`. Tutte le stime sulle pozioni di cura erano falsate.
- **Tab Multi-Prodotto: combustibili alternativi sovrastimati.** Il prezzo del
  blocco veniva passato grezzo invece che normalizzato, mentre il modulo divide
  sempre per la carbonella del Carbone: con Anthracite il costo risultava
  doppio, con Firestone triplo.
- **Tab Multi-Prodotto bloccata all'avvio.** Un solo campo prezzo vuoto in una
  qualsiasi tab faceva fallire l'intero calcolo con
  `could not convert string to float: ''`. Il caso si presentava sempre, perché
  i cinque prezzi dei lingotti nascono vuoti, e bloccava anche prodotti che con
  i lingotti non c'entrano nulla. Ora un campo vuoto vale `0`; i tre campi
  "per 1 b", essendo divisori, usano il valore di ricetta.

### 🧹 Pulizia
- Rimosso il campo **"Sconto cliente (%)"**: veniva salvato e ricaricato, ma
  nessun calcolo lo leggeva — lo sconto inserito non aveva alcun effetto.
- Rimosso l'output di debug stampato a ogni calcolo Multi-Prodotto.
- Il divisore `12.0` scritto a mano ora è `CARBONELLA_PER_BLOCCO` da
  `recipes.json`.

### 🧱 Repository
- **Il file di ignore non era mai stato attivo**: si chiamava `.gitignore.txt`,
  nome che Git non legge. Rinominato in `.gitignore`; le regole già presenti
  (`__pycache__/`, `build/`, `dist/`) sono finalmente in vigore.
- Rimossi dal versionamento 41 artefatti di build e `profiles.json`, che è un
  file di dati utente e vive in `%APPDATA%\ElysiumPozioni`.

---

## [v4.0] — 2026-03-21
### 🗂️ Ricette centralizzate
- Introdotto **`recipes.json`** come fonte unica di verità per tutte le ricette,
  esposto ai moduli tramite `ricette.py`. I valori non sono più sparsi nel
  codice: per adeguarsi a un cambio di bilanciamento del gioco basta modificare
  il JSON.

### 🧩 GUI modulare
- La costruzione dell'interfaccia è stata estratta da `gui_main.py` nel
  pacchetto **`tabs/`**, un modulo per tab.

### 🔥 Multi-combustibile
- Aggiunta la scelta del combustibile: **Carbone** (12 carbonella per blocco),
  **Anthracite** (24) e **Firestone** (36), con conversione automatica.

### 🛒 Lista della spesa
- Nuova tab che, dato un mix di prodotti, calcola gli **ingredienti grezzi**
  totali da acquistare, con arrotondamento all'intero, avanzi e blocchi di
  combustibile necessari.

### ⚠️ Alert perdita
- Se il prezzo di vendita impostato è sotto il costo di produzione, il risultato
  viene evidenziato in rosso con l'importo perso sul lotto.

---

## [v3.2.1] — 2025-12-09 → 2025-12-31
### ✨ Interfaccia
- Grafica rinnovata con tema scuro moderno (palette viola/blu).
- Sistema di **animazioni** per cambio tab e aggiornamento dei risultati.
- Tab compattate a sole icone, con **tooltip** al passaggio del mouse.
- Icone dei materiali in stile Minecraft mostrate accanto ai campi e nei
  risultati.

### 🔻 Nuovi prodotti
- Aggiunte le **Pozioni di Riduzione** (Riduzione I e II).

### 🐞 Correzioni
- Risolto il crash e il comportamento errato dello scroll su combobox e aree di
  testo.

### 🧱 Interno
- Aggiunti **type hints** ai moduli di calcolo.

---

## [v3.0] — 2025-12-08 → 2025-12-09
### ⚔️ Pozioni di Danno
- Aggiunta la tab **Danno**, con Danno I e Danno II (Avvizzimento).

### 🧮 Calcolatrice Multi-Prodotto
- Nuova tab che aggrega **più prodotti in un unico calcolo**: materiali totali,
  costi e profitto complessivo.
- Estesa progressivamente a elisir e rune; per le rune il sistema confronta i
  metalli e **evidenzia l'opzione più economica**.

---

## [v2.5] — 2025-11-25
### 🧱 Refactoring architetturale
- Il monolite `Pozioni.py` è stato smontato in **moduli di sola logica**
  (`calcolo_*.py`), senza alcuna dipendenza da Tkinter, separati dalla GUI
  (`gui_main.py`) e dalla configurazione (`config_app.py`).
- Progetto rinominato in **ElysiumPozioni**.

---

## [v2.0] — 2025-11-09
### ⚗️ Nuovi prodotti
- Aggiunte le tab **Antidoti**, **Revivify**, **Extinguish**, **Elisir di cura**,
  **Rune** e **Pozioni di Velocità**.
- I prezzi condivisi (core, carbone, boccette, resina) vengono propagati
  automaticamente tra le tab.

---

## [v1.4.1] — 2025-11-01
### 🐞 Correzioni
- Risolto un problema all'avvio dell'applicazione.
- I file `config.json` e `profiles.json` vengono ora salvati in
  `%APPDATA%\ElysiumPozioni` invece che nella cartella del programma, con
  migrazione automatica di quelli già esistenti.

---

## [v1.4] — 2025-10-26
### 💰 Analisi profitto
- Aggiunto campo "Prezzo di vendita per pozione (b)".
- Ora il calcolatore mostra automaticamente:
  - Margine per pozione (prezzo vendita - costo produzione)
  - Margine totale sul lotto richiesto
  - Ricarico percentuale (% di profitto rispetto al costo)
- L’anteprima rapida in alto ora, se inserisci un prezzo di vendita, mostra anche il Margine/poz oltre al Costo/poz.

### 🧠 Qualità di vita
- L’ultimo prezzo di vendita inserito viene salvato in `config.json` e ripristinato al riavvio.
- Tutta la gestione profili rimane disponibile direttamente da interfaccia:
  - Salva profilo (crea/aggiorna)
  - Carica profilo
  - Rinomina profilo
  - Elimina profilo (con conferma)

### ⚗️ Produzione
- Restano supportati tutti i calderoni:
  - Terracotta (T1)
  - Rame (T1)
  - Ferro (T2)
  - Oro (T2)
  - Diamante (T3)
- Per ogni calderone continui a vedere:
  - catalyst necessari
  - carbonella totale
  - core fragment e resine
  - boccette richieste
  - efficienza catalyst/pozione e carbonella/pozione
  - costo totale e costo per pozione

### 🔁 Version bump
- `APP_VERSION` aggiornato a `1.4`.
- Interfaccia estesa con pannello "Vendita" dedicato al prezzo di vendita.


## [v1.3.2] — 2025-10-26
### 🧼 Gestione profili completa
- Aggiunto il pulsante **"Elimina profilo"** nel pannello "Profilo prezzi".
- Ora è possibile cancellare un profilo di mercato direttamente dall'interfaccia.
- Prima di eliminare un profilo viene mostrata una conferma di sicurezza.
- Dopo l'eliminazione:
  - il profilo sparisce dal file `profiles.json`
  - la lista dei profili nella combo viene aggiornata
  - se esistono altri profili, viene selezionato automaticamente il primo disponibile

### ♻️ Flusso profili adesso è completo
- Crea profilo
- Salva profilo
- Carica profilo
- Rinomina profilo
- Elimina profilo ✅

### 🔁 Version bump
- `APP_VERSION` aggiornato a `1.3.2`.
- Finestra principale leggermente più larga per accomodare tutti i pulsanti del pannello profili.


## [v1.3.1] — 2025-10-26
### 🛠 Gestione profili migliorata
- Aggiunto il pulsante **"Rinomina profilo"**.
- Ora è possibile rinominare un profilo di mercato direttamente dall'interfaccia, senza modificare a mano il file `profiles.json`.
- Se il nuovo nome esiste già, viene chiesto se sovrascriverlo.
- Dopo la rinomina:
  - il profilo vecchio viene eliminato
  - il profilo nuovo viene salvato
  - la lista dei profili nella GUI si aggiorna automaticamente
  - la selezione viene spostata sul nuovo nome.

### 🔁 Version bump
- `APP_VERSION` aggiornato a `1.3.1`.

---

### Nota
Questa versione è pensata per la qualità della vita degli alchimisti che gestiscono listini multipli (prezzi di gilda, mercato nero, evento fiera, ecc.).


## [v1.3] — 2025-10-26
### ✨ Nuove funzionalità
- Aggiunto supporto ai **profili di mercato** multipli.
  - Ora puoi definire più profili di prezzi (es. "Standard", "Raro", "MercatoNotturno", "GildaHealer", ecc.).
  - Ogni profilo salva:
    - prezzo reagente
    - prezzo core fragment
    - prezzo carbone
    - quante verdure ottieni per 1b
    - quanti vasetti ottieni per 1b
    - quante boccette ottieni per 1b
  - I profili vengono salvati in `profiles.json`.

- Nuovo pannello `Profilo prezzi` con:
  - campo selezione / inserimento nome profilo
  - bottone **Carica profilo** → aggiorna tutti i prezzi nella GUI
  - bottone **Salva profilo** → crea o aggiorna quel profilo sul disco

### 💾 Persistenza migliorata
- `profiles.json` viene creato automaticamente con profili base (`Standard`, `Raro`) se non esiste.
- `config.json` ora memorizza anche l’ultimo profilo selezionato e lo ripristina al prossimo avvio.

### 🧪 Funzioni esistenti mantenute
- Calcolo completo dei costi e dei materiali.
- Supporto a tutti i calderoni:
  - Terracotta (T1), Rame (T1)
  - Ferro (T2), Oro (T2)
  - Diamante (T3)
- Stima dei catalyst, core, resine, boccette, carbonella.
- Efficienza catalyst/pozione e carbonella/pozione.
- Tema scuro, scroll intelligente, breakdown dettagliato.

### 🔁 Version bump
- `APP_VERSION` aggiornata a `1.3`.
- L’output “Dettaglio” ora indica anche il profilo prezzi attivo.

---

## 🚀 Prossimo step pianificato (v1.4)
- Pulsante “Rinomina profilo”.


## [v1.2] — 2025-10-26
### ✨ Nuove funzionalità
- Aggiunti **nuovi calderoni**:
  - 🟤 **Terracotta** → Pozioni di cura T1 (1 catalyst = 2 pozioni, 1 carbonella = 2 pozioni)
  - 🟠 **Rame** → Pozioni di cura T1 (1 catalyst = 3 pozioni, 1 carbonella = 3 pozioni)
  - ⚙️ **Ferro** → Pozioni di cura T2 (1 catalyst = 1 pozione, 2 carbonella = 1 pozione)
  - 🟡 **Oro** → Pozioni di cura T2 (2 catalyst = 3 pozioni, 2 carbonella = 3 pozioni)
  - 💎 **Diamante** → Pozioni di cura T3 (3 catalyst = 2 pozioni, 3 carbonella = 2 pozioni)

### 🧪 Miglioramenti
- L’app ora **riconosce automaticamente** il tipo di pozione prodotta (T1/T2/T3) in base al calderone scelto.
- Aggiunta in output l’**efficienza catalyst/pozioni** e **carbonella/pozioni**, per confrontare meglio i calderoni.
- Mantiene tutte le funzionalità precedenti, inclusi:
  - Tema scuro ottimizzato
  - Salvataggio automatico (`config.json`)
  - Menù "Info" e "Licenza"

### 🧱 Interno
- Refactoring completo della logica dei calderoni per migliorare leggibilità e precisione.
- Aggiornata variabile `APP_VERSION` → `1.2`.

---

## 🪄 **Prossima versione (v1.3 – pianificata)**
- 💾 Possibilità di salvare più profili di prezzo (es. “economico”, “medio”, “raro”)
- 🧮 Ottimizzazione del costo automatico (suggerisce il calderone più efficiente)



## [v1.1] — 2025-10-26
### ✨ Nuova funzionalità
- Aggiunto **salvataggio automatico** delle impostazioni:
  - Numero pozioni
  - Tipo reagente
  - Tipo di calderone
  - Prezzi di reagente, core, carbone
  - Quantità di verdure, vasetti e boccette per 1b
- Alla chiusura dell'app, le impostazioni vengono salvate in `config.json`.
- Al riavvio, i dati vengono caricati automaticamente.

### 🧠 Miglioramenti
- L'app ora ricorda le preferenze dell'utente anche tra sessioni diverse.
- Popup informativo aggiornato con la versione 1.1.

### 🔧 Interno
- Aggiunto file `config.json` salvato nella directory del programma.


## [v1.0.2] — 2025-10-26
### ✨ Nuove funzionalità
- Aggiunto **menu Info** con voci:
  - “Informazioni / Crediti”
  - “Licenza (MIT)”
- Aggiunto **popup informativo** con autore, versione e descrizione del progetto.
- Inserita **licenza MIT** completa all’interno dell’app.
- Nome dell’app ora visualizzato correttamente nella barra del titolo e nella taskbar di Windows.
- Branding grafico:
  - Nuovo **logo quadrato (EP)**
  - Nuovo **banner dark fantasy** nel README
  - Nuova **favicon 32x32** per versioni `.exe` o web

### 🎨 Miglioramenti UI
- Tema scuro ottimizzato con maggiore contrasto.
- Scroll intelligente rifinito (non scorre più tutta la finestra quando il mouse è sul box dettagli).
- Pulsante **CALCOLA** migliorato (colore accentato, feedback al click).
- Layout ottimizzato per finestre 540x500 px.

### 🐞 Correzioni
- Fixata gestione carbonella (2 per 3 pozioni nel calderone d’Oro).
- Corretto calcolo del costo per pozione nei calderoni di Ferro.
- Sistemata visualizzazione di testo nei risultati lunghi.

---

## [v1.0.1] — 2025-10-25
### 🔧 Aggiornamenti intermedi
- Aggiunto **scroll automatico** e ottimizzazione spazi GUI.
- Introdotta **modalità calderone di Ferro** con rese corrette.
- Fix del costo di boccette e vasetti, ora calcolati in base alla quantità ottenibile per 1b.

---

## [v1.0.0] — 2025-10-24
### 🌟 Versione iniziale
- Prima release funzionante del **Calcolatore di Pozioni**:
  - calcolo base dei costi
  - gestione reagenti T1/T2/T3
  - supporto calderone d’Oro
  - stima materiali e prezzi
- Interfaccia grafica base con tema scuro.
- Output dettagliato con breakdown costi e materiali.

---

👤 **Autore:** [ILGUERRIERO22](https://github.com/Ahristogatti)  
🧪 *“Non serve la magia, se conosci la formula.”*
