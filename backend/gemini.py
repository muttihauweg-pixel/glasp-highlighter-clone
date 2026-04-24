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

def analyze_compliance(text, image_bytes=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Returns a dictionary containing the final report and a log of agent actions.
    """
    thought_log = []
    final_text = ""

    try:
        chat = model.start_chat()

        # Initial prompt
        parts = [text]
        if image_bytes:
            parts.append(Part.from_data(data=image_bytes, mime_type="image/jpeg"))

        response = chat.send_message(parts)

        # Function calling loop (max 5 iterations to prevent infinite loops)
        for _ in range(5):
            # Check for function calls in the candidate
            function_calls = response.candidates[0].function_calls

            if not function_calls:
                final_text = response.text
                break

            # Process function calls
            responses_parts = []
            for function_call in function_calls:
                name = function_call.name
                params = {key: value for key, value in function_call.args.items()}

                # Mock execution of tools
                if name == "save_to_google_docs":
                    thought_log.append(f"Action: Saving compliance report to Google Docs ('{params.get('title')}')")
                    result = {"status": "success", "doc_url": "https://docs.google.com/document/d/12345"}
                elif name == "notify_governance_admin":
                    thought_log.append(f"Action: Notifying Governance Admin. Risk: {params.get('risk_level')}. Reason: {params.get('reason')}")
                    result = {"status": "notified", "priority": "high"}
                else:
                    result = {"error": "Unknown tool"}

                responses_parts.append(Part.from_function_response(
                    name=name,
                    response=result
                ))

            # Send the results back to the model
            response = chat.send_message(responses_parts)

        return {
            "report": final_text or response.text,
            "thought_log": thought_log
        }

    except Exception as e:
        return {
            "report": f"Governance Analysis (Demo Mode): Error: {str(e)}",
            "thought_log": [f"Error encountered: {str(e)}"]
        }
