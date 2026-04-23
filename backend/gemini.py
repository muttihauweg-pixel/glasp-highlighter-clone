import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)
import os
import base64

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- 1. Define Function Calling Tools ---
save_to_docs_declaration = FunctionDeclaration(
    name="save_to_google_docs",
    description="Saves the compliance report or processed output to a new Google Doc",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title of the document"},
            "content": {"type": "string", "description": "The text content to save"}
        },
        "required": ["title", "content"]
    }
)

notify_admin_declaration = FunctionDeclaration(
    name="notify_governance_admin",
    description="Sends an urgent notification to the governance administrator for high-risk requests",
    parameters={
        "type": "object",
        "properties": {
            "risk_level": {"type": "string", "description": "The identified risk level"},
            "reason": {"type": "string", "description": "Reason for the high-risk classification"}
        },
        "required": ["risk_level", "reason"]
    }
)

governance_tools = Tool(
    function_declarations=[
        save_to_docs_declaration,
        notify_admin_declaration
    ]
)

# --- 2. System Instruction ---
SYSTEM_INSTRUCTION = """
You are the AI Governance Operating System (AG-OS) Agent.
Your primary directive is to ensure all AI-related requests comply with the EU AI Act and corporate safety policies.

OPERATING PRINCIPLES:
1. AUTONOMY: You proactively assess risks and take necessary actions (like notifying admins or logging results).
2. PRECISION: Categorize risks into 'Unacceptable', 'High', 'Limited', or 'Minimal'.
3. TRACEABILITY: Ensure every decision has a clear rationale for the audit trail.

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs for record-keeping using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.

Respond in a professional, authoritative tone.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input (text + image).
    """
    try:
        chat = model.start_chat()

        content_parts = [text]
        if image_base64:
            # Handle data URL prefix if present
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]

            try:
                image_bytes = base64.b64decode(image_base64)
                content_parts.append(
                    Part.from_data(
                        data=image_bytes,
                        mime_type="image/jpeg" # Defaulting to jpeg for demo
                    )
                )
            except Exception as e:
                print(f"Error decoding image: {e}")

        response = chat.send_message(content_parts)

        # Robust candidate check
        if not response.candidates:
            return "Governance Analysis: The model could not generate a response. This may be due to safety filters or an empty input."

        # Function calling loop
        actions_taken = []

        while (response.candidates[0].content.parts and
               response.candidates[0].content.parts[0].function_call):
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            args = function_call.args

            # Mock execution
            if function_name == "save_to_google_docs":
                result = {"status": "success", "message": f"Saved report '{args['title']}' to Google Docs"}
                actions_taken.append(f"Action: Saved to Google Docs ({args['title']})")
            elif function_name == "notify_governance_admin":
                result = {"status": "notified", "message": f"Admin alerted for {args['risk_level']} risk: {args['reason']}"}
                actions_taken.append(f"Action: Notified Admin ({args['risk_level']})")
            else:
                result = {"error": "Unknown function"}

            # Send result back to Gemini
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response=result,
                )
            )

        final_response = response.text
        if actions_taken:
            final_response += "\n\n--- Proactive Actions Taken ---\n" + "\n".join(actions_taken)

        return final_response
    except Exception as e:
        return f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error: {str(e)}"
