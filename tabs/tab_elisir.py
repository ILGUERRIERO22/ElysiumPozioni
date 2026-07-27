# tabs/tab_elisir.py
"""Tab Elisir di cura - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SMALL_FONT,
)


def build(app):
    """Costruisce la tab Elisir nell'app."""
    self = app

    outer = tk.Frame(self.tab_elisir, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione Elisir", "🏭")
    self.entry_el_num = self.make_labeled_entry(prod_inner, "Numero elisir:", "", row=0)

    tk.Label(prod_inner, text="Tipo elisir:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_el_tipo = ttk.Combobox(
        prod_inner,
        values=["Minor mending", "Inferior mending", "Lesser mending",
                "Medium mending", "Greater mending"],
        width=18, state="readonly", font=LABEL_FONT)
    self.combo_el_tipo.current(0)
    self.combo_el_tipo.grid(row=1, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_el_tipo)

    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI SPECIALI ===
    panel_price, price_inner = self.make_panel(container, "Ingredienti speciali (b)", "💎")

    # Brim (readonly da Antidoti)
    label_frame_brim = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_brim.grid(row=0, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'brim' in self.icons:
        tk.Label(label_frame_brim, image=self.icons['brim'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_brim, text="Brim powder (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_el_brim = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_el_brim.grid(row=0, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Antidoti)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=0, column=2, sticky="w", padx=(8, 0))

    self.entry_spidereye  = self.make_labeled_entry(price_inner, "Occhio di ragno (1x):",    "1.0", row=1, icon_key="spidereye")
    self.entry_membrana   = self.make_labeled_entry(price_inner, "Membrana Phantom (1x):",   "1.0", row=2, icon_key="phantom")
    self.entry_slime      = self.make_labeled_entry(price_inner, "Slimeball (1x):",          "1.0", row=3, icon_key="slimeball")
    self.entry_slime.bind("<KeyRelease>", lambda e: self._aggiorna_prezzi_riduzione())
    self.entry_slime.bind("<FocusOut>",   lambda e: self._aggiorna_prezzi_riduzione())
    self.entry_lost_soul  = self.make_labeled_entry(price_inner, "Lost soul (1x):",          "1.0", row=4, icon_key="lost_soul")

    # Carbone (readonly)
    label_frame_carbone = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_carbone.grid(row=5, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'carbone' in self.icons:
        tk.Label(label_frame_carbone, image=self.icons['carbone'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_carbone, text="Carbone (1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_el_carbone = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_el_carbone.grid(row=5, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=5, column=2, sticky="w", padx=(8, 0))

    # Boccette (readonly)
    label_frame_boccette = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_boccette.grid(row=6, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'boccetta' in self.icons:
        tk.Label(label_frame_boccette, image=self.icons['boccetta'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_boccette, text="Boccette (per 1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_el_boccette = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_el_boccette.grid(row=6, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=6, column=2, sticky="w", padx=(8, 0))

    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI LINGOTTI ===
    panel_metals, metals_inner = self.make_panel(container, "Lingotti (b/lingotto)", "🪙")

    self.entry_price_tin = self.make_labeled_entry(metals_inner, "Tin:",      "", row=0)
    self.entry_price_cu  = self.make_labeled_entry(metals_inner, "Rame:",     "", row=1, icon_key="rame")
    self.entry_price_fe  = self.make_labeled_entry(metals_inner, "Ferro:",    "", row=2, icon_key="ferro")
    self.entry_price_au  = self.make_labeled_entry(metals_inner, "Oro:",      "", row=3, icon_key="oro")
    self.entry_price_dia = self.make_labeled_entry(metals_inner, "Diamante:", "", row=4)

    panel_metals.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
    self.entry_el_prezzo = self.make_labeled_entry(sale_inner, "Prezzo vendita (b):", "", row=0, allow_empty=True)
    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA ELISIR", self.do_calcola_elisir, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(col_out, "label_el_preview", "text_el_result")

    # Bind brim
    try:
        self._aggiorna_brim_elisir()
        self.entry_brim.bind("<KeyRelease>", lambda e: self._aggiorna_brim_elisir())
        self.entry_brim.bind("<FocusOut>",   lambda e: self._aggiorna_brim_elisir())
    except AttributeError:
        pass

    try:
        self._aggiorna_prezzi_elisir()
    except AttributeError:
        pass
