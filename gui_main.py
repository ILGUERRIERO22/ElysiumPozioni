# gui_main.py
# Versione 4.0 - Ricette centralizzate e GUI modulare

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageTk

from config_app import (
    APP_NAME, APP_VERSION, APP_AUTHOR,
    BG_MAIN, BG_PANEL, BG_CARD, BG_RESULT, BG_INPUT,
    FG_TEXT, FG_SUBTLE, FG_BRIGHT,
    ACCENT, ACCENT_HOVER, ACCENT_LIGHT, ACCENT_GLOW,
    SECONDARY, SECONDARY_HOVER,
    SUCCESS, SUCCESS_HOVER,
    DANGER_BG, DANGER_BG_HOVER, DANGER_BG_ACTIVE,
    GOLD, GOLD_HOVER,
    BORDER_SUBTLE, BORDER_ACCENT, INPUT_ERROR, LOSS_BG, LOSS_FG,
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
from calcolo_riduzione import calcola_pozione_riduzione as core_calcola_riduzione
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
        "• Supporto calderoni Terracotta / Rame / Ferro / Oro / Diamante / Smeraldo\n"
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

        # Carica icone materiali
        self.icons = self._load_icons()

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

    def _load_icons(self):
        """Carica le icone dei materiali dalla cartella icon/"""
        icons = {}
        icon_mapping = {
            # Lingotti
            'ferro': 'Iron_Ingot_JE3_BE2.png',
            'oro': 'Gold_Ingot_JE4_BE2.png',
            'rame': 'Copper_Ingot_JE2_BE1.webp',
            # Pepite
            'pepita_ferro': 'Iron_Nugget_JE1_BE1.png',
            'pepita_oro': 'Gold_nugget.png',
            'pepita_rame': 'copper_nugget.png',
            # Reagenti
            'brim': 'Brim.png',
            'phantom': 'Phantom_Membrane_JE1_BE1.webp',
            'blaze': 'Blaze_Powder_JE2_BE1.webp',
            'rotten': 'Rotten_Flesh_JE3_BE2.webp',
            'spidereye': 'Spider_Eye_JE2_BE2.webp',
            'slimeball': 'Slimeball_JE2_BE2.webp',
            'quarzo': 'Nether_Quartz_JE2_BE2.webp',
            'lapis': 'Lapis_Lazuli_JE2_BE2.webp',
            'zucchero': 'Sugar_JE2_BE2.webp',
            'lost_soul': 'soul.png',
            # Materiali base
            'carbone': 'Coal_JE4_BE3.webp',
            'boccetta': 'Water_Bottle_JE2_BE2.png',
            'verdure': 'verdure.png',
            # Pozioni
            'pozione_danno': 'pozione_danno.png'
        }

        # Percorso base per le icone - cerca sia nella directory corrente che nella directory dell'eseguibile
        base_dirs = [
            os.path.join(os.path.dirname(__file__), 'icon'),  # Directory del file .py
            os.path.join(os.getcwd(), 'icon'),  # Directory di lavoro
            'icon'  # Percorso relativo
        ]

        for material, filename in icon_mapping.items():
            icon_loaded = False
            for base_dir in base_dirs:
                icon_path = os.path.join(base_dir, filename)
                if os.path.exists(icon_path):
                    try:
                        # Carica l'icona
                        img = Image.open(icon_path)

                        # Converti in RGBA per gestire la trasparenza
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')

                        # Se l'immagine ha uno sfondo bianco, prova a renderlo trasparente
                        # Questo funziona per icone Minecraft-style con sfondo bianco uniforme
                        datas = img.getdata()
                        newData = []
                        for item in datas:
                            # Cambia tutti i pixel quasi-bianchi in trasparente
                            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                                newData.append((255, 255, 255, 0))
                            else:
                                newData.append(item)
                        img.putdata(newData)

                        # Ridimensiona l'icona
                        img = img.resize((20, 20), Image.Resampling.LANCZOS)
                        icons[material] = ImageTk.PhotoImage(img)
                        icon_loaded = True
                        break
                    except Exception as e:
                        print(f"Errore caricamento icona {material}: {e}")

            if not icon_loaded:
                print(f"Icona non trovata per {material}")

        return icons

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
        
        # Mouse wheel scrolling con controllo intelligente del widget
        def _on_mousewheel(event):
            # Ottieni il widget sotto il mouse
            widget = event.widget

            # Blocca scroll se il mouse è su certi widget
            widget_class = widget.winfo_class()

            # Non scrollare se siamo su combobox popup o Text widget con scrollbar
            if widget_class in ('Listbox', 'TCombobox', 'Toplevel'):
                return

            # Se siamo su un Text widget, non scrollare il canvas principale
            if widget_class == 'Text':
                return

            # Altrimenti scrolla il canvas principale
            try:
                self.outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass
            return "break"

        # Salva il riferimento al handler
        self._mousewheel_handler = _on_mousewheel

        # Bind globale con controllo intelligente
        self.root.bind_all("<MouseWheel>", self._mousewheel_handler)
        
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
        self.tab_riduzione = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_multi = tk.Frame(self.notebook, bg=BG_MAIN)
        self.tab_spesa  = tk.Frame(self.notebook, bg=BG_MAIN)

        # Aggiungi tabs con solo icone
        self.notebook.add(self.tab_pozioni, text="🧪")
        self.notebook.add(self.tab_antidoti, text="💊")
        self.notebook.add(self.tab_revivify, text="✨")
        self.notebook.add(self.tab_extinguish, text="🔥")
        self.notebook.add(self.tab_danno, text="⚔️")
        self.notebook.add(self.tab_rune, text="🔮")
        self.notebook.add(self.tab_elisir, text="💎")
        self.notebook.add(self.tab_velocita, text="⚡")
        self.notebook.add(self.tab_riduzione, text="🔻")
        self.notebook.add(self.tab_multi, text="🧮")
        self.notebook.add(self.tab_spesa,  text="🛒")

        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Animazione cambio tab
        self.current_tab = 0
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

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
            8: "Riduzione",
            9: "Multi-Prodotto",
            10: "Lista della Spesa"
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

    def _on_tab_change(self, event):
        """Gestisce cambio tab con animazione slide-fade"""
        try:
            new_tab = self.notebook.index(self.notebook.select())

            # Determina direzione
            direction = "right" if new_tab > self.current_tab else "left"

            # Applica slide-fade effect al nuovo tab
            current_frame = self.notebook.nametowidget(self.notebook.select())

            # Animazione slide-fade sul tab selezionato
            self.animator.slide_fade_tab(current_frame, direction=direction, duration=150)

            # Aggiorna indice corrente
            self.current_tab = new_tab
        except Exception as e:
            # Fallback silenzioso se l'animazione fallisce
            pass

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
                          hint_text="", width=ENTRY_WIDTH, icon_key=None, allow_empty=False):
        """Crea una coppia label + entry con stile uniforme e icona opzionale"""
        # Frame per label con icona
        label_frame = tk.Frame(parent, bg=BG_CARD)
        label_frame.grid(row=row, column=0, sticky="e", padx=(0, 8), pady=4)

        # Aggiungi icona se disponibile
        if icon_key and icon_key in self.icons:
            icon_label = tk.Label(
                label_frame,
                image=self.icons[icon_key],
                bg=BG_CARD
            )
            icon_label.pack(side="left", padx=(0, 4))

        # Label di testo
        tk.Label(
            label_frame,
            text=label_text,
            font=LABEL_FONT,
            bg=BG_CARD,
            fg=FG_TEXT,
        ).pack(side="left")

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
        self._bind_numeric_validation(entry, allow_empty)

        if hint_text:
            tk.Label(
                parent,
                text=hint_text,
                font=SMALL_FONT,
                bg=BG_CARD,
                fg=FG_SUBTLE,
            ).grid(row=row, column=2, sticky="w", padx=(8, 0))

        return entry

    def _validate_entry(self, entry, allow_empty=False):
        """Valida un campo numerico e aggiorna il colore del bordo."""
        val = entry.get().strip()
        if val == "":
            is_valid = allow_empty
        else:
            try:
                float(val)
                is_valid = True
            except ValueError:
                is_valid = False
        entry.config(
            highlightbackground=BORDER_SUBTLE if is_valid else INPUT_ERROR,
            highlightcolor=ACCENT if is_valid else INPUT_ERROR,
        )
        return is_valid

    def _bind_numeric_validation(self, entry, allow_empty=False):
        """Lega la validazione numerica a un campo entry."""
        validate = lambda e=None: self._validate_entry(entry, allow_empty)
        entry.bind("<KeyRelease>", validate, add="+")
        entry.bind("<FocusOut>",   validate, add="+")

    def update_result_with_fade(self, preview_label, text_widget, preview_text, output_lines):
        """Aggiorna risultati con effetto fade e icone inline"""
        # Pulse effetto sul preview
        original_bg = preview_label.cget('bg')
        preview_label.config(bg=ACCENT_GLOW)
        self.root.after(200, lambda: preview_label.config(bg=original_bg))

        # Aggiorna testo con icone
        preview_label.config(text=f"💰 {preview_text}")
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)

        # Inserisci testo riga per riga con icone
        self._insert_text_with_icons(text_widget, output_lines)

        text_widget.config(state="disabled")

    def _insert_text_with_icons(self, text_widget, output_lines):
        """Inserisce testo con icone inline per i materiali"""
        # Mapping parole chiave -> icone (case insensitive)
        keyword_icons = {
            'ferro': 'ferro',
            'oro': 'oro',
            'rame': 'rame',
            'carbone': 'carbone',
            'carbonella': 'carbone',
            'boccett': 'boccetta',  # Cattura sia "boccetta" che "boccette"
            'verdure': 'verdure',
            'brim': 'brim',
            'phantom': 'phantom',
            'blaze': 'blaze',
            'carne marcia': 'rotten',
            'rotten': 'rotten',
            'ragno': 'spidereye',
            'spider': 'spidereye',
            'slime': 'slimeball',
            'quarzo': 'quarzo',
            'lapis': 'lapis',
            'zucchero': 'zucchero',
            'lost soul': 'lost_soul',
            'soul': 'lost_soul',
        }

        for line in output_lines:
            line_lower = line.lower()
            icon_inserted = False

            # Cerca keyword nella riga
            for keyword, icon_key in keyword_icons.items():
                if keyword in line_lower and icon_key in self.icons:
                    # Trova la posizione della keyword
                    idx = line_lower.find(keyword)

                    # Inserisci testo prima della keyword
                    if idx > 0:
                        text_widget.insert(tk.END, line[:idx])

                    # Inserisci icona
                    text_widget.image_create(tk.END, image=self.icons[icon_key])
                    text_widget.insert(tk.END, " ")

                    # Inserisci resto della riga
                    text_widget.insert(tk.END, line[idx:] + "\n")
                    icon_inserted = True
                    break

            # Se non c'è icona, inserisci normalmente
            if not icon_inserted:
                text_widget.insert(tk.END, line + "\n")


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

        # Blocca scroll su combobox per evitare scroll della finestra principale
        self._block_combobox_scroll(combo)

        return combo

    def _block_combobox_scroll(self, combo):
        """Blocca lo scroll del mouse su una combobox per evitare scroll indesiderato"""
        # Con il nuovo sistema Enter/Leave sul canvas, non serve fare nulla qui
        # Lo scroll funziona solo quando il mouse è sul canvas
        pass

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
        """Costruisce tutte le tab (ogni tab è definita nel proprio modulo tabs/)"""
        from tabs import (
            tab_pozioni, tab_antidoti, tab_revivify, tab_extinguish,
            tab_danno, tab_elisir, tab_rune, tab_velocita, tab_riduzione, tab_multi,
            tab_spesa,
        )
        tab_pozioni.build(self)
        tab_antidoti.build(self)
        tab_revivify.build(self)
        tab_extinguish.build(self)
        tab_danno.build(self)
        tab_elisir.build(self)
        tab_rune.build(self)
        tab_velocita.build(self)
        tab_riduzione.build(self)
        tab_multi.build(self)
        tab_spesa.build(self)

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
                'reagente': float(self.entry_reagente.get()),
                # Normalizzato a equivalente Carbone: i calcoli usano sempre 12 carbonella/blocco
                'carbone': self._get_prezzo_carbone_norm(),
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
                # Riduzione
                'fungo_marrone': float(self.entry_rid_fungo.get() if hasattr(self, 'entry_rid_fungo') else 0),
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
            self._insert_text_with_icons(self.text_multi_result, output_lines)
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

    def _aggiorna_prezzi_riduzione(self):
        """Mostra nella tab Riduzione i prezzi dalle altre tab"""
        # Slimeball dalla tab Elisir
        if hasattr(self, "label_rid_slime"):
            try:
                val = self.entry_slime.get()
            except Exception:
                val = ""
            self.label_rid_slime.config(text=val or "-")

        # Core dalla tab Pozioni
        if hasattr(self, "label_rid_core"):
            try:
                val = self.entry_core.get()
            except Exception:
                val = ""
            self.label_rid_core.config(text=val or "-")

        # Carbone dalla tab Pozioni
        if hasattr(self, "label_rid_carbone"):
            try:
                val = self.entry_carbone.get()
            except Exception:
                val = ""
            self.label_rid_carbone.config(text=val or "-")

        # Boccette dalla tab Pozioni
        if hasattr(self, "label_rid_boccette"):
            try:
                val = self.entry_boccette_per_b.get()
            except Exception:
                val = ""
            self.label_rid_boccette.config(text=val or "-")

    def _aggiorna_prezzi_velocita(self):
        """Mostra nella tab Velocità i prezzi dalle altre tab"""
        # Core dalla tab Pozioni
        if hasattr(self, "label_vel_core"):
            try:
                val = self.entry_core.get()
            except Exception:
                val = ""
            self.label_vel_core.config(text=val or "-")

        # Carbone dalla tab Pozioni
        if hasattr(self, "label_vel_carbone"):
            try:
                val = self.entry_carbone.get()
            except Exception:
                val = ""
            self.label_vel_carbone.config(text=val or "-")

        # Boccette dalla tab Pozioni
        if hasattr(self, "label_vel_boccette"):
            try:
                val = self.entry_boccette_per_b.get()
            except Exception:
                val = ""
            self.label_vel_boccette.config(text=val or "-")

    def _aggiorna_prezzi_antidoti(self):
        """Mostra nella tab Antidoti i prezzi dalle altre tab"""
        # Core dalla tab Pozioni
        if hasattr(self, "label_ant_core"):
            try:
                val = self.entry_core.get()
            except Exception:
                val = ""
            self.label_ant_core.config(text=val or "-")

        # Carbone dalla tab Pozioni
        if hasattr(self, "label_ant_carbone"):
            try:
                val = self.entry_carbone.get()
            except Exception:
                val = ""
            self.label_ant_carbone.config(text=val or "-")

        # Boccette dalla tab Pozioni
        if hasattr(self, "label_ant_boccette"):
            try:
                val = self.entry_boccette_per_b.get()
            except Exception:
                val = ""
            self.label_ant_boccette.config(text=val or "-")

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

    def _aggiorna_prezzi_revivify(self):
        """Mostra nella tab Revivify i prezzi dalle altre tab"""
        # Revival star dalla tab Pozioni
        if hasattr(self, "label_rev_revival"):
            try:
                val = self.entry_revival.get()
            except Exception:
                val = ""
            self.label_rev_revival.config(text=val or "-")

        # Core dalla tab Pozioni
        if hasattr(self, "label_rev_core"):
            try:
                val = self.entry_core.get()
            except Exception:
                val = ""
            self.label_rev_core.config(text=val or "-")

        # Carbone dalla tab Pozioni
        if hasattr(self, "label_rev_carbone"):
            try:
                val = self.entry_carbone.get()
            except Exception:
                val = ""
            self.label_rev_carbone.config(text=val or "-")

        # Boccette dalla tab Pozioni
        if hasattr(self, "label_rev_boccette"):
            try:
                val = self.entry_boccette_per_b.get()
            except Exception:
                val = ""
            self.label_rev_boccette.config(text=val or "-")

    def _aggiorna_prezzi_elisir(self):
        """Mostra nella tab Elisir i prezzi dalle altre tab"""
        # Carbone dalla tab Pozioni
        if hasattr(self, "label_el_carbone"):
            try:
                val = self.entry_carbone.get()
            except Exception:
                val = ""
            self.label_el_carbone.config(text=val or "-")

        # Boccette dalla tab Pozioni
        if hasattr(self, "label_el_boccette"):
            try:
                val = self.entry_boccette_per_b.get()
            except Exception:
                val = ""
            self.label_el_boccette.config(text=val or "-")

    # =========================
    #   CALCOLI
    # =========================

    def _get_prezzo_carbone_norm(self) -> float:
        """Normalizza il prezzo del combustibile scelto a equivalente Carbone (÷ carbonella × 12).
        Questo permette ai calcoli di restare invariati (usano sempre 12 carbonella/blocco).
        """
        from ricette import COMBUSTIBILI, CARBONELLA_PER_BLOCCO
        prezzo = float(self.entry_carbone.get())
        tipo = self.combo_combustibile.get() if hasattr(self, "combo_combustibile") else "Carbone"
        carbonella = COMBUSTIBILI.get(tipo, {}).get("carbonella", CARBONELLA_PER_BLOCCO)
        return prezzo / carbonella * CARBONELLA_PER_BLOCCO

    def _mostra_risultato(self, preview_label, text_widget, result):
        """
        Aggiorna box risultati con animazione fade.
        Se guadagno < 0 prepone un avviso e colora il preview in rosso;
        se guadagno >= 0 ripristina i colori normali.
        """
        guadagno     = result.get("guadagno")
        output_lines = list(result["output_lines"])

        in_perdita = guadagno is not None and guadagno < 0

        if in_perdita:
            output_lines = [
                f"⚠️  VENDITA IN PERDITA  — perdi {abs(guadagno):.2f} b su questo lotto!",
                "",
                *output_lines,
            ]

        # Animazione fade standard
        self.update_result_with_fade(
            preview_label, text_widget,
            result["preview_text"], output_lines)

        # Stile colore preview (sovrascrive dopo il fade)
        if in_perdita:
            preview_label.config(
                text=f"🔴 {result['preview_text']}",
                bg=LOSS_BG, fg=LOSS_FG)
        else:
            preview_label.config(bg=BG_RESULT, fg=FG_TEXT)

    def do_calcola_pozioni(self):
        try:
            num_pozioni = float(self.entry_pozioni.get())
            tier_reagente = self.combo_tier.get()
            tipo_calderone = self.combo_calderone.get()
            
            prezzo_reagente = float(self.entry_reagente.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = self._get_prezzo_carbone_norm()
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

            self._mostra_risultato(self.label_preview, self.text_result, result)
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi: inserisci numeri validi!")

    def do_calcola_antidoti(self):
        try:
            self._aggiorna_resina_da_pozioni()
            
            num = float(self.entry_ant_num.get())
            tipo = self.combo_ant_calderone.get()
            
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_ant_preview, self.text_ant_result, result)
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi degli antidoti: inserisci numeri validi.")

    def do_calcola_revivify(self):
        try:
            num = float(self.entry_rev_num.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_rev_preview, self.text_rev_result, result)
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Revivify: inserisci numeri validi.")

    def do_calcola_extinguish(self):
        try:
            num = float(self.entry_ext_num.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_ext_preview, self.text_ext_result, result)
            
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
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_danno_preview, self.text_danno_result, result)
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Pozioni di Danno: inserisci numeri validi.")

    def do_calcola_elisir(self):
        try:
            num = float(self.entry_el_num.get())
            tipo = self.combo_el_tipo.get()
            
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_el_preview, self.text_el_result, result)
            
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
            self._insert_text_with_icons(self.text_rune_result, result["output_lines"])
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
            prezzo_carbone = self._get_prezzo_carbone_norm()
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
            
            self._mostra_risultato(self.label_vel_preview, self.text_vel_result, result)
            
        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Velocità: inserisci numeri validi.")

    def do_calcola_riduzione(self):
        try:
            num = float(self.entry_rid_num.get())
            tipo = self.combo_rid_tipo.get()

            prezzo_fungo = float(self.entry_rid_fungo.get())
            prezzo_slimeball = float(self.entry_slime.get())
            prezzo_core = float(self.entry_core.get())
            prezzo_carbone = self._get_prezzo_carbone_norm()
            boccette_per_1b = float(self.entry_boccette_per_b.get())

            try:
                prezzo_vendita = float(self.entry_rid_prezzo.get())
            except ValueError:
                prezzo_vendita = None

            result = core_calcola_riduzione(
                num=num, tipo=tipo,
                prezzo_fungo_marrone=prezzo_fungo, prezzo_slimeball=prezzo_slimeball,
                prezzo_core=prezzo_core,
                prezzo_carbone=prezzo_carbone, boccette_per_1b=boccette_per_1b,
                prezzo_vendita=prezzo_vendita,
            )

            self._mostra_risultato(self.label_rid_preview, self.text_rid_result, result)

        except ValueError:
            messagebox.showerror("❌ Errore", "Controlla i campi Riduzione: inserisci numeri validi.")

    def do_genera_lista_spesa(self):
        """Calcola la lista degli ingredienti grezzi per il mix di prodotti."""
        import math
        from tkinter import messagebox
        try:
            from calcolo_spesa import genera_lista_spesa, reagente_dettaglio
            from ricette import get_calderone_pozioni, COMBUSTIBILI

            def get_qty(entry):
                try:
                    v = float(entry.get())
                    return max(v, 0.0)
                except ValueError:
                    return 0.0

            def fmt_riga(nome, raw):
                """Ceil all'intero, mostra avanzo solo se presente e significativo."""
                ceil_val = math.ceil(raw)
                excess   = ceil_val - raw
                base = f"  • {nome:<24} {ceil_val}"
                if excess > 0.001:
                    return base + f"   (avanzo: {excess:.2f})"
                return base

            tipo_comb      = (self.combo_combustibile.get()
                              if hasattr(self, "combo_combustibile") else "Carbone")
            cbn_per_blocco = COMBUSTIBILI.get(tipo_comb, {}).get("carbonella", 12)

            selezioni  = []
            hc_details = {}   # "Reagente TX" → dettaglio HC aggregato

            # --- Pozione di cura ---
            qty = get_qty(self.entry_spesa_poz_qty)
            if qty > 0:
                cal  = self.combo_spesa_poz_cal.get()
                tier = self.combo_spesa_poz_tier.get()   # tier reagente scelto dall'utente
                selezioni.append({
                    "tipo": "poz_cura", "qty": qty,
                    "label": f"Pozione di cura  [{cal}]",
                    "params": {"tier": tier, "calderone": cal},
                })
                # Calcola dettaglio HC per questa selezione
                det = reagente_dettaglio(qty, tier, cal)
                key = f"Reagente {tier}"
                if key not in hc_details:
                    hc_details[key] = {"n_rea": 0, "hc_prod": 0, "hc_need": 0}
                hc_details[key]["n_rea"]   += det["n_reagenti"]
                hc_details[key]["hc_prod"] += det["hc_produced"]
                hc_details[key]["hc_need"] += det["hc_needed"]

            # --- Antidoto ---
            qty = get_qty(self.entry_spesa_ant_qty)
            if qty > 0:
                tipo = self.combo_spesa_ant_tipo.get()
                selezioni.append({
                    "tipo": "antidoto", "qty": qty,
                    "label": f"Antidoto  [{tipo}]",
                    "params": {"tipo": tipo},
                })

            # --- Revivify ---
            qty = get_qty(self.entry_spesa_rev_qty)
            if qty > 0:
                selezioni.append({"tipo": "revivify", "qty": qty, "label": "Revivify"})

            # --- Extinguish ---
            qty = get_qty(self.entry_spesa_ext_qty)
            if qty > 0:
                selezioni.append({"tipo": "extinguish", "qty": qty, "label": "Extinguish"})

            # --- Elisir ---
            qty = get_qty(self.entry_spesa_elisir_qty)
            if qty > 0:
                tipo = self.combo_spesa_elisir_tipo.get()
                selezioni.append({
                    "tipo": "elisir", "qty": qty,
                    "label": f"Elisir  [{tipo}]",
                    "params": {"tipo": tipo},
                })

            # --- Velocità ---
            qty = get_qty(self.entry_spesa_vel_qty)
            if qty > 0:
                tipo = self.combo_spesa_vel_tipo.get()
                selezioni.append({
                    "tipo": "velocita", "qty": qty,
                    "label": f"Velocità  [{tipo}]",
                    "params": {"tipo": tipo},
                })

            # --- Danno ---
            qty = get_qty(self.entry_spesa_danno_qty)
            if qty > 0:
                tipo = self.combo_spesa_danno_tipo.get()
                selezioni.append({
                    "tipo": "danno", "qty": qty,
                    "label": f"Danno  [{tipo}]",
                    "params": {"tipo": tipo},
                })

            # --- Riduzione ---
            qty = get_qty(self.entry_spesa_rid_qty)
            if qty > 0:
                tipo = self.combo_spesa_rid_tipo.get()
                selezioni.append({
                    "tipo": "riduzione", "qty": qty,
                    "label": f"Riduzione  [{tipo}]",
                    "params": {"tipo": tipo},
                })

            if not selezioni:
                messagebox.showwarning("⚠️ Lista vuota",
                    "Inserisci almeno un prodotto con quantità > 0.")
                return

            totale, blocchi_raw = genera_lista_spesa(selezioni, tipo_combustibile=tipo_comb)

            # --- Carbonella e blocchi (nessun avanzo mostrato) ---
            carbonella_tot = totale.get("Carbonella", 0.0)
            blocchi_ceil   = math.ceil(blocchi_raw)

            # --- Gruppi ingredienti ---
            GENERICI    = {"Boccette", "Verdure", "Vasetti", "Core fragment"}
            REAGENTE_PFX = "Reagente "
            generici    = {k: v for k, v in totale.items() if k in GENERICI}
            speciali    = {k: v for k, v in totale.items()
                           if k not in GENERICI
                           and k != "Carbonella"
                           and not k.startswith(REAGENTE_PFX)}

            # --- Mix prodotti ---
            mix_lines = [f" • {s['qty']:.0f}x  {s['label']}" for s in selezioni]

            lines = [
                "Prodotti richiesti:",
                *mix_lines,
                "",
                "─" * 40,
                "🔥  COMBUSTIBILE",
                f"  • {'Carbonella':<24} {int(carbonella_tot)}",
                f"  → {tipo_comb}: {blocchi_ceil} blocchi",
                "",
                "📦  INGREDIENTI GENERICI",
            ]

            # Reagenti con dettaglio HC
            for key, det in hc_details.items():
                hc_avanzo = det["hc_prod"] - det["hc_need"]
                riga = f"  • {key:<24} {det['n_rea']}"
                if hc_avanzo > 0:
                    riga += (f"   ({det['hc_prod']} HC prodotti,"
                             f" {det['hc_need']} usati, avanzo: {hc_avanzo} HC)")
                lines.append(riga)

            for k in ["Boccette", "Verdure", "Vasetti", "Core fragment"]:
                if k in generici:
                    lines.append(fmt_riga(k, generici[k]))

            if speciali:
                lines += ["", "🧪  INGREDIENTI SPECIFICI"]
                for k in sorted(speciali):
                    lines.append(fmt_riga(k, speciali[k]))

            preview = (f"Carbonella: {int(carbonella_tot)}  •  "
                       f"{tipo_comb}: {blocchi_ceil} blocchi  •  "
                       f"Boccette: {math.ceil(totale.get('Boccette', 0))}")

            self.update_result_with_fade(
                self.label_spesa_preview, self.text_spesa_result,
                preview, lines)

        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("❌ Errore", f"Errore nella lista spesa:\n{e}")

    def _reset_lista_spesa(self):
        """Azzera tutte le quantità nella lista spesa."""
        for attr in (
            "entry_spesa_poz_qty", "entry_spesa_ant_qty",
            "entry_spesa_rev_qty", "entry_spesa_ext_qty",
            "entry_spesa_elisir_qty", "entry_spesa_vel_qty",
            "entry_spesa_danno_qty", "entry_spesa_rid_qty",
        ):
            if hasattr(self, attr):
                e = getattr(self, attr)
                e.delete(0, "end")
                e.insert(0, "0")

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

        if hasattr(self, "combo_combustibile"):
            self.combo_combustibile.set(p.get("tipo_combustibile", "Carbone"))
            from ricette import COMBUSTIBILI
            carbonella = COMBUSTIBILI.get(self.combo_combustibile.get(), {}).get("carbonella", 12)
            if hasattr(self, "_label_carbone_hint"):
                self._label_carbone_hint.config(text=f"= {carbonella} carbonella")

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
            "tipo_combustibile": self.combo_combustibile.get() if hasattr(self, "combo_combustibile") else "Carbone",
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
            "tipo_combustibile": self.combo_combustibile.get() if hasattr(self, "combo_combustibile") else "Carbone",
            "verdure_per_1b": self.entry_verdure_per_b.get(),
            "vasetti_per_1b": self.entry_vasetti_per_b.get(),
            "boccette_per_1b": self.entry_boccette_per_b.get(),
            "prezzo_vendita_pozioni": self.entry_prezzo_vendita.get(),
            
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
        if "tipo_combustibile" in data and hasattr(self, "combo_combustibile"):
            self.combo_combustibile.set(data["tipo_combustibile"])
            from ricette import COMBUSTIBILI
            carbonella = COMBUSTIBILI.get(data["tipo_combustibile"], {}).get("carbonella", 12)
            if hasattr(self, "_label_carbone_hint"):
                self._label_carbone_hint.config(text=f"= {carbonella} carbonella")
        load_entry("verdure_per_1b", "entry_verdure_per_b")
        load_entry("vasetti_per_1b", "entry_vasetti_per_b")
        load_entry("boccette_per_1b", "entry_boccette_per_b")
        load_entry("prezzo_vendita_pozioni", "entry_prezzo_vendita")
        
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
        try:
            self._aggiorna_prezzi_riduzione()
        except Exception:
            pass
        try:
            self._aggiorna_prezzi_velocita()
        except Exception:
            pass
        try:
            self._aggiorna_prezzi_antidoti()
        except Exception:
            pass
        try:
            self._aggiorna_prezzi_revivify()
        except Exception:
            pass
        try:
            self._aggiorna_prezzi_elisir()
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
