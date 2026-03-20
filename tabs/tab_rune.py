# tabs/tab_rune.py
"""Tab Rune - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, FG_TEXT, ACCENT_LIGHT,
    LABEL_FONT, SECTION_FONT, ENTRY_WIDTH,
)


def build(app):
    """Costruisce la tab Rune nell'app."""
    self = app

    container = tk.Frame(self.tab_rune, bg=BG_MAIN)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="🔮 Calcolo Rune - Altare delle Rune",
             font=SECTION_FONT, bg=BG_CARD, fg=ACCENT_LIGHT).pack(anchor="w")

    # === TIPO RUNE ===
    panel_tipo, tipo_inner = self.make_panel(container, "Tipo di rune", "⚔️")
    tk.Label(tipo_inner, text="Tipo rune:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_rune_tipo = ttk.Combobox(tipo_inner, values=["Maghi", "Bardi"],
                                        width=ENTRY_WIDTH, state="readonly", font=LABEL_FONT)
    self.combo_rune_tipo.current(0)
    self.combo_rune_tipo.grid(row=0, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_rune_tipo)
    panel_tipo.pack(padx=0, pady=(0, 8), fill="x")

    # === PEPITE ===
    panel_pepite, pepite_inner = self.make_panel(container, "Pepite disponibili", "🪙")

    metals = ["Tin", "Rame", "Ferro", "Oro", "Argento"]
    metal_icons = {"Rame": "pepita_rame", "Ferro": "pepita_ferro", "Oro": "pepita_oro"}
    self.entry_rune_pepite = {}

    for r, met in enumerate(metals):
        icon_key = metal_icons.get(met)
        entry = self.make_labeled_entry(pepite_inner, f"{met} (pepite):", "0", row=r, icon_key=icon_key)
        self.entry_rune_pepite[met] = entry

    panel_pepite.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA RUNE", self.do_calcola_rune, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(container, "label_rune_preview", "text_rune_result")
