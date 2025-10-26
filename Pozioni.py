import tkinter as tk
from tkinter import ttk, messagebox

# --- TEMA SCURO / STILE ---
BG_MAIN = "#1e1e1e"
BG_PANEL = "#2a2a2a"
BG_RESULT = "#111111"
FG_TEXT = "#eaeaea"
FG_SUBTLE = "#9e9e9e"
ACCENT = "#6a5dfd"

TITLE_FONT = ("Segoe UI", 15, "bold")
SECTION_FONT = ("Segoe UI", 11, "bold")
LABEL_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 11, "bold")
RESULT_FONT = ("Consolas", 11)


def calcola():
    try:
        # --- INPUT DI BASE ---
        num_pozioni = int(entry_pozioni.get())
        tier = combo_tier.get()            # T1 / T2 / T3
        tipo_calderone = combo_calderone.get()  # Oro / Ferro

        # --- PREZZI DIRETTI ---
        prezzo_reagente = float(entry_reagente.get())   # costo 1 reagente scelto
        prezzo_core = float(entry_core.get())           # costo 1 core fragment
        prezzo_carbone = float(entry_carbone.get())     # costo 1 carbone (12 carbonella)

        # --- PACCHETTI (quante unità per 1b) ---
        verdure_per_1b = float(entry_verdure_per_b.get())    # es 3 => 1b ogni 3 verdure
        vasetti_per_1b = float(entry_vasetti_per_b.get())    # es 15 => 1b ogni 15 vasetti
        boccette_per_1b = float(entry_boccette_per_b.get())  # es 14 => 1b ogni 14 boccette

        # --- COSTI UNITARI ---
        costo_verdura_unit = 1.0 / verdure_per_1b        # b per 1 verdura
        costo_vasetto_unit = 1.0 / vasetti_per_1b        # b per 1 vasetto
        costo_boccetta_unit = 1.0 / boccette_per_1b      # b per 1 boccetta

        # Resina: 2 verdure + 1 vasetto -> 2 resine
        # => costo singola resina
        costo_resina_unit = (2.0 * costo_verdura_unit + costo_vasetto_unit) / 2.0

        # Carbonella:
        # 1 carbone = 12 carbonella
        costo_carbonella_unit = prezzo_carbone / 12.0

        # --- QUANTITÀ MATERIALI IN BASE AL CALDERONE ---

        # Rese reagente:
        # T1 = 1 catalyst, T2 = 2 catalyst, T3 = 3 catalyst
        catalyst_per_reagente = {"T1": 1.0, "T2": 2.0, "T3": 3.0}

        if tipo_calderone == "Oro":
            # Oro:
            # 2 catalyst = 3 pozioni  => catalyst_per_pozione = 2/3
            # carbonella: 2 carbonella per 3 pozioni => 2/3 a pozione
            catalyst_necessari = (num_pozioni / 3.0) * 2.0
            carbonella_tot = (num_pozioni / 3.0) * 2.0

        elif tipo_calderone == "Ferro":
            # Ferro:
            # 1 catalyst = 1 pozione
            # carbonella: 2 carbonella per 1 pozione
            catalyst_necessari = num_pozioni * 1.0
            carbonella_tot = num_pozioni * 2.0

        else:
            raise ValueError("Tipo calderone non valido")

        # Quanti reagenti servono per fare tutti i catalyst richiesti
        reagenti_usati = catalyst_necessari / catalyst_per_reagente[tier]

        # Ogni reagente 'batch' usa 1 core + 1 resina
        core_usati = reagenti_usati
        resine_usate = reagenti_usati

        # Boccette: sempre 1 per pozione (vale sia Oro che Ferro)
        boccette_tot = num_pozioni * 1.0

        # --- COSTI PARZIALI ---
        costo_reagenti = reagenti_usati * prezzo_reagente
        costo_core = core_usati * prezzo_core
        costo_resine = resine_usate * costo_resina_unit
        costo_carbonella = carbonella_tot * costo_carbonella_unit
        costo_boccette = boccette_tot * costo_boccetta_unit

        costo_totale = (
            costo_reagenti
            + costo_core
            + costo_resine
            + costo_carbonella
            + costo_boccette
        )

        costo_per_pozione = costo_totale / num_pozioni if num_pozioni != 0 else 0.0

        # --- AGGIORNA PREVIEW IN ALTO ---
        label_preview.config(
            text=f"Totale: {costo_totale:.2f} b    •    Per pozione: {costo_per_pozione:.2f} b",
            fg=FG_TEXT,
            bg=BG_MAIN,
        )

        # --- TESTO DETTAGLIATO NEL BOX SCROLLABILE ---
        output_lines = [
            f"Calderone:          {tipo_calderone}",
            f"Pozioni totali:     {num_pozioni}",
            f"Tipo reagente:      {tier}",
            "",
            f"COSTO TOTALE:       {costo_totale:.2f} b",
            f"Costo per pozione:  {costo_per_pozione:.2f} b",
            "",
            f"Catalyst necessari: {catalyst_necessari:.2f}",
            f"Reagenti usati:     {reagenti_usati:.2f}",
            f"Core frammenti:     {core_usati:.2f}",
            f"Resine:             {resine_usate:.2f}",
            f"Carbonella:         {carbonella_tot:.2f}",
            f"Boccette:           {boccette_tot:.2f}",
            "",
            "Costi parziali:",
            f" • Reagenti:     {costo_reagenti:.2f} b",
            f" • Core:         {costo_core:.2f} b",
            f" • Resine:       {costo_resine:.2f} b",
            f" • Carbonella:   {costo_carbonella:.2f} b",
            f" • Boccette:     {costo_boccette:.2f} b",
        ]

        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, "\n".join(output_lines))
        text_result.config(state="disabled")

    except ValueError:
        messagebox.showerror("Errore", "Controlla i campi: inserisci numeri validi!")



# =========================
# GUI con scroll "intelligente"
# =========================

root = tk.Tk()
root.title("Pozioni Alchemiche 😼")
root.geometry("540x500")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# canvas scrollabile per tutto
outer_canvas = tk.Canvas(root, bg=BG_MAIN, highlightthickness=0)
outer_canvas.pack(side="left", fill="both", expand=True)

main_scrollbar = tk.Scrollbar(root, orient="vertical", command=outer_canvas.yview)
main_scrollbar.pack(side="right", fill="y")

outer_canvas.configure(yscrollcommand=main_scrollbar.set)

inner_frame = tk.Frame(outer_canvas, bg=BG_MAIN)
outer_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

def on_configure(event):
    outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
inner_frame.bind("<Configure>", on_configure)

# scroll globale di default
def _on_mousewheel_canvas(event):
    outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
outer_canvas.bind_all("<MouseWheel>", _on_mousewheel_canvas)

# scroll locale dentro il box dettaglio
def _on_mousewheel_text(event):
    text_result.yview_scroll(int(-1 * (event.delta / 120)), "units")
    return "break"  # blocca propagazione

def _bind_wheel_to_text(event):
    outer_canvas.unbind_all("<MouseWheel>")
    text_result.bind_all("<MouseWheel>", _on_mousewheel_text)

def _bind_wheel_to_canvas(event):
    text_result.unbind_all("<MouseWheel>")
    outer_canvas.bind_all("<MouseWheel>", _on_mousewheel_canvas)


# helper pannelli
def make_panel(parent, title):
    frame = tk.Frame(parent, bg=BG_PANEL, bd=0)
    header = tk.Label(
        frame,
        text=title,
        font=SECTION_FONT,
        bg=BG_PANEL,
        fg=FG_TEXT,
        anchor="w",
    )
    header.pack(fill="x", padx=10, pady=(8, 4))
    inner = tk.Frame(frame, bg=BG_PANEL)
    inner.pack(fill="x", padx=10, pady=(0, 10))
    return frame, inner


# --- TITOLO ---
tk.Label(
    inner_frame,
    text="Calcolatore Pozioni",
    font=TITLE_FONT,
    fg=FG_TEXT,
    bg=BG_MAIN,
).pack(pady=8)

# --- PANNELLO PRODUZIONE ---
panel_prod, prod_inner = make_panel(inner_frame, "Produzione")

tk.Label(prod_inner, text="Numero pozioni:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=4)
entry_pozioni = tk.Entry(
    prod_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_pozioni.grid(row=0, column=1, pady=4)

tk.Label(prod_inner, text="Tipo reagente:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=4)
combo_tier = ttk.Combobox(
    prod_inner,
    values=["T1", "T2", "T3"],
    width=8,
    state="readonly",
    font=LABEL_FONT,
)
combo_tier.current(0)
combo_tier.grid(row=1, column=1, pady=4)

tk.Label(prod_inner, text="Calderone:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=4)
combo_calderone = ttk.Combobox(
    prod_inner,
    values=["Oro", "Ferro"],
    width=8,
    state="readonly",
    font=LABEL_FONT,
)
combo_calderone.current(0)
combo_calderone.grid(row=2, column=1, pady=4)

panel_prod.pack(padx=10, pady=6, fill="x")

# --- PANNELLO PREZZI DIRETTI ---
panel_price_direct, price_direct_inner = make_panel(inner_frame, "Prezzi diretti (in b)")

tk.Label(price_direct_inner, text="Reagente (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_reagente = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_reagente.insert(0, "1.5")
entry_reagente.grid(row=0, column=1, pady=3)

tk.Label(price_direct_inner, text="Core fragment (1x):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
entry_core = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_core.insert(0, "1.0")
entry_core.grid(row=1, column=1, pady=3)

tk.Label(price_direct_inner, text="Carbone (1 blocco):", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
entry_carbone = tk.Entry(
    price_direct_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_carbone.insert(0, "1.5")
entry_carbone.grid(row=2, column=1, pady=3)

tk.Label(
    price_direct_inner,
    text="(1 blocco = 12 carbonella)",
    font=("Segoe UI", 8),
    bg=BG_PANEL,
    fg=FG_SUBTLE,
).grid(row=2, column=2, sticky="w", padx=4)

panel_price_direct.pack(padx=10, pady=6, fill="x")

# --- PANNELLO QUANTE UNITÀ PER 1 b ---
panel_bundle, bundle_inner = make_panel(inner_frame, "Quante unità ottieni con 1 b")

tk.Label(bundle_inner, text="Verdure per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=0, column=0, sticky="e", padx=4, pady=3)
entry_verdure_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_verdure_per_b.insert(0, "3")
entry_verdure_per_b.grid(row=0, column=1, pady=3)

tk.Label(bundle_inner, text="Vasetti per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=1, column=0, sticky="e", padx=4, pady=3)
entry_vasetti_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_vasetti_per_b.insert(0, "15")
entry_vasetti_per_b.grid(row=1, column=1, pady=3)

tk.Label(bundle_inner, text="Boccette per 1 b:", font=LABEL_FONT, bg=BG_PANEL, fg=FG_TEXT)\
    .grid(row=2, column=0, sticky="e", padx=4, pady=3)
entry_boccette_per_b = tk.Entry(
    bundle_inner,
    width=10,
    font=LABEL_FONT,
    bg="#3a3a3a",
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
)
entry_boccette_per_b.insert(0, "14")
entry_boccette_per_b.grid(row=2, column=1, pady=3)

panel_bundle.pack(padx=10, pady=6, fill="x")

# --- BOTTONE CALCOLA ---
tk.Button(
    inner_frame,
    text="CALCOLA",
    command=calcola,
    bg=ACCENT,
    fg="white",
    font=BUTTON_FONT,
    activebackground="#574dff",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=6,
).pack(pady=(10, 6))

# --- PREVIEW COSTI VELOCI ---
label_preview = tk.Label(
    inner_frame,
    text="Totale: -    •    Per pozione: -",
    font=("Segoe UI", 11, "bold"),
    bg=BG_MAIN,
    fg=FG_TEXT,
)
label_preview.pack(pady=(0, 10))

# --- DETTAGLIO ---
panel_result = tk.Frame(inner_frame, bg=BG_PANEL)
panel_result.pack(padx=10, pady=(0, 10), fill="both", expand=True)

tk.Label(
    panel_result,
    text="Dettaglio",
    font=SECTION_FONT,
    bg=BG_PANEL,
    fg=FG_TEXT,
    anchor="w",
).pack(fill="x", padx=10, pady=(8, 4))

inner_result = tk.Frame(panel_result, bg=BG_PANEL)
inner_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scrollbar = tk.Scrollbar(inner_result)
scrollbar.pack(side="right", fill="y")

text_result = tk.Text(
    inner_result,
    height=12,
    font=RESULT_FONT,
    state="disabled",
    wrap="word",
    yscrollcommand=scrollbar.set,
    bg=BG_RESULT,
    fg=FG_TEXT,
    insertbackground=FG_TEXT,
    relief="flat",
    padx=10,
    pady=10,
)
text_result.pack(fill="both", expand=True)
scrollbar.config(command=text_result.yview)

# quando il mouse entra nel dettaglio → scrolla dentro
text_result.bind("<Enter>", _bind_wheel_to_text)
# quando esce → torna a scrollare tutta la schermata
text_result.bind("<Leave>", _bind_wheel_to_canvas)

root.mainloop()
