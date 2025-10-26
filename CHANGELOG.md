# 🧾 Elysium Pozioni — Changelog

Tutte le modifiche rilevanti a questo progetto verranno documentate in questo file.  
Il formato segue le linee guida di [Keep a Changelog](https://keepachangelog.com/it/1.0.0/).

---

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

## 🔮 In arrivo
- Salvataggio automatico degli ultimi valori inseriti.
- Cakderine in rame, terracotta e diamante


---

👤 **Autore:** [ILGUERRIERO22](https://github.com/ILGUERRIERO22)  
🧪 *“Non serve la magia, se conosci la formula.”*
