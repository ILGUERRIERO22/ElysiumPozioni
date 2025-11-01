import re
import keyboard
import speech_recognition as sr
import pyttsx3
import time

# =========================
#   CONFIGURAZIONE VOCE
# =========================

tts = pyttsx3.init()
# opzionale: puoi cambiare volume / velocità / voce
tts.setProperty("rate", 180)     # velocità parlato
tts.setProperty("volume", 1.0)   # volume 0.0 - 1.0

def speak(msg: str):
    print("[ASSISTENTE DICE]:", msg)
    tts.say(msg)
    tts.runAndWait()

# =========================
#   LOGICA ALCHEMICA
# =========================

def get_calderone_stats(nome_calderone: str):
    """
    Ritorna:
      pozioni_per_catalyst,
      descrizione_tier_pozione (T1/T2/T3)
    e anche carbonella_per_pozione se vogliamo estenderlo.
    """
    nome = nome_calderone.lower()

    # Terracotta:
    # 1 catalyst -> 2 pozioni T1
    if "terracotta" in nome:
        return {
            "calderone": "Terracotta",
            "tier_pozione": "T1",
            "pozioni_per_catalyst": 2.0,
        }

    # Rame:
    # 1 catalyst -> 3 pozioni T1
    if "rame" in nome:
        return {
            "calderone": "Rame",
            "tier_pozione": "T1",
            "pozioni_per_catalyst": 3.0,
        }

    # Ferro:
    # 1 catalyst -> 1 pozione T2
    if "ferro" in nome:
        return {
            "calderone": "Ferro",
            "tier_pozione": "T2",
            "pozioni_per_catalyst": 1.0,
        }

    # Oro:
    # 2 catalyst -> 3 pozioni T2 => 1 catalyst = 1.5 pozioni
    if "oro" in nome:
        return {
            "calderone": "Oro",
            "tier_pozione": "T2",
            "pozioni_per_catalyst": 1.5,
        }

    # Diamante:
    # 3 catalyst -> 2 pozioni T3 => 1 catalyst = 0.666...
    if "diamante" in nome or "diamant" in nome:
        return {
            "calderone": "Diamante",
            "tier_pozione": "T3",
            "pozioni_per_catalyst": (2.0/3.0),
        }

    return None


def parse_user_text(frase: str):
    """
    Estrae:
    - numero pozioni richieste
    - nome calderone
    - tier richiesto esplicito (T1/T2/T3) oppure None
    """
    testo = frase.lower()

    # 1. numero pozioni
    numeri = re.findall(r"\d+", testo)
    num_pozioni = float(numeri[0]) if numeri else None

    # 2. calderone
    calderoni_keywords = ["terracotta", "rame", "ferro", "oro", "diamante", "diamant"]
    calderone_rilevato = None
    for c in calderoni_keywords:
        if c in testo:
            calderone_rilevato = c
            break

    # 3. tier reagente richiesto (opzionale)
    # supporta "t1", "t2", "t3", "tier 1", "tier2", "reagente t2", ecc.
    tier_match = None
    if re.search(r"\bt\s*1\b|\btier\s*1\b|\breagente\s*t\s*1\b", testo):
        tier_match = "T1"
    elif re.search(r"\bt\s*2\b|\btier\s*2\b|\breagente\s*t\s*2\b", testo):
        tier_match = "T2"
    elif re.search(r"\bt\s*3\b|\btier\s*3\b|\breagente\s*t\s*3\b", testo):
        tier_match = "T3"

    return num_pozioni, calderone_rilevato, tier_match


def calcola_materiali(num_pozioni, info_calderone):
    """
    Dato quante pozioni vuoi e il calderone,
    ritorna:
    - catalyst_totali
    - per ogni tier reagente (T1,T2,T3):
        reagenti_usati, core_usati, resine_usate
    """
    pozioni_per_catalyst = info_calderone["pozioni_per_catalyst"]

    # catalyst necessari = pozioni richieste / (pozioni per catalyst)
    catalyst_totali = num_pozioni / pozioni_per_catalyst

    # rese reagente:
    # T1: 1 catalyst per reagente
    # T2: 2 catalyst per reagente
    # T3: 3 catalyst per reagente
    rese = {
        "T1": 1.0,
        "T2": 2.0,
        "T3": 3.0
    }

    risultati = {}
    for tier_reagente, catalyst_per_reagente in rese.items():
        reagenti_usati = catalyst_totali / catalyst_per_reagente
        core_usati = reagenti_usati          # 1 core per reagente
        resine_usate = reagenti_usati        # 1 resina per reagente
        risultati[tier_reagente] = {
            "reagenti": reagenti_usati,
            "core": core_usati,
            "resine": resine_usate
        }

    return catalyst_totali, risultati


def format_risposta_voce(num_pozioni, calderone_label, catalyst_totali, risultati, tier_specifico=None):
    """
    Genera una frase parlabile.
    Se tier_specifico è impostato (T1/T2/T3), rispondi solo per quel tier.
    Altrimenti fai un riassunto T1 T2 T3.
    """
    if tier_specifico and tier_specifico in risultati:
        r = risultati[tier_specifico]
        return (
            f"Per {int(num_pozioni)} pozioni col calderone {calderone_label}, "
            f"ti servono circa {catalyst_totali:.2f} catalyst totali. "
            f"Se usi reagente {tier_specifico}, ti servono {r['reagenti']:.2f} reagenti, "
            f"{r['core']:.2f} core, e {r['resine']:.2f} resine."
        )

    # Risposta completa su tutti i tier
    r1 = risultati["T1"]
    r2 = risultati["T2"]
    r3 = risultati["T3"]
    return (
        f"Per {int(num_pozioni)} pozioni col calderone {calderone_label}, "
        f"servono {catalyst_totali:.2f} catalyst totali. "
        f"Con T uno: {r1['reagenti']:.2f} reagenti, {r1['core']:.2f} core, {r1['resine']:.2f} resine. "
        f"Con T due: {r2['reagenti']:.2f} reagenti, {r2['core']:.2f} core, {r2['resine']:.2f} resine. "
        f"Con T tre: {r3['reagenti']:.2f} reagenti, {r3['core']:.2f} core, {r3['resine']:.2f} resine."
    )


# =========================
#   ASCOLTO MICROFONO
# =========================

ricon = sr.Recognizer()

def ascolta_comando_vocale():
    """Ascolta una singola frase dal microfono e ritorna testo (stringa) o None."""
    with sr.Microphone() as source:
        speak("Dimmi pure.")
        print("[ASCOLTO] In ascolto...")
        audio = ricon.listen(source)

    try:
        testo = ricon.recognize_google(audio, language="it-IT")
        print("[RICONOSCIUTO]:", testo)
        return testo
    except sr.UnknownValueError:
        speak("Non ho capito.")
        return None
    except sr.RequestError:
        speak("Problema di connessione al servizio vocale.")
        return None


# =========================
#   CICLO HOTKEY
# =========================

def gestisci_richiesta():
    """
    Funzione richiamata quando premi la hotkey.
    1. ascolta voce
    2. parse
    3. calcolo
    4. parla risultato
    """
    speak("Ok.")
    frase = ascolta_comando_vocale()
    if not frase:
        return

    num_pozioni, nome_calderone, tier_specifico = parse_user_text(frase)

    if num_pozioni is None:
        speak("Non ho capito quante pozioni vuoi.")
        return

    if not nome_calderone:
        speak("Dimmi anche che calderone usi, per esempio oro o ferro.")
        return

    info_calderone = get_calderone_stats(nome_calderone)
    if info_calderone is None:
        speak("Non conosco quel calderone.")
        return

    catalyst_totali, risultati = calcola_materiali(num_pozioni, info_calderone)

    risposta = format_risposta_voce(
        num_pozioni=num_pozioni,
        calderone_label=info_calderone["calderone"],
        catalyst_totali=catalyst_totali,
        risultati=risultati,
        tier_specifico=tier_specifico
    )

    speak(risposta)


def main():
    speak("Assistente alchimista attivo. Premi F otto per chiedere.")
    print("[INFO] Assistente alchimista attivo. Premi F8 per parlare. CTRL+C per uscire.")

    keyboard.add_hotkey("f8", gestisci_richiesta)

    # loop infinito finché non chiudi a mano
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        speak("Spengo l'assistente alchimista. A dopo.")
        print("[INFO] Uscita.")


if __name__ == "__main__":
    main()
