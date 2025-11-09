import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# =========================
#   COSTANTI TEMA / STILE
# =========================

import sys
import shutil

# ---- PATCH AVVIO: forza working dir su %APPDATA%\ElysiumPozioni ----
import os, sys, shutil

APP_NAME = "Elysium Pozioni"
APP_DIRNAME = "ElysiumPozioni"
APP_VERSION = "2.0.0"
APP_AUTHOR = "ILGUERRIERO22"

def _get_data_dir():
    base = os.getenv("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, APP_DIRNAME)
    os.makedirs(path, exist_ok=True)
    return path

DATA_DIR = _get_data_dir()

# sposta qui eventuali file legacy se trovati nella dir corrente
for legacy_name in ("config.json", "profiles.json"):
    legacy_src = os.path.join(os.getcwd(), legacy_name)
    legacy_dst = os.path.join(DATA_DIR, legacy_name)
    try:
        if os.path.exists(legacy_src) and not os.path.exists(legacy_dst):
            shutil.move(legacy_src, legacy_dst)
    except Exception as e:
        print("Migrazione legacy fallita:", e)

# CAMBIO WORKING DIR: da qui in poi tutti i path relativi scriveranno in %APPDATA%\ElysiumPozioni
try:
    os.chdir(DATA_DIR)
except Exception as e:
    print("Impossibile cambiare working dir:", e)

# definisci i file come relativi (ora puntano a %APPDATA%\ElysiumPozioni)
CONFIG_FILE   = "config.json"
PROFILES_FILE = "profiles.json"
# ---- FINE PATCH AVVIO ----



BG_MAIN = "#1e1e1e"
BG_PANEL = "#2a2a2a"
BG_RESULT = "#111111"
FG_TEXT = "#eaeaea"
FG_SUBTLE = "#9e9e9e"
ACCENT = "#6a5dfd"
DANGER_BG = "#742e2e"
DANGER_BG_ACTIVE = "#993737"

TITLE_FONT = ("Segoe UI", 15, "bold")
SECTION_FONT = ("Segoe UI", 11, "bold")
LABEL_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 11, "bold")
RESULT_FONT = ("Consolas", 11)


# =========================
#   GESTIONE PROFILI PREZZO
# =========================

def ensure_profiles_file():
    """Crea profiles.json con profili base se non esiste ancora."""
    if not os.path.exists(PROFILES_FILE):
        default_profiles = {
            "Standard": {
                "prezzo_reagente": "1.5",
                "prezzo_core": "1.0",
                "prezzo_carbone": "1.5",
                "verdure_per_1b": "3",
                "vasetti_per_1b": "15",
                "boccette_per_1b": "14"
            },
            "Raro": {
                "prezzo_reagente": "2.5",
                "prezzo_core": "1.5",
                "prezzo_carbone": "2.0",
                "verdure_per_1b": "2",
                "vasetti_per_1b": "12",
                "boccette_per_1b": "10"
            }
        }
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(default_profiles, f, indent=2, ensure_ascii=False)


def load_all_profiles():
    """Ritorna dizionario di tutti i profili salvati."""
    ensure_profiles_file()
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Errore lettura profiles.json:", e)
        return {}


def save_all_profiles(profiles_dict):
    """Scrive tutti i profili sul file."""
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles_dict, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Errore scrittura profiles.json:", e)


def apply_profile():
    """Carica i prezzi dal profilo selezionato nella GUI."""
    name = combo_profile.get().strip()
    if not name:
        messagebox.showerror("Errore", "Seleziona o scrivi un nome profilo.")
        return

    if name not in profiles:
        messagebox.showerror("Errore", f"Profilo '{name}' non trovato.")
        return

    p = profiles[name]

    entry_reagente.delete(0, tk.END)
    entry_reagente.insert(0, p["prezzo_reagente"])

    entry_core.delete(0, tk.END)
    entry_core.insert(0, p["prezzo_core"])

    entry_carbone.delete(0, tk.END)
    entry_carbone.insert(0, p["prezzo_carbone"])

    entry_verdure_per_b.delete(0, tk.END)
    entry_verdure_per_b.insert(0, p["verdure_per_1b"])

    entry_vasetti_per_b.delete(0, tk.END)
    entry_vasetti_per_b.insert(0, p["vasetti_per_1b"])

    entry_boccette_per_b.delete(0, tk.END)
    entry_boccette_per_b.insert(0, p["boccette_per_1b"])

    messagebox.showinfo("Profilo caricato", f"Profilo '{name}' applicato.")


def save_profile():
    """Salva/aggiorna il profilo con i valori attuali dei campi prezzo."""
    name = combo_profile.get().strip()
    if not name:
        messagebox.showerror("Errore", "Inserisci un nome profilo da salvare.")
        return

    new_prof = {
        "prezzo_reagente": entry_reagente.get(),
        "prezzo_core": entry_core.get(),
        "prezzo_carbone": entry_carbone.get(),
        "verdure_per_1b": entry_verdure_per_b.get(),
        "vasetti_per_1b": entry_vasetti_per_b.get(),
        "boccette_per_1b": entry_boccette_per_b.get()
    }

    profiles[name] = new_prof
    save_all_profiles(profiles)

    # aggiorna lista valori nella combo profili
    combo_profile["values"] = list(profiles.keys())

    messagebox.showinfo("Profilo salvato", f"Profilo '{name}' salvato.")


def rename_profile():
    """Rinomina il profilo attuale in un nuovo nome scelto dall'utente."""
    old_name = combo_profile.get().strip()
    if not old_name:
        messagebox.showerror("Errore", "Seleziona il profilo da rinominare prima.")
        return

    if old_name not in profiles:
        messagebox.showerror("Errore", f"Il profilo '{old_name}' non esiste.")
        return

    # Finestra popup per chiedere nuovo nome
    rename_win = tk.Toplevel(root)
    rename_win.title("Rinomina profilo")
    rename_win.configure(bg=BG_MAIN)
    rename_win.resizable(False, False)

    tk.Label(
        rename_win,
        text=f"Nuovo nome per '{old_name}':",
        font=LABEL_FONT,
        bg=BG_MAIN,
        fg=FG_TEXT
    ).pack(padx=10, pady=(10,4), anchor="w")

    new_name_entry = tk.Entry(
        rename_win,
        width=20,
        font=LABEL_FONT,
        bg="#3a3a3a",
        fg=FG_TEXT,
        insertbackground=FG_TEXT,
        relief="flat",
    )
    new_name_entry.pack(padx=10, pady=4)
    new_name_entry.focus()

    def conferma_rinomina():
        new_name = new_name_entry.get().strip()
        if not new_name:
            messagebox.showerror("Errore", "Il nuovo nome non può essere vuoto.")
            return

        # se uguale non serve fare nulla
        if new_name == old_name:
            rename_win.destroy()
            return

        # se il nuovo nome esiste già, chiediamo conferma
        if new_name in profiles:
            sovrascrivi = messagebox.askyesno(
                "Conferma",
                f"Esiste già un profilo chiamato '{new_name}'. Sovrascriverlo?"
            )
            if not sovrascrivi:
                return

        # copia dati e cancella vecchio
        profiles[new_name] = profiles[old_name]
        del profiles[old_name]

        # salva su disco
        save_all_profiles(profiles)

        # aggiorna combobox profili
        combo_profile["values"] = list(profiles.keys())
        combo_profile.set(new_name)

        messagebox.showinfo("Fatto", f"Profilo rinominato in '{new_name}'.")
        rename_win.destroy()

    btn_frame = tk.Frame(rename_win, bg=BG_MAIN)
    btn_frame.pack(padx=10, pady=(8,10), fill="x")

    tk.Button(
        btn_frame,
        text="OK",
        command=conferma_rinomina,
        bg=ACCENT,
        fg="white",
        font=LABEL_FONT,
        activebackground="#574dff",
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=4,
        cursor="hand2",
    ).pack(side="left")

    tk.Button(
        btn_frame,
        text="Annulla",
        command=rename_win.destroy,
        bg="#444",
        fg=FG_TEXT,
        font=LABEL_FONT,
        activebackground="#555",
        activeforeground=FG_TEXT,
        relief="flat",
        padx=10,
        pady=4,
        cursor="hand2",
    ).pack(side="right")


def delete_profile():
    """Elimina definitivamente il profilo selezionato dalla lista e da profiles.json."""
    name = combo_profile.get().strip()
    if not name:
        messagebox.showerror("Errore", "Seleziona il profilo da eliminare.")
        return

    if name not in profiles:
        messagebox.showerror("Errore", f"Il profilo '{name}' non esiste.")
        return

    conferma = messagebox.askyesno(
        "Conferma eliminazione",
        f"Sei sicuro di voler eliminare il profilo '{name}'?\n"
        "Questa azione non può essere annullata."
    )
    if not conferma:
        return

    # rimuovi dalla memoria
    del profiles[name]

    # salva su disco
    save_all_profiles(profiles)

    # aggiorna combobox
    nuovi_nomi = list(profiles.keys())
    combo_profile["values"] = nuovi_nomi

    if nuovi_nomi:
        combo_profile.set(nuovi_nomi[0])
    else:
        combo_profile.set("")

    messagebox.showinfo("Profilo eliminato", f"Profilo '{name}' rimosso.")


# =========================
#   CONFIG SESSIONE (config.json)
# =========================

def save_config():
    """Salva lo stato corrente (ultimo uso) in config.json."""
    data = {
        "num_pozioni": entry_pozioni.get(),
        "tier": combo_tier.get(),
        "calderone": combo_calderone.get(),
        "prezzo_reagente": entry_reagente.get(),
        "prezzo_core": entry_core.get(),
        "prezzo_carbone": entry_carbone.get(),
        "verdure_per_1b": entry_verdure_per_b.get(),
        "vasetti_per_1b": entry_vasetti_per_b.get(),
        "boccette_per_1b": entry_boccette_per_b.get(),
        "prezzo_vendita": entry_prezzo_vendita.get(),
        "last_profile": combo_profile.get(),
        "sconto_perc": entry_sconto_perc.get(),
        "ant_num": entry_ant_num.get(),
        "ant_calderone": combo_ant_calderone.get(),
        "ant_prezzo": entry_ant_prezzo.get(),
        "prezzo_brim": entry_brim.get(),
        "prezzo_rotten": entry_rotten.get(),
        "prezzo_revival": entry_revival.get(),
        "rev_prezzo": entry_rev_prezzo.get(),
        "ext_num": entry_ext_num.get(),
        "ext_prezzo": entry_ext_prezzo.get(),
        "prezzo_quartz": entry_quartz.get(),
        "price_tin": entry_price_tin.get(),
        "price_cu": entry_price_cu.get(),
        "price_fe": entry_price_fe.get(),
        "price_au": entry_price_au.get(),
        "price_dia": entry_price_dia.get(),
        "rune_tipo": combo_rune_tipo.get(),
        "rune_metallo": combo_rune_metallo.get(),
        "inv_tipo": combo_inv_tipo.get(),
        "inv_quante": entry_inv_quante.get(),
        "rune_pepite": entry_rune_pepite.get(),





        

    }

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Errore salvataggio config:", e)


def load_config():
    """Carica l'ultimo stato usato (se esiste) da config.json nella GUI."""
    if not os.path.exists(CONFIG_FILE):
        return

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Errore lettura config:", e)
        return

    if "num_pozioni" in data:
        entry_pozioni.delete(0, tk.END)
        entry_pozioni.insert(0, data["num_pozioni"])

    if "tier" in data and data["tier"] in ["T1", "T2", "T3"]:
        combo_tier.set(data["tier"])

    if "calderone" in data and data["calderone"] in ["Terracotta", "Rame", "Ferro", "Oro", "Diamante"]:
        combo_calderone.set(data["calderone"])

    if "prezzo_reagente" in data:
        entry_reagente.delete(0, tk.END)
        entry_reagente.insert(0, data["prezzo_reagente"])

    if "prezzo_core" in data:
        entry_core.delete(0, tk.END)
        entry_core.insert(0, data["prezzo_core"])

    if "prezzo_carbone" in data:
        entry_carbone.delete(0, tk.END)
        entry_carbone.insert(0, data["prezzo_carbone"])

    if "verdure_per_1b" in data:
        entry_verdure_per_b.delete(0, tk.END)
        entry_verdure_per_b.insert(0, data["verdure_per_1b"])

    if "vasetti_per_1b" in data:
        entry_vasetti_per_b.delete(0, tk.END)
        entry_vasetti_per_b.insert(0, data["vasetti_per_1b"])

    if "boccette_per_1b" in data:
        entry_boccette_per_b.delete(0, tk.END)
        entry_boccette_per_b.insert(0, data["boccette_per_1b"])

    if "prezzo_vendita" in data:
        entry_prezzo_vendita.delete(0, tk.END)
        entry_prezzo_vendita.insert(0, data["prezzo_vendita"])


    if "sconto_perc" in data:
        entry_sconto_perc.delete(0, tk.END)
        entry_sconto_perc.insert(0, data["sconto_perc"])

    
    if "ant_num" in data:
        entry_ant_num.delete(0, tk.END); entry_ant_num.insert(0, data["ant_num"])

    if "ant_calderone" in data and data["ant_calderone"] in ["Terracotta", "Ferro"]:
        combo_ant_calderone.set(data["ant_calderone"])

    if "ant_prezzo" in data:
        entry_ant_prezzo.delete(0, tk.END); entry_ant_prezzo.insert(0, data["ant_prezzo"])

    if "prezzo_brim" in data:
        entry_brim.delete(0, tk.END); entry_brim.insert(0, data["prezzo_brim"])

    if "prezzo_rotten" in data:
        entry_rotten.delete(0, tk.END); entry_rotten.insert(0, data["prezzo_rotten"])

    if "prezzo_revival" in data:
        entry_revival.delete(0, tk.END); entry_revival.insert(0, data["prezzo_revival"])

    if "rev_prezzo" in data:
        entry_rev_prezzo.delete(0, tk.END)
        entry_rev_prezzo.insert(0, data["rev_prezzo"])

    if "ext_num" in data:
        entry_ext_num.delete(0, tk.END); entry_ext_num.insert(0, data["ext_num"])

    if "ext_prezzo" in data:
        entry_ext_prezzo.delete(0, tk.END); entry_ext_prezzo.insert(0, data["ext_prezzo"])

    if "prezzo_quartz" in data:
        entry_quartz.delete(0, tk.END); entry_quartz.insert(0, data["prezzo_quartz"])


    for k, widget in [
        ("price_tin", entry_price_tin), ("price_cu", entry_price_cu),
        ("price_fe", entry_price_fe), ("price_au", entry_price_au),
        ("price_dia", entry_price_dia),
        ("inv_quante", entry_inv_quante),
    ]:
        if k in data:
            widget.delete(0, tk.END); widget.insert(0, data[k])

    if "rune_tipo" in data and data["rune_tipo"] in ["Normali","Bardiche"]:
        combo_rune_tipo.set(data["rune_tipo"])
    if "rune_metallo" in data and data["rune_metallo"] in ["Tin","Rame","Ferro","Oro","Diamante"]:
        combo_rune_metallo.set(data["rune_metallo"])
    if "inv_tipo" in data and data["inv_tipo"] in ["Normali","Bardiche"]:
        combo_inv_tipo.set(data["inv_tipo"])


    if "rune_pepite" in data:
        entry_rune_pepite.delete(0, tk.END)
        entry_rune_pepite.insert(0, data["rune_pepite"])





    if "last_profile" in data and data["last_profile"] in profiles:
        combo_profile.set(data["last_profile"])

    


# =========================
#   FUNZIONI DI UTILITÀ
# =========================

def show_info():
    """Mostra popup con crediti / versione."""
    msg = (
        f"{APP_NAME} v{APP_VERSION}\n"
        f"Autore: {APP_AUTHOR}\n\n"
        "Calcolatore di costo e profitto pozioni per Elysium.\n"
        "Supporta calderoni Terracotta / Rame / Ferro / Oro / Diamante.\n"
        "Profili di mercato multipli, rinomina/elimina profili,\n"
        "salvataggio automatico e analisi margine.\n\n"
        "Miao 😺"
    )
    messagebox.showinfo("Informazioni", msg)


def show_license():
    """Mostra popup con licenza MIT semplificata."""
    mit_text = (
        "Licenza MIT\n\n"
        f"Copyright (c) 2025 {APP_AUTHOR}\n\n"
        "È consentito usare, copiare, modificare e distribuire questo software "
        "senza restrizioni, anche per uso commerciale, purché venga mantenuta "
        "questa nota di copyright e la presente licenza.\n\n"
        "IL SOFTWARE VIENE FORNITO \"COSÌ COM'È\", SENZA ALCUNA GARANZIA."
    )
    messagebox.showinfo("Licenza", mit_text)


def calcola():
    try:
        # --- INPUT DI BASE ---
        num_pozioni = float(entry_pozioni.get())
        tier_reagente = combo_tier.get()              # T1 / T2 / T3
        tipo_calderone = combo_calderone.get()        # Terracotta / Rame / Ferro / Oro / Diamante

        # --- PREZZI DIRETTI ---
        prezzo_reagente = float(entry_reagente.get())   # costo 1 reagente scelto
        prezzo_core = float(entry_core.get())           # costo 1 core fragment
        prezzo_carbone = float(entry_carbone.get())     # costo 1 carbone (12 carbonella)

        # --- PACCHETTI (quante unità per 1b) ---
        verdure_per_1b = float(entry_verdure_per_b.get())    # es 3 => 1b ogni 3 verdure
        vasetti_per_1b = float(entry_vasetti_per_b.get())    # es 15 => 1b ogni 15 vasetti
        boccette_per_1b = float(entry_boccette_per_b.get())  # es 14 => 1b ogni 14 boccette

        # --- COSTO UNITARIO ---
        costo_verdura_unit = 1.0 / verdure_per_1b        # b per 1 verdura
        costo_vasetto_unit = 1.0 / vasetti_per_1b        # b per 1 vasetto
        costo_boccetta_unit = 1.0 / boccette_per_1b      # b per 1 boccetta

        # Resina: 2 verdure + 1 vasetto -> 2 resine
        costo_resina_unit = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0

        # Carbonella: 1 carbone = 12 carbonella
        costo_carbonella_unit = prezzo_carbone / 12.0

        # ======================================================
        # LOGICA CALDERONI
        # ======================================================

        if tipo_calderone == "Terracotta":
            # 1 catalyst -> 2 pozioni T1
            # 1 carbonella -> 2 pozioni
            pozioni_per_catalyst = 2.0
            pozioni_per_carbonella = 2.0
            tier_pozione_prodotta = "T1"

        elif tipo_calderone == "Rame":
            # 1 catalyst -> 3 pozioni T1
            # 1 carbonella -> 3 pozioni
            pozioni_per_catalyst = 3.0
            pozioni_per_carbonella = 3.0
            tier_pozione_prodotta = "T1"

        elif tipo_calderone == "Ferro":
            # 1 catalyst -> 1 pozione T2
            # 2 carbonella -> 1 pozione
            pozioni_per_catalyst = 1.0
            pozioni_per_carbonella = 1.0 / 2.0
            tier_pozione_prodotta = "T2"

        elif tipo_calderone == "Oro":
            # 2 catalyst -> 3 pozioni T2  => 1 catalyst -> 1.5 pozioni
            # 2 carbonella -> 3 pozioni   => 1 carbonella -> 1.5 pozioni
            pozioni_per_catalyst = 1.5
            pozioni_per_carbonella = 1.5
            tier_pozione_prodotta = "T2"

        elif tipo_calderone == "Diamante":
            # 3 catalyst -> 2 pozioni T3  => 1 catalyst -> 0.666...
            # 3 carbonella -> 2 pozioni   => 1 carbonella -> 0.666...
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
        # Rese reagente:
        # T1 = 1 catalyst
        # T2 = 2 catalyst
        # T3 = 3 catalyst
        catalyst_per_reagente = {"T1": 1.0, "T2": 2.0, "T3": 3.0}

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
        # PROFITTO / MARGINE (1.5) — netto
        # =========================
        # prezzo di vendita per pozione (lordo)
                # =========================
        # PROFITTO / MARGINE (pulito)
        # =========================
        try:
            prezzo_vendita = float(entry_prezzo_vendita.get())
        except ValueError:
            prezzo_vendita = None

        if prezzo_vendita is not None:
            ricavo_lotto = prezzo_vendita * num_pozioni
            guadagno = ricavo_lotto - costo_totale
            margine_per_pozione = guadagno / num_pozioni if num_pozioni else 0.0
            ricarico_percent = (margine_per_pozione / costo_per_pozione * 100.0) if costo_per_pozione > 0 else 0.0

            # prezzo di pareggio (esatto)
            prezzo_break_even = costo_per_pozione
        else:
            ricavo_lotto = None
            guadagno = None
            margine_per_pozione = None
            ricarico_percent = None
            prezzo_break_even = None


        # =========================
        # ANTEPRIMA COSTO RAPIDO (label_preview)
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


        label_preview.config(
            text=preview_text,
            fg=FG_TEXT,
            bg=BG_MAIN,
        )

        # =========================
        # OUTPUT DETTAGLIATO
        # =========================
        output_lines = [
            f"Profilo prezzi attivo:    {combo_profile.get().strip() or '(non salvato)'}",
            f"Calderone:                {tipo_calderone}",
            f"Pozione prodotta:         {tier_pozione_prodotta}",
            f"Pozioni totali richieste: {num_pozioni:.2f}",
            f"Tipo reagente usato:      {tier_reagente}",
            "",
            f"COSTO TOTALE:             {costo_totale:.2f} b",
            f"Costo per pozione:        {costo_per_pozione:.2f} b",
        ]

        # se è stato inserito un prezzo di vendita, aggiungiamo sezione profitto
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
            f"{APP_NAME} v{APP_VERSION} — {APP_AUTHOR}",
            "Profili multipli, salvataggio automatico e analisi margine.",
        ]

        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, "\n".join(output_lines))
        text_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi: inserisci numeri validi!")


def calcola_antidoti():
    try:
        # --- INPUT DI BASE ---
        num = float(entry_ant_num.get())
        tipo = combo_ant_calderone.get()  # Terracotta / Ferro

        # --- PREZZI GLOBALI (già presenti nella tab Pozioni) ---
        prezzo_carbone = float(entry_carbone.get())      # b per 1 blocco (12 carbonella)
        boccette_per_1b = float(entry_boccette_per_b.get())
        vasetti_per_1b = float(entry_vasetti_per_b.get())
        verdure_per_1b = float(entry_verdure_per_b.get())

        # --- PREZZI ANTIDOTI ---
        prezzo_brim = float(entry_brim.get())            # 1 brim powder
        prezzo_rotten = float(entry_rotten.get())        # 1 carne marcia
        prezzo_revival = float(entry_revival.get())      # 1 revival star

        # --- COSTI UNITARI DERIVATI GLOBALI ---
        costo_boccetta_unit = 1.0 / boccette_per_1b
        costo_vasetto_unit = 1.0 / vasetti_per_1b
        costo_verdura_unit = 1.0 / verdure_per_1b
        costo_resina_unit = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0
        costo_carbonella_unit = prezzo_carbone / 12.0

        # --- RICETTE ANTIDOTO ---
        # Terracotta: brim + carne marcia + 1 carbonella + 1 boccetta
        # Ferro:      resina + revival star + 2 carbonella + 2 boccette
        if tipo == "Terracotta":
            q_brim = num * 1.0
            q_rotten = num * 1.0
            q_resina = 0.0
            q_revival = 0.0
            q_carbonella = num * 1.0
            q_boccette = num * 1.0
        elif tipo == "Ferro":
            q_brim = 0.0
            q_rotten = 0.0
            q_resina = num * 1.0
            q_revival = num * 1.0
            q_carbonella = num * 2.0
            q_boccette = num * 2.0
        else:
            raise ValueError("Tipo calderone antidoti non valido")

        # --- COSTI PARZIALI ---
        costo_brim = q_brim * prezzo_brim
        costo_rotten = q_rotten * prezzo_rotten
        costo_resina = q_resina * costo_resina_unit
        costo_revival = q_revival * prezzo_revival
        costo_carbonella = q_carbonella * costo_carbonella_unit
        costo_boccette = q_boccette * costo_boccetta_unit

        costo_tot = costo_brim + costo_rotten + costo_resina + costo_revival + costo_carbonella + costo_boccette
        costo_unit = costo_tot / num if num else 0.0

        # --- PROFITTO (facoltativo) ---
        try:
            prezzo_vendita = float(entry_ant_prezzo.get())
        except ValueError:
            prezzo_vendita = None

        if prezzo_vendita is not None:
            ricavo = prezzo_vendita * num
            guadagno = ricavo - costo_tot
            margine_unit = guadagno / num if num else 0.0
            ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0
        else:
            ricavo = guadagno = margine_unit = ricarico_pct = None

        # --- PREVIEW ---
        if prezzo_vendita is not None:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Costo/ant: {costo_unit:.2f} b    •    "
                f"Guadagno: {guadagno:.2f} b"
            )
        else:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Per antidoto: {costo_unit:.2f} b"
            )
        label_ant_preview.config(text=preview, fg=FG_TEXT, bg=BG_MAIN)

        # --- DETTAGLIO ---
        lines = [
            f"Calderone antidoti:       {tipo}",
            f"Antidoti totali richiesti:{num:.2f}",
            "",
            f"COSTO TOTALE:             {costo_tot:.2f} b",
            f"Costo per antidoto:       {costo_unit:.2f} b",
            "",
            "Materiali richiesti:",
            f" • Brim powder:           {q_brim:.2f}",
            f" • Carne marcia:          {q_rotten:.2f}",
            f" • Resina:                {q_resina:.2f}",
            f" • Revival star:          {q_revival:.2f}",
            f" • Carbonella:            {q_carbonella:.2f}",
            f" • Boccette:              {q_boccette:.2f}",
            "",
            "Costi parziali:",
            f" • Brim powder:           {costo_brim:.2f} b",
            f" • Carne marcia:          {costo_rotten:.2f} b",
            f" • Resina:                {costo_resina:.2f} b",
            f" • Revival star:          {costo_revival:.2f} b",
            f" • Carbonella:            {costo_carbonella:.2f} b",
            f" • Boccette:              {costo_boccette:.2f} b",
        ]

        if prezzo_vendita is not None:
            lines += [
                "",
                "Vendita & Profitto:",
                f" • Prezzo/antidoto:       {prezzo_vendita:.2f} b",
                f" • Ricavo totale:         {ricavo:.2f} b",
                f" • Guadagno totale:       {guadagno:.2f} b",
                f" • Margine per antidoto:  {margine_unit:.2f} b",
                f" • Ricarico %:            {ricarico_pct:.1f} %",
            ]

        text_ant_result.config(state="normal")
        text_ant_result.delete("1.0", tk.END)
        text_ant_result.insert(tk.END, "\n".join(lines))
        text_ant_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi degli antidoti: inserisci numeri validi!")


def calcola_revivify():
    try:
        # --- INPUT ---
        num = float(entry_rev_num.get())
        if num <= 0:
            raise ValueError

        # Prezzi già presenti nelle altre tab
        prezzo_core = float(entry_core.get())                 # Core fragment (tab Pozioni)  :contentReference[oaicite:6]{index=6}
        prezzo_carbone = float(entry_carbone.get())           # Carbone blocco (tab Pozioni) :contentReference[oaicite:7]{index=7}
        boccette_per_1b = float(entry_boccette_per_b.get())   # (bundle)                     :contentReference[oaicite:8]{index=8}
        prezzo_revival = float(entry_revival.get())           # Revival star (tab Antidoti)

        # Aggiorna le label riepilogo prezzi nella tab Revivify
        lab_rev_core.config(text=f"{prezzo_core}")
        lab_rev_revival.config(text=f"{prezzo_revival}")
        lab_rev_carbone.config(text=f"{prezzo_carbone}")
        lab_rev_boccette.config(text=f"{boccette_per_1b}")

        # Derivati
        costo_carbonella_unit = prezzo_carbone / 12.0
        costo_boccetta_unit = 1.0 / boccette_per_1b

        # Ricetta per 1 Revivify in Rame:
        # 1 Revival Star + 1 Core + 1 Carbonella + 1 Boccetta
        q_revival = num * 1.0
        q_core = num * 1.0
        q_carbonella = num * 1.0
        q_boccette = num * 1.0

        # Costi parziali
        costo_revival = q_revival * prezzo_revival
        costo_core = q_core * prezzo_core
        costo_carbonella = q_carbonella * costo_carbonella_unit
        costo_boccette = q_boccette * costo_boccetta_unit

        costo_tot = costo_revival + costo_core + costo_carbonella + costo_boccette
        costo_unit = costo_tot / num if num else 0.0

        # Profitto (se inserito il prezzo)
        try:
            prezzo_vendita = float(entry_rev_prezzo.get())
        except ValueError:
            prezzo_vendita = None

        if prezzo_vendita is not None:
            ricavo = prezzo_vendita * num
            guadagno = ricavo - costo_tot
            margine_unit = guadagno / num if num else 0.0
            ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0
        else:
            ricavo = guadagno = margine_unit = ricarico_pct = None

        # Preview
        if prezzo_vendita is not None:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Costo/Rev: {costo_unit:.2f} b    •    "
                f"Guadagno: {guadagno:.2f} b"
            )
        else:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Per Revivify: {costo_unit:.2f} b"
            )
        label_rev_preview.config(text=preview, fg=FG_TEXT, bg=BG_MAIN)

        # Dettaglio
        lines = [
            "Calderone: Rame (obbligatorio)",
            f"Revivify richieste:        {num:.2f}",
            "",
            f"COSTO TOTALE:             {costo_tot:.2f} b",
            f"Costo per Revivify:       {costo_unit:.2f} b",
            "",
            "Materiali richiesti:",
            f" • Revival star:           {q_revival:.2f}",
            f" • Core fragment:          {q_core:.2f}",
            f" • Carbonella:             {q_carbonella:.2f}",
            f" • Boccette:               {q_boccette:.2f}",
            "",
            "Costi parziali:",
            f" • Revival star:           {costo_revival:.2f} b",
            f" • Core fragment:          {costo_core:.2f} b",
            f" • Carbonella:             {costo_carbonella:.2f} b",
            f" • Boccette:               {costo_boccette:.2f} b",
        ]

        if prezzo_vendita is not None:
            lines += [
                "",
                "Vendita & Profitto:",
                f" • Prezzo/Rev:             {prezzo_vendita:.2f} b",
                f" • Ricavo totale:          {ricavo:.2f} b",
                f" • Guadagno totale:        {guadagno:.2f} b",
                f" • Margine per Rev:        {margine_unit:.2f} b",
                f" • Ricarico %:             {ricarico_pct:.1f} %",
            ]

        text_rev_result.config(state="normal")
        text_rev_result.delete("1.0", tk.END)
        text_rev_result.insert(tk.END, "\n".join(lines))
        text_rev_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi di Revivify: inserisci numeri validi!")


def calcola_extinguish():
    try:
        # --- INPUT ---
        num = float(entry_ext_num.get())
        if num <= 0:
            raise ValueError

        # Prezzi globali già presenti
        prezzo_core = float(entry_core.get())                 # Core (Pozioni)     :contentReference[oaicite:5]{index=5}
        prezzo_carbone = float(entry_carbone.get())           # Carbone (Pozioni)  :contentReference[oaicite:6]{index=6}
        boccette_per_1b = float(entry_boccette_per_b.get())   # Bundle (Pozioni)   :contentReference[oaicite:7]{index=7}

        # Prezzo specifico Extinguish
        prezzo_quartz = float(entry_quartz.get())

        # Aggiorna label riepilogo prezzi
        lab_ext_core.config(text=f"{prezzo_core}")
        lab_ext_carbone.config(text=f"{prezzo_carbone}")
        lab_ext_boccette.config(text=f"{boccette_per_1b}")

        # Derivati
        costo_carbonella_unit = prezzo_carbone / 12.0
        costo_boccetta_unit = 1.0 / boccette_per_1b

        # Ricetta per 1 Extinguish in Rame:
        # 1 Quarzo + 1 Core + 1 Carbonella + 1 Boccetta
        q_quartz = num * 1.0
        q_core = num * 1.0
        q_carbonella = num * 1.0
        q_boccette = num * 1.0

        # Costi parziali
        costo_quartz = q_quartz * prezzo_quartz
        costo_core = q_core * prezzo_core
        costo_carbonella = q_carbonella * costo_carbonella_unit
        costo_boccette = q_boccette * costo_boccetta_unit

        costo_tot = costo_quartz + costo_core + costo_carbonella + costo_boccette
        costo_unit = costo_tot / num if num else 0.0

        # Profitto (se inserito il prezzo)
        try:
            prezzo_vendita = float(entry_ext_prezzo.get())
        except ValueError:
            prezzo_vendita = None

        if prezzo_vendita is not None:
            ricavo = prezzo_vendita * num
            guadagno = ricavo - costo_tot
            margine_unit = guadagno / num if num else 0.0
            ricarico_pct = (margine_unit / costo_unit * 100.0) if costo_unit > 0 else 0.0
        else:
            ricavo = guadagno = margine_unit = ricarico_pct = None

        # Preview
        if prezzo_vendita is not None:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Costo/Ext: {costo_unit:.2f} b    •    "
                f"Guadagno: {guadagno:.2f} b"
            )
        else:
            preview = (
                f"Totale: {costo_tot:.2f} b    •    "
                f"Per Extinguish: {costo_unit:.2f} b"
            )
        label_ext_preview.config(text=preview, fg=FG_TEXT, bg=BG_MAIN)

        # Dettaglio
        lines = [
            "Calderone: Rame (obbligatorio)",
            f"Extinguish richieste:      {num:.2f}",
            "",
            f"COSTO TOTALE:             {costo_tot:.2f} b",
            f"Costo per Extinguish:     {costo_unit:.2f} b",
            "",
            "Materiali richiesti:",
            f" • Quarzo:                 {q_quartz:.2f}",
            f" • Core fragment:          {q_core:.2f}",
            f" • Carbonella:             {q_carbonella:.2f}",
            f" • Boccette:               {q_boccette:.2f}",
            "",
            "Costi parziali:",
            f" • Quarzo:                 {costo_quartz:.2f} b",
            f" • Core fragment:          {costo_core:.2f} b",
            f" • Carbonella:             {costo_carbonella:.2f} b",
            f" • Boccette:               {costo_boccette:.2f} b",
        ]

        if prezzo_vendita is not None:
            lines += [
                "",
                "Vendita & Profitto:",
                f" • Prezzo/Extinguish:      {prezzo_vendita:.2f} b",
                f" • Ricavo totale:          {ricavo:.2f} b",
                f" • Guadagno totale:        {guadagno:.2f} b",
                f" • Margine per Ext:        {margine_unit:.2f} b",
                f" • Ricarico %:             {ricarico_pct:.1f} %",
            ]

        text_ext_result.config(state="normal")
        text_ext_result.delete("1.0", tk.END)
        text_ext_result.insert(tk.END, "\n".join(lines))
        text_ext_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi di Extinguish: inserisci numeri validi!")



# --- Costanti resa per 9 pepite (lordo), poi togliamo 1 runa consumata ---

# Resa netta per 1 pepita (già tolta 1 runa "usata")
#  - Normali: Rame=11, Ferro=23, Oro=35 (Tin/Diamante non definite)
#  - Bardiche: Tin=23, Rame=23, Ferro=23, Oro=35 (Diamante non definita)
RESA_PEPITA_NET = {
    "Normali":  {"Tin": 0,  "Rame": 11, "Ferro": 23, "Oro": 35, "Diamante": 0},
    "Bardiche": {"Tin": 23, "Rame": 23, "Ferro": 23, "Oro": 35, "Diamante": 0},
}


PEPITE_PER_LINGOTTO = 9

def _get_prezzo_lingotto(met):
    mapping = {
        "Tin": entry_price_tin, "Rame": entry_price_cu, "Ferro": entry_price_fe,
        "Oro": entry_price_au, "Diamante": entry_price_dia
    }
    try:
        return float(mapping[met].get())
    except:
        return 0.0

def _manodopera(tipo, q_rune):
    # Normali: 1b ogni 32 rune (proporzionale)
    base = (q_rune / 32.0) * 1.0
    if tipo == "Bardiche":
        # sempre 1b in meno, ma minimo 1
        return max(1.0, base - 1.0)
    return max(0.0, base)


def calcola_rune_diretto():
    try:
        tipo = combo_rune_tipo.get()       # Normali/Bardiche
        met  = combo_rune_metallo.get()    # Tin/Rame/Ferro/Oro/Diamante
        pepite = float(entry_rune_pepite.get())        
        if pepite <= 0: 
            raise ValueError

        # prezzi e pepite
        prezzo_lingotto = _get_prezzo_lingotto(met)
        prezzo_pepita = prezzo_lingotto / 9.0 if prezzo_lingotto > 0 else 0.0

        # resa per pepita
        rune_per_pepita = RESA_PEPITA_NET.get(tipo, {}).get(met, 0)          # rune nette per 9 pepite
        if rune_per_pepita <= 0:
            messagebox.showerror("Resa non definita", f"Nessuna resa definita per {tipo} con {met}.")
            return
       

        # output
        rune_tot = pepite * rune_per_pepita
        costo_materiali = pepite * prezzo_pepita
        costo_lavoro = _manodopera(tipo, rune_tot)
        costo_tot = costo_materiali + costo_lavoro
        costo_per_runa = (costo_tot / rune_tot) if rune_tot > 0 else 0.0

        # preview
        label_rune_preview.config(
            text=f"Totale: {costo_tot:.2f} b    •    Costo/runa: {costo_per_runa:.3f} b",
            fg=FG_TEXT, bg=BG_MAIN
        )

        # dettaglio
        lines = [
            f"Tipo runa: {tipo} — Metallo: {met}",
            f"Pepite totali:           {pepite:.2f}",
            f"Resa netta per pepita: {rune_per_pepita} rune",
            "",
            f"RUNE PRODOTTE:           {rune_tot:.2f}",
            "",
            f"Costo materiali:         {costo_materiali:.2f} b (pepita = {prezzo_pepita:.4f} b)",
            f"Manodopera:              {costo_lavoro:.2f} b",
            f"COSTO TOTALE:            {costo_tot:.2f} b",
            f"Costo per runa:          {costo_per_runa:.4f} b",
        ]
        text_rune_result.config(state="normal"); text_rune_result.delete("1.0", tk.END)
        text_rune_result.insert(tk.END, "\n".join(lines)); text_rune_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi: numeri validi (lingotti > 0).")

def calcola_rune_inverso():
    import math
    try:
        # Input
        tipo = combo_inv_tipo.get()            # "Normali" / "Bardiche"
        target = float(entry_inv_quante.get()) # quante rune vuoi
        if target <= 0:
            raise ValueError

        # Prezzi lingotti (per derivare prezzo pepita)
        prezzi_lingotto = {
            "Tin": _get_prezzo_lingotto("Tin"),
            "Rame": _get_prezzo_lingotto("Rame"),
            "Ferro": _get_prezzo_lingotto("Ferro"),
            "Oro": _get_prezzo_lingotto("Oro"),
            "Diamante": _get_prezzo_lingotto("Diamante"),
        }

        righe = []
        best = None

        for met, pl in prezzi_lingotto.items():
            # Resa netta PER PEPITA (già tolta 1 runa consumata)
            rpp = RESA_PEPITA_NET.get(tipo, {}).get(met, 0)
            if rpp <= 0:
                continue

            # Pepite minime per raggiungere l'obiettivo (senza forzare lingotti interi)
            pepite_needed = math.ceil(target / rpp)

            # Se vuoi anche lo scenario "compro lingotti interi"
            lingotti_needed = math.ceil(pepite_needed / 9)
            pepite_eff = lingotti_needed * 9  # pepite effettive se compri lingotti

            # Prezzi
            prezzo_pepita = (pl / 9.0) if pl > 0 else 0.0

            # **Scenario A**: compro pepite precise (teorico, se puoi comprarle singole)
            rune_prod_A = pepite_needed * rpp
            costo_mat_A = pepite_needed * prezzo_pepita
            costo_lav_A = _manodopera(tipo, rune_prod_A)
            costo_tot_A = costo_mat_A + costo_lav_A
            costo_unit_A = (costo_tot_A / rune_prod_A) if rune_prod_A > 0 else 0.0

            # **Scenario B**: compro lingotti interi (9 pepite ciascuno)
            rune_prod_B = pepite_eff * rpp
            costo_mat_B = pepite_eff * prezzo_pepita
            costo_lav_B = _manodopera(tipo, rune_prod_B)
            costo_tot_B = costo_mat_B + costo_lav_B
            costo_unit_B = (costo_tot_B / rune_prod_B) if rune_prod_B > 0 else 0.0

            info = {
                "metallo": met,
                "pep_needed": pepite_needed,
                "lingotti_needed": lingotti_needed,
                "pep_eff": pepite_eff,
                "rpp": rpp,
                "A_rune": rune_prod_A, "A_costo": costo_tot_A, "A_unit": costo_unit_A,
                "B_rune": rune_prod_B, "B_costo": costo_tot_B, "B_unit": costo_unit_B,
            }
            righe.append(info)

            # scegli il migliore sullo scenario B (più realistico per acquisto)
            cand = costo_tot_B
            if best is None or cand < best["B_costo"]:
                best = info

        if not righe:
            messagebox.showerror("Rese non definite", "Nessuna resa disponibile per il tipo selezionato.")
            return

        # Ordina per costo totale (scenario B: lingotti interi)
        righe.sort(key=lambda x: x["B_costo"])

        # Output dettagliato
        lines = [
            f"Obiettivo: {target:.0f} rune {tipo}",
            "",
            "Metallo  |  Pepite min  |  Lingotti (x9)  |  Resa (rune/pepita)  |  SCENARIO A (pep. precise): Costo / Unit  |  SCENARIO B (lingotti interi): Costo / Unit",
            "-" * 120,
        ]
        for r in righe:
            lines.append(
                f"{r['metallo']:<8} | {r['pep_needed']:>11} | {r['lingotti_needed']:>14} | {r['rpp']:>18} | "
                f"A: {r['A_costo']:.2f} b / {r['A_unit']:.4f} b  |  "
                f"B: {r['B_costo']:.2f} b / {r['B_unit']:.4f} b"
            )

        lines += [
            "",
            f"MIGLIORE (lingotti interi): {best['metallo']}  →  {best['lingotti_needed']} lingotti "
            f"({best['pep_eff']} pepite)  →  {best['B_rune']:.0f} rune  |  "
            f"Costo {best['B_costo']:.2f} b  (Unit {best['B_unit']:.4f} b)"
        ]

        text_rune_result.config(state="normal")
        text_rune_result.delete("1.0", tk.END)
        text_rune_result.insert(tk.END, "\n".join(lines))
        text_rune_result.config(state="disabled")

        # preview breve
        label_rune_preview.config(
            text=f"Migliore: {best['metallo']} — {best['pep_needed']} pepite (≈ {best['lingotti_needed']} lingotti)",
            fg=FG_TEXT, bg=BG_MAIN
        )

    except ValueError:
        messagebox.showerror("Errore", "Inserisci un numero valido di rune.")


# =========================
#   GUI + SCROLL INTELLIGENTE
# =========================

root = tk.Tk()
root.title(f"{APP_NAME} ⚗️ v{APP_VERSION}")
root.geometry("760x620")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# canvas scrollabile
outer_canvas = tk.Canvas(root, bg=BG_MAIN, highlightthickness=0)
outer_canvas.pack(side="left", fill="both", expand=True)

main_scrollbar = tk.Scrollbar(root, orient="vertical", command=outer_canvas.yview)
main_scrollbar.pack(side="right", fill="y")

outer_canvas.configure(yscrollcommand=main_scrollbar.set)

inner_frame = tk.Frame(outer_canvas, bg=BG_MAIN)
outer_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

def on_configure(event):
    outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
inner_frame.bind("<Configure>", on_configure)

# scroll globale
def _on_mousewheel_canvas(event):
    outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
outer_canvas.bind_all("<MouseWheel>", _on_mousewheel_canvas)

# scroll solo nel box dettaglio
def _on_mousewheel_text(event):
    text_result.yview_scroll(int(-1 * (event.delta / 120)), "units")
    return "break"

def _bind_wheel_to_text(event):
    outer_canvas.unbind_all("<MouseWheel>")
    text_result.bind_all("<MouseWheel>", _on_mousewheel_text)

def _bind_wheel_to_canvas(event):
    text_result.unbind_all("<MouseWheel>")
    outer_canvas.bind_all("<MouseWheel>", _on_mousewheel_canvas)

# === NOTEBOOK A DUE TAB (v2.0) ===
notebook = ttk.Notebook(inner_frame)
tab_pozioni = tk.Frame(notebook, bg=BG_MAIN)
tab_antidoti = tk.Frame(notebook, bg=BG_MAIN)
tab_revivify = tk.Frame(notebook, bg=BG_MAIN)
tab_extinguish = tk.Frame(notebook, bg=BG_MAIN)  
tab_rune = tk.Frame(notebook, bg=BG_MAIN)
notebook.add(tab_pozioni, text="Pozioni di cura")
notebook.add(tab_antidoti, text="Antidoti")
notebook.add(tab_revivify, text="Revivify")
notebook.add(tab_extinguish, text="Extinguish")
notebook.add(tab_rune, text="Rune")
notebook.pack(fill="both", expand=True, padx=0, pady=0)


def make_panel(parent, title):
    frame = tk.Frame(parent, bg=BG_PANEL, bd=0)
    header = tk.Label(
        frame,
        text=title,
        font=SECTION_FONT,
        bg=BG_PANEL,
        fg=FG_TEXT,
        anchor="w",
    )
    header.pack(fill="x", padx=10, pady=(8, 4))
    inner = tk.Frame(frame, bg=BG_PANEL)
    inner.pack(fill="x", padx=10, pady=(0, 10))
    return frame, inner


# =========================
#   MENU "INFO"
# =========================

menubar = tk.Menu(root, tearoff=0)

menu_info = tk.Menu(menubar, tearoff=0, bg="white", fg="black")
menu_info.add_command(label="Informazioni / Crediti", command=show_info)
menu_info.add_command(label="Licenza", command=show_license)
menubar.add_cascade(label="Info", menu=menu_info)

root.config(menu=menubar)


# =========================
#   SEZIONI UI
# =========================

# TITOLO
tk.Label(
    tab_pozioni,
    text=f"{APP_NAME}",
    font=TITLE_FONT,
    fg=FG_TEXT,
    bg=BG_MAIN,
).pack(pady=8)

# --- PANNELLO PROFILO PREZZI ---
panel_prof, prof_inner = make_panel(tab_pozioni, "Profilo prezzi")

tk.Label(
    prof_inner,
    text="Profilo prezzi:",
    font=LABEL_FONT,
    bg=BG_PANEL,
    fg=FG_TEXT
).grid(row=0, column=0, sticky="e", padx=4, pady=4)

# combobox EDITABILE per poter scrivere / rinominare / creare nomi nuovi
combo_profile = ttk.Combobox(
    prof_inner,
    width=16,
    font=LABEL_FONT,
)  # non readonly apposta
combo_profile.grid(row=0, column=1, padx=4, pady=4, sticky="w")

btn_load_prof = tk.Button(
    prof_inner,
    text="Carica profilo",
    command=apply_profile,
    bg="#444",
    fg=FG_TEXT,
    font=LABEL_FONT,
    activebackground="#555",
    activeforeground=FG_TEXT,
    relief="flat",
    padx=8,
    pady=4,
    cursor="hand2",
)
btn_load_prof.grid(row=0, column=2, padx=4, pady=4)

btn_save_prof = tk.Button(
    prof_inner,
    text="Salva profilo",
    command=save_profile,
    bg=ACCENT,
    fg="white",
    font=LABEL_FONT,
    activebackground="#574dff",
    activeforeground="white",
    relief="flat",
    padx=8,
    pady=4,
    cursor="hand2",
)
btn_save_prof.grid(row=0, column=3, padx=4, pady=4)

btn_rename_prof = tk.Button(
    prof_inner,
    text="Rinomina profilo",
    command=rename_profile,
    bg="#444",
    fg=FG_TEXT,
    font=LABEL_FONT,
    activebackground="#555",
    activeforeground=FG_TEXT,
    relief="flat",
    padx=8,
    pady=4,
    cursor="hand2",
)
btn_rename_prof.grid(row=0, column=4, padx=4, pady=4)

btn_delete_prof = tk.Button(
    prof_inner,
    text="Elimina profilo",
    command=delete_profile,
    bg=DANGER_BG,
    fg="white",
    font=LABEL_FONT,
    activebackground=DANGER_BG_ACTIVE,
    activeforeground="white",
    relief="flat",
    padx=8,
    pady=4,
    cursor="hand2",
)
btn_delete_prof.grid(row=0, column=5, padx=4, pady=4)

panel_prof.pack(padx=10, pady=6, fill="x")

# --- PRODUZIONE ---
panel_prod, prod_inner = make_panel(tab_pozioni, "Produzione")

tk.Label(prod_inner, text="Numero pozioni:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_pozioni = tk.Entry(
    prod_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_pozioni.grid(row=0, column=1, pady=4)

tk.Label(prod_inner, text="Tipo reagente:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=4)
combo_tier = ttk.Combobox(
    prod_inner,
    values=["T1", "T2", "T3"],
    width=10,
    state="readonly",
    font=LABEL_FONT,
)
combo_tier.current(0)
combo_tier.grid(row=1, column=1, pady=4)

tk.Label(prod_inner, text="Calderone:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=4)
combo_calderone = ttk.Combobox(
    prod_inner,
    values=["Terracotta", "Rame", "Ferro", "Oro", "Diamante"],
    width=12,
    state="readonly",
    font=LABEL_FONT,
)
combo_calderone.current(0)
combo_calderone.grid(row=2, column=1, pady=4)

panel_prod.pack(padx=10, pady=6, fill="x")

# --- PREZZI DIRETTI ---
panel_price_direct, price_direct_inner = make_panel(tab_pozioni, "Prezzi diretti (in b)")

tk.Label(price_direct_inner, text="Reagente (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_reagente = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_reagente.insert(0, "1.5")
entry_reagente.grid(row=0, column=1, pady=3)

tk.Label(price_direct_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
entry_core = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_core.insert(0, "1.0")
entry_core.grid(row=1, column=1, pady=3)

tk.Label(price_direct_inner, text="Carbone (1 blocco):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
entry_carbone = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_carbone.insert(0, "1.5")
entry_carbone.grid(row=2, column=1, pady=3)

tk.Label(
    price_direct_inner,
    text="(1 blocco = 12 carbonella)",
    font=("Segoe UI", 8),
    bg=BG_PANEL,
    fg=FG_SUBTLE,
).grid(row=2, column=2, sticky="w", padx=4)

panel_price_direct.pack(padx=10, pady=6, fill="x")

# --- QUANTE UNITÀ OTTIENI CON 1 b ---
panel_bundle, bundle_inner = make_panel(tab_pozioni, "Quante unità ottieni con 1 b")

tk.Label(bundle_inner, text="Verdure per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_verdure_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_verdure_per_b.insert(0, "3")
entry_verdure_per_b.grid(row=0, column=1, pady=3)

tk.Label(bundle_inner, text="Vasetti per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
entry_vasetti_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_vasetti_per_b.insert(0, "15")
entry_vasetti_per_b.grid(row=1, column=1, pady=3)

tk.Label(bundle_inner, text="Boccette per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
entry_boccette_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_boccette_per_b.insert(0, "14")
entry_boccette_per_b.grid(row=2, column=1, pady=3)

panel_bundle.pack(padx=10, pady=6, fill="x")



# --- REVIVIFY: PRODUZIONE ---
rev_prod, rev_prod_inner = make_panel(tab_revivify, "Produzione (Revivify)")

tk.Label(rev_prod_inner, text="Numero Revivify:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_rev_num = tk.Entry(
    rev_prod_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat",
)
entry_rev_num.grid(row=0, column=1, pady=4)

# calderone fisso: Rame
tk.Label(rev_prod_inner, text="Calderone: Rame (fisso)", font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)\
    .grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=2)

rev_prod.pack(padx=10, pady=6, fill="x")

# --- REVIVIFY: PREZZI ---
# NOTA: usiamo gli stessi campi globali già esistenti:
# - Core fragment: entry_core (tab Pozioni)            (profilabile)  :contentReference[oaicite:3]{index=3}
# - Carbone (blocchi->carbonella): entry_carbone       (profilabile)  :contentReference[oaicite:4]{index=4}
# - Boccette per 1 b: entry_boccette_per_b             (profilabile)  :contentReference[oaicite:5]{index=5}
# - Revival star: entry_revival (tab Antidoti)                        (nuovo campo già creato)

rev_price, rev_price_inner = make_panel(tab_revivify, "Prezzi usati (solo lettura)")

tk.Label(rev_price_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
lab_rev_core = tk.Label(rev_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_rev_core.grid(row=0, column=1, sticky="w", pady=3)

tk.Label(rev_price_inner, text="Revival star (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
lab_rev_revival = tk.Label(rev_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_rev_revival.grid(row=1, column=1, sticky="w", pady=3)

tk.Label(rev_price_inner, text="Carbone (1 blocco = 12 carbonella):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
lab_rev_carbone = tk.Label(rev_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_rev_carbone.grid(row=2, column=1, sticky="w", pady=3)

tk.Label(rev_price_inner, text="Boccette per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=3, column=0, sticky="e", padx=4, pady=3)
lab_rev_boccette = tk.Label(rev_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_rev_boccette.grid(row=3, column=1, sticky="w", pady=3)

rev_price.pack(padx=10, pady=6, fill="x")

# --- REVIVIFY: VENDITA ---
rev_sale, rev_sale_inner = make_panel(tab_revivify, "Vendita (Revivify)")
tk.Label(rev_sale_inner, text="Prezzo di vendita per Revivify (b):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_rev_prezzo = tk.Entry(
    rev_sale_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat",
)
entry_rev_prezzo.insert(0, "")
entry_rev_prezzo.grid(row=0, column=1, pady=4)
rev_sale.pack(padx=10, pady=6, fill="x")

# --- REVIVIFY: BOTTONE & PREVIEW ---
tk.Button(
    tab_revivify, text="CALCOLA REVIVIFY", command=lambda: calcola_revivify(),
    bg=ACCENT, fg="white", font=BUTTON_FONT, activebackground="#574dff",
    activeforeground="white", relief="flat", cursor="hand2", padx=12, pady=6,
).pack(pady=(10, 6))

label_rev_preview = tk.Label(
    tab_revivify, text="Totale: -    •    Per Revivify: -",
    font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=FG_TEXT,
)
label_rev_preview.pack(pady=(0, 10))

rev_panel_result = tk.Frame(tab_revivify, bg=BG_PANEL)
rev_panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

tk.Label(rev_panel_result, text="Dettaglio", font=SECTION_FONT, bg=BG_PANEL, fg=FG_TEXT, anchor="w")\
    .pack(fill="x", padx=10, pady=(8, 4))

rev_inner_result = tk.Frame(rev_panel_result, bg=BG_PANEL)
rev_inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

rev_scrollbar = tk.Scrollbar(rev_inner_result)
rev_scrollbar.pack(side="right", fill="y")

text_rev_result = tk.Text(
    rev_inner_result, height=14, font=RESULT_FONT, state="disabled", wrap="word",
    yscrollcommand=rev_scrollbar.set, bg=BG_RESULT, fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat", padx=10, pady=10,
)
text_rev_result.pack(fill="both", expand=True)
rev_scrollbar.config(command=text_rev_result.yview)



# --- EXTINGUISH: PRODUZIONE ---
ext_prod, ext_prod_inner = make_panel(tab_extinguish, "Produzione (Extinguish)")

tk.Label(ext_prod_inner, text="Numero Extinguish:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_ext_num = tk.Entry(
    ext_prod_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat",
)
entry_ext_num.grid(row=0, column=1, pady=4)

# calderone fisso: Rame
tk.Label(ext_prod_inner, text="Calderone: Rame (fisso)", font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)\
    .grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=2)

ext_prod.pack(padx=10, pady=6, fill="x")

# --- EXTINGUISH: PREZZI ---
ext_price, ext_price_inner = make_panel(tab_extinguish, "Prezzi (Extinguish)")

tk.Label(ext_price_inner, text="Quarzo (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_quartz = tk.Entry(ext_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
                        insertbackground=FG_TEXT, relief="flat")
entry_quartz.insert(0, "1.0")
entry_quartz.grid(row=0, column=1, pady=3)

# Mostriamo (solo lettura) i prezzi globali usati per core/carbone/boccette
tk.Label(ext_price_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
lab_ext_core = tk.Label(ext_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_ext_core.grid(row=1, column=1, sticky="w", pady=3)

tk.Label(ext_price_inner, text="Carbone (1 blocco = 12 carbonella):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
lab_ext_carbone = tk.Label(ext_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_ext_carbone.grid(row=2, column=1, sticky="w", pady=3)

tk.Label(ext_price_inner, text="Boccette per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=3, column=0, sticky="e", padx=4, pady=3)
lab_ext_boccette = tk.Label(ext_price_inner, font=LABEL_FONT, bg=BG_PANEL, fg=FG_SUBTLE)
lab_ext_boccette.grid(row=3, column=1, sticky="w", pady=3)

ext_price.pack(padx=10, pady=6, fill="x")

# --- EXTINGUISH: VENDITA ---
ext_sale, ext_sale_inner = make_panel(tab_extinguish, "Vendita (Extinguish)")
tk.Label(ext_sale_inner, text="Prezzo di vendita per Extinguish (b):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_ext_prezzo = tk.Entry(
    ext_sale_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat",
)
entry_ext_prezzo.insert(0, "")
entry_ext_prezzo.grid(row=0, column=1, pady=4)
ext_sale.pack(padx=10, pady=6, fill="x")

# --- EXTINGUISH: BOTTONE & PREVIEW ---
tk.Button(
    tab_extinguish, text="CALCOLA EXTINGUISH", command=lambda: calcola_extinguish(),
    bg=ACCENT, fg="white", font=BUTTON_FONT, activebackground="#574dff",
    activeforeground="white", relief="flat", cursor="hand2", padx=12, pady=6,
).pack(pady=(10, 6))

label_ext_preview = tk.Label(
    tab_extinguish, text="Totale: -    •    Per Extinguish: -",
    font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=FG_TEXT,
)
label_ext_preview.pack(pady=(0, 10))

ext_panel_result = tk.Frame(tab_extinguish, bg=BG_PANEL)
ext_panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

tk.Label(ext_panel_result, text="Dettaglio", font=SECTION_FONT, bg=BG_PANEL, fg=FG_TEXT, anchor="w")\
    .pack(fill="x", padx=10, pady=(8, 4))

ext_inner_result = tk.Frame(ext_panel_result, bg=BG_PANEL)
ext_inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

ext_scrollbar = tk.Scrollbar(ext_inner_result)
ext_scrollbar.pack(side="right", fill="y")

text_ext_result = tk.Text(
    ext_inner_result, height=14, font=RESULT_FONT, state="disabled", wrap="word",
    yscrollcommand=ext_scrollbar.set, bg=BG_RESULT, fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat", padx=10, pady=10,
)
text_ext_result.pack(fill="both", expand=True)
ext_scrollbar.config(command=text_ext_result.yview)


# --- RUNE: PREZZI LINGOTTI (b per 1 lingotto) ---
rune_price_panel, rune_price_inner = make_panel(tab_rune, "Prezzi lingotti (b per 1 lingotto)")
tk.Label(rune_price_inner, text="Tin:",   font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0, sticky="e", padx=4, pady=3)
tk.Label(rune_price_inner, text="Rame:",  font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=2, sticky="e", padx=4, pady=3)
tk.Label(rune_price_inner, text="Ferro:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=4, sticky="e", padx=4, pady=3)
tk.Label(rune_price_inner, text="Oro:",   font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0, sticky="e", padx=4, pady=3)
tk.Label(rune_price_inner, text="Diamante:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=2, sticky="e", padx=4, pady=3)

entry_price_tin  = tk.Entry(rune_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_price_tin.insert(0, "9.0");  entry_price_tin.grid(row=0, column=1, pady=3)
entry_price_cu   = tk.Entry(rune_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_price_cu.insert(0, "9.0");   entry_price_cu.grid(row=0, column=3, pady=3)
entry_price_fe   = tk.Entry(rune_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_price_fe.insert(0, "9.0");   entry_price_fe.grid(row=0, column=5, pady=3)
entry_price_au   = tk.Entry(rune_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_price_au.insert(0, "12.0");  entry_price_au.grid(row=1, column=1, pady=3)
entry_price_dia  = tk.Entry(rune_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_price_dia.insert(0, "18.0"); entry_price_dia.grid(row=1, column=3, pady=3)

rune_price_panel.pack(padx=10, pady=6, fill="x")


# --- RUNE: CALCOLO DA LINGOTTI (diretto) ---
rune_make_panel, rune_make_inner = make_panel(tab_rune, "Calcolo diretto (da pepite → rune)")

tk.Label(rune_make_inner, text="Tipo runa:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0, sticky="e", padx=4, pady=4)
combo_rune_tipo = ttk.Combobox(rune_make_inner, values=["Normali", "Bardiche"], width=12, state="readonly", font=LABEL_FONT); combo_rune_tipo.current(0)
combo_rune_tipo.grid(row=0, column=1, pady=4)

tk.Label(rune_make_inner, text="Metallo:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0, sticky="e", padx=4, pady=4)
combo_rune_metallo = ttk.Combobox(rune_make_inner, values=["Tin", "Rame", "Ferro", "Oro", "Diamante"], width=12, state="readonly", font=LABEL_FONT); combo_rune_metallo.current(1)
combo_rune_metallo.grid(row=1, column=1, pady=4)

tk.Label(rune_make_inner, text="Pepite da usare:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=2, column=0, sticky="e", padx=4, pady=4)
entry_rune_pepite = tk.Entry(rune_make_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_rune_pepite.insert(0, "1")
entry_rune_pepite.grid(row=2, column=1, pady=4)

tk.Button(rune_make_inner, text="CALCOLA RUNE", command=lambda: calcola_rune_diretto(), bg=ACCENT, fg="white",
          font=BUTTON_FONT, activebackground="#574dff", activeforeground="white", relief="flat", cursor="hand2",
          padx=12, pady=6).grid(row=3, column=0, columnspan=2, pady=(6, 2))

label_rune_preview = tk.Label(rune_make_inner, text="Totale: -    •    Costo/runa: -", font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=FG_TEXT)
label_rune_preview.grid(row=4, column=0, columnspan=3, pady=(6, 4))

rune_make_panel.pack(padx=10, pady=6, fill="x")


# --- RUNE: CALCOLO INVERSO (da quantità → pepite/lingotti & best metal) ---
rune_inv_panel, rune_inv_inner = make_panel(tab_rune, "Calcolo inverso (quante rune vuoi?)")

tk.Label(rune_inv_inner, text="Tipo runa:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=0, column=0, sticky="e", padx=4, pady=4)
combo_inv_tipo = ttk.Combobox(rune_inv_inner, values=["Normali", "Bardiche"], width=12, state="readonly", font=LABEL_FONT); combo_inv_tipo.current(0)
combo_inv_tipo.grid(row=0, column=1, pady=4)

tk.Label(rune_inv_inner, text="Rune desiderate:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT).grid(row=1, column=0, sticky="e", padx=4, pady=4)
entry_inv_quante = tk.Entry(rune_inv_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT, insertbackground=FG_TEXT, relief="flat"); entry_inv_quante.insert(0, "32")
entry_inv_quante.grid(row=1, column=1, pady=4)

tk.Button(rune_inv_inner, text="OTTIMIZZA COSTO", command=lambda: calcola_rune_inverso(),
          bg=ACCENT, fg="white", font=BUTTON_FONT, activebackground="#574dff", activeforeground="white",
          relief="flat", cursor="hand2", padx=12, pady=6).grid(row=2, column=0, columnspan=2, pady=(6, 2))


rune_inv_panel.pack(padx=10, pady=6, fill="x")


rune_result_panel = tk.Frame(tab_rune, bg=BG_PANEL); rune_result_panel.pack(padx=10, pady=(0, 10), fill="both", expand=True)
tk.Label(rune_result_panel, text="Dettaglio", font=SECTION_FONT, bg=BG_PANEL, fg=FG_TEXT, anchor="w").pack(fill="x", padx=10, pady=(8, 4))
rune_inner_result = tk.Frame(rune_result_panel, bg=BG_PANEL); rune_inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

rune_scrollbar = tk.Scrollbar(rune_inner_result); rune_scrollbar.pack(side="right", fill="y")
text_rune_result = tk.Text(rune_inner_result, height=14, font=RESULT_FONT, state="disabled", wrap="word",
                           yscrollcommand=rune_scrollbar.set, bg=BG_RESULT, fg=FG_TEXT,
                           insertbackground=FG_TEXT, relief="flat", padx=10, pady=10)
text_rune_result.pack(fill="both", expand=True); rune_scrollbar.config(command=text_rune_result.yview)






# --- VENDITA / PROFITTO (1.5) ---
panel_sale, sale_inner = make_panel(tab_pozioni, "Vendita")

# Prezzo vendita
tk.Label(
    sale_inner,
    text="Prezzo di vendita per pozione (b):",
    font=LABEL_FONT,
    bg=BG_PANEL,
    fg=FG_TEXT
).grid(row=0, column=0, sticky="e", padx=4, pady=4)

entry_prezzo_vendita = tk.Entry(
    sale_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_prezzo_vendita.insert(0, "")
entry_prezzo_vendita.grid(row=0, column=1, pady=4, sticky="w")



# Sconto applicato al cliente (%)
tk.Label(
    sale_inner,
    text="Sconto al cliente (%):",
    font=LABEL_FONT,
    bg=BG_PANEL,
    fg=FG_TEXT
).grid(row=2, column=0, sticky="e", padx=4, pady=4)

entry_sconto_perc = tk.Entry(
    sale_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_sconto_perc.insert(0, "0")
entry_sconto_perc.grid(row=2, column=1, pady=4, sticky="w")



panel_sale.pack(padx=10, pady=6, fill="x")


# --- BOTTONE CALCOLA ---
tk.Button(
    tab_pozioni,
    text="CALCOLA",
    command=calcola,
    bg=ACCENT,
    fg="white",
    font=BUTTON_FONT,
    activebackground="#574dff",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=6,
).pack(pady=(10, 6))

# --- PREVIEW COSTI RAPIDI ---
label_preview = tk.Label(
    tab_pozioni,
    text="Totale: -    •    Per pozione: -",
    font=("Segoe UI", 11, "bold"),
    bg=BG_MAIN,
    fg=FG_TEXT,
)
label_preview.pack(pady=(0, 10))

# --- DETTAGLIO ---
panel_result = tk.Frame(tab_pozioni, bg=BG_PANEL)
panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

tk.Label(
    panel_result,
    text="Dettaglio",
    font=SECTION_FONT,
    bg=BG_PANEL,
    fg=FG_TEXT,
    anchor="w",
).pack(fill="x", padx=10, pady=(8, 4))

inner_result = tk.Frame(panel_result, bg=BG_PANEL)
inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scrollbar = tk.Scrollbar(inner_result)
scrollbar.pack(side="right", fill="y")

text_result = tk.Text(
    inner_result,
    height=14,
    font=RESULT_FONT,
    state="disabled",
    wrap="word",
    yscrollcommand=scrollbar.set,
    bg=BG_RESULT,
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
    padx=10,
    pady=10,
)
text_result.pack(fill="both", expand=True)
scrollbar.config(command=text_result.yview)

text_result.bind("<Enter>", _bind_wheel_to_text)
text_result.bind("<Leave>", _bind_wheel_to_canvas)


# --- ANTIDOTI: PRODUZIONE ---
ant_prod, ant_prod_inner = make_panel(tab_antidoti, "Produzione (Antidoti)")

tk.Label(ant_prod_inner, text="Numero antidoti:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_ant_num = tk.Entry(
    ant_prod_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat",
)
entry_ant_num.grid(row=0, column=1, pady=4)

tk.Label(ant_prod_inner, text="Calderone:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=4)
combo_ant_calderone = ttk.Combobox(
    ant_prod_inner, values=["Terracotta", "Ferro"], width=12, state="readonly", font=LABEL_FONT
)
combo_ant_calderone.current(0)
combo_ant_calderone.grid(row=1, column=1, pady=4)

ant_prod.pack(padx=10, pady=6, fill="x")

# --- ANTIDOTI: PREZZI DIRETTI ---
ant_price, ant_price_inner = make_panel(tab_antidoti, "Prezzi diretti (Antidoti)")

tk.Label(ant_price_inner, text="Brim powder (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_brim = tk.Entry(ant_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
                      insertbackground=FG_TEXT, relief="flat")
entry_brim.insert(0, "1.0")
entry_brim.grid(row=0, column=1, pady=3)

tk.Label(ant_price_inner, text="Carne marcia (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
entry_rotten = tk.Entry(ant_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
                        insertbackground=FG_TEXT, relief="flat")
entry_rotten.insert(0, "1.0")
entry_rotten.grid(row=1, column=1, pady=3)

tk.Label(ant_price_inner, text="Revival star (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
entry_revival = tk.Entry(ant_price_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
                         insertbackground=FG_TEXT, relief="flat")
entry_revival.insert(0, "2.0")
entry_revival.grid(row=2, column=1, pady=3)

# Nota: resina, carbonella, boccette usano i prezzi/pacchetti GLOBALI già inseriti nella tab Pozioni:
# - resina = calcolata da verdure/vasetti (già presenti)
# - carbonella = da 'Carbone (1 blocco)' / 12
# - boccette = da 'Boccette per 1 b'

ant_price.pack(padx=10, pady=6, fill="x")

# --- ANTIDOTI: VENDITA ---
ant_sale, ant_sale_inner = make_panel(tab_antidoti, "Vendita (Antidoti)")
tk.Label(ant_sale_inner, text="Prezzo di vendita per antidoto (b):",
         font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_ant_prezzo = tk.Entry(ant_sale_inner, width=10, font=LABEL_FONT, bg="#3a3a3a", fg=FG_TEXT,
                            insertbackground=FG_TEXT, relief="flat")
entry_ant_prezzo.insert(0, "")
entry_ant_prezzo.grid(row=0, column=1, pady=4)
ant_sale.pack(padx=10, pady=6, fill="x")

# --- ANTIDOTI: BOTTONE & PREVIEW ---
tk.Button(
    tab_antidoti, text="CALCOLA ANTIDOTI", command=lambda: calcola_antidoti(),
    bg=ACCENT, fg="white", font=BUTTON_FONT, activebackground="#574dff",
    activeforeground="white", relief="flat", cursor="hand2", padx=12, pady=6,
).pack(pady=(10, 6))

label_ant_preview = tk.Label(
    tab_antidoti, text="Totale: -    •    Per antidoto: -",
    font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=FG_TEXT,
)
label_ant_preview.pack(pady=(0, 10))

ant_panel_result = tk.Frame(tab_antidoti, bg=BG_PANEL)
ant_panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

tk.Label(
    ant_panel_result, text="Dettaglio", font=SECTION_FONT,
    bg=BG_PANEL, fg=FG_TEXT, anchor="w",
).pack(fill="x", padx=10, pady=(8, 4))

ant_inner_result = tk.Frame(ant_panel_result, bg=BG_PANEL)
ant_inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

ant_scrollbar = tk.Scrollbar(ant_inner_result)
ant_scrollbar.pack(side="right", fill="y")

text_ant_result = tk.Text(
    ant_inner_result, height=14, font=RESULT_FONT, state="disabled", wrap="word",
    yscrollcommand=ant_scrollbar.set, bg=BG_RESULT, fg=FG_TEXT,
    insertbackground=FG_TEXT, relief="flat", padx=10, pady=10,
)
text_ant_result.pack(fill="both", expand=True)
ant_scrollbar.config(command=text_ant_result.yview)



# =========================
#   INIZIALIZZAZIONE PROFILI
# =========================

profiles = load_all_profiles()
combo_profile["values"] = list(profiles.keys())
if combo_profile["values"]:
    combo_profile.set(combo_profile["values"][0])  # pre-seleziona un profilo esistente


# =========================
#   HOOK DI CHIUSURA (SALVA AUTO)
# =========================

def on_close():
    save_config()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)


# =========================
#   CARICA CONFIG ALL'AVVIO
# =========================

load_config()


# =========================
#   LOOP FINALE
# =========================

root.mainloop()
