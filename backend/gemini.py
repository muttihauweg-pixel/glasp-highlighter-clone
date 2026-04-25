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

# --- 2. Tool Implementations (Mocks) ---
def save_to_google_docs(title, content):
    print(f"[MOCK] Saving to Google Docs: {title}")
    return f"SUCCESS: Document '{title}' successfully saved to Google Docs."

def notify_governance_admin(risk_level, reason):
    print(f"[MOCK] Notifying Admin: {risk_level} - {reason}")
    return f"SUCCESS: Governance admin notified about {risk_level} risk."

available_functions = {
    "save_to_google_docs": save_to_google_docs,
    "notify_governance_admin": notify_governance_admin,
}

# --- 3. System Instruction ---
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
        content_parts = [text]

        if image_base64:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(image_base64)
            image_part = Part.from_data(data=image_bytes, mime_type="image/png")
            content_parts.append(image_part)

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        # Loop to handle multiple function calls if necessary
        for _ in range(5): # Limit recursion
            if not response.candidates[0].content.parts[0].function_call:
                break

            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            args = {key: val for key, val in function_call.args.items()}

            if function_name in available_functions:
                print(f"Executing function: {function_name} with args {args}")
                function_response = available_functions[function_name](**args)

                # Send the function response back to the model
                response = chat.send_message(
                    Part.from_function_response(
                        name=function_name,
                        response={"result": function_response}
                    )
                )
            else:
                break

        return response.text
    except Exception as e:
        return f"Governance Analysis (Demo Mode): Analysis failed. Error: {str(e)}"
