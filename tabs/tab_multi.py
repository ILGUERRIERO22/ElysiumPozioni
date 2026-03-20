# tabs/tab_multi.py
"""Tab Multi-Prodotto - costruzione UI."""

import tkinter as tk
from tkinter import ttk
from config_app import (
    BG_MAIN, BG_CARD, BG_RESULT, FG_TEXT, FG_SUBTLE, ACCENT_LIGHT,
    LABEL_FONT, SECTION_FONT, SMALL_FONT,
)
from calcolo_multi_prodotto import get_tipi_prodotti_disponibili


def build(app):
    """Costruisce la tab Multi-Prodotto nell'app."""
    self = app

    container = tk.Frame(self.tab_multi, bg=BG_MAIN)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Info header
    info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
    info_frame.pack(fill="x", pady=(0, 10))
    tk.Label(info_frame, text="🧮 Calcolatrice Multi-Prodotto",
             font=SECTION_FONT, bg=BG_CARD, fg=ACCENT_LIGHT).pack(anchor="w")
    tk.Label(info_frame, text="Calcola materiali aggregati per produzioni multiple",
             font=SMALL_FONT, bg=BG_CARD, fg=FG_SUBTLE).pack(anchor="w", pady=(4, 0))

    # === AGGIUNGI PRODOTTO ===
    panel_add, add_inner = self.make_panel(container, "Aggiungi Prodotto", "➕")

    tk.Label(add_inner, text="Tipo prodotto:", font=LABEL_FONT, bg=BG_CARD, fg=FG_TEXT
             ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)

    tipi_prodotti = get_tipi_prodotti_disponibili()
    self.combo_multi_tipo = ttk.Combobox(
        add_inner, values=[nome for _, nome in tipi_prodotti],
        width=30, state="readonly", font=LABEL_FONT)
    self.combo_multi_tipo.current(0)
    self.combo_multi_tipo.grid(row=0, column=1, pady=4, sticky="w", columnspan=2)
    self._block_combobox_scroll(self.combo_multi_tipo)

    self.entry_multi_qty    = self.make_labeled_entry(add_inner, "Quantità:",             "10", row=1)
    self.entry_multi_prezzo = self.make_labeled_entry(add_inner, "Prezzo vendita (opz):", "",   row=2, allow_empty=True)

    btn_aggiungi = self.make_action_button(
        add_inner, "Aggiungi alla lista", self.do_aggiungi_multi_prodotto, "primary", "➕")
    btn_aggiungi.grid(row=3, column=0, columnspan=3, pady=8)

    panel_add.pack(padx=0, pady=(0, 8), fill="x")

    # === LISTA PRODUZIONE ===
    panel_lista, lista_inner = self.make_panel(container, "Lista Produzione", "📦")

    list_container = tk.Frame(lista_inner, bg=BG_CARD)
    list_container.pack(fill="both", expand=True)

    scrollbar_list = ttk.Scrollbar(list_container, style="Vertical.TScrollbar")
    scrollbar_list.pack(side="right", fill="y")

    self.multi_lista_text = tk.Text(
        list_container, height=8, font=LABEL_FONT, state="disabled",
        wrap="word", yscrollcommand=scrollbar_list.set,
        bg=BG_RESULT, fg=FG_TEXT, relief="flat", padx=10, pady=8)
    self.multi_lista_text.pack(fill="both", expand=True)
    scrollbar_list.config(command=self.multi_lista_text.yview)

    btn_frame = tk.Frame(lista_inner, bg=BG_CARD)
    btn_frame.pack(pady=8)

    self.make_action_button(btn_frame, "Svuota Tutto", self.do_svuota_multi_lista, "danger", "🗑️").pack(side="left", padx=4)

    calc_multi_btn = self.make_action_button(btn_frame, "CALCOLA TOTALE", self.do_calcola_multi, "success", "🧮")
    calc_multi_btn.config(font=("Segoe UI", 11, "bold"), padx=20, pady=8)
    calc_multi_btn.pack(side="left", padx=4)

    panel_lista.pack(padx=0, pady=(0, 8), fill="both", expand=True)

    # === RISULTATI ===
    self.make_result_area(container, "label_multi_preview", "text_multi_result")

    # Inizializza lista
    self.multi_prodotti_lista = []
