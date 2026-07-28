# tabs/tab_spesa.py
"""Tab Lista della Spesa - ingredienti aggregati per un mix di prodotti."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, BG_INPUT,
    FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SMALL_FONT, ENTRY_WIDTH,
    BORDER_SUBTLE, ACCENT,
)


def build(app):
    """Costruisce la tab Lista della Spesa nell'app."""
    self = app

    outer = tk.Frame(self.tab_spesa, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODOTTI ===
    panel_prod, prod_inner = self.make_panel(container, "Prodotti da produrre", "🛒")

    # Header riga
    tk.Label(prod_inner, text="Prodotto",     font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 4))
    tk.Label(prod_inner, text="Tipo / Config", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=0, column=1, columnspan=2, sticky="w", padx=(0, 8), pady=(0, 4))
    tk.Label(prod_inner, text="Quantità",     font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=0, column=3, sticky="w", pady=(0, 4))

    def make_qty(parent, row_):
        e = tk.Entry(parent, width=8, font=LABEL_FONT,
                     bg=BG_INPUT, fg=FG_TEXT, insertbackground=ACCENT_LIGHT,
                     relief="flat", highlightthickness=2,
                     highlightbackground=BORDER_SUBTLE, highlightcolor=ACCENT)
        e.insert(0, "0")
        e.grid(row=row_, column=3, pady=2, padx=(10, 0), sticky="w")
        self._bind_numeric_validation(e, allow_empty=False)
        return e

    def make_combo(parent, values, row_, col, width_=10):
        c = ttk.Combobox(parent, values=values, width=width_,
                         state="readonly", font=LABEL_FONT)
        c.current(0)
        c.grid(row=row_, column=col, pady=2, padx=(0, 4), sticky="w")
        self._block_combobox_scroll(c)
        return c

    def lbl(parent, text, row_):
        tk.Label(parent, text=text, font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
                 ).grid(row=row_, column=0, sticky="e", padx=(0, 8), pady=2)

    r = 1

    # Pozione di cura — calderone + tier reagente (scelte indipendenti)
    lbl(prod_inner, "Pozione di cura:", r)
    self.combo_spesa_poz_cal  = make_combo(prod_inner,
        ["Terracotta", "Rame", "Ferro", "Oro", "Diamante", "Smeraldo"], r, 1, 11)
    self.combo_spesa_poz_tier = make_combo(prod_inner, ["T1", "T2", "T3"], r, 2, 4)
    self.entry_spesa_poz_qty  = make_qty(prod_inner, r); r += 1

    # Antidoto
    lbl(prod_inner, "Antidoto:", r)
    self.combo_spesa_ant_tipo = make_combo(prod_inner, ["Terracotta", "Ferro"], r, 1, 10)
    self.entry_spesa_ant_qty  = make_qty(prod_inner, r); r += 1

    # Revivify
    lbl(prod_inner, "Revivify:", r)
    self.entry_spesa_rev_qty = make_qty(prod_inner, r); r += 1

    # Extinguish
    lbl(prod_inner, "Extinguish:", r)
    self.entry_spesa_ext_qty = make_qty(prod_inner, r); r += 1

    # Elisir
    lbl(prod_inner, "Elisir:", r)
    self.combo_spesa_elisir_tipo = make_combo(prod_inner,
        ["Minor mending", "Inferior mending", "Lesser mending",
         "Medium mending", "Greater mending"], r, 1, 16)
    self.entry_spesa_elisir_qty = make_qty(prod_inner, r); r += 1

    # Velocità
    lbl(prod_inner, "Velocità:", r)
    self.combo_spesa_vel_tipo = make_combo(prod_inner, ["Velocità I", "Velocità II"], r, 1, 10)
    self.entry_spesa_vel_qty  = make_qty(prod_inner, r); r += 1

    # Danno
    lbl(prod_inner, "Danno:", r)
    self.combo_spesa_danno_tipo = make_combo(prod_inner, ["Danno I", "Danno II"], r, 1, 10)
    self.entry_spesa_danno_qty  = make_qty(prod_inner, r); r += 1

    # Riduzione
    lbl(prod_inner, "Riduzione:", r)
    self.combo_spesa_rid_tipo = make_combo(prod_inner, ["Riduzione I", "Riduzione II"], r, 1, 10)
    self.entry_spesa_rid_qty  = make_qty(prod_inner, r); r += 1

    # Forza
    lbl(prod_inner, "Forza:", r)
    self.combo_spesa_forza_tipo = make_combo(prod_inner, ["Forza II"], r, 1, 10)
    self.entry_spesa_forza_qty  = make_qty(prod_inner, r); r += 1

    # Supportive Revivify: il calderone sceglie fra le due ricette alternative
    lbl(prod_inner, "Supportive:", r)
    self.combo_spesa_supp_tipo = make_combo(prod_inner, ["Oro", "Smeraldo"], r, 1, 10)
    self.entry_spesa_supp_qty  = make_qty(prod_inner, r)

    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONI ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=8)

    calc_btn = self.make_action_button(
        btn_container, "GENERA LISTA", self.do_genera_lista_spesa, "success", "🛒")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=20, pady=8)
    calc_btn.pack(side="left", padx=4)

    reset_btn = self.make_action_button(
        btn_container, "Reset", self._reset_lista_spesa, "secondary", "🔄")
    reset_btn.pack(side="left", padx=4)

    # === RISULTATI ===
    self.make_result_area(col_out, "label_spesa_preview", "text_spesa_result")
