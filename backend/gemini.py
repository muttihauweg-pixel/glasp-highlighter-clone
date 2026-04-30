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
Your response MUST always include a line starting with 'RISK_ASSESSMENT:' followed by one of the levels (Minimal, Limited, High, Unacceptable).
"""

_model = None

def get_model():
    global _model
    if _model is None:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        _model = GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[governance_tools]
        )
    return _model

def handle_function_call(function_call):
    """
    Simulates tool execution for the AG-OS demo.
    """
    name = function_call.name
    params = function_call.args

    if name == "save_to_google_docs":
        return {
            "status": "Success",
            "message": f"Document '{params['title']}' saved to Google Docs."
        }
    elif name == "notify_governance_admin":
        return {
            "status": "Alert Sent",
            "message": f"Governance Admin notified of {params['risk_level']} risk. Reason: {params['reason']}"
        }
    return {"error": "Unknown function"}

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Implements a recursive loop to handle multiple model turns for tool use.
    """
    try:
        model = get_model()
        content_parts = [Part.from_text(text)]

        if image_data:
            if ";base64," in image_data:
                header, base64_data = image_data.split(";base64,")
                mime_type = header.replace("data:", "")
                image_bytes = base64.b64decode(base64_data)
                content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        # Recursive loop for function calling
        max_turns = 5
        actions_taken = []

        for _ in range(max_turns):
            # Check all parts of the response for any function calls
            function_calls = [part.function_call for part in response.candidates[0].content.parts if part.function_call]

            if not function_calls:
                break

            tool_responses = []
            for fc in function_calls:
                actions_taken.append(fc.name)
                result = handle_function_call(fc)
                tool_responses.append(
                    Part.from_function_response(
                        name=fc.name,
                        response=result
                    )
                )

            # Send tool results back to model
            response = chat.send_message(tool_responses)

        return {
            "text": response.text,
            "actions": actions_taken
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "actions": []
        }
