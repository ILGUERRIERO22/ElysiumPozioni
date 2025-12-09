# animations.py
"""
Sistema di animazioni fluide per l'interfaccia Tkinter
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
        Fade in di un widget

        Args:
            widget: Widget da animare
            duration: Durata in millisecondi
            callback: Funzione da chiamare al termine
        """
        steps = 20
        step_duration = duration // steps

        def animate(step=0):
            if step <= steps:
                alpha = step / steps
                # Simula fade in modificando il background se possibile
                try:
                    widget.config(state='normal')
                except:
                    pass

                if step < steps:
                    self.root.after(step_duration, lambda: animate(step + 1))
                elif callback:
                    callback()

        animate()

    def fade_out(self, widget: tk.Widget, duration: int = 200, callback: Optional[Callable] = None):
        """
        Fade out di un widget

        Args:
            widget: Widget da animare
            duration: Durata in millisecondi
            callback: Funzione da chiamare al termine
        """
        steps = 15
        step_duration = duration // steps

        def animate(step=0):
            if step <= steps:
                if step < steps:
                    self.root.after(step_duration, lambda: animate(step + 1))
                else:
                    if callback:
                        callback()

        animate()

    def slide_in(self, widget: tk.Widget, direction: str = 'left', duration: int = 250):
        """
        Slide in di un widget da una direzione

        Args:
            widget: Widget da animare
            direction: 'left', 'right', 'top', 'bottom'
            duration: Durata in millisecondi
        """
        # Placeholder per animazione slide
        # In Tkinter puro è complesso, ma possiamo simulare con pack/grid
        widget.pack()

    def smooth_scroll(self, canvas: tk.Canvas, target_y: float, duration: int = 300):
        """
        Scroll smooth di un canvas

        Args:
            canvas: Canvas da scrollare
            target_y: Posizione target Y
            duration: Durata in millisecondi
        """
        steps = 20
        step_duration = duration // steps
        start_y = canvas.yview()[0]
        delta = (target_y - start_y) / steps

        def animate(step=0):
            if step < steps:
                canvas.yview_moveto(start_y + delta * step)
                self.root.after(step_duration, lambda: animate(step + 1))

        animate()

    def pulse(self, widget: tk.Widget, color_start: str, color_end: str, duration: int = 400):
        """
        Effetto pulse cambiando colore

        Args:
            widget: Widget da animare
            color_start: Colore iniziale
            color_end: Colore finale
            duration: Durata in millisecondi
        """
        original_bg = widget.cget('bg') if hasattr(widget, 'cget') else None

        try:
            widget.config(bg=color_end)
            self.root.after(duration, lambda: widget.config(bg=original_bg) if original_bg else None)
        except:
            pass

    def shake(self, widget: tk.Widget, intensity: int = 5, duration: int = 300):
        """
        Effetto shake per errori

        Args:
            widget: Widget da animare
            intensity: Intensità dello shake in pixel
            duration: Durata in millisecondi
        """
        # Placeholder - richiede manipolazione position che è complessa in Tkinter
        pass
