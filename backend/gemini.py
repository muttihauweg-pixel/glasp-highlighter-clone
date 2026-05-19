import base64
import os
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)

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

MANDATORY RESPONSE FORMAT:
- RISK: [Unacceptable/High/Limited/Minimal]
- RATIONALE: [Detailed explanation]
- ACTION: [List of tools called or suggested]

Respond in a professional, authoritative tone.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input (text + optional image) with autonomous agent capabilities and function calling.
    Returns the final response and a list of tool steps taken.
    """
    try:
        content = [text]
        if image_data:
            if "," in image_data:
                header, image_data = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                mime_type = "image/png"

            image_bytes = base64.b64decode(image_data)
            content.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content)

        tool_steps = []

        # Recursive function calling loop (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].content.parts[0].function_call:
                break

            function_call = response.candidates[0].content.parts[0].function_call
            tool_name = function_call.name
            tool_args = function_call.args

            tool_steps.append({
                "action": tool_name,
                "parameters": dict(tool_args)
            })

            # Mock tool execution responses for the demo
            if tool_name == "save_to_google_docs":
                api_response = {"status": "success", "doc_url": "https://docs.google.com/document/d/demo-id"}
            elif tool_name == "notify_governance_admin":
                api_response = {"status": "alert_sent", "priority": "high"}
            else:
                api_response = {"error": "unknown_tool"}

            response = chat.send_message(
                Part.from_function_response(
                    name=tool_name,
                    response=api_response
                )
            )

        return {
            "text": response.text,
            "tool_steps": tool_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Error: {str(e)}",
            "tool_steps": []
        }
