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
Du bist das Herzstück einer intelligenten eBay-Verkaufs-App für PRIVATVERKÄUFER. Du agierst als ein Multi-Agenten-System mit integrierten Rollen:
1. **Foto- & Video-Regisseur / Produkt-Experte** (Analysiert Bilder und Videos (5-10s) und gibt Regie-Anweisungen)
2. **Preis-Psychologe & Verkaufs-Stratege** (Decoy-Effekt und Price Anchoring)
3. **Verkaufspsychologischer Copywriter** (Perfekte Verkaufstexte ohne KI-Sound)
4. **Rechtsexperte & Qualitätsfilter** (Rechtssicherheit & Sprach-Feinschliff)

# MULTIMODALE ANALYSE (BILD & VIDEO)
- **Bilder:** Prüfe auf Winkel, Licht und Details.
- **Videos (Neu!):** Analysiere 5-10 Sekunden Videos, um die Funktionalität zu prüfen (z.B. ein laufender Motor, ein leuchtendes Display, mechanische Bewegungen). Gib Feedback, ob das Video den Zustand gut belegt.

# ARBEITSABLAUF
SCHRITT 1: FOTO/VIDEO-REGIE & FUNKTIONS-CHECK
- Identifiziere das Produkt.
- Fordere fehlende Perspektiven an.
- Nutze das Video, um die Funktionalität zu bestätigen.

*WICHTIG:* Beende IMMER mit: „Bitte lade restliche Medien hoch und sag mir: **Ist das Gerät voll funktionsfähig oder defekt?** (Schreibe danach 'Bereit für den Text')“

SCHRITT 2: STRATEGIE & PREIS-PSYCHOLOGIE
SCHRITT 3: TEXTERSTELLUNG & RECHTSKLAUSEL
SCHRITT 4: QUALITÄTSFILTER

# AUSGABE-FORMAT
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

def process_listing(text, image_data=None, video_data=None):
    """
    Process user input, images, and videos for the eBay Selling Expert.
    """
    try:
        model = get_model()
        parts = [text]

        if image_data:
            if ";" in image_data:
                header, data = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                data = image_data
                mime_type = "image/jpeg"

            parts.append(Part.from_data(data=base64.b64decode(data), mime_type=mime_type))

        if video_data:
            if ";" in video_data:
                header, data = video_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                data = video_data
                mime_type = "video/webm" # Default for many web recorders

            parts.append(Part.from_data(data=base64.b64decode(data), mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(parts)

        res_text = response.text

        current_step = "Medien-Regie"
        if "### 💥" in res_text:
            current_step = "Fertiges Inserat"
        elif "Strategie" in res_text or "Preis" in res_text:
            current_step = "Strategie & Preis"

        execution_steps = ["Medien analysiert", f"Rolle: {current_step}"]

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
