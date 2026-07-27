# tabs/tab_antidoti.py
"""Tab Antidoti - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, BG_INPUT,
    FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SMALL_FONT, ENTRY_WIDTH,
)


def build(app):
    """Costruisce la tab Antidoti nell'app."""
    self = app

    outer = tk.Frame(self.tab_antidoti, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione Antidoti", "🏭")

    self.entry_ant_num = self.make_labeled_entry(prod_inner, "Numero antidoti:", "", row=0)

    tk.Label(prod_inner, text="Calderone:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_ant_calderone = ttk.Combobox(
        prod_inner, values=["Terracotta", "Ferro"],
        width=ENTRY_WIDTH, state="readonly", font=LABEL_FONT)
    self.combo_ant_calderone.current(0)
    self.combo_ant_calderone.grid(row=1, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_ant_calderone)

    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI ===
    panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti", "💰")

    self.entry_brim    = self.make_labeled_entry(price_inner, "Brim powder (1x):",   "1.0", row=0, icon_key="brim")
    self.entry_rotten  = self.make_labeled_entry(price_inner, "Carne marcia (1x):",  "1.0", row=1, icon_key="rotten")
    self.entry_revival = self.make_labeled_entry(price_inner, "Revival star (1x):",  "2.0", row=2)

    def update_revival_prices(e=None):
        self._aggiorna_prezzi_revivify()

    self.entry_revival.bind("<KeyRelease>", update_revival_prices)
    self.entry_revival.bind("<FocusOut>",   update_revival_prices)

    # Resina (readonly, calcolata)
    tk.Label(price_inner, text="Resina (auto):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)

    self.resina_var = tk.StringVar()
    self.entry_resina = tk.Entry(
        price_inner, width=ENTRY_WIDTH, font=LABEL_FONT,
        bg=BG_INPUT, fg=FG_SUBTLE, disabledbackground=BG_INPUT,
        disabledforeground=FG_SUBTLE, relief="flat",
        textvariable=self.resina_var, state="disabled")
    self.entry_resina.grid(row=3, column=1, pady=4, sticky="w")

    tk.Label(price_inner, text="(calcolato da verdure/vasetti)", font=SMALL_FONT,
             bg=BG_CARD, fg=FG_SUBTLE).grid(row=3, column=2, sticky="w", padx=(8, 0))

    # Core (readonly da Pozioni)
    tk.Label(price_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=4, column=0, sticky="e", padx=(0, 8), pady=3)
    self.label_ant_core = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_ant_core.grid(row=4, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=4, column=2, sticky="w", padx=(8, 0))

    # Carbone (readonly da Pozioni)
    label_frame_carbone = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_carbone.grid(row=5, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'carbone' in self.icons:
        tk.Label(label_frame_carbone, image=self.icons['carbone'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_carbone, text="Carbone (1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_ant_carbone = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_ant_carbone.grid(row=5, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=5, column=2, sticky="w", padx=(8, 0))

    # Boccette (readonly da Pozioni)
    label_frame_boccette = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_boccette.grid(row=6, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'boccetta' in self.icons:
        tk.Label(label_frame_boccette, image=self.icons['boccetta'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_boccette, text="Boccette (per 1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_ant_boccette = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_ant_boccette.grid(row=6, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=6, column=2, sticky="w", padx=(8, 0))

    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
    self.entry_ant_prezzo = self.make_labeled_entry(sale_inner, "Prezzo vendita/antidoto:", "", row=0, allow_empty=True)
    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA ANTIDOTI", self.do_calcola_antidoti, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(col_out, "label_ant_preview", "text_ant_result")

    # Inizializzazioni
    self._aggiorna_resina_da_pozioni()
    try:
        self._aggiorna_prezzi_antidoti()
    except AttributeError:
        pass
