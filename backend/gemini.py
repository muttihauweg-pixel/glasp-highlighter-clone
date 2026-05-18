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

STRUCTURED OUTPUT:
You MUST end your final response with exactly these two markers:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of your reasoning]

Respond in a professional, authoritative tone.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input (text and optional image) with autonomous agent capabilities and function calling.
    Returns a dict with response text and tool execution steps.
    """
    try:
        content_parts = [text]

        if image_data:
            # Handle base64 image data
            if "," in image_data:
                header, encoded = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                encoded = image_data
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(encoded)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        tool_steps = []
        max_iterations = 5

        for _ in range(max_iterations):
            if not response.candidates[0].content.parts:
                break

            function_calls = [p.function_call for p in response.candidates[0].content.parts if p.function_call]

            if not function_calls:
                break

            responses = []
            for fc in function_calls:
                tool_steps.append({
                    "function": fc.name,
                    "args": dict(fc.args)
                })

                # Mocking tool execution results
                if fc.name == "save_to_google_docs":
                    result = {"status": "success", "url": "https://docs.google.com/example"}
                elif fc.name == "notify_governance_admin":
                    result = {"status": "notified", "admin": "compliance-officer@company.com"}
                else:
                    result = {"error": "unknown function"}

                responses.append(Part.from_function_response(
                    name=fc.name,
                    response=result
                ))

            response = chat.send_message(responses)

        return {
            "text": response.text,
            "steps": tool_steps
        }

    except Exception as e:
        return {
            "text": f"RISK: High\nRATIONALE: Error during analysis: {str(e)}",
            "steps": []
        }
