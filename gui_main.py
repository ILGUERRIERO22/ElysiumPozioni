# gui_main.py

import tkinter as tk
from tkinter import ttk, messagebox

from config_app import (
    APP_NAME, APP_VERSION, APP_AUTHOR,
    BG_MAIN, BG_PANEL, BG_RESULT,
    FG_TEXT, FG_SUBTLE, ACCENT,
    DANGER_BG, DANGER_BG_ACTIVE,     # <--- AGGIUNGERE QUESTE
    TITLE_FONT, SECTION_FONT, LABEL_FONT, BUTTON_FONT, RESULT_FONT,
    CONFIG_FILE, PROFILES_FILE,
)



from calcolo_pozioni import calcola_pozioni
from calcolo_antidoti import calcola_antidoti as core_calcola_antidoti
from calcolo_revivify import calcola_revivify as core_calcola_revivify
from calcolo_extinguish import calcola_extinguish as core_calcola_extinguish
from calcolo_rune import (
    calcola_rune_diretto as core_rune_diretto,
    calcola_rune_inverso as core_rune_inverso,
)
from calcolo_elisir import calcola_elisir as core_calcola_elisir
from calcolo_rune import calcola_rune_diretto
from calcolo_velocita import calcola_pozione_velocita as core_calcola_velocita



import json
import os

# =========================
#   GESTIONE PROFILI (come prima, ma usando PROFILES_FILE)
# =========================

def ensure_profiles_file():
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
    ensure_profiles_file()
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Errore lettura profiles.json:", e)
        return {}

def save_all_profiles(profiles_dict):
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles_dict, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Errore scrittura profiles.json:", e)

# (qui puoi copiare pari pari apply_profile, save_profile, rename_profile, delete_profile
# dal tuo file originale, adattando solo dove servono variabili globali GUI)


# =========================
#   FUNZIONI UTILI INFO
# =========================

def show_info():
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
    mit_text = (
        "Licenza MIT\n\n"
        f"Copyright (c) 2025 {APP_AUTHOR}\n\n"
        "È consentito usare, copiare, modificare e distribuire questo software "
        "senza restrizioni, anche per uso commerciale, purché venga mantenuta "
        "questa nota di copyright e la presente licenza.\n\n"
        "IL SOFTWARE VIENE FORNITO \"COSÌ COM'È\", SENZA ALCUNA GARANZIA."
    )
    messagebox.showinfo("Licenza", mit_text)


# =========================
#   CLASSE APP (GUI)
# =========================

class ElysiumPozioniApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME} ⚗️ v{APP_VERSION}")
        self.root.geometry("760x620")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        # profili in memoria
        self.profiles = load_all_profiles()

        # costruiamo tutta la GUI
        self._build_menu()
        self._build_main_layout()
        self._build_tabs()

        # carica config (dopo aver creato i widget)
        self.load_config()

    # ---- Menu Info ----
    def _build_menu(self):
        menubar = tk.Menu(self.root, tearoff=0)
        menu_info = tk.Menu(menubar, tearoff=0, bg="white", fg="black")
        menu_info.add_command(label="Informazioni / Crediti", command=show_info)
        menu_info.add_command(label="Licenza", command=show_license)
        menubar.add_cascade(label="Info", menu=menu_info)
        self.root.config(menu=menubar)

    # ---- Canvas scrollabile + notebook ----
    def _build_main_layout(self):
        self.outer_canvas = tk.Canvas(self.root, bg=BG_MAIN, highlightthickness=0)
        self.outer_canvas.pack(side="left", fill="both", expand=True)

        main_scrollbar = tk.Scrollbar(
            self.root, orient="vertical", command=self.outer_canvas.yview
        )
        main_scrollbar.pack(side="right", fill="y")

        self.outer_canvas.configure(yscrollcommand=main_scrollbar.set)

        self.inner_frame = tk.Frame(self.outer_canvas, bg=BG_MAIN)
        self.outer_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        def on_configure(event):
            self.outer_canvas.configure(scrollregion=self.outer_canvas.bbox("all"))

        self.inner_frame.bind("<Configure>", on_configure)

        def _on_mousewheel_canvas(event):
            self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.outer_canvas.bind_all("<MouseWheel>", _on_mousewheel_canvas)

        # Notebook
        self.notebook = ttk.Notebook(self.inner_frame)
        self.tab_pozioni = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_antidoti = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_revivify = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_extinguish = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_rune = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_elisir = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_velocita = tk.Frame(self.notebook, bg=BG_MAIN)

        self.notebook.add(self.tab_pozioni, text="Pozioni di cura")
        self.notebook.add(self.tab_antidoti, text="Antidoti")
        self.notebook.add(self.tab_revivify, text="Revivify")
        self.notebook.add(self.tab_extinguish, text="Extinguish")
        self.notebook.add(self.tab_rune, text="Rune")
        self.notebook.add(self.tab_elisir, text="Elisir")
        self.notebook.add(self.tab_velocita, text="Velocità")
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)
        


    def make_panel(self, parent, title):
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

    # ---- Costruzione tab (qui incolli il tuo codice GUI) ----
        # ---- Costruzione tab (partiamo dalla tab Pozioni completa) ----
    def _build_tabs(self):
        # TITOLO
        tk.Label(
            self.tab_pozioni,
            text=f"{APP_NAME}",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- PANNELLO PROFILO PREZZI ---
        panel_prof, prof_inner = self.make_panel(self.tab_pozioni, "Profilo prezzi")

        tk.Label(
            prof_inner,
            text="Profilo prezzi:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        # combobox EDITABILE per poter scrivere / rinominare / creare nomi nuovi
        self.combo_profile = ttk.Combobox(
            prof_inner,
            width=16,
            font=LABEL_FONT,
        )  # non readonly apposta
        self.combo_profile.grid(row=0, column=1, padx=4, pady=4, sticky="w")

        self.btn_load_prof = tk.Button(
            prof_inner,
            text="Carica profilo",
            command=self.apply_profile,
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
        self.btn_load_prof.grid(row=0, column=2, padx=4, pady=4)

        self.btn_save_prof = tk.Button(
            prof_inner,
            text="Salva profilo",
            command=self.save_profile,
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
        self.btn_save_prof.grid(row=0, column=3, padx=4, pady=4)

        self.btn_rename_prof = tk.Button(
            prof_inner,
            text="Rinomina profilo",
            command=self.rename_profile,
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
        self.btn_rename_prof.grid(row=0, column=4, padx=4, pady=4)

        self.btn_delete_prof = tk.Button(
            prof_inner,
            text="Elimina profilo",
            command=self.delete_profile,
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
        self.btn_delete_prof.grid(row=0, column=5, padx=4, pady=4)

        panel_prof.pack(padx=10, pady=6, fill="x")

        # --- PRODUZIONE ---
        panel_prod, prod_inner = self.make_panel(self.tab_pozioni, "Produzione")

        tk.Label(
            prod_inner,
            text="Numero pozioni:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_pozioni = tk.Entry(
            prod_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_pozioni.grid(row=0, column=1, pady=4)

        tk.Label(
            prod_inner,
            text="Tipo reagente:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=4)

        self.combo_tier = ttk.Combobox(
            prod_inner,
            values=["T1", "T2", "T3"],
            width=10,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_tier.current(0)
        self.combo_tier.grid(row=1, column=1, pady=4)

        tk.Label(
            prod_inner,
            text="Calderone:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=4)

        self.combo_calderone = ttk.Combobox(
            prod_inner,
            values=["Terracotta", "Rame", "Ferro", "Oro", "Diamante"],
            width=12,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_calderone.current(0)
        self.combo_calderone.grid(row=2, column=1, pady=4)

        panel_prod.pack(padx=10, pady=6, fill="x")

        # --- PREZZI DIRETTI ---
        panel_price_direct, price_direct_inner = self.make_panel(
            self.tab_pozioni, "Prezzi diretti"
        )

        tk.Label(
            price_direct_inner,
            text="Reagente (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=3)

        self.entry_reagente = tk.Entry(
            price_direct_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_reagente.insert(0, "1.5")
        self.entry_reagente.grid(row=0, column=1, pady=3)

        tk.Label(
            price_direct_inner,
            text="Core fragment (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=3)

        self.entry_core = tk.Entry(
            price_direct_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_core.insert(0, "1.0")
        self.entry_core.grid(row=1, column=1, pady=3)

        tk.Label(
            price_direct_inner,
            text="Carbone (1 blocco):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=3)

        self.entry_carbone = tk.Entry(
            price_direct_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_carbone.insert(0, "1.5")
        self.entry_carbone.grid(row=2, column=1, pady=3)

        tk.Label(
            price_direct_inner,
            text="(1 blocco = 12 carbonella)",
            font=("Segoe UI", 8),
            bg=BG_PANEL,
            fg=FG_SUBTLE,
        ).grid(row=2, column=2, sticky="w", padx=4)

        panel_price_direct.pack(padx=10, pady=6, fill="x")

        # --- QUANTE UNITÀ OTTIENI CON 1 b ---
        panel_bundle, bundle_inner = self.make_panel(
            self.tab_pozioni, "Quante unità ottieni con 1 b"
        )

        tk.Label(
            bundle_inner,
            text="Verdure per 1 b:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=3)

        self.entry_verdure_per_b = tk.Entry(
            bundle_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_verdure_per_b.insert(0, "3")
        self.entry_verdure_per_b.grid(row=0, column=1, pady=3)

        tk.Label(
            bundle_inner,
            text="Vasetti per 1 b:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=3)

        self.entry_vasetti_per_b = tk.Entry(
            bundle_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vasetti_per_b.insert(0, "15")
        self.entry_vasetti_per_b.grid(row=1, column=1, pady=3)

        

        tk.Label(
            bundle_inner,
            text="Boccette per 1 b:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=3)

        self.entry_boccette_per_b = tk.Entry(
            bundle_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_boccette_per_b.insert(0, "14")
        self.entry_boccette_per_b.grid(row=2, column=1, pady=3)

        self.entry_verdure_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())
        self.entry_vasetti_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())


        panel_bundle.pack(padx=10, pady=6, fill="x")


        panel_bundle.pack(padx=10, pady=6, fill="x")

        # --- VENDITA / PROFITTO ---
        panel_sale, sale_inner = self.make_panel(self.tab_pozioni, "Vendita")

        tk.Label(
            sale_inner,
            text="Prezzo di vendita per pozione (b):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_prezzo_vendita = tk.Entry(
            sale_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_prezzo_vendita.insert(0, "")
        self.entry_prezzo_vendita.grid(row=0, column=1, pady=4, sticky="w")

        tk.Label(
            sale_inner,
            text="Sconto al cliente (%):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=4)

        self.entry_sconto_perc = tk.Entry(
            sale_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_sconto_perc.insert(0, "0")
        self.entry_sconto_perc.grid(row=2, column=1, pady=4, sticky="w")

        panel_sale.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE CALCOLA ---
        tk.Button(
            self.tab_pozioni,
            text="CALCOLA",
            command=self.do_calcola_pozioni,
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
        self.label_preview = tk.Label(
            self.tab_pozioni,
            text="Totale: -    •    Per pozione: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        panel_result = tk.Frame(self.tab_pozioni, bg=BG_PANEL)
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

        self.text_result = tk.Text(
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
        self.text_result.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_result.yview)

        # Inizializza combobox profili
        self.combo_profile["values"] = list(self.profiles.keys())
        if self.combo_profile["values"]:
            self.combo_profile.set(self.combo_profile["values"][0])

        self._build_tab_antidoti()
        self._build_tab_revivify()
        self._build_tab_extinguish()
        self._build_tab_elisir()
        self._build_tab_rune()
        self._build_tab_velocita()





    def save_config(self):
        data = {
            # --- Pozioni ---
            "num_pozioni": self.entry_pozioni.get(),
            "tier": self.combo_tier.get(),
            "calderone": self.combo_calderone.get(),
            "prezzo_reagente": self.entry_reagente.get(),
            "prezzo_core": self.entry_core.get(),
            "prezzo_carbone": self.entry_carbone.get(),
            "verdure_per_1b": self.entry_verdure_per_b.get(),
            "vasetti_per_1b": self.entry_vasetti_per_b.get(),
            "boccette_per_1b": self.entry_boccette_per_b.get(),
            "prezzo_vendita_pozioni": self.entry_prezzo_vendita.get(),
            "sconto_pozioni": self.entry_sconto_perc.get(),

            # --- Antidoti ---
            "prezzo_brim": self.entry_brim.get(),
            "prezzo_rotten": self.entry_rotten.get(),
            "prezzo_revival": self.entry_revival.get(),
            "prezzo_vendita_antidoti": self.entry_ant_prezzo_vendita.get() if hasattr(self, "entry_ant_prezzo_vendita") else "",

            # --- Revivify ---
            "rev_num": self.entry_rev_num.get() if hasattr(self, "entry_rev_num") else "",
            "rev_prezzo_vendita": self.entry_rev_prezzo_vendita.get() if hasattr(self, "entry_rev_prezzo_vendita") else "",

            # --- Extinguish ---
            "ext_num": self.entry_ext_num.get() if hasattr(self, "entry_ext_num") else "",
            "ext_quartz": self.entry_ext_quartz.get() if hasattr(self, "entry_ext_quartz") else "",
            "ext_prezzo_vendita": self.entry_ext_prezzo_vendita.get() if hasattr(self, "entry_ext_prezzo_vendita") else "",

            # --- Elisir ---
            "elisir_num": self.entry_el_num.get() if hasattr(self, "entry_el_num") else "",
            "elisir_tipo": self.combo_el_tipo.get() if hasattr(self, "combo_el_tipo") else "",
            "elisir_spidereye": self.entry_spidereye.get() if hasattr(self, "entry_spidereye") else "",
            "elisir_membrana": self.entry_membrana.get() if hasattr(self, "entry_membrana") else "",
            "elisir_slime": self.entry_slime.get() if hasattr(self, "entry_slime") else "",
            "elisir_lost_soul": self.entry_lost_soul.get() if hasattr(self, "entry_lost_soul") else "",
            "elisir_price_tin": self.entry_price_tin.get() if hasattr(self, "entry_price_tin") else "",
            "elisir_price_cu": self.entry_price_cu.get() if hasattr(self, "entry_price_cu") else "",
            "elisir_price_fe": self.entry_price_fe.get() if hasattr(self, "entry_price_fe") else "",
            "elisir_price_au": self.entry_price_au.get() if hasattr(self, "entry_price_au") else "",
            "elisir_price_dia": self.entry_price_dia.get() if hasattr(self, "entry_price_dia") else "",
            "elisir_prezzo_vendita": self.entry_el_prezzo.get() if hasattr(self, "entry_el_prezzo") else "",

            #velocità
            "vel_num": self.entry_vel_num.get() if hasattr(self, "entry_vel_num") else "",
            "vel_tipo": self.combo_vel_tipo.get() if hasattr(self, "combo_vel_tipo") else "",
            "vel_lapis": self.entry_vel_lapis.get() if hasattr(self, "entry_vel_lapis") else "",
            "vel_zucchero": self.entry_vel_zucchero.get() if hasattr(self, "entry_vel_zucchero") else "",
            "vel_blaze": self.entry_vel_blaze.get() if hasattr(self, "entry_vel_blaze") else "",
            "vel_prezzo_vendita": self.entry_vel_prezzo.get() if hasattr(self, "entry_vel_prezzo") else "",


            # --- Rune ---
            "rune_tipo": self.combo_rune_tipo.get() if hasattr(self, "combo_rune_tipo") else "",
            "rune_pepite": {
                met: entry.get()
                for met, entry in getattr(self, "entry_rune_pepite", {}).items()
            },
        }

        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Errore salvataggio config:", e)


    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("Errore lettura config:", e)
            return

        # --- Pozioni ---
        if "num_pozioni" in data:
            self.entry_pozioni.delete(0, tk.END)
            self.entry_pozioni.insert(0, data["num_pozioni"])

        if "tier" in data:
            self.combo_tier.set(data["tier"])

        if "calderone" in data:
            self.combo_calderone.set(data["calderone"])

        for key, widget_name in [
            ("prezzo_reagente", "entry_reagente"),
            ("prezzo_core", "entry_core"),
            ("prezzo_carbone", "entry_carbone"),
            ("verdure_per_1b", "entry_verdure_per_b"),
            ("vasetti_per_1b", "entry_vasetti_per_b"),
            ("boccette_per_1b", "entry_boccette_per_b"),
            ("prezzo_vendita_pozioni", "entry_prezzo_vendita"),
            ("sconto_pozioni", "entry_sconto_perc"),
        ]:
            if key in data and hasattr(self, widget_name):
                w = getattr(self, widget_name)
                w.delete(0, tk.END)
                w.insert(0, data[key])

        # --- Antidoti ---
        for key, widget_name in [
            ("prezzo_brim", "entry_brim"),
            ("prezzo_rotten", "entry_rotten"),
            ("prezzo_revival", "entry_revival"),
        ]:
            if key in data and hasattr(self, widget_name):
                w = getattr(self, widget_name)
                w.delete(0, tk.END)
                w.insert(0, data[key])

        if "prezzo_vendita_antidoti" in data and hasattr(self, "entry_ant_prezzo_vendita"):
            self.entry_ant_prezzo_vendita.delete(0, tk.END)
            self.entry_ant_prezzo_vendita.insert(0, data["prezzo_vendita_antidoti"])

        # --- Revivify ---
        if "rev_num" in data and hasattr(self, "entry_rev_num"):
            self.entry_rev_num.delete(0, tk.END)
            self.entry_rev_num.insert(0, data["rev_num"])

        if "rev_prezzo_vendita" in data and hasattr(self, "entry_rev_prezzo_vendita"):
            self.entry_rev_prezzo_vendita.delete(0, tk.END)
            self.entry_rev_prezzo_vendita.insert(0, data["rev_prezzo_vendita"])

        # --- Extinguish ---
        if "ext_num" in data and hasattr(self, "entry_ext_num"):
            self.entry_ext_num.delete(0, tk.END)
            self.entry_ext_num.insert(0, data["ext_num"])

        if "ext_quartz" in data and hasattr(self, "entry_ext_quartz"):
            self.entry_ext_quartz.delete(0, tk.END)
            self.entry_ext_quartz.insert(0, data["ext_quartz"])

        if "ext_prezzo_vendita" in data and hasattr(self, "entry_ext_prezzo_vendita"):
            self.entry_ext_prezzo_vendita.delete(0, tk.END)
            self.entry_ext_prezzo_vendita.insert(0, data["ext_prezzo_vendita"])

        # --- Elisir ---
        if "elisir_num" in data and hasattr(self, "entry_el_num"):
            self.entry_el_num.delete(0, tk.END)
            self.entry_el_num.insert(0, data["elisir_num"])

        if "elisir_tipo" in data and hasattr(self, "combo_el_tipo"):
            self.combo_el_tipo.set(data["elisir_tipo"])

        for key, widget_name in [
            ("elisir_spidereye", "entry_spidereye"),
            ("elisir_membrana", "entry_membrana"),
            ("elisir_slime", "entry_slime"),
            ("elisir_lost_soul", "entry_lost_soul"),
            ("elisir_price_tin", "entry_price_tin"),
            ("elisir_price_cu", "entry_price_cu"),
            ("elisir_price_fe", "entry_price_fe"),
            ("elisir_price_au", "entry_price_au"),
            ("elisir_price_dia", "entry_price_dia"),
            ("elisir_prezzo_vendita", "entry_el_prezzo"),
        ]:
            if key in data and hasattr(self, widget_name):
                w = getattr(self, widget_name)
                w.delete(0, tk.END)
                w.insert(0, data[key])

        # --- Rune ---
        if "rune_tipo" in data and hasattr(self, "combo_rune_tipo"):
            self.combo_rune_tipo.set(data["rune_tipo"])

        if "rune_pepite" in data and hasattr(self, "entry_rune_pepite"):
            for met, val in data["rune_pepite"].items():
                if met in self.entry_rune_pepite:
                    e = self.entry_rune_pepite[met]
                    e.delete(0, tk.END)
                    e.insert(0, val)

        # --- Velocità ---
        if "vel_num" in data and hasattr(self, "entry_vel_num"):
            self.entry_vel_num.delete(0, tk.END)
            self.entry_vel_num.insert(0, data["vel_num"])

        if "vel_tipo" in data and hasattr(self, "combo_vel_tipo"):
            self.combo_vel_tipo.set(data["vel_tipo"])

        for key, widget_name in [
            ("vel_lapis", "entry_vel_lapis"),
            ("vel_zucchero", "entry_vel_zucchero"),
            ("vel_blaze", "entry_vel_blaze"),
            ("vel_prezzo_vendita", "entry_vel_prezzo"),
        ]:
            if key in data and hasattr(self, widget_name):
                w = getattr(self, widget_name)
                w.delete(0, tk.END)
                w.insert(0, data[key])


        # aggiorna il brim label e la resina, giusto per stare sicuri
        try:
            self._aggiorna_resina_da_pozioni()
        except Exception:
            pass
        try:
            self._aggiorna_brim_elisir()
        except Exception:
            pass


    # =========================
    #   CALLBACK DI CALCOLO (wrappano i moduli calcolo_*.py)
    # =========================


        # =========================
    #   GESTIONE PROFILI (metodi di istanza)
    # =========================

    def _build_tab_antidoti(self):
        # TITOLO
        tk.Label(
            self.tab_antidoti,
            text="Antidoti - Calcolo costi e profitti",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- ANTIDOTI: PRODUZIONE ---
        ant_prod, ant_prod_inner = self.make_panel(self.tab_antidoti, "Produzione (Antidoti)")

        tk.Label(
            ant_prod_inner,
            text="Numero antidoti:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_ant_num = tk.Entry(
            ant_prod_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_ant_num.grid(row=0, column=1, pady=4)

        tk.Label(
            ant_prod_inner,
            text="Calderone:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=4)

        self.combo_ant_calderone = ttk.Combobox(
            ant_prod_inner,
            values=["Terracotta", "Ferro"],
            width=12,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_ant_calderone.current(0)
        self.combo_ant_calderone.grid(row=1, column=1, pady=4)

        ant_prod.pack(padx=10, pady=6, fill="x")

        # --- ANTIDOTI: PREZZI DIRETTI ---
        ant_price, ant_price_inner = self.make_panel(
            self.tab_antidoti,
            "Prezzi diretti (Antidoti)",
        )

        tk.Label(
            ant_price_inner,
            text="Brim powder (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=3)

        self.entry_brim = tk.Entry(
            ant_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_brim.insert(0, "1.0")
        self.entry_brim.grid(row=0, column=1, pady=3)

        tk.Label(
            ant_price_inner,
            text="Carne marcia (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=3)

        self.entry_rotten = tk.Entry(
            ant_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_rotten.insert(0, "1.0")
        self.entry_rotten.grid(row=1, column=1, pady=3)

        tk.Label(
            ant_price_inner,
            text="Revival star (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=3)

        self.entry_revival = tk.Entry(
            ant_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_revival.insert(0, "2.0")
        self.entry_revival.grid(row=2, column=1, pady=3)

        ant_price.pack(padx=10, pady=6, fill="x")

        tk.Label(
            ant_price_inner,
            text="Resina (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=3, column=0, sticky="e", padx=4, pady=3)

        # Valore SOLO LETTURA, aggiornato automaticamente dai parametri delle pozioni
        self.resina_var = tk.StringVar()

        self.entry_resina = tk.Entry(
            ant_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",          # sfondo scuro
            fg=FG_TEXT,           # testo chiaro
            disabledbackground="#3a3a3a",  # colore sfondo quando disabilitato
            disabledforeground=FG_TEXT,   # colore testo quando disabilitato
            relief="flat",
            textvariable=self.resina_var,
            state="disabled",     # <--- BLOCCA IL CAMPO MA RISPETTA I COLORI
        )
        self.entry_resina.grid(row=3, column=1, pady=3)




        # --- VENDITA / PROFITTO ---
        ant_sale, ant_sale_inner = self.make_panel(self.tab_antidoti, "Vendita")

        tk.Label(
            ant_sale_inner,
            text="Prezzo vendita per antidoto (b):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_ant_prezzo = tk.Entry(
            ant_sale_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_ant_prezzo.insert(0, "")
        self.entry_ant_prezzo.grid(row=0, column=1, pady=4)

        ant_sale.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE & PREVIEW ---
        tk.Button(
            self.tab_antidoti,
            text="CALCOLA ANTIDOTI",
            command=self.do_calcola_antidoti,
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

        self.label_ant_preview = tk.Label(
            self.tab_antidoti,
            text="Totale: -    •    Per antidoto: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_ant_preview.pack(pady=(0, 10))

        ant_panel_result = tk.Frame(self.tab_antidoti, bg=BG_PANEL)
        ant_panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        tk.Label(
            ant_panel_result,
            text="Dettaglio",
            font=SECTION_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))

        ant_inner_result = tk.Frame(ant_panel_result, bg=BG_PANEL)
        ant_inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ant_scrollbar = tk.Scrollbar(ant_inner_result)
        ant_scrollbar.pack(side="right", fill="y")

        self.text_ant_result = tk.Text(
            ant_inner_result,
            height=14,
            font=RESULT_FONT,
            state="disabled",
            wrap="word",
            yscrollcommand=ant_scrollbar.set,
            bg=BG_RESULT,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.text_ant_result.pack(fill="both", expand=True)
        ant_scrollbar.config(command=self.text_ant_result.yview)

        # Calcola subito il costo resina all'avvio, usando i valori di default delle pozioni
        self._aggiorna_resina_da_pozioni()




    def _aggiorna_resina_da_pozioni(self):
        """Calcola il costo di 1 resina usando i parametri delle pozioni e lo mostra nel campo resina."""
        try:
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())

            if verdure_per_1b <= 0 or vasetti_per_1b <= 0:
                self.resina_var.set("")
                return

            costo_verdura = 1.0 / verdure_per_1b
            costo_vasetto = 1.0 / vasetti_per_1b

            # stessa formula che usavi prima:
            # costo_resina = (2 verdure + 1 vasetto) / 2
            costo_resina = (2.0 * costo_verdura + costo_vasetto) / 2.0

            self.resina_var.set(f"{costo_resina:.2f}")
        except ValueError:
            # se i campi verdure/vasetti non sono numerici, lascio vuoto
            self.resina_var.set("")


    def _aggiorna_brim_elisir(self):
        """Mostra nella tab Elisir il prezzo del Brim preso dalla tab Antidoti."""
        if not hasattr(self, "label_el_brim"):
            return
        try:
            val = self.entry_brim.get()
        except Exception:
            val = ""
        self.label_el_brim.config(text=val or "-")



    def do_calcola_antidoti(self):
        try:
            self._aggiorna_resina_da_pozioni()
            # --- INPUT DI BASE ---
            num = float(self.entry_ant_num.get())
            tipo = self.combo_ant_calderone.get()  # "Terracotta" / "Ferro"

            # --- PREZZI GLOBALI dalla tab Pozioni ---
            prezzo_carbone   = float(self.entry_carbone.get())          # b per 1 blocco (12 carbonella)
            boccette_per_1b  = float(self.entry_boccette_per_b.get())
            vasetti_per_1b   = float(self.entry_vasetti_per_b.get())
            verdure_per_1b   = float(self.entry_verdure_per_b.get())

            # --- PREZZI SPECIFICI ANTIDOTI ---
            prezzo_brim    = float(self.entry_brim.get())        # 1 brim powder
            prezzo_rotten  = float(self.entry_rotten.get())      # 1 carne marcia
            prezzo_revival = float(self.entry_revival.get())     # 1 revival star

            # --- PREZZO DI VENDITA (facoltativo) ---
            try:
                prezzo_vendita = float(self.entry_ant_prezzo.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_antidoti(
                num,
                tipo,
                prezzo_carbone,
                boccette_per_1b,
                vasetti_per_1b,
                verdure_per_1b,
                prezzo_brim,
                prezzo_rotten,
                prezzo_revival,
                prezzo_vendita=prezzo_vendita,
            )

            self.label_ant_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_ant_result.config(state="normal")
            self.text_ant_result.delete("1.0", tk.END)
            self.text_ant_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_ant_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla i campi degli antidoti: inserisci numeri validi.",
            )


    def _build_tab_revivify(self):
        tk.Label(
            self.tab_revivify,
            text="Revivify - Calderone in rame",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- PRODUZIONE ---
        panel_prod, prod_inner = self.make_panel(self.tab_revivify, "Produzione (Revivify)")

        tk.Label(
            prod_inner,
            text="Numero Revivify:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_rev_num = tk.Entry(
            prod_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_rev_num.grid(row=0, column=1, pady=4)

        panel_prod.pack(padx=10, pady=6, fill="x")

        # --- VENDITA ---
        panel_sale, sale_inner = self.make_panel(self.tab_revivify, "Vendita")

        tk.Label(
            sale_inner,
            text="Prezzo vendita per Revivify (b):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_rev_prezzo_vendita = tk.Entry(
            sale_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_rev_prezzo_vendita.grid(row=0, column=1, pady=4, sticky="w")

        panel_sale.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE ---
        tk.Button(
            self.tab_revivify,
            text="CALCOLA REVIVIFY",
            command=self.do_calcola_revivify,
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

        # --- PREVIEW ---
        self.label_rev_preview = tk.Label(
            self.tab_revivify,
            text="Totale: -    •    Per Revivify: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_rev_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        panel_result = tk.Frame(self.tab_revivify, bg=BG_PANEL)
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

        self.text_rev_result = tk.Text(
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
        self.text_rev_result.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_rev_result.yview)



    def do_calcola_revivify(self):
        try:
            num = float(self.entry_rev_num.get())

            # --- valori condivisi dalle pozioni ---
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())

            # --- prezzo revival star già impostato in Antidoti ---
            prezzo_revival = float(self.entry_revival.get())

            # --- prezzo di vendita (facoltativo) ---
            try:
                prezzo_vendita = float(self.entry_rev_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_revivify(
                num=num,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_revival=prezzo_revival,
                prezzo_vendita=prezzo_vendita,
            )

            self.label_rev_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_rev_result.config(state="normal")
            self.text_rev_result.delete("1.0", tk.END)
            self.text_rev_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_rev_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla i campi Revivify: inserisci numeri validi.",
            )


    def _build_tab_extinguish(self):
        tk.Label(
            self.tab_extinguish,
            text="Extinguish - Calderone in rame",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- PRODUZIONE ---
        panel_prod, prod_inner = self.make_panel(self.tab_extinguish, "Produzione (Extinguish)")

        tk.Label(
            prod_inner,
            text="Numero Extinguish:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_ext_num = tk.Entry(
            prod_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_ext_num.grid(row=0, column=1, pady=4)

        panel_prod.pack(padx=10, pady=6, fill="x")

        # --- PREZZO QUARZO ---
        panel_price, price_inner = self.make_panel(self.tab_extinguish, "Prezzo quarzo")

        tk.Label(
            price_inner,
            text="Quarzo (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_ext_quartz = tk.Entry(
            price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_ext_quartz.insert(0, "1.0")
        self.entry_ext_quartz.grid(row=0, column=1, pady=4)

        panel_price.pack(padx=10, pady=6, fill="x")

        # --- VENDITA ---
        panel_sale, sale_inner = self.make_panel(self.tab_extinguish, "Vendita")

        tk.Label(
            sale_inner,
            text="Prezzo vendita per Extinguish (b):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_ext_prezzo_vendita = tk.Entry(
            sale_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_ext_prezzo_vendita.grid(row=0, column=1, pady=4, sticky="w")

        panel_sale.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE ---
        tk.Button(
            self.tab_extinguish,
            text="CALCOLA EXTINGUISH",
            command=self.do_calcola_extinguish,
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

        # --- PREVIEW ---
        self.label_ext_preview = tk.Label(
            self.tab_extinguish,
            text="Totale: -    •    Per Extinguish: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_ext_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        panel_result = tk.Frame(self.tab_extinguish, bg=BG_PANEL)
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

        self.text_ext_result = tk.Text(
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
        self.text_ext_result.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_ext_result.yview)

    def do_calcola_extinguish(self):
        try:
            num = float(self.entry_ext_num.get())

            # valori condivisi dalle pozioni
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())

            # prezzo quarzo solo per Extinguish
            prezzo_quartz = float(self.entry_ext_quartz.get())

            # prezzo di vendita (facoltativo)
            try:
                prezzo_vendita = float(self.entry_ext_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_extinguish(
                num=num,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_quartz=prezzo_quartz,
                prezzo_vendita=prezzo_vendita,
            )

            self.label_ext_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_ext_result.config(state="normal")
            self.text_ext_result.delete("1.0", tk.END)
            self.text_ext_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_ext_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla i campi Extinguish: inserisci numeri validi.",
            )


    def _build_tab_elisir(self):
        tk.Label(
            self.tab_elisir,
            text="Elisir di cura",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- PRODUZIONE ---
        el_prod, el_prod_inner = self.make_panel(self.tab_elisir, "Produzione (Elisir)")

        tk.Label(
            el_prod_inner,
            text="Numero elisir:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_el_num = tk.Entry(
            el_prod_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_el_num.grid(row=0, column=1, pady=4)

        tk.Label(
            el_prod_inner,
            text="Tipo elisir:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=4)

        self.combo_el_tipo = ttk.Combobox(
            el_prod_inner,
            values=["Minor mending", "Inferior mending", "Lesser mending", "Medium mending", "Greater mending"],
            width=18,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_el_tipo.current(0)
        self.combo_el_tipo.grid(row=1, column=1, pady=4, sticky="w")

        el_prod.pack(padx=10, pady=6, fill="x")

        # --- PREZZI SPECIFICI ---
        el_price, el_price_inner = self.make_panel(
            self.tab_elisir,
            "Prezzi ingredienti speciali (in b)"
        )

        # Brim powder: solo label che legge dalla tab Antidoti
        tk.Label(
            el_price_inner,
            text="Brim powder (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=3)

        self.label_el_brim = tk.Label(
            el_price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        )
        self.label_el_brim.grid(row=0, column=1, sticky="w", padx=4, pady=3)

        tk.Label(
            el_price_inner,
            text="(usa il prezzo Brim dalla tab Antidoti)",
            font=("Segoe UI", 8),
            bg=BG_PANEL,
            fg=FG_SUBTLE,
        ).grid(row=0, column=2, sticky="w", padx=4)

        # Occhio di ragno
        tk.Label(
            el_price_inner,
            text="Occhio di ragno (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=3)

        self.entry_spidereye = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_spidereye.insert(0, "1.0")
        self.entry_spidereye.grid(row=1, column=1, pady=3)

        # Membrana di Phantom
        tk.Label(
            el_price_inner,
            text="Membrana di Phantom (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=3)

        self.entry_membrana = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_membrana.insert(0, "1.0")
        self.entry_membrana.grid(row=2, column=1, pady=3)

        # Slimeball
        tk.Label(
            el_price_inner,
            text="Slimeball (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=3, column=0, sticky="e", padx=4, pady=3)

        self.entry_slime = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_slime.insert(0, "1.0")
        self.entry_slime.grid(row=3, column=1, pady=3)

        # Lost soul
        tk.Label(
            el_price_inner,
            text="Lost soul (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=4, column=0, sticky="e", padx=4, pady=3)

        self.entry_lost_soul = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_lost_soul.insert(0, "1.0")
        self.entry_lost_soul.grid(row=4, column=1, pady=3)


        # Prezzi lingotti (per pepite)
        tk.Label(
            el_price_inner,
            text="Tin (1 lingotto):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=5, column=0, sticky="e", padx=4, pady=3)
        self.entry_price_tin = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_price_tin.grid(row=5, column=1, pady=3)

        tk.Label(
            el_price_inner,
            text="Rame (1 lingotto):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=6, column=0, sticky="e", padx=4, pady=3)
        self.entry_price_cu = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_price_cu.grid(row=6, column=1, pady=3)

        tk.Label(
            el_price_inner,
            text="Ferro (1 lingotto):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=7, column=0, sticky="e", padx=4, pady=3)
        self.entry_price_fe = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_price_fe.grid(row=7, column=1, pady=3)

        tk.Label(
            el_price_inner,
            text="Oro (1 lingotto):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=8, column=0, sticky="e", padx=4, pady=3)
        self.entry_price_au = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_price_au.grid(row=8, column=1, pady=3)

        el_price.pack(padx=10, pady=6, fill="x")

        tk.Label(
            el_price_inner,
            text="Diamante (1 lingotto):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=9, column=0, sticky="e", padx=4, pady=3)

        self.entry_price_dia = tk.Entry(
            el_price_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_price_dia.grid(row=9, column=1, pady=3)


        # --- VENDITA ---
        el_sell, el_sell_inner = self.make_panel(self.tab_elisir, "Vendita / Profitto")

        tk.Label(
            el_sell_inner,
            text="Prezzo vendita (b / elisir):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_el_prezzo = tk.Entry(
            el_sell_inner,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_el_prezzo.grid(row=0, column=1, pady=4, sticky="w")

        el_sell.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE ---
        tk.Button(
            self.tab_elisir,
            text="CALCOLA ELISIR",
            command=self.do_calcola_elisir,
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

        # --- PREVIEW ---
        self.label_el_preview = tk.Label(
            self.tab_elisir,
            text="Totale: -    •    Per elisir: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_el_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        el_det = tk.Frame(self.tab_elisir, bg=BG_PANEL)
        el_det.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        tk.Label(
            el_det,
            text="Dettaglio",
            font=SECTION_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))

        el_det_inner = tk.Frame(el_det, bg=BG_PANEL)
        el_det_inner.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        el_scrollbar = tk.Scrollbar(el_det_inner)
        el_scrollbar.pack(side="right", fill="y")

        self.text_el_result = tk.Text(
            el_det_inner,
            height=14,
            font=RESULT_FONT,
            state="disabled",
            wrap="word",
            yscrollcommand=el_scrollbar.set,
            bg=BG_RESULT,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.text_el_result.pack(fill="both", expand=True)
        el_scrollbar.config(command=self.text_el_result.yview)

        # inizializza il label del Brim
        try:
            self._aggiorna_brim_elisir()
            self.entry_brim.bind("<KeyRelease>", lambda e: self._aggiorna_brim_elisir())
            self.entry_brim.bind("<FocusOut>",  lambda e: self._aggiorna_brim_elisir())
        except AttributeError:
            # nel caso in cui per qualche motivo entry_brim non esista ancora
            pass

    def do_calcola_elisir(self):
        try:
            num = float(self.entry_el_num.get())
            tipo = self.combo_el_tipo.get()

            # Prezzi globali (tab Pozioni)
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            vasetti_per_1b  = float(self.entry_vasetti_per_b.get())
            verdure_per_1b  = float(self.entry_verdure_per_b.get())

            # Prezzo Brim dalla tab Antidoti
            prezzo_brim = float(self.entry_brim.get())

            # Prezzi speciali Elisir
            prezzo_spidereye = float(self.entry_spidereye.get())
            prezzo_membrana  = float(self.entry_membrana.get())
            prezzo_slime     = float(self.entry_slime.get())
            prezzo_lost_soul = float(self.entry_lost_soul.get())

            # Prezzi lingotti (possono anche essere vuoti -> 0)
            price_tin = float(self.entry_price_tin.get() or "0")
            price_cu  = float(self.entry_price_cu.get()  or "0")
            price_fe  = float(self.entry_price_fe.get()  or "0")
            price_au  = float(self.entry_price_au.get()  or "0")
            price_dia = float(self.entry_price_dia.get() or "0")

            try:
                prezzo_vendita = float(self.entry_el_prezzo.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_elisir(
                num=num,
                tipo=tipo,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                vasetti_per_1b=vasetti_per_1b,
                verdure_per_1b=verdure_per_1b,
                prezzo_brim=prezzo_brim,
                prezzo_spidereye=prezzo_spidereye,
                prezzo_membrana=prezzo_membrana,
                prezzo_slime=prezzo_slime,
                prezzo_lost_soul=prezzo_lost_soul,
                price_tin=price_tin,
                price_cu=price_cu,
                price_fe=price_fe,
                price_au=price_au,
                price_dia=price_dia,
                prezzo_vendita=prezzo_vendita,
            )

            self.label_el_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_el_result.config(state="normal")
            self.text_el_result.delete("1.0", tk.END)
            self.text_el_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_el_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla i campi degli elisir: inserisci numeri validi.",
            )

    def _build_tab_rune(self):
        # TITOLO
        tk.Label(
            self.tab_rune,
            text="Calcolo Rune (Altare delle rune)",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- SCELTA TIPO RUNE ---
        panel_tipo, inner_tipo = self.make_panel(self.tab_rune, "Tipo di rune")

        tk.Label(
            inner_tipo,
            text="Tipo rune:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.combo_rune_tipo = ttk.Combobox(
            inner_tipo,
            values=["Maghi", "Bardi"],
            width=12,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_rune_tipo.current(0)
        self.combo_rune_tipo.grid(row=0, column=1, pady=4, sticky="w")

        panel_tipo.pack(padx=10, pady=6, fill="x")

        # --- QUANTE PEPITE PER METALLO ---
        panel_pepite, inner_pepite = self.make_panel(
            self.tab_rune, "Pepite disponibili (per metallo)"
        )

        # righe: Tin, Rame, Ferro, Oro, Argento
        metals = ["Tin", "Rame", "Ferro", "Oro", "Argento"]
        self.entry_rune_pepite = {}  # dict: metallo -> Entry

        for r, met in enumerate(metals):
            tk.Label(
                inner_pepite,
                text=f"{met} (pep):",
                font=LABEL_FONT,
                bg=BG_PANEL,
                fg=FG_TEXT,
            ).grid(row=r, column=0, sticky="e", padx=4, pady=3)

            e = tk.Entry(
                inner_pepite,
                width=10,
                font=LABEL_FONT,
                bg="#3a3a3a",
                fg=FG_TEXT,
                insertbackground=FG_TEXT,
                relief="flat",
            )
            e.insert(0, "0")
            e.grid(row=r, column=1, pady=3, sticky="w")

            self.entry_rune_pepite[met] = e

        panel_pepite.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE CALCOLO ---
        tk.Button(
            self.tab_rune,
            text="CALCOLA RUNE",
            command=self.do_calcola_rune,
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

        # --- PREVIEW ---
        self.label_rune_preview = tk.Label(
            self.tab_rune,
            text="Totale rune: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_rune_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        panel_result = tk.Frame(self.tab_rune, bg=BG_PANEL)
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

        rune_scrollbar = tk.Scrollbar(inner_result)
        rune_scrollbar.pack(side="right", fill="y")

        self.text_rune_result = tk.Text(
            inner_result,
            height=14,
            font=RESULT_FONT,
            state="disabled",
            wrap="word",
            yscrollcommand=rune_scrollbar.set,
            bg=BG_RESULT,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.text_rune_result.pack(fill="both", expand=True)
        rune_scrollbar.config(command=self.text_rune_result.yview)


    def do_calcola_rune(self):
        try:
            tipo = self.combo_rune_tipo.get().strip() or "Maghi"

            # Leggi tutte le pepite
            q_pepite = {}
            for met, entry in self.entry_rune_pepite.items():
                txt = entry.get().strip()
                if not txt:
                    val = 0.0
                else:
                    val = float(txt.replace(",", "."))
                q_pepite[met] = val

            # Usa solo il calcolo diretto (quello inverso non è ancora implementato)
            result = core_rune_diretto(tipo, q_pepite)

            self.label_rune_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_rune_result.config(state="normal")
            self.text_rune_result.delete("1.0", tk.END)
            self.text_rune_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_rune_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla le quantità di pepite: inserisci solo numeri.",
            )
        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Si è verificato un errore durante il calcolo delle rune:\n{e}",
            )

    def _build_tab_velocita(self):
        tk.Label(
            self.tab_velocita,
            text="Pozioni di Velocità",
            font=TITLE_FONT,
            fg=FG_TEXT,
            bg=BG_MAIN,
        ).pack(pady=8)

        # --- PRODUZIONE ---
        panel_prod, inner_prod = self.make_panel(self.tab_velocita, "Produzione")

        tk.Label(
            inner_prod,
            text="Numero pozioni:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_vel_num = tk.Entry(
            inner_prod,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vel_num.grid(row=0, column=1, pady=4)

        tk.Label(
            inner_prod,
            text="Tipo pozione:",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=4)

        self.combo_vel_tipo = ttk.Combobox(
            inner_prod,
            values=["Velocità I", "Velocità II"],
            width=14,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_vel_tipo.current(0)
        self.combo_vel_tipo.grid(row=1, column=1, pady=4, sticky="w")

        panel_prod.pack(padx=10, pady=6, fill="x")

        # --- PREZZI INGREDIENTI ---
        panel_price, inner_price = self.make_panel(
            self.tab_velocita, "Prezzi ingredienti (in b)"
        )

        tk.Label(
            inner_price,
            text="Lapis (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=3)

        self.entry_vel_lapis = tk.Entry(
            inner_price,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vel_lapis.insert(0, "1.0")
        self.entry_vel_lapis.grid(row=0, column=1, pady=3)

        tk.Label(
            inner_price,
            text="Zucchero (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=4, pady=3)

        self.entry_vel_zucchero = tk.Entry(
            inner_price,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vel_zucchero.insert(0, "1.0")
        self.entry_vel_zucchero.grid(row=1, column=1, pady=3)

        tk.Label(
            inner_price,
            text="Blaze (1x):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=4, pady=3)

        self.entry_vel_blaze = tk.Entry(
            inner_price,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vel_blaze.insert(0, "1.0")
        self.entry_vel_blaze.grid(row=2, column=1, pady=3)

        tk.Label(
            inner_price,
            text="(Core, carbone e boccette usano i prezzi della tab Pozioni)",
            font=("Segoe UI", 8),
            bg=BG_PANEL,
            fg=FG_SUBTLE,
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=4, pady=(4, 0))

        panel_price.pack(padx=10, pady=6, fill="x")

        # --- VENDITA ---
        panel_sale, inner_sale = self.make_panel(self.tab_velocita, "Vendita / Profitto")

        tk.Label(
            inner_sale,
            text="Prezzo vendita (b / pozione):",
            font=LABEL_FONT,
            bg=BG_PANEL,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=4, pady=4)

        self.entry_vel_prezzo = tk.Entry(
            inner_sale,
            width=10,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        self.entry_vel_prezzo.grid(row=0, column=1, pady=4, sticky="w")

        panel_sale.pack(padx=10, pady=6, fill="x")

        # --- BOTTONE ---
        tk.Button(
            self.tab_velocita,
            text="CALCOLA VELOCITÀ",
            command=self.do_calcola_velocita,
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

        # --- PREVIEW ---
        self.label_vel_preview = tk.Label(
            self.tab_velocita,
            text="Totale: -    •    Per pozione: -",
            font=("Segoe UI", 11, "bold"),
            bg=BG_MAIN,
            fg=FG_TEXT,
        )
        self.label_vel_preview.pack(pady=(0, 10))

        # --- DETTAGLIO ---
        panel_result = tk.Frame(self.tab_velocita, bg=BG_PANEL)
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

        self.text_vel_result = tk.Text(
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
        self.text_vel_result.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_vel_result.yview)

    def do_calcola_velocita(self):
        try:
            num = float(self.entry_vel_num.get())
            tipo = self.combo_vel_tipo.get()

            prezzo_lapis    = float(self.entry_vel_lapis.get())
            prezzo_zucchero = float(self.entry_vel_zucchero.get())
            prezzo_blaze    = float(self.entry_vel_blaze.get())

            # prezzi condivisi dalla tab Pozioni
            prezzo_core      = float(self.entry_core.get())
            prezzo_carbone   = float(self.entry_carbone.get())
            boccette_per_1b  = float(self.entry_boccette_per_b.get())

            try:
                prezzo_vendita = float(self.entry_vel_prezzo.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_velocita(
                num=num,
                tipo=tipo,
                prezzo_lapis=prezzo_lapis,
                prezzo_zucchero=prezzo_zucchero,
                prezzo_blaze=prezzo_blaze,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
            )

            self.label_vel_preview.config(
                text=result["preview_text"],
                fg=FG_TEXT,
                bg=BG_MAIN,
            )

            self.text_vel_result.config(state="normal")
            self.text_vel_result.delete("1.0", tk.END)
            self.text_vel_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_vel_result.config(state="disabled")

        except ValueError:
            messagebox.showerror(
                "Errore",
                "Controlla i campi Velocità: inserisci numeri validi.",
            )



    def apply_profile(self):
        """Carica i prezzi dal profilo selezionato nella GUI."""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("Errore", "Seleziona o scrivi un nome profilo.")
            return

        if name not in self.profiles:
            messagebox.showerror("Errore", f"Profilo '{name}' non trovato.")
            return

        p = self.profiles[name]

        self.entry_reagente.delete(0, tk.END)
        self.entry_reagente.insert(0, p["prezzo_reagente"])

        self.entry_core.delete(0, tk.END)
        self.entry_core.insert(0, p["prezzo_core"])

        self.entry_carbone.delete(0, tk.END)
        self.entry_carbone.insert(0, p["prezzo_carbone"])

        self.entry_verdure_per_b.delete(0, tk.END)
        self.entry_verdure_per_b.insert(0, p["verdure_per_1b"])

        self.entry_vasetti_per_b.delete(0, tk.END)
        self.entry_vasetti_per_b.insert(0, p["vasetti_per_1b"])

        self.entry_boccette_per_b.delete(0, tk.END)
        self.entry_boccette_per_b.insert(0, p["boccette_per_1b"])

        messagebox.showinfo("Profilo caricato", f"Profilo '{name}' applicato.")

    def save_profile(self):
        """Salva/aggiorna il profilo con i valori attuali dei campi prezzo."""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("Errore", "Inserisci un nome profilo da salvare.")
            return

        new_prof = {
            "prezzo_reagente": self.entry_reagente.get(),
            "prezzo_core": self.entry_core.get(),
            "prezzo_carbone": self.entry_carbone.get(),
            "verdure_per_1b": self.entry_verdure_per_b.get(),
            "vasetti_per_1b": self.entry_vasetti_per_b.get(),
            "boccette_per_1b": self.entry_boccette_per_b.get()
        }

        self.profiles[name] = new_prof
        save_all_profiles(self.profiles)

        # aggiorna lista valori nella combo profili
        self.combo_profile["values"] = list(self.profiles.keys())

        messagebox.showinfo("Profilo salvato", f"Profilo '{name}' salvato.")

    def rename_profile(self):
        """Rinomina il profilo attuale in un nuovo nome scelto dall'utente."""
        old_name = self.combo_profile.get().strip()
        if not old_name:
            messagebox.showerror("Errore", "Seleziona il profilo da rinominare prima.")
            return

        if old_name not in self.profiles:
            messagebox.showerror("Errore", f"Il profilo '{old_name}' non esiste.")
            return

        rename_win = tk.Toplevel(self.root)
        rename_win.title("Rinomina profilo")
        rename_win.configure(bg=BG_MAIN)
        rename_win.resizable(False, False)

        tk.Label(
            rename_win,
            text=f"Nuovo nome per '{old_name}':",
            font=LABEL_FONT,
            bg=BG_MAIN,
            fg=FG_TEXT
        ).pack(padx=10, pady=(10, 4), anchor="w")

        new_name_entry = tk.Entry(
            rename_win,
            width=20,
            font=LABEL_FONT,
            bg="#3a3a3a",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
        )
        new_name_entry.pack(padx=10, pady=(0, 10))
        new_name_entry.focus_set()

        def conferma_rinomina():
            new_name = new_name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Errore", "Inserisci un nuovo nome per il profilo.")
                return

            if new_name in self.profiles and new_name != old_name:
                sovrascrivi = messagebox.askyesno(
                    "Conferma sovrascrittura",
                    f"Esiste già un profilo chiamato '{new_name}'.\n"
                    "Sovrascriverlo?"
                )
                if not sovrascrivi:
                    return

            # copia dati e cancella vecchio
            self.profiles[new_name] = self.profiles[old_name]
            if new_name != old_name:
                del self.profiles[old_name]

            # salva su disco
            save_all_profiles(self.profiles)

            # aggiorna combobox profili
            self.combo_profile["values"] = list(self.profiles.keys())
            self.combo_profile.set(new_name)

            messagebox.showinfo("Fatto", f"Profilo rinominato in '{new_name}'.")
            rename_win.destroy()

        btn_frame = tk.Frame(rename_win, bg=BG_MAIN)
        btn_frame.pack(padx=10, pady=(8, 10), fill="x")

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

    def delete_profile(self):
        """Elimina definitivamente il profilo selezionato dalla lista e da profiles.json."""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("Errore", "Seleziona il profilo da eliminare.")
            return

        if name not in self.profiles:
            messagebox.showerror("Errore", f"Il profilo '{name}' non esiste.")
            return

        conferma = messagebox.askyesno(
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il profilo '{name}'?\n"
            "Questa azione non può essere annullata."
        )
        if not conferma:
            return

        del self.profiles[name]
        save_all_profiles(self.profiles)

        nuovi_nomi = list(self.profiles.keys())
        self.combo_profile["values"] = nuovi_nomi

        if nuovi_nomi:
            self.combo_profile.set(nuovi_nomi[0])
        else:
            self.combo_profile.set("")

        messagebox.showinfo("Profilo eliminato", f"Profilo '{name}' rimosso.")


    def do_calcola_pozioni(self):
        try:
            num_pozioni = float(self.entry_pozioni.get())
            tier_reagente = self.combo_tier.get()
            tipo_calderone = self.combo_calderone.get()

            prezzo_reagente = float(self.entry_reagente.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())

            try:
                prezzo_vendita = float(self.entry_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None

            profilo_attivo = self.combo_profile.get().strip() or "(non salvato)"

            result = calcola_pozioni(
                num_pozioni,
                tier_reagente,
                tipo_calderone,
                prezzo_reagente,
                prezzo_core,
                prezzo_carbone,
                verdure_per_1b,
                vasetti_per_1b,
                boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
                profilo_attivo=profilo_attivo,
            )

            self.label_preview.config(
                text=result["preview_text"], fg=FG_TEXT, bg=BG_MAIN
            )
            self.text_result.config(state="normal")
            self.text_result.delete("1.0", tk.END)
            self.text_result.insert(tk.END, "\n".join(result["output_lines"]))
            self.text_result.config(state="disabled")

        except ValueError:
            messagebox.showerror("Errore", "Controlla i campi: inserisci numeri validi!")

    # Funzioni simili per antidoti, revivify, extinguish, rune, elisir,
    # che chiamano core_calcola_antidoti, core_calcola_revivify, ecc.,
    # e aggiornano le rispettive label/text.

def run_app():
    root = tk.Tk()
    app = ElysiumPozioniApp(root)
    root.mainloop()
