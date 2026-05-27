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

MANDATORY RESPONSE FORMAT:
Your response must ALWAYS include:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of your governance decision]

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

def analyze_compliance(text, image_data=None, mime_type=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input (text + image).
    """
    try:
        chat = model.start_chat()

        content_parts = [text]
        if image_data and mime_type:
            image_part = Part.from_data(data=base64.b64decode(image_data), mime_type=mime_type)
            content_parts.append(image_part)

        response = chat.send_message(content_parts)

        # Recursive function calling loop
        iterations = 0
        max_iterations = 5
        tool_calls_made = []

        while response.candidates[0].function_calls and iterations < max_iterations:
            iterations += 1
            function_calls = response.candidates[0].function_calls

            responses_to_send = []
            for function_call in function_calls:
                name = function_call.name
                params = {key: value for key, value in function_call.args.items()}

                # Mock execution for demo
                tool_calls_made.append({"name": name, "params": params})

                # We return a mock success message to the model
                responses_to_send.append(
                    Part.from_function_response(
                        name=name,
                        response={"result": f"Successfully executed {name}"}
                    )
                )

            response = chat.send_message(responses_to_send)

        return {
            "text": response.text,
            "tool_calls": tool_calls_made
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "tool_calls": []
        }
