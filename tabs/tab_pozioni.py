# tabs/tab_pozioni.py
"""Tab Pozioni di cura - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, BG_INPUT,
    FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SECTION_FONT, SMALL_FONT, ENTRY_WIDTH,
    BORDER_SUBTLE, ACCENT,
)


def build(app):
    """Costruisce la tab Pozioni di cura nell'app."""
    self = app  # alias per usare il codice originale invariato

    container = tk.Frame(self.tab_pozioni, bg=BG_MAIN)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # === PROFILO PREZZI ===
    panel_prof, prof_inner = self.make_panel(container, "Gestione Profili", "👤")

    tk.Label(
        prof_inner, text="Profilo:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
    ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)

    self.combo_profile = ttk.Combobox(prof_inner, width=16, font=LABEL_FONT)
    self.combo_profile.grid(row=0, column=1, padx=4, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_profile)

    btn_frame = tk.Frame(prof_inner, bg=BG_CARD)
    btn_frame.grid(row=0, column=2, columnspan=4, padx=(10, 0), pady=4, sticky="w")

    self.make_action_button(btn_frame, "Carica",   self.apply_profile,  "secondary", "📥").pack(side="left", padx=2)
    self.make_action_button(btn_frame, "Salva",    self.save_profile,   "primary",   "💾").pack(side="left", padx=2)
    self.make_action_button(btn_frame, "Rinomina", self.rename_profile, "secondary", "✏️").pack(side="left", padx=2)
    self.make_action_button(btn_frame, "Elimina",  self.delete_profile, "danger",    "🗑️").pack(side="left", padx=2)

    panel_prof.pack(padx=0, pady=(0, 8), fill="x")

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")

    self.entry_pozioni = self.make_labeled_entry(prod_inner, "Numero pozioni:", "", row=0)

    tk.Label(prod_inner, text="Tipo reagente:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_tier = ttk.Combobox(prod_inner, values=["T1", "T2", "T3"], width=ENTRY_WIDTH,
                                   state="readonly", font=LABEL_FONT)
    self.combo_tier.current(0)
    self.combo_tier.grid(row=1, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_tier)

    tk.Label(prod_inner, text="Calderone:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_calderone = ttk.Combobox(
        prod_inner, values=["Terracotta", "Rame", "Ferro", "Oro", "Diamante", "Smeraldo"],
        width=ENTRY_WIDTH, state="readonly", font=LABEL_FONT)
    self.combo_calderone.current(0)
    self.combo_calderone.grid(row=2, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_calderone)

    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI DIRETTI ===
    panel_price, price_inner = self.make_panel(container, "Prezzi diretti (b)", "💰")

    self.entry_reagente = self.make_labeled_entry(price_inner, "Reagente (1x):",       "1.5", row=0)
    self.entry_core     = self.make_labeled_entry(price_inner, "Core fragment (1x):",  "1.0", row=1)

    def update_core_prices(e=None):
        self._aggiorna_prezzi_riduzione()
        self._aggiorna_prezzi_velocita()
        self._aggiorna_prezzi_antidoti()
        self._aggiorna_prezzi_revivify()

    self.entry_core.bind("<KeyRelease>", update_core_prices)
    self.entry_core.bind("<FocusOut>",   update_core_prices)

    # === Combustibile row (creazione manuale per avere riferimento all'hint label dinamica) ===
    _carb_lbl_frame = tk.Frame(price_inner, bg=BG_CARD)
    _carb_lbl_frame.grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
    if "carbone" in self.icons:
        tk.Label(_carb_lbl_frame, image=self.icons["carbone"], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(_carb_lbl_frame, text="Combustibile (1 blocco):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")

    self.entry_carbone = tk.Entry(
        price_inner, width=ENTRY_WIDTH, font=LABEL_FONT,
        bg=BG_INPUT, fg=FG_TEXT, insertbackground=ACCENT_LIGHT,
        relief="flat", highlightthickness=2,
        highlightbackground=BORDER_SUBTLE, highlightcolor=ACCENT)
    self.entry_carbone.insert(0, "1.5")
    self.entry_carbone.grid(row=2, column=1, pady=4, sticky="w")
    self._bind_numeric_validation(self.entry_carbone, allow_empty=False)

    self.combo_combustibile = ttk.Combobox(
        price_inner, values=["Carbone", "Anthracite", "Firestone"],
        width=11, state="readonly", font=LABEL_FONT)
    self.combo_combustibile.current(0)
    self.combo_combustibile.grid(row=2, column=2, pady=4, padx=(8, 4), sticky="w")
    self._block_combobox_scroll(self.combo_combustibile)

    self._label_carbone_hint = tk.Label(
        price_inner, text="= 12 carbonella",
        font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE)
    self._label_carbone_hint.grid(row=2, column=3, sticky="w", padx=(4, 0))

    def update_carbone_prices(e=None):
        self._aggiorna_prezzi_riduzione()
        self._aggiorna_prezzi_velocita()
        self._aggiorna_prezzi_antidoti()
        self._aggiorna_prezzi_revivify()
        self._aggiorna_prezzi_elisir()

    def _on_combustibile_change(e=None):
        from ricette import COMBUSTIBILI
        tipo = self.combo_combustibile.get()
        carbonella = COMBUSTIBILI.get(tipo, {}).get("carbonella", 12)
        self._label_carbone_hint.config(text=f"= {carbonella} carbonella")
        update_carbone_prices()

    self.combo_combustibile.bind("<<ComboboxSelected>>", _on_combustibile_change)
    self.entry_carbone.bind("<KeyRelease>", update_carbone_prices)
    self.entry_carbone.bind("<FocusOut>",   update_carbone_prices)

    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === QUANTITÀ PER 1b ===
    panel_bundle, bundle_inner = self.make_panel(container, "Unità per 1 b", "📦")

    self.entry_verdure_per_b  = self.make_labeled_entry(bundle_inner, "Verdure per 1 b:",  "3",  row=0, icon_key="verdure")
    self.entry_vasetti_per_b  = self.make_labeled_entry(bundle_inner, "Vasetti per 1 b:",  "15", row=1)
    self.entry_boccette_per_b = self.make_labeled_entry(bundle_inner, "Boccette per 1 b:", "14", row=2, icon_key="boccetta")

    def update_boccette_prices(e=None):
        self._aggiorna_prezzi_riduzione()
        self._aggiorna_prezzi_velocita()
        self._aggiorna_prezzi_antidoti()
        self._aggiorna_prezzi_revivify()
        self._aggiorna_prezzi_elisir()

    self.entry_boccette_per_b.bind("<KeyRelease>", update_boccette_prices)
    self.entry_boccette_per_b.bind("<FocusOut>",   update_boccette_prices)

    self.entry_verdure_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())
    self.entry_vasetti_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())

    panel_bundle.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita & Profitto", "📈")

    self.entry_prezzo_vendita = self.make_labeled_entry(
        sale_inner, "Prezzo vendita/poz (b):", "", row=0, hint_text="Lascia vuoto per solo costo", allow_empty=True)
    self.entry_sconto_perc = self.make_labeled_entry(sale_inner, "Sconto cliente (%):", "0", row=1)

    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE CALCOLA ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)

    calc_btn = self.make_action_button(btn_container, "CALCOLA POZIONI", self.do_calcola_pozioni, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(container, "label_preview", "text_result")

    # Inizializza combobox profili
    self.combo_profile["values"] = list(self.profiles.keys())
    if self.combo_profile["values"]:
        self.combo_profile.set(self.combo_profile["values"][0])
