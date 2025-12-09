# gui_main.py
# Versione 3.2 - UI Moderna con Animazioni

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from config_app import (
    APP_NAME, APP_VERSION, APP_AUTHOR,
    BG_MAIN, BG_PANEL, BG_CARD, BG_RESULT, BG_INPUT,
    FG_TEXT, FG_SUBTLE, FG_BRIGHT,
    ACCENT, ACCENT_HOVER, ACCENT_LIGHT, ACCENT_GLOW,
    SECONDARY, SECONDARY_HOVER,
    SUCCESS, SUCCESS_HOVER,
    DANGER_BG, DANGER_BG_HOVER, DANGER_BG_ACTIVE,
    GOLD, GOLD_HOVER,
    BORDER_SUBTLE, BORDER_ACCENT,
    TAB_SELECTED, TAB_HOVER,
    TITLE_FONT, SECTION_FONT, LABEL_FONT, BUTTON_FONT, RESULT_FONT,
    SMALL_FONT, PREVIEW_FONT,
    BUTTON_PADX, BUTTON_PADY, PANEL_PADX, PANEL_PADY, ENTRY_WIDTH,
    CONFIG_FILE, PROFILES_FILE,
)

from animations import AnimationManager

from calcolo_pozioni import calcola_pozioni
from calcolo_antidoti import calcola_antidoti as core_calcola_antidoti
from calcolo_revivify import calcola_revivify as core_calcola_revivify
from calcolo_extinguish import calcola_extinguish as core_calcola_extinguish
from calcolo_rune import (
    calcola_rune_diretto as core_rune_diretto,
    calcola_rune_inverso as core_rune_inverso,
)
from calcolo_elisir import calcola_elisir as core_calcola_elisir
from calcolo_rune import calcola_rune_diretto
from calcolo_velocita import calcola_pozione_velocita as core_calcola_velocita
from calcolo_danno import calcola_pozione_danno as core_calcola_danno
from calcolo_multi_prodotto import calcola_multi_prodotto as core_multi_prod, get_tipi_prodotti_disponibili


# =========================
#   GESTIONE PROFILI
# =========================

def ensure_profiles_file():
    if not os.path.exists(PROFILES_FILE):
        default_profiles = {
            "Standard": {
                "prezzo_reagente": "1.5",
                "prezzo_core": "1.0",
                "prezzo_carbone": "1.5",
                "verdure_per_1b": "3",
                "vasetti_per_1b": "15",
                "boccette_per_1b": "14"
            },
            "Raro": {
                "prezzo_reagente": "2.5",
                "prezzo_core": "1.5",
                "prezzo_carbone": "2.0",
                "verdure_per_1b": "2",
                "vasetti_per_1b": "12",
                "boccette_per_1b": "10"
            }
        }
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(default_profiles, f, indent=2, ensure_ascii=False)

def load_all_profiles():
    ensure_profiles_file()
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Errore lettura profiles.json:", e)
        return {}

def save_all_profiles(profiles_dict):
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles_dict, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Errore scrittura profiles.json:", e)


# =========================
#   FUNZIONI INFO
# =========================

def show_info():
    msg = (
        f"{APP_NAME} v{APP_VERSION}\n"
        f"Autore: {APP_AUTHOR}\n\n"
        "🧪 Calcolatore di costo e profitto pozioni per Elysium.\n\n"
        "✨ Funzionalità:\n"
        "• Supporto calderoni Terracotta / Rame / Ferro / Oro / Diamante\n"
        "• Profili di mercato multipli\n"
        "• Salvataggio automatico configurazione\n"
        "• Analisi margine e profitto\n"
        "• Calcolo rune, elisir, antidoti e altro\n\n"
        "Miao 😺"
    )
    messagebox.showinfo("ℹ️ Informazioni", msg)

def show_license():
    mit_text = (
        "📜 Licenza MIT\n\n"
        f"Copyright (c) 2025 {APP_AUTHOR}\n\n"
        "È consentito usare, copiare, modificare e distribuire questo software "
        "senza restrizioni, anche per uso commerciale, purché venga mantenuta "
        "questa nota di copyright e la presente licenza.\n\n"
        "IL SOFTWARE VIENE FORNITO \"COSÌ COM'È\", SENZA ALCUNA GARANZIA."
    )
    messagebox.showinfo("📜 Licenza", mit_text)


# =========================
#   WIDGET PERSONALIZZATI
# =========================

class ModernButton(tk.Canvas):
    """Bottone moderno con effetti hover e bordi arrotondati"""
    def __init__(self, parent, text, command=None, 
                 bg_color=ACCENT, hover_color=ACCENT_HOVER, 
                 fg_color=FG_BRIGHT, width=140, height=38,
                 icon="", **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.command = command
        self.text = icon + " " + text if icon else text
        self.width = width
        self.height = height
        self.is_hovered = False
        
        self._draw_button(self.bg_color)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
        
    def _draw_button(self, color):
        self.delete("all")
        r = 10  # radius più grande per bordi più arrotondati
        w, h = self.width, self.height

        # Ombra sottile per profondità
        shadow_offset = 2
        shadow_color = "#000000"
        self.create_arc(shadow_offset, shadow_offset, r*2+shadow_offset, r*2+shadow_offset,
                       start=90, extent=90, fill=shadow_color, outline=shadow_color, stipple="gray50")
        self.create_arc(w-r*2+shadow_offset, shadow_offset, w+shadow_offset, r*2+shadow_offset,
                       start=0, extent=90, fill=shadow_color, outline=shadow_color, stipple="gray50")
        self.create_arc(shadow_offset, h-r*2+shadow_offset, r*2+shadow_offset, h+shadow_offset,
                       start=180, extent=90, fill=shadow_color, outline=shadow_color, stipple="gray50")
        self.create_arc(w-r*2+shadow_offset, h-r*2+shadow_offset, w+shadow_offset, h+shadow_offset,
                       start=270, extent=90, fill=shadow_color, outline=shadow_color, stipple="gray50")

        # Disegna rettangolo arrotondato principale
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=color, outline=color)
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=color, outline=color)
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=color, outline=color)
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)

        # Testo
        self.create_text(w//2, h//2, text=self.text, fill=self.fg_color,
                        font=BUTTON_FONT)
        
    def _on_enter(self, event):
        self.is_hovered = True
        self._animate_color_transition(self.bg_color, self.hover_color, duration=150)
        self.config(cursor="hand2")

    def _on_leave(self, event):
        self.is_hovered = False
        self._animate_color_transition(self.hover_color, self.bg_color, duration=150)

    def _on_click(self, event):
        # Effetto press con leggera riduzione
        self._draw_button(self.bg_color)

    def _on_release(self, event):
        if self.is_hovered and self.command:
            # Piccolo feedback visivo
            self._draw_button(ACCENT_LIGHT)
            self.after(50, lambda: self._draw_button(self.hover_color if self.is_hovered else self.bg_color))
            # Esegue comando dopo feedback
            self.after(100, self.command)
        else:
            self._draw_button(self.hover_color if self.is_hovered else self.bg_color)

    def _animate_color_transition(self, color_from: str, color_to: str, duration: int = 150):
        """Anima transizione di colore smooth"""
        # Per ora usa cambio diretto, ma prepara per future animazioni
        self._draw_button(color_to)


class ModernEntry(tk.Entry):
    """Entry con stile moderno"""
    def __init__(self, parent, placeholder="", **kwargs):
        self.placeholder = placeholder
        self.placeholder_color = FG_SUBTLE
        self.default_fg = FG_TEXT
        
        super().__init__(parent, 
                        font=LABEL_FONT,
                        bg=BG_INPUT,
                        fg=self.default_fg,
                        insertbackground=ACCENT_LIGHT,
                        relief="flat",
                        highlightthickness=2,
                        highlightbackground=BORDER_SUBTLE,
                        highlightcolor=ACCENT,
                        **kwargs)
        
        if placeholder:
            self._add_placeholder()
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
    
    def _add_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
        
    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg)
            
    def _on_focus_out(self, event):
        if not self.get():
            self._add_placeholder()


class GlowLabel(tk.Label):
    """Label con effetto glow per i titoli"""
    def __init__(self, parent, text, glow_color=ACCENT_LIGHT, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        

# =========================
#   CLASSE APP PRINCIPALE
# =========================

class ElysiumPozioniApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"⚗️ {APP_NAME} v{APP_VERSION}")
        self.root.geometry("850x720")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        # Profili in memoria
        self.profiles = load_all_profiles()

        # Sistema di animazioni
        self.animator = AnimationManager(self.root)

        # Configura stili ttk
        self._configure_styles()
        
        # Costruisci GUI
        self._build_menu()
        self._build_header()
        self._build_main_layout()
        self._build_tabs()
        
        # Carica config
        self.load_config()
        
        # Bind chiusura
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        """Salva config alla chiusura"""
        self.save_config()
        self.root.destroy()

    def _configure_styles(self):
        """Configura gli stili ttk per un look moderno e accattivante"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook (tabs) - Design più moderno con bordi e transizioni
        style.configure("TNotebook",
                       background=BG_MAIN,
                       borderwidth=0,
                       padding=0,
                       relief="flat")
        style.configure("TNotebook.Tab",
                       background=BG_PANEL,
                       foreground=FG_SUBTLE,
                       padding=[20, 12],  # Padding più generoso
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       relief="flat")
        style.map("TNotebook.Tab",
                 background=[("selected", ACCENT), ("active", TAB_HOVER)],
                 foreground=[("selected", FG_BRIGHT), ("active", FG_TEXT)],
                 expand=[("selected", [1, 1, 1, 0])],  # Espansione per effetto rialzato
                 borderwidth=[("selected", 0)])

        # Combobox - Bordi più definiti e colori migliorati
        style.configure("TCombobox",
                       fieldbackground=BG_INPUT,
                       background=BG_INPUT,
                       foreground=FG_TEXT,
                       arrowcolor=ACCENT_LIGHT,
                       borderwidth=1,
                       bordercolor=BORDER_SUBTLE,
                       padding=8,  # Padding maggiore
                       relief="flat")
        style.map("TCombobox",
                 fieldbackground=[("readonly", BG_INPUT), ("focus", BG_INPUT)],
                 selectbackground=[("readonly", ACCENT)],
                 selectforeground=[("readonly", FG_BRIGHT)],
                 bordercolor=[("focus", ACCENT), ("!focus", BORDER_SUBTLE)],
                 arrowcolor=[("active", ACCENT_HOVER)])

        # Scrollbar - Più sottile e moderna
        style.configure("Vertical.TScrollbar",
                       background=BG_PANEL,
                       troughcolor=BG_MAIN,
                       borderwidth=0,
                       arrowsize=12,
                       width=12)  # Scrollbar più sottile
        style.map("Vertical.TScrollbar",
                 background=[("active", ACCENT_LIGHT), ("pressed", ACCENT)])

    def _build_menu(self):
        """Costruisce il menu"""
        menubar = tk.Menu(self.root, tearoff=0, bg=BG_PANEL, fg=FG_TEXT,
                         activebackground=ACCENT, activeforeground=FG_BRIGHT,
                         font=LABEL_FONT)
        
        menu_info = tk.Menu(menubar, tearoff=0, bg=BG_PANEL, fg=FG_TEXT,
                           activebackground=ACCENT, activeforeground=FG_BRIGHT,
                           font=LABEL_FONT)
        menu_info.add_command(label="ℹ️ Informazioni", command=show_info)
        menu_info.add_command(label="📜 Licenza", command=show_license)
        menu_info.add_separator()
        menu_info.add_command(label="💾 Salva configurazione", command=self.save_config)
        
        menubar.add_cascade(label="Menu", menu=menu_info)
        self.root.config(menu=menubar)

    def _build_header(self):
        """Costruisce l'header con logo e titolo"""
        header_frame = tk.Frame(self.root, bg=BG_MAIN)
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        # Titolo con icona
        title_label = tk.Label(
            header_frame,
            text=f"⚗️ {APP_NAME}",
            font=("Segoe UI", 24, "bold"),
            fg=ACCENT_LIGHT,
            bg=BG_MAIN
        )
        title_label.pack(side="left")
        
        # Versione
        version_label = tk.Label(
            header_frame,
            text=f"v{APP_VERSION}",
            font=SMALL_FONT,
            fg=FG_SUBTLE,
            bg=BG_MAIN
        )
        version_label.pack(side="left", padx=(10, 0), pady=(12, 0))
        
        # Autore (a destra)
        author_label = tk.Label(
            header_frame,
            text=f"by {APP_AUTHOR}",
            font=SMALL_FONT,
            fg=FG_SUBTLE,
            bg=BG_MAIN
        )
        author_label.pack(side="right", pady=(12, 0))

    def _build_main_layout(self):
        """Costruisce il layout principale con canvas scrollabile"""
        # Container principale
        main_container = tk.Frame(self.root, bg=BG_MAIN)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Canvas scrollabile
        self.outer_canvas = tk.Canvas(main_container, bg=BG_MAIN, highlightthickness=0)
        self.outer_canvas.pack(side="left", fill="both", expand=True)
        
        # Scrollbar verticale con stile
        main_scrollbar = ttk.Scrollbar(
            main_container, 
            orient="vertical", 
            command=self.outer_canvas.yview,
            style="Vertical.TScrollbar"
        )
        main_scrollbar.pack(side="right", fill="y")
        
        self.outer_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Frame interno
        self.inner_frame = tk.Frame(self.outer_canvas, bg=BG_MAIN)
        self.canvas_window = self.outer_canvas.create_window((0, 0), 
                                                              window=self.inner_frame, 
                                                              anchor="nw")
        
        def on_configure(event):
            self.outer_canvas.configure(scrollregion=self.outer_canvas.bbox("all"))
            # Ridimensiona la finestra interna alla larghezza del canvas
            canvas_width = event.width
            self.outer_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.outer_canvas.bind("<Configure>", on_configure)
        self.inner_frame.bind("<Configure>", 
                             lambda e: self.outer_canvas.configure(
                                 scrollregion=self.outer_canvas.bbox("all")))
        
        # Mouse wheel scrolling con controllo del widget
        def _on_mousewheel(event):
            # Controlla se l'evento proviene da un widget che gestisce il proprio scroll
            widget = event.widget

            # Verifica che widget sia un oggetto valido e non una stringa
            if isinstance(widget, str):
                # Se è una stringa, prova a ottenere il widget dal nametowidget
                try:
                    widget = self.root.nametowidget(widget)
                except:
                    # Se fallisce, scrolla il canvas normalmente
                    self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    return

            try:
                widget_class = widget.winfo_class()
            except:
                # Se non possiamo ottenere la classe, scrolla normalmente
                self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return

            # Blocca lo scroll se siamo su:
            # - Listbox (menu dropdown della combobox)
            # - Text (area testo scrollabile)
            # - Combobox stessa
            if widget_class in ('Listbox', 'Text'):
                return "break"

            # Controlla anche i widget parent
            check_widget = widget
            while check_widget:
                if isinstance(check_widget, (ttk.Combobox, tk.Text)):
                    return "break"
                check_widget = check_widget.master if hasattr(check_widget, 'master') else None

            # Altrimenti scrolla il canvas normalmente
            self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind a tutti i widget
        self.outer_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.inner_frame)
        
        # Crea i frame per ogni tab
        self.tab_pozioni = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_antidoti = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_revivify = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_extinguish = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_danno = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_rune = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_elisir = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_velocita = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_multi = tk.Frame(self.notebook, bg=BG_MAIN)
        
        # Aggiungi tabs con solo icone
        self.notebook.add(self.tab_pozioni, text="🧪")
        self.notebook.add(self.tab_antidoti, text="💊")
        self.notebook.add(self.tab_revivify, text="✨")
        self.notebook.add(self.tab_extinguish, text="🔥")
        self.notebook.add(self.tab_danno, text="⚔️")
        self.notebook.add(self.tab_rune, text="🔮")
        self.notebook.add(self.tab_elisir, text="💎")
        self.notebook.add(self.tab_velocita, text="⚡")
        self.notebook.add(self.tab_multi, text="🧮")
        
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Setup tooltip per le tab
        self._setup_tab_tooltips()

    def _setup_tab_tooltips(self):
        """Configura i tooltip per le tab del notebook"""
        self.tab_names = {
            0: "Pozioni di cura",
            1: "Antidoti", 
            2: "Revivify",
            3: "Extinguish",
            4: "Danno",
            5: "Rune",
            6: "Elisir",
            7: "Velocità",
            8: "Multi-Prodotto"
        }
        
        self.tooltip_window = None
        self.current_tab_hover = None
        
        # Bind eventi al notebook
        self.notebook.bind("<Motion>", self._on_tab_motion)
        self.notebook.bind("<Leave>", self._on_tab_leave)
    
    def _on_tab_motion(self, event):
        """Gestisce il movimento del mouse sulle tab"""
        try:
            # Identifica quale tab è sotto il mouse
            elem = self.notebook.identify(event.x, event.y)
            if elem == "label":
                # Ottieni l'indice del tab
                tab_index = self.notebook.index(f"@{event.x},{event.y}")
                
                if tab_index != self.current_tab_hover:
                    self.current_tab_hover = tab_index
                    self._show_tooltip(event, tab_index)
            else:
                self._hide_tooltip()
        except:
            self._hide_tooltip()
    
    def _on_tab_leave(self, event):
        """Nascondi tooltip quando il mouse esce dal notebook"""
        self._hide_tooltip()
        self.current_tab_hover = None
    
    def _show_tooltip(self, event, tab_index):
        """Mostra il tooltip per il tab specificato"""
        self._hide_tooltip()
        
        if tab_index in self.tab_names:
            text = self.tab_names[tab_index]
            x = event.x_root + 10
            y = event.y_root + 10
            
            self.tooltip_window = tk.Toplevel(self.root)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            self.tooltip_window.attributes("-topmost", True)
            
            label = tk.Label(
                self.tooltip_window,
                text=text,
                background="#1f2937",
                foreground="#f3f4f6",
                relief="solid",
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=10,
                pady=5
            )
            label.pack()
    
    def _hide_tooltip(self):
        """Nascondi il tooltip corrente"""
        if self.tooltip_window:
            try:
                self.tooltip_window.destroy()
            except:
                pass
            self.tooltip_window = None

    def make_panel(self, parent, title, icon=""):
        """Crea un pannello card con stile moderno"""
        # Frame esterno con bordo
        outer = tk.Frame(parent, bg=BORDER_SUBTLE, padx=1, pady=1)
        
        # Frame interno
        frame = tk.Frame(outer, bg=BG_CARD)
        frame.pack(fill="both", expand=True)
        
        # Header del pannello
        header_frame = tk.Frame(frame, bg=BG_CARD)
        header_frame.pack(fill="x", padx=12, pady=(10, 6))
        
        # Indicatore colorato
        indicator = tk.Frame(header_frame, bg=ACCENT, width=4, height=18)
        indicator.pack(side="left", padx=(0, 8))
        indicator.pack_propagate(False)
        
        # Titolo
        title_text = f"{icon} {title}" if icon else title
        header = tk.Label(
            header_frame,
            text=title_text,
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
            anchor="w",
        )
        header.pack(side="left", fill="x")
        
        # Linea separatrice sottile
        separator = tk.Frame(frame, bg=BORDER_SUBTLE, height=1)
        separator.pack(fill="x", padx=12, pady=(0, 8))
        
        # Inner frame per il contenuto
        inner = tk.Frame(frame, bg=BG_CARD)
        inner.pack(fill="x", padx=12, pady=(0, 12))
        
        return outer, inner

    def make_labeled_entry(self, parent, label_text, default_value="", row=0, 
                          hint_text="", width=ENTRY_WIDTH):
        """Crea una coppia label + entry con stile uniforme"""
        tk.Label(
            parent,
            text=label_text,
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=row, column=0, sticky="e", padx=(0, 8), pady=4)
        
        entry = tk.Entry(
            parent,
            width=width,
            font=LABEL_FONT,
            bg=BG_INPUT,
            fg=FG_TEXT,
            insertbackground=ACCENT_LIGHT,
            relief="flat",
            highlightthickness=2,
            highlightbackground=BORDER_SUBTLE,
            highlightcolor=ACCENT,
        )
        entry.insert(0, default_value)
        entry.grid(row=row, column=1, pady=4, sticky="w")
        
        if hint_text:
            tk.Label(
                parent,
                text=hint_text,
                font=SMALL_FONT,
                bg=BG_CARD,
                fg=FG_SUBTLE,
            ).grid(row=row, column=2, sticky="w", padx=(8, 0))
        
        return entry

    def update_result_with_fade(self, preview_label, text_widget, preview_text, output_lines):
        """Aggiorna risultati con effetto fade"""
        # Pulse effetto sul preview
        original_bg = preview_label.cget('bg')
        preview_label.config(bg=ACCENT_GLOW)
        self.root.after(200, lambda: preview_label.config(bg=original_bg))

        # Aggiorna testo
        preview_label.config(text=f"💰 {preview_text}")
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "\n".join(output_lines))
        text_widget.config(state="disabled")

    def make_labeled_combo(self, parent, label_text, values, row=0, width=12):
        """Crea una coppia label + combobox"""
        tk.Label(
            parent,
            text=label_text,
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=row, column=0, sticky="e", padx=(0, 8), pady=4)
        
        combo = ttk.Combobox(
            parent,
            values=values,
            width=width,
            state="readonly",
            font=LABEL_FONT,
        )
        combo.current(0)
        combo.grid(row=row, column=1, pady=4, sticky="w")

        return combo

    def make_action_button(self, parent, text, command, style="primary", icon=""):
        """Crea un bottone azione con stile"""
        colors = {
            "primary": (ACCENT, ACCENT_HOVER),
            "secondary": ("#374151", "#4b5563"),
            "success": (SUCCESS, SUCCESS_HOVER),
            "danger": (DANGER_BG, DANGER_BG_HOVER),
            "gold": (GOLD, GOLD_HOVER),
        }
        bg, hover = colors.get(style, colors["primary"])
        
        btn_text = f"{icon} {text}" if icon else text
        
        btn = tk.Button(
            parent,
            text=btn_text,
            command=command,
            bg=bg,
            fg=FG_BRIGHT,
            font=BUTTON_FONT,
            activebackground=hover,
            activeforeground=FG_BRIGHT,
            relief="flat",
            cursor="hand2",
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            borderwidth=0,
        )
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn

    def make_result_area(self, parent, preview_var_name, text_var_name):
        """Crea l'area risultati con preview e dettaglio"""
        # Preview box
        preview_frame = tk.Frame(parent, bg=BG_PANEL, padx=2, pady=2)
        preview_frame.pack(padx=12, pady=(0, 10), fill="x")
        
        preview_inner = tk.Frame(preview_frame, bg=BG_RESULT)
        preview_inner.pack(fill="x")
        
        preview_label = tk.Label(
            preview_inner,
            text="💰 Totale: -    •    Per unità: -",
            font=PREVIEW_FONT,
            bg=BG_RESULT,
            fg=ACCENT_LIGHT,
            pady=12,
        )
        preview_label.pack()
        setattr(self, preview_var_name, preview_label)
        
        # Dettaglio panel
        detail_outer = tk.Frame(parent, bg=BORDER_SUBTLE, padx=1, pady=1)
        detail_outer.pack(padx=12, pady=(0, 12), fill="both", expand=True)
        
        detail_frame = tk.Frame(detail_outer, bg=BG_CARD)
        detail_frame.pack(fill="both", expand=True)
        
        # Header dettaglio
        detail_header = tk.Frame(detail_frame, bg=BG_CARD)
        detail_header.pack(fill="x", padx=10, pady=(8, 4))
        
        tk.Label(
            detail_header,
            text="📋 Dettaglio calcolo",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).pack(side="left")
        
        # Text area con scrollbar
        text_container = tk.Frame(detail_frame, bg=BG_CARD)
        text_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(text_container, style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(
            text_container,
            height=12,
            font=RESULT_FONT,
            state="disabled",
            wrap="word",
            yscrollcommand=scrollbar.set,
            bg=BG_RESULT,
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            padx=12,
            pady=10,
            selectbackground=ACCENT,
            selectforeground=FG_BRIGHT,
        )
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        setattr(self, text_var_name, text_widget)

    # =========================
    #   BUILD TABS
    # =========================

    def _build_tabs(self):
        """Costruisce tutte le tab"""
        self._build_tab_pozioni()
        self._build_tab_antidoti()
        self._build_tab_revivify()
        self._build_tab_extinguish()
        self._build_tab_danno()
        self._build_tab_elisir()
        self._build_tab_rune()
        self._build_tab_velocita()
        self._build_tab_multi()

    def _build_tab_pozioni(self):
        """Tab Pozioni di cura - principale"""
        container = tk.Frame(self.tab_pozioni, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === PROFILO PREZZI ===
        panel_prof, prof_inner = self.make_panel(container, "Gestione Profili", "👤")
        
        # Riga profilo
        tk.Label(
            prof_inner,
            text="Profilo:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT
        ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_profile = ttk.Combobox(
            prof_inner,
            width=16,
            font=LABEL_FONT,
        )
        self.combo_profile.grid(row=0, column=1, padx=4, pady=4, sticky="w")
        
        # Bottoni profilo
        btn_frame = tk.Frame(prof_inner, bg=BG_CARD)
        btn_frame.grid(row=0, column=2, columnspan=4, padx=(10, 0), pady=4, sticky="w")
        
        self.make_action_button(
            btn_frame, "Carica", self.apply_profile, "secondary", "📥"
        ).pack(side="left", padx=2)
        
        self.make_action_button(
            btn_frame, "Salva", self.save_profile, "primary", "💾"
        ).pack(side="left", padx=2)
        
        self.make_action_button(
            btn_frame, "Rinomina", self.rename_profile, "secondary", "✏️"
        ).pack(side="left", padx=2)
        
        self.make_action_button(
            btn_frame, "Elimina", self.delete_profile, "danger", "🗑️"
        ).pack(side="left", padx=2)
        
        panel_prof.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
        
        self.entry_pozioni = self.make_labeled_entry(
            prod_inner, "Numero pozioni:", "", row=0
        )
        
        tk.Label(
            prod_inner,
            text="Tipo reagente:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_tier = ttk.Combobox(
            prod_inner,
            values=["T1", "T2", "T3"],
            width=ENTRY_WIDTH,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_tier.current(0)
        self.combo_tier.grid(row=1, column=1, pady=4, sticky="w")
        
        tk.Label(
            prod_inner,
            text="Calderone:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_calderone = ttk.Combobox(
            prod_inner,
            values=["Terracotta", "Rame", "Ferro", "Oro", "Diamante"],
            width=ENTRY_WIDTH,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_calderone.current(0)
        self.combo_calderone.grid(row=2, column=1, pady=4, sticky="w")
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI DIRETTI ===
        panel_price, price_inner = self.make_panel(container, "Prezzi diretti (b)", "💰")
        
        self.entry_reagente = self.make_labeled_entry(
            price_inner, "Reagente (1x):", "1.5", row=0
        )
        self.entry_core = self.make_labeled_entry(
            price_inner, "Core fragment (1x):", "1.0", row=1
        )
        self.entry_carbone = self.make_labeled_entry(
            price_inner, "Carbone (1 blocco):", "1.5", row=2, 
            hint_text="= 12 carbonella"
        )
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === QUANTITÀ PER 1b ===
        panel_bundle, bundle_inner = self.make_panel(container, "Unità per 1 b", "📦")
        
        self.entry_verdure_per_b = self.make_labeled_entry(
            bundle_inner, "Verdure per 1 b:", "3", row=0
        )
        self.entry_vasetti_per_b = self.make_labeled_entry(
            bundle_inner, "Vasetti per 1 b:", "15", row=1
        )
        self.entry_boccette_per_b = self.make_labeled_entry(
            bundle_inner, "Boccette per 1 b:", "14", row=2
        )
        
        # Bind per aggiornare resina
        self.entry_verdure_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())
        self.entry_vasetti_per_b.bind("<FocusOut>", lambda e: self._aggiorna_resina_da_pozioni())
        
        panel_bundle.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita & Profitto", "📈")
        
        self.entry_prezzo_vendita = self.make_labeled_entry(
            sale_inner, "Prezzo vendita/poz (b):", "", row=0,
            hint_text="Lascia vuoto per solo costo"
        )
        self.entry_sconto_perc = self.make_labeled_entry(
            sale_inner, "Sconto cliente (%):", "0", row=1
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE CALCOLA ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA POZIONI", self.do_calcola_pozioni, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_preview", "text_result")
        
        # Inizializza combobox profili
        self.combo_profile["values"] = list(self.profiles.keys())
        if self.combo_profile["values"]:
            self.combo_profile.set(self.combo_profile["values"][0])

    def _build_tab_antidoti(self):
        """Tab Antidoti"""
        container = tk.Frame(self.tab_antidoti, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione Antidoti", "🏭")
        
        self.entry_ant_num = self.make_labeled_entry(
            prod_inner, "Numero antidoti:", "", row=0
        )
        
        tk.Label(
            prod_inner,
            text="Calderone:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_ant_calderone = ttk.Combobox(
            prod_inner,
            values=["Terracotta", "Ferro"],
            width=ENTRY_WIDTH,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_ant_calderone.current(0)
        self.combo_ant_calderone.grid(row=1, column=1, pady=4, sticky="w")
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI ===
        panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti", "💰")
        
        self.entry_brim = self.make_labeled_entry(
            price_inner, "Brim powder (1x):", "1.0", row=0
        )
        self.entry_rotten = self.make_labeled_entry(
            price_inner, "Carne marcia (1x):", "1.0", row=1
        )
        self.entry_revival = self.make_labeled_entry(
            price_inner, "Revival star (1x):", "2.0", row=2
        )
        
        # Resina (readonly)
        tk.Label(
            price_inner,
            text="Resina (auto):",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.resina_var = tk.StringVar()
        self.entry_resina = tk.Entry(
            price_inner,
            width=ENTRY_WIDTH,
            font=LABEL_FONT,
            bg=BG_INPUT,
            fg=FG_SUBTLE,
            disabledbackground=BG_INPUT,
            disabledforeground=FG_SUBTLE,
            relief="flat",
            textvariable=self.resina_var,
            state="disabled",
        )
        self.entry_resina.grid(row=3, column=1, pady=4, sticky="w")
        
        tk.Label(
            price_inner,
            text="(calcolato da verdure/vasetti)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=3, column=2, sticky="w", padx=(8, 0))
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_ant_prezzo = self.make_labeled_entry(
            sale_inner, "Prezzo vendita/antidoto:", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA ANTIDOTI", self.do_calcola_antidoti, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_ant_preview", "text_ant_result")
        
        # Inizializza resina
        self._aggiorna_resina_da_pozioni()

    def _build_tab_revivify(self):
        """Tab Revivify"""
        container = tk.Frame(self.tab_revivify, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="✨ Revivify - Calderone in Rame",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=SECONDARY,
        ).pack(anchor="w")
        tk.Label(
            info_frame,
            text="Ricetta: 1 Revival star + 1 Core + 1 Carbonella + 1 Boccetta = 1 Revivify",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).pack(anchor="w", pady=(4, 0))
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
        
        self.entry_rev_num = self.make_labeled_entry(
            prod_inner, "Numero Revivify:", "", row=0
        )
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_rev_prezzo_vendita = self.make_labeled_entry(
            sale_inner, "Prezzo vendita (b):", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA REVIVIFY", self.do_calcola_revivify, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_rev_preview", "text_rev_result")

    def _build_tab_extinguish(self):
        """Tab Extinguish"""
        container = tk.Frame(self.tab_extinguish, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="🔥 Extinguish - Calderone in Rame",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=GOLD,
        ).pack(anchor="w")
        tk.Label(
            info_frame,
            text="Ricetta: 1 Quarzo + 1 Core + 1 Carbonella + 1 Boccetta = 1 Extinguish",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).pack(anchor="w", pady=(4, 0))
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
        
        self.entry_ext_num = self.make_labeled_entry(
            prod_inner, "Numero Extinguish:", "", row=0
        )
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZO QUARZO ===
        panel_price, price_inner = self.make_panel(container, "Prezzo ingrediente", "💰")
        
        self.entry_ext_quartz = self.make_labeled_entry(
            price_inner, "Quarzo (1x):", "1.0", row=0
        )
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_ext_prezzo_vendita = self.make_labeled_entry(
            sale_inner, "Prezzo vendita (b):", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA EXTINGUISH", self.do_calcola_extinguish, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_ext_preview", "text_ext_result")

    def _build_tab_danno(self):
        """Tab Pozioni di Danno (I e II)"""
        container = tk.Frame(self.tab_danno, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="⚔️ Pozioni di Danno",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=DANGER_BG_HOVER,
        ).pack(anchor="w")
        tk.Label(
            info_frame,
            text="Danno I: Rame | Danno II (Avvizzimento): Oro (upgrade da Danno I)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).pack(anchor="w", pady=(4, 0))
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
        
        self.entry_danno_num = self.make_labeled_entry(
            prod_inner, "Numero pozioni:", "", row=0
        )
        
        tk.Label(
            prod_inner,
            text="Tipo pozione:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_danno_tipo = ttk.Combobox(
            prod_inner,
            values=["Danno I", "Danno II"],
            width=14,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_danno_tipo.current(0)
        self.combo_danno_tipo.grid(row=1, column=1, pady=4, sticky="w")
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI INGREDIENTI ===
        panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti (b)", "💰")
        
        # Occhio di ragno (readonly da Elisir)
        tk.Label(
            price_inner,
            text="Occhio di ragno (1x):",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=3)
        
        self.label_danno_spidereye = tk.Label(
            price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        )
        self.label_danno_spidereye.grid(row=0, column=1, sticky="w", padx=4, pady=3)
        
        tk.Label(
            price_inner,
            text="(dalla tab Elisir)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=0, column=2, sticky="w", padx=(8, 0))
        
        # Withering dust
        self.entry_withering_dust = self.make_labeled_entry(
            price_inner, "Withering dust (1x):", "1.0", row=1
        )
        
        # Core (readonly da Pozioni)
        tk.Label(
            price_inner,
            text="Core fragment (1x):",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=2, column=0, sticky="e", padx=(0, 8), pady=3)
        
        self.label_danno_core = tk.Label(
            price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        )
        self.label_danno_core.grid(row=2, column=1, sticky="w", padx=4, pady=3)
        
        tk.Label(
            price_inner,
            text="(dalla tab Pozioni)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=2, column=2, sticky="w", padx=(8, 0))
        
        # Carbone (readonly da Pozioni)
        tk.Label(
            price_inner,
            text="Carbone (1 blocco):",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=3, column=0, sticky="e", padx=(0, 8), pady=3)
        
        self.label_danno_carbone = tk.Label(
            price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        )
        self.label_danno_carbone.grid(row=3, column=1, sticky="w", padx=4, pady=3)
        
        tk.Label(
            price_inner,
            text="(dalla tab Pozioni)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=3, column=2, sticky="w", padx=(8, 0))
        
        # Boccette (readonly da Pozioni)
        tk.Label(
            price_inner,
            text="Boccette per 1b:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=4, column=0, sticky="e", padx=(0, 8), pady=3)
        
        self.label_danno_boccette = tk.Label(
            price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        )
        self.label_danno_boccette.grid(row=4, column=1, sticky="w", padx=4, pady=3)
        
        tk.Label(
            price_inner,
            text="(dalla tab Pozioni)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=4, column=2, sticky="w", padx=(8, 0))
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_danno_prezzo_vendita = self.make_labeled_entry(
            sale_inner, "Prezzo vendita (b):", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA DANNO", self.do_calcola_danno, "danger", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_danno_preview", "text_danno_result")
        
        # Inizializza label prezzi
        self._aggiorna_prezzi_danno()

    def _build_tab_elisir(self):
        """Tab Elisir di cura"""
        container = tk.Frame(self.tab_elisir, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione Elisir", "🏭")
        
        self.entry_el_num = self.make_labeled_entry(
            prod_inner, "Numero elisir:", "", row=0
        )
        
        tk.Label(
            prod_inner,
            text="Tipo elisir:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_el_tipo = ttk.Combobox(
            prod_inner,
            values=["Minor mending", "Inferior mending", "Lesser mending", 
                   "Medium mending", "Greater mending"],
            width=18,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_el_tipo.current(0)
        self.combo_el_tipo.grid(row=1, column=1, pady=4, sticky="w")
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI SPECIALI ===
        panel_price, price_inner = self.make_panel(container, "Ingredienti speciali (b)", "💎")
        
        # Brim (readonly da antidoti)
        tk.Label(
            price_inner,
            text="Brim powder (1x):",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=3)
        
        self.label_el_brim = tk.Label(
            price_inner,
            text="-",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        )
        self.label_el_brim.grid(row=0, column=1, sticky="w", padx=4, pady=3)
        
        tk.Label(
            price_inner,
            text="(dalla tab Antidoti)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=0, column=2, sticky="w", padx=(8, 0))
        
        self.entry_spidereye = self.make_labeled_entry(
            price_inner, "Occhio di ragno (1x):", "1.0", row=1
        )
        self.entry_membrana = self.make_labeled_entry(
            price_inner, "Membrana Phantom (1x):", "1.0", row=2
        )
        self.entry_slime = self.make_labeled_entry(
            price_inner, "Slimeball (1x):", "1.0", row=3
        )
        self.entry_lost_soul = self.make_labeled_entry(
            price_inner, "Lost soul (1x):", "1.0", row=4
        )
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI LINGOTTI ===
        panel_metals, metals_inner = self.make_panel(container, "Lingotti (b/lingotto)", "🪙")
        
        self.entry_price_tin = self.make_labeled_entry(
            metals_inner, "Tin:", "", row=0
        )
        self.entry_price_cu = self.make_labeled_entry(
            metals_inner, "Rame:", "", row=1
        )
        self.entry_price_fe = self.make_labeled_entry(
            metals_inner, "Ferro:", "", row=2
        )
        self.entry_price_au = self.make_labeled_entry(
            metals_inner, "Oro:", "", row=3
        )
        self.entry_price_dia = self.make_labeled_entry(
            metals_inner, "Diamante:", "", row=4
        )
        
        panel_metals.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_el_prezzo = self.make_labeled_entry(
            sale_inner, "Prezzo vendita (b):", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA ELISIR", self.do_calcola_elisir, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_el_preview", "text_el_result")
        
        # Bind per aggiornare brim
        try:
            self._aggiorna_brim_elisir()
            self.entry_brim.bind("<KeyRelease>", lambda e: self._aggiorna_brim_elisir())
            self.entry_brim.bind("<FocusOut>", lambda e: self._aggiorna_brim_elisir())
        except AttributeError:
            pass

    def _build_tab_rune(self):
        """Tab Rune"""
        container = tk.Frame(self.tab_rune, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="🔮 Calcolo Rune - Altare delle Rune",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        ).pack(anchor="w")
        
        # === TIPO RUNE ===
        panel_tipo, tipo_inner = self.make_panel(container, "Tipo di rune", "⚔️")
        
        tk.Label(
            tipo_inner,
            text="Tipo rune:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_rune_tipo = ttk.Combobox(
            tipo_inner,
            values=["Maghi", "Bardi"],
            width=ENTRY_WIDTH,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_rune_tipo.current(0)
        self.combo_rune_tipo.grid(row=0, column=1, pady=4, sticky="w")
        
        panel_tipo.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PEPITE ===
        panel_pepite, pepite_inner = self.make_panel(container, "Pepite disponibili", "🪙")
        
        metals = ["Tin", "Rame", "Ferro", "Oro", "Argento"]
        self.entry_rune_pepite = {}
        
        for r, met in enumerate(metals):
            entry = self.make_labeled_entry(
                pepite_inner, f"{met} (pepite):", "0", row=r
            )
            self.entry_rune_pepite[met] = entry
        
        panel_pepite.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA RUNE", self.do_calcola_rune, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_rune_preview", "text_rune_result")

    def _build_tab_velocita(self):
        """Tab Velocità"""
        container = tk.Frame(self.tab_velocita, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="⚡ Pozioni di Velocità",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=GOLD,
        ).pack(anchor="w")
        tk.Label(
            info_frame,
            text="Velocità I: Terracotta | Velocità II: Ferro (upgrade da Vel I)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).pack(anchor="w", pady=(4, 0))
        
        # === PRODUZIONE ===
        panel_prod, prod_inner = self.make_panel(container, "Produzione", "🏭")
        
        self.entry_vel_num = self.make_labeled_entry(
            prod_inner, "Numero pozioni:", "", row=0
        )
        
        tk.Label(
            prod_inner,
            text="Tipo pozione:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        
        self.combo_vel_tipo = ttk.Combobox(
            prod_inner,
            values=["Velocità I", "Velocità II"],
            width=14,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_vel_tipo.current(0)
        self.combo_vel_tipo.grid(row=1, column=1, pady=4, sticky="w")
        
        panel_prod.pack(padx=0, pady=(0, 8), fill="x")
        
        # === PREZZI ===
        panel_price, price_inner = self.make_panel(container, "Prezzi ingredienti (b)", "💰")
        
        self.entry_vel_lapis = self.make_labeled_entry(
            price_inner, "Lapis (1x):", "1.0", row=0
        )
        self.entry_vel_zucchero = self.make_labeled_entry(
            price_inner, "Zucchero (1x):", "1.0", row=1
        )
        self.entry_vel_blaze = self.make_labeled_entry(
            price_inner, "Blaze (1x):", "1.0", row=2
        )
        
        tk.Label(
            price_inner,
            text="(Core, carbone e boccette dalla tab Pozioni)",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 0))
        
        panel_price.pack(padx=0, pady=(0, 8), fill="x")
        
        # === VENDITA ===
        panel_sale, sale_inner = self.make_panel(container, "Vendita", "📈")
        
        self.entry_vel_prezzo = self.make_labeled_entry(
            sale_inner, "Prezzo vendita (b):", "", row=0
        )
        
        panel_sale.pack(padx=0, pady=(0, 8), fill="x")
        
        # === BOTTONE ===
        btn_container = tk.Frame(container, bg=BG_MAIN)
        btn_container.pack(pady=12)
        
        calc_btn = self.make_action_button(
            btn_container, "CALCOLA VELOCITÀ", self.do_calcola_velocita, "success", "🧮"
        )
        calc_btn.config(font=("Segoe UI", 12, "bold"), padx=24, pady=10)
        calc_btn.pack()
        
        # === RISULTATI ===
        self.make_result_area(container, "label_vel_preview", "text_vel_result")

# CODICE_TAB_MULTI.txt
# Questo è il codice da inserire dopo _build_tab_velocita()

    def _build_tab_multi(self):
        """Tab Calcolatrice Multi-Prodotto"""
        container = tk.Frame(self.tab_multi, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Info header
        info_frame = tk.Frame(container, bg=BG_CARD, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            info_frame,
            text="🧮 Calcolatrice Multi-Prodotto",
            font=SECTION_FONT,
            bg=BG_CARD,
            fg=ACCENT_LIGHT,
        ).pack(anchor="w")
        tk.Label(
            info_frame,
            text="Calcola materiali aggregati per produzioni multiple",
            font=SMALL_FONT,
            bg=BG_CARD,
            fg=FG_SUBTLE,
        ).pack(anchor="w", pady=(4, 0))
        
        # === AGGIUNGI PRODOTTO ===
        panel_add, add_inner = self.make_panel(container, "Aggiungi Prodotto", "➕")
        
        tk.Label(
            add_inner,
            text="Tipo prodotto:",
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        
        tipi_prodotti = get_tipi_prodotti_disponibili()
        self.combo_multi_tipo = ttk.Combobox(
            add_inner,
            values=[nome for _, nome in tipi_prodotti],
            width=30,
            state="readonly",
            font=LABEL_FONT,
        )
        self.combo_multi_tipo.current(0)
        self.combo_multi_tipo.grid(row=0, column=1, pady=4, sticky="w", columnspan=2)

        self.entry_multi_qty = self.make_labeled_entry(
            add_inner, "Quantità:", "10", row=1
        )
        
        self.entry_multi_prezzo = self.make_labeled_entry(
            add_inner, "Prezzo vendita (opz):", "", row=2
        )
        
        btn_aggiungi = self.make_action_button(
            add_inner, "Aggiungi alla lista", self.do_aggiungi_multi_prodotto, "primary", "➕"
        )
        btn_aggiungi.grid(row=3, column=0, columnspan=3, pady=8)
        
        panel_add.pack(padx=0, pady=(0, 8), fill="x")
        
        # === LISTA PRODUZIONE ===
        panel_lista, lista_inner = self.make_panel(container, "Lista Produzione", "📦")
        
        # Frame scrollabile per lista
        list_container = tk.Frame(lista_inner, bg=BG_CARD)
        list_container.pack(fill="both", expand=True)
        
        scrollbar_list = ttk.Scrollbar(list_container, style="Vertical.TScrollbar")
        scrollbar_list.pack(side="right", fill="y")
        
        self.multi_lista_text = tk.Text(
            list_container,
            height=8,
            font=LABEL_FONT,
            state="disabled",
            wrap="word",
            yscrollcommand=scrollbar_list.set,
            bg=BG_RESULT,
            fg=FG_TEXT,
            relief="flat",
            padx=10,
            pady=8,
        )
        self.multi_lista_text.pack(fill="both", expand=True)
        scrollbar_list.config(command=self.multi_lista_text.yview)
        
        # Bottoni azioni
        btn_frame = tk.Frame(lista_inner, bg=BG_CARD)
        btn_frame.pack(pady=8)
        
        self.make_action_button(
            btn_frame, "Svuota Tutto", self.do_svuota_multi_lista, "danger", "🗑️"
        ).pack(side="left", padx=4)
        
        self.make_action_button(
            btn_frame, "CALCOLA TOTALE", self.do_calcola_multi, "success", "🧮"
        ).config(font=("Segoe UI", 11, "bold"), padx=20, pady=8)
        self.make_action_button(
            btn_frame, "CALCOLA TOTALE", self.do_calcola_multi, "success", "🧮"
        ).pack(side="left", padx=4)
        
        panel_lista.pack(padx=0, pady=(0, 8), fill="both", expand=True)
        
        # === RISULTATI ===
        self.make_result_area(container, "label_multi_preview", "text_multi_result")
        
        # Inizializza lista prodotti
        self.multi_prodotti_lista = []

    def do_aggiungi_multi_prodotto(self):
        """Aggiungi prodotto alla lista"""
        try:
            tipo_nome = self.combo_multi_tipo.get()
            qty = float(self.entry_multi_qty.get())
            
            if qty <= 0:
                messagebox.showerror("Errore", "La quantità deve essere maggiore di 0")
                return
            
            # Trova tipo codice dal nome
            tipi = get_tipi_prodotti_disponibili()
            tipo_code = None
            for code, nome in tipi:
                if nome == tipo_nome:
                    tipo_code = code
                    break
            
            if not tipo_code:
                messagebox.showerror("Errore", "Tipo prodotto non valido")
                return
            
            # Prezzo vendita opzionale
            try:
                prezzo = float(self.entry_multi_prezzo.get())
            except:
                prezzo = None
            
            # Aggiungi alla lista
            prodotto = {
                'tipo': tipo_code,
                'nome': tipo_nome,
                'quantita': qty,
                'prezzo_vendita': prezzo
            }
            self.multi_prodotti_lista.append(prodotto)
            
            # Aggiorna visualizzazione
            self._aggiorna_lista_multi()
            
            # Reset campi
            self.entry_multi_qty.delete(0, tk.END)
            self.entry_multi_qty.insert(0, "10")
            self.entry_multi_prezzo.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi")
    
    def do_svuota_multi_lista(self):
        """Svuota la lista prodotti"""
        if self.multi_prodotti_lista and messagebox.askyesno(
            "Conferma", "Vuoi svuotare tutta la lista?"
        ):
            self.multi_prodotti_lista = []
            self._aggiorna_lista_multi()
            # Pulisci risultati
            self.label_multi_preview.config(text="💰 Aggiungi prodotti e calcola")
            self.text_multi_result.config(state="normal")
            self.text_multi_result.delete("1.0", tk.END)
            self.text_multi_result.config(state="disabled")
    
    def _aggiorna_lista_multi(self):
        """Aggiorna la visualizzazione della lista"""
        self.multi_lista_text.config(state="normal")
        self.multi_lista_text.delete("1.0", tk.END)
        
        if not self.multi_prodotti_lista:
            self.multi_lista_text.insert("1.0", "Lista vuota. Aggiungi prodotti sopra.")
        else:
            for i, prod in enumerate(self.multi_prodotti_lista, 1):
                prezzo_str = f" (vendita: {prod['prezzo_vendita']}b)" if prod['prezzo_vendita'] else ""
                line = f"{i}. {prod['quantita']:.0f}x {prod['nome']}{prezzo_str}\n"
                self.multi_lista_text.insert(tk.END, line)
        
        self.multi_lista_text.config(state="disabled")
    
    def do_calcola_multi(self):
        """Calcola materiali aggregati e costi"""
        if not self.multi_prodotti_lista:
            messagebox.showwarning("Attenzione", "Lista vuota! Aggiungi prodotti prima di calcolare.")
            return
        
        try:
            # Prepara prezzi base
            prezzi_base = {
                'core': float(self.entry_core.get()),
                'carbone': float(self.entry_carbone.get()),
                'boccette_per_1b': float(self.entry_boccette_per_b.get()),
                'spidereye': float(self.entry_spidereye.get()),
                'withering_dust': float(self.entry_withering_dust.get()),
                'brim': float(self.entry_brim.get()),
                'rotten': float(self.entry_rotten.get()),
                'revival': float(self.entry_revival.get()),
                'verdure_per_1b': float(self.entry_verdure_per_b.get()),
                'vasetti_per_1b': float(self.entry_vasetti_per_b.get()),
                'quartz': float(self.entry_ext_quartz.get()),
                'lapis': float(self.entry_vel_lapis.get()),
                'zucchero': float(self.entry_vel_zucchero.get()),
                'blaze': float(self.entry_vel_blaze.get()),
                # Prezzi elisir (lingotti)
                'tin': float(self.entry_price_tin.get() if hasattr(self, 'entry_price_tin') else 0),
                'copper': float(self.entry_price_cu.get() if hasattr(self, 'entry_price_cu') else 0),
                'iron': float(self.entry_price_fe.get() if hasattr(self, 'entry_price_fe') else 0),
                'gold': float(self.entry_price_au.get() if hasattr(self, 'entry_price_au') else 0),
                'diamond': float(self.entry_price_dia.get() if hasattr(self, 'entry_price_dia') else 0),
                # Ingredienti speciali elisir
                'membrana': float(self.entry_membrana.get() if hasattr(self, 'entry_membrana') else 0),
                'slime': float(self.entry_slime.get() if hasattr(self, 'entry_slime') else 0),
                'lost_soul': float(self.entry_lost_soul.get() if hasattr(self, 'entry_lost_soul') else 0),
                # Argento per rune (stesso prezzo del diamante)
                'silver': float(self.entry_price_dia.get() if hasattr(self, 'entry_price_dia') else 0),
            }
            
            # Calcola
            risultato = core_multi_prod(self.multi_prodotti_lista, prezzi_base)

            # DEBUG: Stampa risultato per diagnosi
            print("=== DEBUG MULTI-PRODOTTO ===")
            print(f"Materiali aggregati: {risultato['materiali_aggregati']}")
            print(f"Costi materiali: {risultato['costi_materiali']}")
            print(f"Costo totale: {risultato['costo_totale']}")
            print("============================")

            # Mostra preview
            preview = f"Totale: {risultato['costo_totale']:.2f}b"
            if risultato['profitto_netto']:
                preview += f"    •    Profitto: {risultato['profitto_netto']:.2f}b"
            self.label_multi_preview.config(text=f"💰 {preview}")
            
            # Mostra dettaglio
            output_lines = []
            output_lines.append("=" * 60)
            output_lines.append("CALCOLATRICE MULTI-PRODOTTO")
            output_lines.append("=" * 60)
            output_lines.append("")
            
            # Materiali aggregati
            output_lines.append("MATERIALI NECESSARI (AGGREGATI):")
            output_lines.append("-" * 60)
            for mat, qty in sorted(risultato['materiali_aggregati'].items()):
                costo = risultato['costi_materiali'].get(mat, None)
                if costo is not None:
                    output_lines.append(f"  • {mat:25s} {qty:8.2f} unità  ({costo:8.2f}b)")
                else:
                    # Materiale senza costo (opzione runa non selezionata)
                    output_lines.append(f"  • {mat:25s} {qty:8.2f} unità")
            
            output_lines.append("")
            output_lines.append("=" * 60)
            output_lines.append("RIEPILOGO FINANZIARIO")
            output_lines.append("=" * 60)
            output_lines.append(f"Costo totale materiali: {risultato['costo_totale']:10.2f}b")
            if risultato['ricavo_totale']:
                output_lines.append(f"Ricavo totale vendita:  {risultato['ricavo_totale']:10.2f}b")
                output_lines.append(f"Profitto netto:         {risultato['profitto_netto']:10.2f}b")
                margine = (risultato['profitto_netto'] / risultato['costo_totale']) * 100
                output_lines.append(f"Margine di profitto:    {margine:10.1f}%")
            
            output_lines.append("")
            output_lines.append("=" * 60)
            output_lines.append("DETTAGLIO PER PRODOTTO")
            output_lines.append("=" * 60)
            for det in risultato['dettaglio_prodotti']:
                output_lines.append("")
                output_lines.append(f"{det['nome']} (x{det['quantita']:.0f})")
                output_lines.append(f"  Costo: {det['costo']:.2f}b (unitario: {det['costo_unitario']:.2f}b)")
                if det['prezzo_vendita']:
                    output_lines.append(f"  Ricavo: {det['ricavo']:.2f}b")
                    output_lines.append(f"  Profitto: {det['profitto']:.2f}b")
            
            self.text_multi_result.config(state="normal")
            self.text_multi_result.delete("1.0", tk.END)
            self.text_multi_result.insert("1.0", "\n".join(output_lines))
            self.text_multi_result.config(state="disabled")
            
        except ValueError as e:
            messagebox.showerror("Errore", f"Controlla i prezzi nelle altre tab: {e}")


    # =========================
    #   FUNZIONI HELPER
    # =========================

    def _aggiorna_resina_da_pozioni(self):
        """Calcola il costo di 1 resina usando i parametri delle pozioni"""
        try:
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())
            
            if verdure_per_1b <= 0 or vasetti_per_1b <= 0:
                self.resina_var.set("")
                return
            
            costo_verdura = 1.0 / verdure_per_1b
            costo_vasetto = 1.0 / vasetti_per_1b
            costo_resina = (2.0 * costo_verdura + costo_vasetto) / 2.0
            
            self.resina_var.set(f"{costo_resina:.3f}")
        except (ValueError, AttributeError):
            self.resina_var.set("")

    def _aggiorna_brim_elisir(self):
        """Mostra nella tab Elisir il prezzo del Brim dalla tab Antidoti"""
        if not hasattr(self, "label_el_brim"):
            return
        try:
            val = self.entry_brim.get()
        except Exception:
            val = ""
        self.label_el_brim.config(text=val or "-")

    def _aggiorna_prezzi_danno(self):
        """Mostra nella tab Danno i prezzi dalle altre tab"""
        if not hasattr(self, "label_danno_spidereye"):
            return
        try:
            val_spider = self.entry_spidereye.get()
        except Exception:
            val_spider = ""
        self.label_danno_spidereye.config(text=val_spider or "-")
        
        try:
            val_core = self.entry_core.get()
        except Exception:
            val_core = ""
        self.label_danno_core.config(text=val_core or "-")
        
        try:
            val_carbone = self.entry_carbone.get()
        except Exception:
            val_carbone = ""
        self.label_danno_carbone.config(text=val_carbone or "-")
        
        try:
            val_boccette = self.entry_boccette_per_b.get()
        except Exception:
            val_boccette = ""
        self.label_danno_boccette.config(text=val_boccette or "-")

    # =========================
    #   CALCOLI
    # =========================

    def do_calcola_pozioni(self):
        try:
            num_pozioni = float(self.entry_pozioni.get())
            tier_reagente = self.combo_tier.get()
            tipo_calderone = self.combo_calderone.get()
            
            prezzo_reagente = float(self.entry_reagente.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            
            try:
                prezzo_vendita = float(self.entry_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None
            
            profilo_attivo = self.combo_profile.get().strip() or "(non salvato)"
            
            result = calcola_pozioni(
                num_pozioni,
                tier_reagente,
                tipo_calderone,
                prezzo_reagente,
                prezzo_core,
                prezzo_carbone,
                verdure_per_1b,
                vasetti_per_1b,
                boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
                profilo_attivo=profilo_attivo,
            )

            # Aggiorna con animazione
            self.update_result_with_fade(
                self.label_preview,
                self.text_result,
                result['preview_text'],
                result["output_lines"]
            )
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi: inserisci numeri validi!")

    def do_calcola_antidoti(self):
        try:
            self._aggiorna_resina_da_pozioni()
            
            num = float(self.entry_ant_num.get())
            tipo = self.combo_ant_calderone.get()
            
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            
            prezzo_brim = float(self.entry_brim.get())
            prezzo_rotten = float(self.entry_rotten.get())
            prezzo_revival = float(self.entry_revival.get())
            
            try:
                prezzo_vendita = float(self.entry_ant_prezzo.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_antidoti(
                num, tipo, prezzo_carbone, boccette_per_1b, vasetti_per_1b,
                verdure_per_1b, prezzo_brim, prezzo_rotten, prezzo_revival,
                prezzo_vendita=prezzo_vendita,
            )
            
            self.label_ant_preview.config(text=f"💰 {result['preview_text']}")
            self.text_ant_result.config(state="normal")
            self.text_ant_result.delete("1.0", tk.END)
            self.text_ant_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_ant_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi degli antidoti: inserisci numeri validi.")

    def do_calcola_revivify(self):
        try:
            num = float(self.entry_rev_num.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            prezzo_revival = float(self.entry_revival.get())
            
            try:
                prezzo_vendita = float(self.entry_rev_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_revivify(
                num=num,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_revival=prezzo_revival,
                prezzo_vendita=prezzo_vendita,
            )
            
            self.label_rev_preview.config(text=f"💰 {result['preview_text']}")
            self.text_rev_result.config(state="normal")
            self.text_rev_result.delete("1.0", tk.END)
            self.text_rev_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_rev_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Revivify: inserisci numeri validi.")

    def do_calcola_extinguish(self):
        try:
            num = float(self.entry_ext_num.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            prezzo_quartz = float(self.entry_ext_quartz.get())
            
            try:
                prezzo_vendita = float(self.entry_ext_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_extinguish(
                num=num,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_quartz=prezzo_quartz,
                prezzo_vendita=prezzo_vendita,
            )
            
            self.label_ext_preview.config(text=f"💰 {result['preview_text']}")
            self.text_ext_result.config(state="normal")
            self.text_ext_result.delete("1.0", tk.END)
            self.text_ext_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_ext_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Extinguish: inserisci numeri validi.")

    def do_calcola_danno(self):
        try:
            self._aggiorna_prezzi_danno()
            
            num = float(self.entry_danno_num.get())
            tipo = self.combo_danno_tipo.get()
            
            prezzo_spidereye = float(self.entry_spidereye.get())
            prezzo_withering_dust = float(self.entry_withering_dust.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            
            try:
                prezzo_vendita = float(self.entry_danno_prezzo_vendita.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_danno(
                num=num,
                tipo=tipo,
                prezzo_spidereye=prezzo_spidereye,
                prezzo_withering_dust=prezzo_withering_dust,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone,
                boccette_per_1b=boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
            )
            
            self.label_danno_preview.config(text=f"💰 {result['preview_text']}")
            self.text_danno_result.config(state="normal")
            self.text_danno_result.delete("1.0", tk.END)
            self.text_danno_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_danno_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Pozioni di Danno: inserisci numeri validi.")

    def do_calcola_elisir(self):
        try:
            num = float(self.entry_el_num.get())
            tipo = self.combo_el_tipo.get()
            
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            vasetti_per_1b = float(self.entry_vasetti_per_b.get())
            verdure_per_1b = float(self.entry_verdure_per_b.get())
            
            prezzo_brim = float(self.entry_brim.get())
            prezzo_spidereye = float(self.entry_spidereye.get())
            prezzo_membrana = float(self.entry_membrana.get())
            prezzo_slime = float(self.entry_slime.get())
            prezzo_lost_soul = float(self.entry_lost_soul.get())
            
            price_tin = float(self.entry_price_tin.get() or "0")
            price_cu = float(self.entry_price_cu.get() or "0")
            price_fe = float(self.entry_price_fe.get() or "0")
            price_au = float(self.entry_price_au.get() or "0")
            price_dia = float(self.entry_price_dia.get() or "0")
            
            try:
                prezzo_vendita = float(self.entry_el_prezzo.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_elisir(
                num=num, tipo=tipo, prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone, boccette_per_1b=boccette_per_1b,
                vasetti_per_1b=vasetti_per_1b, verdure_per_1b=verdure_per_1b,
                prezzo_brim=prezzo_brim, prezzo_spidereye=prezzo_spidereye,
                prezzo_membrana=prezzo_membrana, prezzo_slime=prezzo_slime,
                prezzo_lost_soul=prezzo_lost_soul, price_tin=price_tin,
                price_cu=price_cu, price_fe=price_fe, price_au=price_au,
                price_dia=price_dia, prezzo_vendita=prezzo_vendita,
            )
            
            self.label_el_preview.config(text=f"💰 {result['preview_text']}")
            self.text_el_result.config(state="normal")
            self.text_el_result.delete("1.0", tk.END)
            self.text_el_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_el_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi degli elisir: inserisci numeri validi.")

    def do_calcola_rune(self):
        try:
            tipo = self.combo_rune_tipo.get().strip() or "Maghi"
            
            q_pepite = {}
            for met, entry in self.entry_rune_pepite.items():
                txt = entry.get().strip()
                val = float(txt.replace(",", ".")) if txt else 0.0
                q_pepite[met] = val
            
            result = core_rune_diretto(tipo, q_pepite)
            
            self.label_rune_preview.config(text=f"🔮 {result['preview_text']}")
            self.text_rune_result.config(state="normal")
            self.text_rune_result.delete("1.0", tk.END)
            self.text_rune_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_rune_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla le quantità di pepite: inserisci solo numeri.")
        except Exception as e:
            messagebox.showerror("❌ Errore", f"Errore durante il calcolo delle rune:\n{e}")

    def do_calcola_velocita(self):
        try:
            num = float(self.entry_vel_num.get())
            tipo = self.combo_vel_tipo.get()
            
            prezzo_lapis = float(self.entry_vel_lapis.get())
            prezzo_zucchero = float(self.entry_vel_zucchero.get())
            prezzo_blaze = float(self.entry_vel_blaze.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = float(self.entry_carbone.get())
            boccette_per_1b = float(self.entry_boccette_per_b.get())
            
            try:
                prezzo_vendita = float(self.entry_vel_prezzo.get())
            except ValueError:
                prezzo_vendita = None
            
            result = core_calcola_velocita(
                num=num, tipo=tipo,
                prezzo_lapis=prezzo_lapis, prezzo_zucchero=prezzo_zucchero,
                prezzo_blaze=prezzo_blaze, prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone, boccette_per_1b=boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
            )
            
            self.label_vel_preview.config(text=f"💰 {result['preview_text']}")
            self.text_vel_result.config(state="normal")
            self.text_vel_result.delete("1.0", tk.END)
            self.text_vel_result.insert("1.0", "\n".join(result["output_lines"]))
            self.text_vel_result.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Velocità: inserisci numeri validi.")

    # =========================
    #   GESTIONE PROFILI
    # =========================

    def apply_profile(self):
        """Carica i prezzi dal profilo selezionato"""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("❌ Errore", "Seleziona o scrivi un nome profilo.")
            return
        
        if name not in self.profiles:
            messagebox.showerror("❌ Errore", f"Profilo '{name}' non trovato.")
            return
        
        p = self.profiles[name]
        
        self.entry_reagente.delete(0, tk.END)
        self.entry_reagente.insert(0, p.get("prezzo_reagente", "1.5"))
        
        self.entry_core.delete(0, tk.END)
        self.entry_core.insert(0, p.get("prezzo_core", "1.0"))
        
        self.entry_carbone.delete(0, tk.END)
        self.entry_carbone.insert(0, p.get("prezzo_carbone", "1.5"))
        
        self.entry_verdure_per_b.delete(0, tk.END)
        self.entry_verdure_per_b.insert(0, p.get("verdure_per_1b", "3"))
        
        self.entry_vasetti_per_b.delete(0, tk.END)
        self.entry_vasetti_per_b.insert(0, p.get("vasetti_per_1b", "15"))
        
        self.entry_boccette_per_b.delete(0, tk.END)
        self.entry_boccette_per_b.insert(0, p.get("boccette_per_1b", "14"))
        
        self._aggiorna_resina_da_pozioni()
        messagebox.showinfo("✅ Profilo caricato", f"Profilo '{name}' applicato.")

    def save_profile(self):
        """Salva/aggiorna il profilo con i valori attuali"""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("❌ Errore", "Inserisci un nome profilo da salvare.")
            return
        
        new_prof = {
            "prezzo_reagente": self.entry_reagente.get(),
            "prezzo_core": self.entry_core.get(),
            "prezzo_carbone": self.entry_carbone.get(),
            "verdure_per_1b": self.entry_verdure_per_b.get(),
            "vasetti_per_1b": self.entry_vasetti_per_b.get(),
            "boccette_per_1b": self.entry_boccette_per_b.get()
        }
        
        self.profiles[name] = new_prof
        save_all_profiles(self.profiles)
        
        self.combo_profile["values"] = list(self.profiles.keys())
        messagebox.showinfo("✅ Profilo salvato", f"Profilo '{name}' salvato.")

    def rename_profile(self):
        """Rinomina il profilo attuale"""
        old_name = self.combo_profile.get().strip()
        if not old_name:
            messagebox.showerror("❌ Errore", "Seleziona il profilo da rinominare.")
            return
        
        if old_name not in self.profiles:
            messagebox.showerror("❌ Errore", f"Profilo '{old_name}' non esiste.")
            return
        
        # Finestra di dialogo per rinomina
        rename_win = tk.Toplevel(self.root)
        rename_win.title("✏️ Rinomina profilo")
        rename_win.configure(bg=BG_MAIN)
        rename_win.resizable(False, False)
        rename_win.geometry("350x150")
        rename_win.transient(self.root)
        rename_win.grab_set()
        
        # Centra la finestra
        rename_win.update_idletasks()
        x = (rename_win.winfo_screenwidth() // 2) - (175)
        y = (rename_win.winfo_screenheight() // 2) - (75)
        rename_win.geometry(f"+{x}+{y}")
        
        tk.Label(
            rename_win,
            text=f"Nuovo nome per '{old_name}':",
            font=LABEL_FONT,
            bg=BG_MAIN,
            fg=FG_TEXT
        ).pack(padx=20, pady=(20, 8), anchor="w")
        
        new_name_entry = tk.Entry(
            rename_win,
            width=30,
            font=LABEL_FONT,
            bg=BG_INPUT,
            fg=FG_TEXT,
            insertbackground=ACCENT_LIGHT,
            relief="flat",
            highlightthickness=2,
            highlightbackground=BORDER_SUBTLE,
            highlightcolor=ACCENT,
        )
        new_name_entry.pack(padx=20, pady=(0, 15))
        new_name_entry.focus_set()
        
        def conferma_rinomina():
            new_name = new_name_entry.get().strip()
            if not new_name:
                messagebox.showerror("❌ Errore", "Inserisci un nuovo nome.")
                return
            
            if new_name in self.profiles and new_name != old_name:
                if not messagebox.askyesno(
                    "⚠️ Conferma",
                    f"Profilo '{new_name}' esiste già. Sovrascrivere?"
                ):
                    return
            
            self.profiles[new_name] = self.profiles[old_name]
            if new_name != old_name:
                del self.profiles[old_name]
            
            save_all_profiles(self.profiles)
            self.combo_profile["values"] = list(self.profiles.keys())
            self.combo_profile.set(new_name)
            
            messagebox.showinfo("✅ Fatto", f"Profilo rinominato in '{new_name}'.")
            rename_win.destroy()
        
        btn_frame = tk.Frame(rename_win, bg=BG_MAIN)
        btn_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        self.make_action_button(
            btn_frame, "Conferma", conferma_rinomina, "primary", "✓"
        ).pack(side="left")
        
        self.make_action_button(
            btn_frame, "Annulla", rename_win.destroy, "secondary", "✕"
        ).pack(side="right")

    def delete_profile(self):
        """Elimina definitivamente il profilo selezionato"""
        name = self.combo_profile.get().strip()
        if not name:
            messagebox.showerror("❌ Errore", "Seleziona il profilo da eliminare.")
            return
        
        if name not in self.profiles:
            messagebox.showerror("❌ Errore", f"Profilo '{name}' non esiste.")
            return
        
        if not messagebox.askyesno(
            "⚠️ Conferma eliminazione",
            f"Eliminare definitivamente il profilo '{name}'?\n"
            "Questa azione non può essere annullata."
        ):
            return
        
        del self.profiles[name]
        save_all_profiles(self.profiles)
        
        nuovi_nomi = list(self.profiles.keys())
        self.combo_profile["values"] = nuovi_nomi
        
        if nuovi_nomi:
            self.combo_profile.set(nuovi_nomi[0])
        else:
            self.combo_profile.set("")
        
        messagebox.showinfo("✅ Eliminato", f"Profilo '{name}' rimosso.")

    # =========================
    #   SALVATAGGIO CONFIG
    # =========================

    def save_config(self):
        """Salva la configurazione corrente"""
        data = {
            # Pozioni
            "num_pozioni": self.entry_pozioni.get(),
            "tier": self.combo_tier.get(),
            "calderone": self.combo_calderone.get(),
            "prezzo_reagente": self.entry_reagente.get(),
            "prezzo_core": self.entry_core.get(),
            "prezzo_carbone": self.entry_carbone.get(),
            "verdure_per_1b": self.entry_verdure_per_b.get(),
            "vasetti_per_1b": self.entry_vasetti_per_b.get(),
            "boccette_per_1b": self.entry_boccette_per_b.get(),
            "prezzo_vendita_pozioni": self.entry_prezzo_vendita.get(),
            "sconto_pozioni": self.entry_sconto_perc.get(),
            
            # Antidoti
            "ant_num": getattr(self, 'entry_ant_num', tk.Entry()).get() if hasattr(self, 'entry_ant_num') else "",
            "prezzo_brim": self.entry_brim.get() if hasattr(self, 'entry_brim') else "",
            "prezzo_rotten": self.entry_rotten.get() if hasattr(self, 'entry_rotten') else "",
            "prezzo_revival": self.entry_revival.get() if hasattr(self, 'entry_revival') else "",
            "prezzo_vendita_antidoti": self.entry_ant_prezzo.get() if hasattr(self, 'entry_ant_prezzo') else "",
            
            # Revivify
            "rev_num": self.entry_rev_num.get() if hasattr(self, 'entry_rev_num') else "",
            "rev_prezzo_vendita": self.entry_rev_prezzo_vendita.get() if hasattr(self, 'entry_rev_prezzo_vendita') else "",
            
            # Extinguish
            "ext_num": self.entry_ext_num.get() if hasattr(self, 'entry_ext_num') else "",
            "ext_quartz": self.entry_ext_quartz.get() if hasattr(self, 'entry_ext_quartz') else "",
            "ext_prezzo_vendita": self.entry_ext_prezzo_vendita.get() if hasattr(self, 'entry_ext_prezzo_vendita') else "",
            
            # Danno
            "danno_num": self.entry_danno_num.get() if hasattr(self, 'entry_danno_num') else "",
            "danno_tipo": self.combo_danno_tipo.get() if hasattr(self, 'combo_danno_tipo') else "",
            "danno_withering_dust": self.entry_withering_dust.get() if hasattr(self, 'entry_withering_dust') else "",
            "danno_prezzo_vendita": self.entry_danno_prezzo_vendita.get() if hasattr(self, 'entry_danno_prezzo_vendita') else "",
            
            # Elisir
            "elisir_num": self.entry_el_num.get() if hasattr(self, 'entry_el_num') else "",
            "elisir_tipo": self.combo_el_tipo.get() if hasattr(self, 'combo_el_tipo') else "",
            "elisir_spidereye": self.entry_spidereye.get() if hasattr(self, 'entry_spidereye') else "",
            "elisir_membrana": self.entry_membrana.get() if hasattr(self, 'entry_membrana') else "",
            "elisir_slime": self.entry_slime.get() if hasattr(self, 'entry_slime') else "",
            "elisir_lost_soul": self.entry_lost_soul.get() if hasattr(self, 'entry_lost_soul') else "",
            "elisir_price_tin": self.entry_price_tin.get() if hasattr(self, 'entry_price_tin') else "",
            "elisir_price_cu": self.entry_price_cu.get() if hasattr(self, 'entry_price_cu') else "",
            "elisir_price_fe": self.entry_price_fe.get() if hasattr(self, 'entry_price_fe') else "",
            "elisir_price_au": self.entry_price_au.get() if hasattr(self, 'entry_price_au') else "",
            "elisir_price_dia": self.entry_price_dia.get() if hasattr(self, 'entry_price_dia') else "",
            "elisir_prezzo_vendita": self.entry_el_prezzo.get() if hasattr(self, 'entry_el_prezzo') else "",
            
            # Velocità
            "vel_num": self.entry_vel_num.get() if hasattr(self, 'entry_vel_num') else "",
            "vel_tipo": self.combo_vel_tipo.get() if hasattr(self, 'combo_vel_tipo') else "",
            "vel_lapis": self.entry_vel_lapis.get() if hasattr(self, 'entry_vel_lapis') else "",
            "vel_zucchero": self.entry_vel_zucchero.get() if hasattr(self, 'entry_vel_zucchero') else "",
            "vel_blaze": self.entry_vel_blaze.get() if hasattr(self, 'entry_vel_blaze') else "",
            "vel_prezzo_vendita": self.entry_vel_prezzo.get() if hasattr(self, 'entry_vel_prezzo') else "",
            
            # Rune
            "rune_tipo": self.combo_rune_tipo.get() if hasattr(self, 'combo_rune_tipo') else "",
            "rune_pepite": {
                met: entry.get()
                for met, entry in getattr(self, 'entry_rune_pepite', {}).items()
            },
        }
        
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Errore salvataggio config:", e)

    def load_config(self):
        """Carica la configurazione salvata"""
        if not os.path.exists(CONFIG_FILE):
            return
        
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("Errore lettura config:", e)
            return
        
        # Helper per caricare un valore
        def load_entry(key, widget_name):
            if key in data and hasattr(self, widget_name):
                w = getattr(self, widget_name)
                w.delete(0, tk.END)
                w.insert(0, data[key])
        
        # Pozioni
        load_entry("num_pozioni", "entry_pozioni")
        if "tier" in data:
            self.combo_tier.set(data["tier"])
        if "calderone" in data:
            self.combo_calderone.set(data["calderone"])
        
        load_entry("prezzo_reagente", "entry_reagente")
        load_entry("prezzo_core", "entry_core")
        load_entry("prezzo_carbone", "entry_carbone")
        load_entry("verdure_per_1b", "entry_verdure_per_b")
        load_entry("vasetti_per_1b", "entry_vasetti_per_b")
        load_entry("boccette_per_1b", "entry_boccette_per_b")
        load_entry("prezzo_vendita_pozioni", "entry_prezzo_vendita")
        load_entry("sconto_pozioni", "entry_sconto_perc")
        
        # Antidoti
        load_entry("ant_num", "entry_ant_num")
        load_entry("prezzo_brim", "entry_brim")
        load_entry("prezzo_rotten", "entry_rotten")
        load_entry("prezzo_revival", "entry_revival")
        load_entry("prezzo_vendita_antidoti", "entry_ant_prezzo")
        
        # Revivify
        load_entry("rev_num", "entry_rev_num")
        load_entry("rev_prezzo_vendita", "entry_rev_prezzo_vendita")
        
        # Extinguish
        load_entry("ext_num", "entry_ext_num")
        load_entry("ext_quartz", "entry_ext_quartz")
        load_entry("ext_prezzo_vendita", "entry_ext_prezzo_vendita")
        
        # Danno
        load_entry("danno_num", "entry_danno_num")
        if "danno_tipo" in data and hasattr(self, 'combo_danno_tipo'):
            self.combo_danno_tipo.set(data["danno_tipo"])
        load_entry("danno_withering_dust", "entry_withering_dust")
        load_entry("danno_prezzo_vendita", "entry_danno_prezzo_vendita")
        
        # Elisir
        load_entry("elisir_num", "entry_el_num")
        if "elisir_tipo" in data and hasattr(self, 'combo_el_tipo'):
            self.combo_el_tipo.set(data["elisir_tipo"])
        load_entry("elisir_spidereye", "entry_spidereye")
        load_entry("elisir_membrana", "entry_membrana")
        load_entry("elisir_slime", "entry_slime")
        load_entry("elisir_lost_soul", "entry_lost_soul")
        load_entry("elisir_price_tin", "entry_price_tin")
        load_entry("elisir_price_cu", "entry_price_cu")
        load_entry("elisir_price_fe", "entry_price_fe")
        load_entry("elisir_price_au", "entry_price_au")
        load_entry("elisir_price_dia", "entry_price_dia")
        load_entry("elisir_prezzo_vendita", "entry_el_prezzo")
        
        # Velocità
        load_entry("vel_num", "entry_vel_num")
        if "vel_tipo" in data and hasattr(self, 'combo_vel_tipo'):
            self.combo_vel_tipo.set(data["vel_tipo"])
        load_entry("vel_lapis", "entry_vel_lapis")
        load_entry("vel_zucchero", "entry_vel_zucchero")
        load_entry("vel_blaze", "entry_vel_blaze")
        load_entry("vel_prezzo_vendita", "entry_vel_prezzo")
        
        # Rune
        if "rune_tipo" in data and hasattr(self, 'combo_rune_tipo'):
            self.combo_rune_tipo.set(data["rune_tipo"])
        if "rune_pepite" in data and hasattr(self, 'entry_rune_pepite'):
            for met, val in data["rune_pepite"].items():
                if met in self.entry_rune_pepite:
                    e = self.entry_rune_pepite[met]
                    e.delete(0, tk.END)
                    e.insert(0, val)
        
        # Aggiorna valori calcolati
        try:
            self._aggiorna_resina_da_pozioni()
        except Exception:
            pass
        try:
            self._aggiorna_brim_elisir()
        except Exception:
            pass


def run_app():
    """Avvia l'applicazione"""
    root = tk.Tk()
    
    # Imposta icona se disponibile
    try:
        # Su Windows potresti avere un file .ico
        # root.iconbitmap("icon.ico")
        pass
    except:
        pass
    
    app = ElysiumPozioniApp(root)
    root.mainloop()
