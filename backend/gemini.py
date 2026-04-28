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

When you identify a risk level, explicitly state it at the beginning of your final summary in the format: 'RISK LEVEL: [Level]'.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def handle_function_call(function_call):
    """Mocks the execution of tool calls for the demo."""
    name = function_call.name
    params = function_call.args

    if name == "save_to_google_docs":
        print(f"[TOOL] Saving to Google Docs: {params['title']}")
        return {"status": "success", "message": f"Document '{params['title']}' created successfully."}

    if name == "notify_governance_admin":
        print(f"[TOOL] Notifying Admin: {params['risk_level']}")
        return {"status": "notified", "admin_response": "Acknowledged. Review scheduled."}

    return {"error": "Unknown function"}

def analyze_compliance(text, image_bytes=None, mime_type=None):
    """
    Analyzes user input with autonomous agent capabilities, multimodality, and recursive function calling.
    """
    try:
        chat = model.start_chat()

        content = [text]
        if image_bytes and mime_type:
            content.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        response = chat.send_message(content)

        # Recursive loop for function calling
        for _ in range(5): # Limit recursion to avoid infinite loops
            if not response.candidates[0].content.parts[0].function_call:
                break

            function_call = response.candidates[0].content.parts[0].function_call
            function_response = handle_function_call(function_call)

            # Send the result back to the model
            response = chat.send_message(
                Part.from_function_response(
                    name=function_call.name,
                    response=function_response
                )
            )

        return response.text
    except Exception as e:
        return f"Governance Analysis Error: {str(e)}"
