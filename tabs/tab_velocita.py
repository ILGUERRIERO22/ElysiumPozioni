# tabs/tab_velocita.py
"""Tab Velocità - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, FG_TEXT, FG_SUBTLE, ACCENT_LIGHT, GOLD,
    LABEL_FONT, SECTION_FONT, SMALL_FONT,
)


def build(app):
    """Costruisce la tab Velocità nell'app."""
    self = app

    outer = tk.Frame(self.tab_velocita, bg=BG_MAIN)
    outer.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(outer, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="⚡ Pozioni di Velocità",
             font=SECTION_FONT, bg=BG_CARD, fg=GOLD).pack(anchor="w")
    tk.Label(info_frame, text="Velocità I: Terracotta | Velocità II: Ferro (upgrade da Vel I)",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w", pady=(4, 0))

    # Input a sinistra, risultati a destra: restano visibili insieme.
    container, col_out = self.make_split(outer)

    # === PRODUZIONE ===
    panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
    self.entry_vel_num = self.make_labeled_entry(prod_inner, "Numero pozioni:", "", row=0)

    tk.Label(prod_inner, text="Tipo pozione:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
    self.combo_vel_tipo = ttk.Combobox(prod_inner, values=["Velocità I", "Velocità II"],
                                       width=14, state="readonly", font=LABEL_FONT)
    self.combo_vel_tipo.current(0)
    self.combo_vel_tipo.grid(row=1, column=1, pady=4, sticky="w")
    self._block_combobox_scroll(self.combo_vel_tipo)

    panel_prod.pack(padx=0, pady=(0, 8), fill="x")

    # === PREZZI ===
    panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti (b)", "💰")

    self.entry_vel_lapis    = self.make_labeled_entry(price_inner, "Lapis (1x):",    "1.0", row=0, icon_key="lapis")
    self.entry_vel_zucchero = self.make_labeled_entry(price_inner, "Zucchero (1x):", "1.0", row=1, icon_key="zucchero")
    self.entry_vel_blaze    = self.make_labeled_entry(price_inner, "Blaze (1x):",    "1.0", row=2, icon_key="blaze")

    # Core (readonly)
    tk.Label(price_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=3)
    self.label_vel_core = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_vel_core.grid(row=3, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=3, column=2, sticky="w", padx=(8, 0))

    # Carbone (readonly)
    label_frame_carbone = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_carbone.grid(row=4, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'carbone' in self.icons:
        tk.Label(label_frame_carbone, image=self.icons['carbone'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_carbone, text="Carbone (1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_vel_carbone = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_vel_carbone.grid(row=4, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=4, column=2, sticky="w", padx=(8, 0))

    # Boccette (readonly)
    label_frame_boccette = tk.Frame(price_inner, bg=BG_CARD)
    label_frame_boccette.grid(row=5, column=0, sticky="e", padx=(0, 8), pady=3)
    if 'boccetta' in self.icons:
        tk.Label(label_frame_boccette, image=self.icons['boccetta'], bg=BG_CARD).pack(side="left", padx=(0, 4))
    tk.Label(label_frame_boccette, text="Boccette (per 1b):", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT).pack(side="left")
    self.label_vel_boccette = tk.Label(price_inner, text="-", font=LABEL_FONT, bg=BG_CARD, fg=ACCENT_LIGHT)
    self.label_vel_boccette.grid(row=5, column=1, sticky="w", padx=4, pady=3)
    tk.Label(price_inner, text="(dalla tab Pozioni)", font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE
             ).grid(row=5, column=2, sticky="w", padx=(8, 0))

    panel_price.pack(padx=0, pady=(0, 8), fill="x")

    # === VENDITA ===
    panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
    self.entry_vel_prezzo = self.make_labeled_entry(sale_inner, "Prezzo vendita (b):", "", row=0, allow_empty=True)
    panel_sale.pack(padx=0, pady=(0, 8), fill="x")

    # === BOTTONE ===
    btn_container = tk.Frame(container, bg=BG_MAIN)
    btn_container.pack(pady=12)
    calc_btn = self.make_action_button(btn_container, "CALCOLA VELOCITÀ", self.do_calcola_velocita, "success", "🧮")
    calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
    calc_btn.pack()

    # === RISULTATI ===
    self.make_result_area(col_out, "label_vel_preview", "text_vel_result")

    try:
        self._aggiorna_prezzi_velocita()
    except AttributeError:
        pass
