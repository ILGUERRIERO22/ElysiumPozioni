<p align="center">
  <img src="logo.png?raw=true" alt="Logo Elysium Pozioni" width="150" style="border-radius:12px;">
</p>

<p align="center">
  <img src="banner.png?raw=true" alt="Elysium Pozioni Banner" width="820">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Tkinter-GUI-green?logo=windowsterminal&logoColor=white" alt="Tkinter GUI">
  <img src="https://img.shields.io/badge/Status-Attivo-brightgreen?style=flat" alt="Status">
  <img src="https://img.shields.io/github/v/release/ILGUERRIERO22/ElysiumPozioni?color=orange&label=versione&style=flat-square" alt="Versione GitHub">
  <img src="https://img.shields.io/github/downloads/ILGUERRIERO22/ElysiumPozioni/total?color=brightgreen&label=download%20totali&style=flat-square" alt="Download Totali">
  <img src="https://img.shields.io/badge/Licenza-MIT-yellow?style=flat" alt="Licenza">
  <img src="https://img.shields.io/badge/Made%20by-ILGUERRIERO22-purple?style=flat-square" alt="Autore">
</p>

---

# ⚗️ Elysium Pozioni

**Elysium Pozioni** è un tool in **Python + Tkinter** pensato per tenere sotto controllo costi, materiali e profitti di tutte le pozioni del mondo di **Elysium**.

L’app raccoglie in un’unica interfaccia:

- pozioni di cura (T1, T2, T3)
- antidoti
- Revivify
- Extinguish
- elisir di cura
- rune
- pozioni di velocità (Velocità I e Velocità II)
- pozioni di danno (Danno I e Danno II – Avvizzimento)
- pozioni di riduzione (Riduzione I e Riduzione II)

Più due strumenti di pianificazione:

- **Multi-Prodotto** — costi e profitti di più produzioni in un unico calcolo
- **Lista della spesa** — gli ingredienti grezzi da comprare per un mix di prodotti

Il tutto con tema scuro, profili di mercato multipli e salvataggio automatico delle impostazioni.

---

## 🧪 Funzionalità principali

### 🔹 Pozioni di cura

Tab **“Pozioni di cura”**

- Calcolo del **costo totale** e **costo per singola pozione**
- Gestione dei **tier reagenti T1 / T2 / T3**
- Supporto a tutti i calderoni:
  - 🟤 Terracotta → pozioni T1  
  - 🟠 Rame → pozioni T1  
  - ⚙️ Ferro → pozioni T2  
  - 🟡 Oro → pozioni T2  
  - 💎 Diamante → pozioni T3  
  - 💚 Smeraldo → pozioni T3  
- Breakdown dettagliato di:
  - catalyst necessari
  - core fragment
  - resine
  - carbonella
  - boccette
- Campo **“Prezzo di vendita per pozione”** con:
  - margine per pozione
  - guadagno totale sul lotto
  - ricarico percentuale

### 🔹 Antidoti

Tab **“Antidoti”**

- Supporta i calderoni **Terracotta** e **Ferro**
- Usa automaticamente il **costo della resina** calcolato dalla tab pozioni
- Puoi impostare il prezzo della **Brim powder**, **carne marcia** e **Revival star**
- Calcola:
  - costo totale per lotto
  - costo per antidoto
  - guadagno e ricarico percentuale (se inserisci un prezzo di vendita)

### 🔹 Revivify

Tab **“Revivify”**

- Calderone in **rame**
- Ricetta: 1 Revival star + 1 Core fragment + 1 Carbonella + 1 Boccetta  
- Riutilizza automaticamente:
  - prezzo del core
  - prezzo del carbone
  - costo boccette
  - prezzo Revival star dalla tab Antidoti
- Calcolo di costi e profitto come per le altre pozioni.

### 🔹 Extinguish

Tab **“Extinguish”**

- Calderone in **rame**
- Ricetta: 1 Quarzo + 1 Core fragment + 1 Carbonella + 1 Boccetta  
- Parametri configurabili:
  - prezzo quarzo
  - prezzo core
  - prezzo carbone
  - costo boccette
- Analisi costo totale, costo per pozione e margine di vendita.

### 🔹 Elisir di cura

Tab **“Elisir”**

Gestisce tutte le varianti di **mending** (Minor, Inferior, Lesser, Medium, Greater) con le loro ricette specifiche di:

- Brim powder (prezzo condiviso con la tab Antidoti)
- Occhio di ragno
- Membrana di Phantom
- Slimeball
- Lost soul
- Pepite costruite da lingotti (Tin, Rame, Ferro, Oro, Diamante)

Per ogni elisir puoi vedere:

- costo per lotto
- costo per singolo elisir
- guadagno totale e ricarico (se inserisci un prezzo di vendita)

### 🔹 Rune

Tab **“Rune”**

- Calcolo delle rune ottenibili da un certo numero di **pepite**:
  - Tin, Rame, Ferro, Oro, Argento
- Due tipologie di rune:
  - **Maghi**
  - **Bardi**
- Inserisci quante pepite hai per ogni metallo → il tool ti mostra:
  - quante rune ottieni per metallo
  - il totale complessivo di rune prodotte

### 🔹 Pozioni di Velocità

Tab **“Velocità”**

Gestisce due livelli:

- **Velocità I** (calderone in Terracotta)  
  - Ricetta: 1 Lapis + 1 Zucchero + 1 Carbonella + 1 Boccetta  
- **Velocità II** (calderone in Ferro)  
  - Ricetta: 1 Blaze + 1 Core fragment + 2 Carbonella + 1 pozione di Velocità I  

L’app calcola automaticamente:

- costo base di Velocità I
- costo aggiuntivo per trasformarla in Velocità II
- costo totale per lotto
- costo unitario
- margine e ricarico se inserisci il prezzo di vendita

### 🔹 Pozioni di Danno

Tab **“Danno”**

- **Danno I** (calderone in Rame)
  - Ricetta: 1 Occhio di ragno + 1 Core fragment + 1 Carbonella + 1 Boccetta
- **Danno II — Avvizzimento** (calderone in Oro)
  - Ricetta: 1 Withering dust + 1 Core fragment + 2 Carbonella + 1 pozione di Danno I

Come per la velocità, il costo di Danno II comprende automaticamente quello
della pozione di base.

### 🔹 Pozioni di Riduzione

Tab **“Riduzione”**

- **Riduzione I** (calderone in Rame)
  - Ricetta: 1 Fungo marrone + 1 Core fragment + 1 Carbonella + 1 Boccetta
- **Riduzione II** (calderone in Oro)
  - Ricetta: 1 Slimeball + 1 Core fragment + 2 Carbonella + 1 pozione di Riduzione I

### 🔹 Multi-Prodotto

Tab **“Multi-Prodotto”**

Serve a pianificare **più produzioni in un colpo solo**:

- componi una lista di prodotti (tipo + quantità + prezzo di vendita)
- il tool calcola i **materiali aggregati** su tutta la lista, evitando di
  sommare a mano
- mostra costo totale, ricavo, profitto netto e margine percentuale
- per ogni prodotto vedi anche il breakdown di costo e profitto
- per le rune confronta i metalli e **evidenzia l’opzione più economica**

I prezzi vengono presi automaticamente dalle altre tab.

### 🔹 Lista della spesa

Tab **“Lista della spesa”**

Risponde alla domanda *“cosa devo comprare per produrre tutto questo?”*:

- inserisci le quantità dei prodotti che vuoi ottenere
- ricevi la lista degli **ingredienti grezzi** da acquistare, arrotondati
  all’intero, con l’indicazione di quanto avanza
- i reagenti mostrano quanti **HC** vengono prodotti, quanti servono davvero e
  quanti restano
- la carbonella viene convertita nei **blocchi di combustibile** necessari

---

## 🔥 Combustibile

Nella tab “Pozioni di cura” puoi scegliere con cosa alimentare i calderoni:

| Combustibile | Carbonella per blocco |
|--------------|----------------------|
| Carbone      | 12                   |
| Anthracite   | 24                   |
| Firestone    | 36                   |

Inserisci il prezzo di **un blocco** del combustibile scelto: l’app normalizza
automaticamente il costo per carbonella, così i confronti restano corretti in
tutte le tab.

---

## 💼 Profili di mercato

Per evitare di riscrivere ogni volta i prezzi, esiste il pannello **“Profilo prezzi”**:

- crea profili con prezzi diversi (es. `Standard`, `Evento`, `MercatoNero`)
- puoi:
  - **salvare** un profilo
  - **caricare** un profilo
  - **rinominare** un profilo
  - **eliminare** un profilo

I profili sono salvati nel file `profiles.json`.

---

## 💾 Salvataggio automatico

- L’app salva automaticamente l’ultimo stato in `config.json`
  - numero pozioni
  - tipo reagente
  - calderone
  - prezzi
  - quantità per 1 blocco (verdure, vasetti, boccette)
  - parametri antidoti, elisir, rune, velocità, ecc.
- Alla riapertura, ritrovi tutti i valori com’erano.

Entrambi i file (`config.json` e `profiles.json`) vengono salvati in:

```text
%APPDATA%\ElysiumPozioni
```

Se avevi una versione precedente che li teneva nella cartella del programma,
vengono spostati automaticamente al primo avvio.

---

## 🚀 Installazione

### 🌐 Versione web — nessuna installazione

**[Apri il calcolatore nel browser](https://ilguerriero22.github.io/ElysiumPozioni/)**

Funziona anche da telefono e ricorda i prezzi che inserisci. Copre **tutti gli
undici calcolatori** dell'app desktop, inclusi Multi-Prodotto e Lista della spesa.

### Eseguibile (consigliato)

Scarica `ElysiumPozioni.exe` dalla sezione
[Releases](https://github.com/ILGUERRIERO22/ElysiumPozioni/releases) e avvialo:
non serve installare Python.

### Da sorgente

Richiede **Python 3.10+**.

```bash
git clone https://github.com/ILGUERRIERO22/ElysiumPozioni.git
cd ElysiumPozioni
pip install -r Requirements.txt
python main.py
```

### Compilare l’eseguibile

```bash
pip install pyinstaller
pyinstaller ElysiumPozioni.spec
```

L’eseguibile viene creato in `dist/`.

---

## 📜 Licenza

Distribuito con licenza MIT. Vedi il changelog in
[CHANGELOG.md](CHANGELOG.md) per la cronologia delle versioni.
