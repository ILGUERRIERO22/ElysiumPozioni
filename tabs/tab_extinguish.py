# tabs/tab_extinguish.py
"""Tab Extinguish - costruzione UI."""

import tkinter as tk
from config_app import (
    BG_MAIN, BG_CARD, FG_TEXT, FG_SUBTLE, GOLD,
    LABEL_FONT, SECTION_FONT, SMALL_FONT,
)


def build(app):
    """Costruisce la tab Extinguish nell'app."""
    self = app

    outer = tk.Frame(self.tab_extinguish, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(outer, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="🔥 Extinguish - Calderone in Rame",
             font=SECTION_FONT, bg=BG_CARD, fg=GOLD).pack(anchor="w")
    tk.Label(info_frame, text="Ricetta: 1 Quarzo + 1 Core + 1 Carbonella + 1 Boccetta = 1 Extinguish",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w", pady=(4, 0))

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
    self.entry_ext_num = self.make_labeled_entry(prod_inner, "Numero Extinguish:", "", row=0)
    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZO QUARZO ===
    panel_price, price_inner = self.make_panel(container, "Prezzo ingrediente", "💰")
    self.entry_ext_quartz = self.make_labeled_entry(price_inner, "Quarzo (1x):", "1.0", row=0, icon_key="quarzo")

    # Il quarzo serve anche alla tab Forza: la tiene allineata
    def _aggiorna_forza(e=None):
        try:
            self._aggiorna_prezzi_forza()
        except AttributeError:
            pass

    self.entry_ext_quartz.bind("<KeyRelease>", _aggiorna_forza, add="+")
    self.entry_ext_quartz.bind("<FocusOut>",   _aggiorna_forza, add="+")
    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
    self.entry_ext_prezzo_vendita = self.make_labeled_entry(sale_inner, "Prezzo vendita (b):", "", row=0, allow_empty=True)
    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA EXTINGUISH", self.do_calcola_extinguish, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(col_out, "label_ext_preview", "text_ext_result")
