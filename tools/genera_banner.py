"""Genera banner.png, il banner in pixel art del README.

Si disegna su una griglia a bassa risoluzione (205x64 blocchi) e ogni blocco
diventa un quadrato di S pixel: cosi i bordi restano netti, senza sfocature.
I colori vengono dalla palette dell'app in config_app.py.

Uso, dalla radice del progetto:

    python tools/genera_banner.py banner.png

Senza argomenti scrive su prova.png, comodo per provare modifiche senza
sovrascrivere il banner buono.
"""
import sys, os, random
from PIL import Image, ImageDraw

OUT = sys.argv[1] if len(sys.argv) > 1 else "prova.png"

BG       = (13, 13, 24)
BG_ALT   = (20, 20, 34)
VETRO    = (214, 222, 240)
VETRO_SC = (108, 120, 156)
TAPPO    = (150, 118, 74)
TAPPO_SC = (104, 80, 50)
VIOLA    = (124,  58, 237)
VIOLA_CH = (176, 148, 255)
TESTO    = (240, 242, 252)
OMBRA    = (52, 40, 88)

POZIONI = [
    ((239,  68,  68), (255, 150, 150)),
    (( 16, 185, 129), ( 90, 235, 190)),
    ((251, 191,  36), (255, 226, 140)),
    (( 96, 165, 250), (160, 205, 255)),
    ((196, 132, 252), (225, 190, 255)),
]

S = 8
GW, GH = 205, 64
img = Image.new("RGB", (GW*S, GH*S), BG)
d = ImageDraw.Draw(img)

def px(x, y, col, w=1, h=1):
    d.rectangle([x*S, y*S, (x+w)*S-1, (y+h)*S-1], fill=col)

# fondo a fasce
for y in range(0, GH, 3):
    px(0, y, BG_ALT, GW, 1)

random.seed(11)
for _ in range(90):
    px(random.randrange(GW), random.randrange(GH),
       random.choice([(34,34,58),(46,42,76),(60,52,96)]))


def boccetta(ox, oy, liq, liq_ch, scala=1):
    """Boccetta Minecraft: tappo, collo, corpo tondo. 10x14 blocchi."""
    def p(x, y, c, w=1, h=1):
        px(ox + x*scala, oy + y*scala, c, w*scala, h*scala)
    p(4, 0, TAPPO, 3, 1)
    p(4, 1, TAPPO_SC, 3, 1)
    p(4, 2, VETRO, 1, 2); p(6, 2, VETRO_SC, 1, 2)
    p(3, 4, VETRO, 1, 1);  p(7, 4, VETRO_SC, 1, 1)
    p(2, 5, VETRO, 1, 1);  p(8, 5, VETRO_SC, 1, 1)
    p(1, 6, VETRO, 1, 5);  p(9, 6, VETRO_SC, 1, 5)
    p(2, 11, VETRO, 1, 1); p(8, 11, VETRO_SC, 1, 1)
    p(3, 12, VETRO, 5, 1)
    # liquido
    p(2, 7, liq, 7, 4)
    p(3, 11, liq, 5, 1)
    p(2, 6, BG, 7, 1)
    # bolle e riflesso
    p(3, 8, liq_ch); p(6, 9, liq_ch); p(5, 10, liq_ch)
    p(2, 7, (255,255,255))
    p(2, 8, (255,255,255))


def calderone(ox, oy, sc=2):
    """Calderone di ferro: bordo sporgente, corpo svasato, piedini, vapore."""
    FERRO   = (92, 92, 106)
    FERRO_S = (56, 56, 68)
    FERRO_C = (124, 124, 140)
    def p(x, y, c, w=1, h=1):
        px(ox + x*sc, oy + y*sc, c, w*sc, h*sc)

    # Apertura vista in prospettiva: e' l'ellisse in cima a rendere
    # riconoscibile il recipiente. Bordo esterno...
    p(2, 0, FERRO_C, 10, 1)
    p(1, 1, FERRO_C, 1, 1); p(12, 1, FERRO_S, 1, 1)
    # ...e imboccatura scura vista dall'alto
    p(3, 1, (20, 20, 30), 8, 1)
    p(2, 2, (20, 20, 30), 10, 1)

    # superficie del liquido dentro l'imboccatura
    p(3, 2, VIOLA, 8, 1)
    p(4, 2, (206, 186, 255), 3, 1)

    # pareti che si stringono verso il basso
    p(1, 2, FERRO_C, 1, 7)
    p(12, 2, FERRO_S, 1, 7)
    p(2, 3, VIOLA, 10, 6)
    p(2, 3, (150,120,220), 1, 6)        # ombra interna a sinistra
    p(11, 3, (96, 44, 180), 1, 6)       # ombra interna a destra
    p(5, 5, VIOLA_CH); p(8, 4, VIOLA_CH); p(7, 7, VIOLA_CH)

    # fondo arrotondato e piedini
    p(2, 9, FERRO, 10, 1)
    p(3, 10, FERRO_S, 8, 1)
    p(2, 11, FERRO_S, 2, 2)
    p(10, 11, FERRO_S, 2, 2)

    # vapore che sale, sfumando
    for vx, vy, c in [(4,-2,(96,78,146)), (8,-3,(84,68,128)),
                      (5,-5,(72,58,112)), (9,-6,(64,52,100)),
                      (6,-8,(52,44,84)),  (10,-9,(44,38,72)),
                      (7,-11,(34,30,58))]:
        p(vx, vy, c)


GLIFI = {
 'E': ["1111","1000","1110","1000","1111"],
 'L': ["1000","1000","1000","1000","1111"],
 'Y': ["1001","1001","0110","0100","0100"],
 'S': ["0111","1000","0110","0001","1110"],
 'I': ["1110","0100","0100","0100","1110"],
 'U': ["1001","1001","1001","1001","0110"],
 'M': ["10001","11011","10101","10001","10001"],
 'P': ["1110","1001","1110","1000","1000"],
 'O': ["0110","1001","1001","1001","0110"],
 'Z': ["1111","0001","0110","1000","1111"],
 'N': ["1001","1101","1011","1001","1001"],
 'W': ["10001","10001","10101","11011","10001"],
 ' ': ["0000","0000","0000","0000","0000"],
}

def scrivi(testo, ox, oy, col, scala):
    x = ox
    for ch in testo:
        g = GLIFI.get(ch)
        if g:
            for r, riga in enumerate(g):
                for c, v in enumerate(riga):
                    if v == "1":
                        px(x + c*scala + scala//2, oy + r*scala + scala//2, OMBRA, scala, scala)
            for r, riga in enumerate(g):
                for c, v in enumerate(riga):
                    if v == "1":
                        px(x + c*scala, oy + r*scala, col, scala, scala)
        x += (len(g[0]) + 1)*scala if g else 5*scala
    return x

# titolo a sinistra
scrivi("ELYSIUM", 10, 10, TESTO, 3)
scrivi("POZIONI", 10, 29, VIOLA_CH, 3)

# sottolineatura tratteggiata
for x in range(10, 118, 5):
    px(x, 46, (58, 48, 96), 3, 1)

# fila di boccette sotto il titolo
for i, (c, cc) in enumerate(POZIONI):
    boccetta(11 + i*14, 49, c, cc)

# Tre boccette grandi a destra, di dimensione decrescente: la piu' grande
# al centro fa da fulcro visivo. Il calderone e' stato scartato: in pixel art
# a questa scala si leggeva come uno schermo, non come un recipiente.
boccetta(120, 32, (251,191,36), (255,226,140), scala=1)
boccetta(133, 20, (16,185,129), (90,235,190), scala=3)
boccetta(168, 30, (167,139,250), (215,195,255), scala=2)
boccetta(190, 34, (239,68,68), (255,150,150), scala=1)

# scintille attorno alla boccetta centrale
for sx, sy, c in [(130,18,(120,100,180)), (166,22,(140,115,205)),
                  (128,46,(96,80,150)),  (188,26,(110,92,168)),
                  (150,14,(150,125,215)), (183,50,(88,74,140))]:
    px(sx, sy, c)

img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=64)
img.save(OUT, optimize=True, compress_level=9)
print(f"{os.path.basename(OUT)}: {img.size[0]}x{img.size[1]}, {os.path.getsize(OUT)/1024:.0f} KB")
