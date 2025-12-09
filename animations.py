# animations.py
"""
Sistema di animazioni visibili per l'interfaccia Tkinter
"""
import tkinter as tk
from typing import Callable, Optional


class AnimationManager:
    """Gestisce animazioni fluide per widget Tkinter"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.active_animations = {}

    def fade_in(self, widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """
        Fade in simulato con effetto flash sul background

        Args:
            widget: Widget da animare
            duration: Durata in millisecondi
            callback: Funzione da chiamare al termine
        """
        # Effetto flash per simulare fade in
        try:
            original_bg = widget.cget('bg')
            # Usa un colore più chiaro per simulare fade
            lighter_color = '#2a2a3e'  # Colore intermedio

            widget.config(bg=lighter_color)
            self.root.after(50, lambda: widget.config(bg=original_bg))

            if callback:
                self.root.after(duration, callback)
        except:
            if callback:
                self.root.after(duration, callback)

    def pulse(self, widget: tk.Widget, color_start: str, color_end: str, duration: int = 400):
        """
        Effetto pulse cambiando colore con transizione visibile

        Args:
            widget: Widget da animare (es. Label)
            color_start: Colore iniziale
            color_end: Colore finale (accent)
            duration: Durata in millisecondi
        """
        try:
            # Cambia al colore accent
            widget.config(bg=color_end)
            # Torna al colore originale dopo duration
            self.root.after(duration, lambda: widget.config(bg=color_start))
        except:
            pass

    def button_flash(self, canvas: tk.Canvas, color_flash: str, original_color: str, duration: int = 100):
        """
        Flash su un canvas button con colore temporaneo

        Args:
            canvas: Canvas del bottone
            color_flash: Colore del flash
            original_color: Colore originale da ripristinare
            duration: Durata del flash
        """
        try:
            # Trova il rettangolo nel canvas
            items = canvas.find_all()
            for item in items:
                if canvas.type(item) == 'rectangle':
                    canvas.itemconfig(item, fill=color_flash)
                    self.root.after(duration, lambda: canvas.itemconfig(item, fill=original_color))
                    break
        except:
            pass

    def slide_fade_tab(self, widget: tk.Widget, direction: str = 'left', duration: int = 200):
        """
        Effetto slide simulato per cambio tab con flash

        Args:
            widget: Frame della tab
            direction: 'left' o 'right'
            duration: Durata dell'animazione
        """
        try:
            # Flash rapido per indicare cambio
            original_bg = widget.cget('bg')
            flash_color = '#1f1f2e'

            widget.config(bg=flash_color)
            self.root.after(50, lambda: widget.config(bg=original_bg))
        except:
            pass

    def smooth_scroll(self, canvas: tk.Canvas, target_y: float, duration: int = 300):
        """
        Scroll smooth di un canvas

        Args:
            canvas: Canvas da scrollare
            target_y: Posizione target Y
            duration: Durata in millisecondi
        """
        steps = 15
        step_duration = duration // steps

        try:
            start_y = canvas.yview()[0]
            delta = (target_y - start_y) / steps

            def animate(step=0):
                if step < steps:
                    canvas.yview_moveto(start_y + delta * step)
                    self.root.after(step_duration, lambda: animate(step + 1))

            animate()
        except:
            pass

    def shake(self, widget: tk.Widget, intensity: int = 5, duration: int = 300):
        """
        Effetto shake simulato con configurazione rapida

        Args:
            widget: Widget da "shakare"
            intensity: Intensità (non usato, per compatibilità)
            duration: Durata totale
        """
        try:
            # Shake simulato con flash rosso
            original_bg = widget.cget('bg')
            widget.config(bg='#3d1f1f')
            self.root.after(100, lambda: widget.config(bg=original_bg))
        except:
            pass
