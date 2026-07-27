# tabs/tab_revivify.py
"""Tab Revivify - costruzione UI."""

import tkinter as tk
from config_app import (
    BG_MAIN, BG_CARD, FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SECTION_FONT, SMALL_FONT, SECONDARY,
)


def build(app):
    """Costruisce la tab Revivify nell'app."""
    self = app

    outer = tk.Frame(self.tab_revivify, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(outer, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="✨ Revivify - Calderone in Rame",
             font=SECTION_FONT, bg=BG_CARD, fg=SECONDARY).pack(anchor="w")
    tk.Label(info_frame, text="Ricetta: 1 Revival star + 1 Core + 1 Carbonella + 1 Boccetta = 1 Revivify",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w", pady=(4, 0))

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
    self.entry_rev_num = self.make_labeled_entry(prod_inner, "Numero Revivify:", "", row=0)
    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI (readonly) ===
    panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti (b)", "💰")

    # Revival star
    tk.Label(price_inner, text="Revival star (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=3)
    self.label_rev_revival = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_rev_revival.grid(row=0, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=0, column=2, sticky="w", padx=(8, 0))

    # Core
    tk.Label(price_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=3)
    self.label_rev_core = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_rev_core.grid(row=1, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=1, column=2, sticky="w", padx=(8, 0))

    # Carbone
    label_frame_carbone = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_carbone.grid(row=2, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'carbone' in self.icons:
        tk.Label(label_frame_carbone, image=self.icons['carbone'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_carbone, text="Carbone (1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_rev_carbone = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_rev_carbone.grid(row=2, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=2, column=2, sticky="w", padx=(8, 0))

    # Boccette
    label_frame_boccette = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_boccette.grid(row=3, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'boccetta' in self.icons:
        tk.Label(label_frame_boccette, image=self.icons['boccetta'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_boccette, text="Boccette (per 1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_rev_boccette = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_rev_boccette.grid(row=3, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=3, column=2, sticky="w", padx=(8, 0))

    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
    self.entry_rev_prezzo_vendita = self.make_labeled_entry(sale_inner, "Prezzo vendita (b):", "", row=0, allow_empty=True)
    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA REVIVIFY", self.do_calcola_revivify, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(col_out, "label_rev_preview", "text_rev_result")

    try:
        self._aggiorna_prezzi_revivify()
    except AttributeError:
        pass
