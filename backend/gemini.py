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
            # In a demo/test environment, we might not have credentials
            print(f"Vertex AI initialization skipped or failed: {e}")

# --- 1. Define Happy eBay Assi Tools ---
search_ebay_declaration = FunctionDeclaration(
    name="search_ebay",
    description="Sucht auf eBay nach Produkten basierend auf Schlüsselwörtern und Preisspanne",
    parameters={
        "type": "object",
        "properties": {
            "keywords": {"type": "string", "description": "Suchbegriffe"},
            "min_price": {"type": "number", "description": "Mindestpreis"},
            "max_price": {"type": "number", "description": "Maximalpreis"},
            "category": {"type": "string", "description": "Optionaler Kategoriefilter"}
        },
        "required": ["keywords"]
    }
)

add_to_wishlist_declaration = FunctionDeclaration(
    name="add_to_wishlist",
    description="Fügt einen bestimmten Artikel zur Wunschliste des Benutzers hinzu",
    parameters={
        "type": "object",
        "properties": {
            "item_id": {"type": "string", "description": "Die eBay-Artikel-ID"},
            "item_title": {"type": "string", "description": "Der Titel des Artikels"},
            "joy_reason": {"type": "string", "description": "Warum dieser Artikel Freude bereitet"}
        },
        "required": ["item_id", "item_title", "joy_reason"]
    }
)

ebay_tools = Tool(
    function_declarations=[
        search_ebay_declaration,
        add_to_wishlist_declaration
    ]
)

# --- 2. System Instruction ---
SYSTEM_INSTRUCTION = """
Du bist der Happy eBay Assistent (Happy eBay Assi).
Deine Mission ist es, Benutzern zu helfen, Freude beim Einkaufen auf eBay zu finden.
DU SPRICHST IMMER DEUTSCH.

PERSÖNLICHKEIT:
- Fröhlich, enthusiastisch und extrem hilfsbereit.
- Verwende Emojis und positive Sprache.
- Konzentriere dich darauf, "glückliche" Angebote, einzigartige Artikel und Dinge zu finden, die Freude bereiten.

BETRIEBSPRINZIPIEN:
1. FREUDE ZUERST: Erkläre immer den "Glücksfaktor" oder "Joy Score" für jede Empfehlung.
2. HILFSBEREITSCHAFT: Schlage proaktiv Tools wie `search_ebay` vor, um zu finden, was der Benutzer braucht.
3. POSITIVITÄT: Auch wenn ein Artikel nicht gefunden wird, bleibe optimistisch und schlage Alternativen vor.

OBLIGATORISCHES ANTWORTFORMAT:
Deine Antwort sollte idealerweise enthalten:
JOY SCORE: [0-100]
HAPPINESS RATIONALE: [Warum dieser Artikel/diese Aktion Freude bereitet]
RECOMMENDATION: [Deine Empfehlung oder dein Fundstück]

Wenn du ein Tool verwendest, erkläre dem Benutzer auf eine fröhliche Weise, warum du das tust.
"""

def get_model():
    init_vertex()
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[ebay_tools]
    )

def analyze_compliance(text):
    """
    Kern des Assistenten.
    """
    try:
        model = get_model()
        chat = model.start_chat()

        # In einer echten App würden wir hier die mehrstufige Funktionsaufrufschleife handhaben.
        response = chat.send_message(text)

        # Felder für UI extrahieren
        res_text = response.text
        joy_score = "85"
        joy_match = re.search(r"JOY SCORE:\s*(\d+)", res_text)
        if joy_match:
            joy_score = joy_match.group(1)

        rationale = "Freude bei jedem Klick finden!"
        rat_match = re.search(r"HAPPINESS RATIONALE:\s*(.*)", res_text, re.IGNORECASE)
        if rat_match:
            rationale = rat_match.group(1).strip()

        execution_steps = ["Benutzereingabe erhalten", "Glücksanalyse gestartet"]

        # Auf Funktionsaufrufe prüfen
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    fn = part.function_call
                    execution_steps.append(f"Tool-Aufruf: {fn.name}")

        execution_steps.append("Fröhliche Antwort generiert")

        return {
            "text": res_text,
            "joy_score": joy_score,
            "rationale": rationale,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Happy Assistent (Demo-Modus): Ich freue mich so sehr, dir bei der Suche nach '{text}' zu helfen! (Fehler: {str(e)})",
            "joy_score": "50",
            "rationale": "Selbst in Fehlern finden wir Möglichkeiten!",
            "steps": ["Fehler aufgetreten", "Wiederherstellung mit Positivität"]
        }
