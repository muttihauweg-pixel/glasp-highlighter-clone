import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)
import os

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

def analyze_compliance(text, image_bytes=None, mime_type="image/jpeg"):
    """
    Analyzes user input with autonomous agent capabilities, multimodal support, and function calling.
    """
    actions_taken = []

    content = [text]
    if image_bytes:
        image_part = Part.from_data(data=image_bytes, mime_type=mime_type)
        content.append(image_part)

    try:
        chat = model.start_chat()
        response = chat.send_message(content)

        # Recursive loop for function calls
        while True:
            if not response.candidates[0].function_calls:
                break

            tool_responses = []
            for function_call in response.candidates[0].function_calls:
                name = function_call.name
                args = function_call.args

                actions_taken.append({
                    "name": name,
                    "params": dict(args)
                })

                # Mocking execution of tools
                if name == "save_to_google_docs":
                    result = {"status": "success", "doc_url": "https://docs.google.com/example"}
                elif name == "notify_governance_admin":
                    result = {"status": "notified", "admin_id": "admin_01"}
                else:
                    result = {"status": "error", "message": "Unknown tool"}

                tool_responses.append(
                    Part.from_function_response(
                        name=name,
                        response=result
                    )
                )

            # Send function responses back to model
            response = chat.send_message(tool_responses)

        return {
            "text": response.text,
            "actions": actions_taken
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "actions": actions_taken
        }
