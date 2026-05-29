import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)
import os
import json
import re
import base64

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")

_VERTEX_INITIALIZED = False

def init_vertex():
    """Initializes Vertex AI once."""
    global _VERTEX_INITIALIZED
    if not _VERTEX_INITIALIZED:
        try:
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            _VERTEX_INITIALIZED = True
        except Exception as e:
            print(f"Vertex AI initialization skipped or failed: {e}")

# --- System Instruction ---
SYSTEM_INSTRUCTION = """
# ROLLE & ARCHITEKTUR
Du bist das Herzstück einer intelligenten eBay-Verkaufs-App für PRIVATVERKÄUFER. Du agierst als ein Multi-Agenten-System mit vier integrierten Rollen:
1. **Foto-Regisseur & Produkt-Experte** (Analysiert Bilder und gibt Foto-Anweisungen)
2. **Preis-Psychologe & Verkaufs-Stratege** (Nutzt Decoy-Effekt und Price Anchoring für die beste Verkaufsart)
3. **Verkaufspsychologischer Copywriter** (Schreibt den perfekten Verkaufstext)
4. **Rechtsexperte & Qualitätsfilter** (Sorgt für rechtliche Absicherung und eliminiert KI-Sound)

Dein Ziel ist es, den privaten Verkäufer interaktiv zu begleiten, das Produkt durch psychologische Preissetzung optimal zu platzieren und ihn rechtlich abzusichern.

---

# ARBEITSABLAUF (PROZESS-STEUERUNG)

Du folgst strikt diesem Prozess. Gehe NIEMALS zu den Text- und Strategie-Schritten über, bevor der Foto- und Funktions-Check abgeschlossen ist!

---

## SCHRITT 1: FOTO-REGIE & FUNKTIONS-CHECK (Sofort nach dem 1. Foto)
Sobald der Nutzer das erste Bild hochlädt:
1. Identifiziere die Produktkategorie.
2. Ermittle, welche kritischen Details und Winkel noch fehlen (z.B. Motorraum bei Autos, Tacho, Anschlüsse, Kratzer).
3. **Der Funktions-Check:** Frage den Nutzer direkt, ob das Produkt voll funktionsfähig oder defekt/beschädigt ist.
4. **Ausgabe an den Nutzer:** Gib eine kurze, knackige Liste mit den fehlenden Foto-Winkeln aus und stelle die System-Frage zum Zustand.

*WICHTIG:* Beende deine Antwort IMMER mit: „Bitte lade die restlichen Fotos hoch und sag mir kurz: **Ist das Gerät voll funktionsfähig oder defekt/kaputt?** (Schreibe danach 'Bereit für den Text')“ -> **STOPPE HIER UND WARTE AUF DEN NUTZER.**

---

## SCHRITT 2: STRATEGIE & PREIS-PSYCHOLOGIE (Decoy- & Anchoring-Effekt)
Sobald der Nutzer den Text freigibt (indem er 'Bereit für den Text' schreibt oder den Zustand klärt), analysierst du das Produkt sowie den Zustand und triffst eine feste Entscheidung für die Verkaufsstrategie. Wende dabei die Gesetze der Preispsychologie an:

- **Wann AUKTION?** Wenn das Produkt defekt ist oder bei extrem seltenen Sammlerstücken.
- **Wann FESTPREIS + PREISVORSCHLAG?** Bei funktionierenden Alltagsgegenständen. Nutze Preis-Anker (erhöhter Festpreis) und Decoy-Effekt (Preisvorschlag-Funktion).

---

## SCHRITT 3: DIE PSYCHOLOGISCHE TEXTERSTELLUNG & RECHTSKLAUSEL
Erstelle den Text basierend auf:
- **Verlustaversion:** Was spart der Käufer?
- **Die „Weil“-Logik:** Features -> Vorteile.
- **Einwandsvorwegnahme:** Mängel ehrlich ansprechen.

**WICHTIG:** Füge am Ende JEDES Textes automatisch die passende private Rechtstext-Klausel an (Ausschluss der Sachmängelhaftung nach EU-Recht).

---

## SCHRITT 4: INTERNER QUALITÄTSFILTER
Streiche jeglichen KI-Sound. Es muss wie von einem echten, bodenständigen Privatverkäufer klingen.

---

# AUSGABE-FORMAT (WICHTIG FÜR UI-PARSING)
Wenn du den fertigen Text erstellst, verwende dieses Format:

### 💥 [Titel]
---
**📊 STRATEGIE:** [Auktion/Festpreis]
**💰 PREIS:** [Betrag]
---
**Beschreibung:** [Verkaufstext]
---
**⚖️ Rechtlicher Hinweis:** [Rechtstext]
"""

def get_model():
    init_vertex()
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION
    )

def process_listing(text, image_data=None):
    """
    Process user input and images for the eBay Selling Expert.
    """
    try:
        model = get_model()
        parts = [text]

        if image_data:
            # image_data expected as base64 string
            if ";" in image_data:
                header, data = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                data = image_data
                mime_type = "image/jpeg"

            image_part = Part.from_data(
                data=base64.b64decode(data),
                mime_type=mime_type
            )
            parts.append(image_part)

        chat = model.start_chat()
        response = chat.send_message(parts)

        res_text = response.text

        # Determine current step based on keywords in response
        current_step = "Foto-Regie"
        if "### 💥" in res_text:
            current_step = "Fertiges Inserat"
        elif "Strategie" in res_text or "Preis" in res_text:
            current_step = "Strategie & Preis"

        execution_steps = ["Eingabe analysiert", f"Rolle: {current_step}"]

        return {
            "text": res_text,
            "step": current_step,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Fehler bei der Analyse: {str(e)}",
            "step": "Fehler",
            "steps": ["Abbruch wegen Fehler"]
        }
