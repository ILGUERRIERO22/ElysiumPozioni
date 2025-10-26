import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# =========================
#   COSTANTI TEMA / STILE
# =========================

APP_NAME = "Elysium Pozioni"
APP_VERSION = "1.3.2"
APP_AUTHOR = "ILGUERRIERO22"

CONFIG_FILE = "config.json"      # salva ultimo stato usato
PROFILES_FILE = "profiles.json"  # salva profili di prezzo multipli

BG_MAIN = "#1e1e1e"
BG_PANEL = "#2a2a2a"
BG_RESULT = "#111111"
FG_TEXT = "#eaeaea"
FG_SUBTLE = "#9e9e9e"
ACCENT = "#6a5dfd"

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
    """Rinomina il profilo attuale (chiave nel dict) in un nuovo nome scelto dall'utente."""
    old_name = combo_profile.get().strip()
    if not old_name:
        messagebox.showerror("Errore", "Seleziona il profilo da rinominare prima.")
        return

    if old_name not in profiles:
        messagebox.showerror("Errore", f"Il profilo '{old_name}' non esiste.")
        return

    # Chiediamo il nuovo nome con una piccola finestra popup
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

        # se il nome è uguale, niente da fare
        if new_name == old_name:
            rename_win.destroy()
            return

        # se il nuovo nome già esiste, chiediamo conferma
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

    # Chiedi conferma: questa azione è distruttiva
    conferma = messagebox.askyesno(
        "Conferma eliminazione",
        f"Sei sicuro di voler eliminare il profilo '{name}'?\n"
        "Questa azione non può essere annullata."
    )
    if not conferma:
        return

    # Elimina dal dizionario in memoria
    del profiles[name]

    # Salva nuovo stato su disco
    save_all_profiles(profiles)

    # Aggiorna combobox
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
        "last_profile": combo_profile.get()
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
        "Calcolatore di costo pozioni per Elysium.\n"
        "Supporta calderoni Terracotta / Rame / Ferro / Oro / Diamante.\n"
        "Salvataggio automatico e profili di mercato multipli.\n\n"
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

        # --- COSTI UNITARI CALCOLATI ---
        costo_verdura_unit = 1.0 / verdure_per_1b        # b per 1 verdura
        costo_vasetto_unit = 1.0 / vasetti_per_1b        # b per 1 vasetto
        costo_boccetta_unit = 1.0 / boccette_per_1b      # b per 1 boccetta

        # Resina: 2 verdure + 1 vasetto -> 2 resine
        costo_resina_unit = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0

        # Carbonella: 1 carbone = 12 carbonella
        costo_carbonella_unit = prezzo_carbone / 12.0

        # ======================================================
        # LOGICA CALDERONI (ereditata da v1.2)
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
            # 2 catalyst -> 3 pozioni T2 => 1 catalyst -> 1.5 pozioni
            # 2 carbonella -> 3 pozioni => 1 carbonella -> 1.5 pozioni
            pozioni_per_catalyst = 1.5
            pozioni_per_carbonella = 1.5
            tier_pozione_prodotta = "T2"

        elif tipo_calderone == "Diamante":
            # 3 catalyst -> 2 pozioni T3 => 1 catalyst -> 0.666...
            # 3 carbonella -> 2 pozioni => 1 carbonella -> 0.666...
            pozioni_per_catalyst = (2.0 / 3.0)
            pozioni_per_carbonella = (2.0 / 3.0)
            tier_pozione_prodotta = "T3"

        else:
            raise ValueError("Tipo calderone non valido")

        # catalyst necessari = pozioni richieste / pozioni prodotte per catalyst
        catalyst_necessari = num_pozioni / pozioni_per_catalyst

        # carbonella necessaria = pozioni richieste / pozioni prodotte per carbonella
        carbonella_tot = num_pozioni / pozioni_per_carbonella

        # Efficienze per output leggibile
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
        costo_reagenti = reagenti_usati * float(entry_reagente.get())
        costo_core = core_usati * float(entry_core.get())
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
        # ANTEPRIMA COSTO RAPIDO
        # =========================
        label_preview.config(
            text=f"Totale: {costo_totale:.2f} b    •    Per pozione: {costo_per_pozione:.2f} b",
            fg=FG_TEXT,
            bg=BG_MAIN,
        )

        # =========================
        # OUTPUT DETTAGLIATO
        # =========================
        output_lines = [
            f"Profilo prezzi attivo:   {combo_profile.get().strip() or '(non salvato)'}",
            f"Calderone:               {tipo_calderone}",
            f"Pozione prodotta:        {tier_pozione_prodotta}",
            f"Pozioni totali richieste:{num_pozioni:.2f}",
            f"Tipo reagente usato:     {tier_reagente}",
            "",
            f"COSTO TOTALE:            {costo_totale:.2f} b",
            f"Costo per pozione:       {costo_per_pozione:.2f} b",
            "",
            "Efficienza calderone:",
            f" • Catalyst per pozione:   {catalyst_per_pozione:.4f}",
            f" • Carbonella per pozione: {carbonella_per_pozione:.4f}",
            "",
            "Materiali richiesti:",
            f" • Catalyst totali:        {catalyst_necessari:.2f}",
            f" • Reagenti usati:         {reagenti_usati:.2f}",
            f" • Core frammenti:         {core_usati:.2f}",
            f" • Resine:                 {resine_usate:.2f}",
            f" • Carbonella totale:      {carbonella_tot:.2f}",
            f" • Boccette:               {boccette_tot:.2f}",
            "",
            "Costi parziali:",
            f" • Reagenti:               {costo_reagenti:.2f} b",
            f" • Core:                   {costo_core:.2f} b",
            f" • Resine:                 {costo_resine:.2f} b",
            f" • Carbonella:             {costo_carbonella:.2f} b",
            f" • Boccette:               {costo_boccette:.2f} b",
            "",
            f"{APP_NAME} v{APP_VERSION} — {APP_AUTHOR}",
            "Impostazioni e profili salvati automaticamente.",
        ]

        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, "\n".join(output_lines))
        text_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi: inserisci numeri validi!")


# =========================
#   GUI + SCROLL INTELLIGENTE
# =========================

root = tk.Tk()
root.title(f"{APP_NAME} ⚗️ v{APP_VERSION}")
root.geometry("760x580")
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
    inner_frame,
    text=f"{APP_NAME}",
    font=TITLE_FONT,
    fg=FG_TEXT,
    bg=BG_MAIN,
).pack(pady=8)

# --- PANNELLO PROFILO PREZZI ---
panel_prof, prof_inner = make_panel(inner_frame, "Profilo prezzi")

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
    bg="#742e2e",
    fg="white",
    font=LABEL_FONT,
    activebackground="#993737",
    activeforeground="white",
    relief="flat",
    padx=8,
    pady=4,
    cursor="hand2",
)
btn_delete_prof.grid(row=0, column=5, padx=4, pady=4)

panel_prof.pack(padx=10, pady=6, fill="x")


# --- PRODUZIONE ---
panel_prod, prod_inner = make_panel(inner_frame, "Produzione")

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
panel_price_direct, price_direct_inner = make_panel(inner_frame, "Prezzi diretti (in b)")

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
panel_bundle, bundle_inner = make_panel(inner_frame, "Quante unità ottieni con 1 b")

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

# --- BOTTONE CALCOLA ---
tk.Button(
    inner_frame,
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
    inner_frame,
    text="Totale: -    •    Per pozione: -",
    font=("Segoe UI", 11, "bold"),
    bg=BG_MAIN,
    fg=FG_TEXT,
)
label_preview.pack(pady=(0, 10))

# --- DETTAGLIO ---
panel_result = tk.Frame(inner_frame, bg=BG_PANEL)
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
    height=12,
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


# =========================
#   INIZIALIZZAZIONE PROFILI
# =========================

profiles = load_all_profiles()
combo_profile["values"] = list(profiles.keys())
if combo_profile["values"]:
    combo_profile.set(combo_profile["values"][0])  # pre-seleziona qualcosa di esistente


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
