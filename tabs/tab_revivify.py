# tabs/tab_revivify.py
"""Tab Revivify - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, BG_INPUT, FG_TEXT, FG_SUBTLE, ACCENT_LIGHT, ACCENT,
    LABEL_FONT, SECTION_FONT, SMALL_FONT, SECONDARY,
    ENTRY_WIDTH, BORDER_SUBTLE,
)


def build(app):
    """Costruisce la tab Revivify nell'app."""
    self = app

    outer = tk.Frame(self.tab_revivify, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(outer, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="✨ Revivify e Supportive Revivify",
             font=SECTION_FONT, bg=BG_CARD, fg=SECONDARY).pack(anchor="w")
    tk.Label(info_frame,
             text="Revivify (Rame): 1 Revival star + 1 Core + 1 Carbonella + 1 Boccetta",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w", pady=(4, 0))
    tk.Label(info_frame,
             text="Supportive (Oro): 1 Healing catalyst + 1 Core + 2 Carbonella + 1 Revivify  →  1",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w")
    tk.Label(info_frame,
             text="Supportive (Smeraldo): 1 Demonic slab + 1 End shard + 1 Core + 3 Carbonella + 1 Revivify  →  2",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w")

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
    self.entry_rev_num = self.make_labeled_entry(prod_inner, "Numero pozioni:", "", row=0)

    tk.Label(prod_inner, text="Tipo:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_rev_tipo = ttk.Combobox(
        prod_inner,
        values=["Revivify", "Supportive (Oro)", "Supportive (Smeraldo)"],
        width=20, state="readonly", font=LABEL_FONT)
    self.combo_rev_tipo.current(0)
    self.combo_rev_tipo.grid(row=1, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_rev_tipo)

    # Tier del reagente: serve solo alla Supportive in Oro, che consuma
    # un healing catalyst ricavato dai reagenti.
    self._lbl_rev_tier = tk.Label(prod_inner, text="Tipo reagente:", font=LABEL_FONT,
                                  bg=BG_CARD, fg=FG_TEXT)
    self._lbl_rev_tier.grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_rev_tier = ttk.Combobox(prod_inner, values=["T1", "T2", "T3"],
                                       width=8, state="readonly", font=LABEL_FONT)
    self.combo_rev_tier.current(0)
    self.combo_rev_tier.grid(row=2, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_rev_tier)
    self._hint_rev_tier = tk.Label(prod_inner, text="1 reagente T2 = 2 catalyst",
                                   font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE)
    self._hint_rev_tier.grid(row=2, column=2, sticky="w", padx=(8, 0))

    def _toggle_campi(event=None):
        """Mostra solo i campi che la ricetta scelta usa davvero."""
        tipo = self.combo_rev_tipo.get()
        for w in (self._lbl_rev_tier, self.combo_rev_tier, self._hint_rev_tier):
            w.grid() if tipo == "Supportive (Oro)" else w.grid_remove()
        for w in self._widget_smeraldo:
            w.grid() if tipo == "Supportive (Smeraldo)" else w.grid_remove()

    self.combo_rev_tipo.bind("<<ComboboxSelected>>", _toggle_campi)
    self._toggle_rev_campi = _toggle_campi

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

    # Reagente: da cui si ricava l'healing catalyst (solo Supportive in Oro)
    tk.Label(price_inner, text="Reagente (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=4, column=0, sticky="e", padx=(0, 8), pady=3)
    self.label_rev_reagente = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_rev_reagente.grid(row=4, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=4, column=2, sticky="w", padx=(8, 0))

    # Ingredienti della sola ricetta in Smeraldo
    _lbl_slab = tk.Label(price_inner, text="Demonic slab (1x):", font=LABEL_FONT,
                         bg=BG_CARD, fg=FG_TEXT)
    _lbl_slab.grid(row=5, column=0, sticky="e", padx=(0, 8), pady=3)
    self.entry_rev_slab = tk.Entry(
        price_inner, width=ENTRY_WIDTH, font=LABEL_FONT, bg=BG_INPUT, fg=FG_TEXT,
        insertbackground=ACCENT_LIGHT, relief="flat", highlightthickness=2,
        highlightbackground=BORDER_SUBTLE, highlightcolor=ACCENT)
    self.entry_rev_slab.insert(0, "5.0")
    self.entry_rev_slab.grid(row=5, column=1, pady=3, sticky="w")
    self._bind_numeric_validation(self.entry_rev_slab)

    _lbl_shard = tk.Label(price_inner, text="End shard (1x):", font=LABEL_FONT,
                          bg=BG_CARD, fg=FG_TEXT)
    _lbl_shard.grid(row=6, column=0, sticky="e", padx=(0, 8), pady=3)
    self.entry_rev_shard = tk.Entry(
        price_inner, width=ENTRY_WIDTH, font=LABEL_FONT, bg=BG_INPUT, fg=FG_TEXT,
        insertbackground=ACCENT_LIGHT, relief="flat", highlightthickness=2,
        highlightbackground=BORDER_SUBTLE, highlightcolor=ACCENT)
    self.entry_rev_shard.insert(0, "4.0")
    self.entry_rev_shard.grid(row=6, column=1, pady=3, sticky="w")
    self._bind_numeric_validation(self.entry_rev_shard)

    self._widget_smeraldo = (_lbl_slab, self.entry_rev_slab,
                             _lbl_shard, self.entry_rev_shard)

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

    # Alla partenza mostra solo i campi della ricetta selezionata
    _toggle_campi()

    try:
        self._aggiorna_prezzi_revivify()
    except AttributeError:
        pass
