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
Include your final verdict in the format:
Risk Level: [Level]
Rationale: [Reasoning]
"""

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input.
    """
    # Initialize Vertex AI inside the function to facilitate mocking
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[governance_tools]
    )

    try:
        content_parts = [Part.from_text(text)]

        if image_base64:
            # Extract mime type from base64 string (e.g. data:image/png;base64,...)
            if "," in image_base64:
                header, data = image_base64.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                data = image_base64
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(data)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        execution_steps = ["Governance Analysis Initiated"]

        # Recursive function calling loop (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            function_responses = []
            for function_call in response.candidates[0].function_calls:
                name = function_call.name
                params = function_call.args

                execution_steps.append(f"Executing Tool: {name}")

                # Mock execution of tools for the demo
                if name == "save_to_google_docs":
                    result = {"status": "success", "doc_url": "https://docs.google.com/document/d/12345"}
                elif name == "notify_governance_admin":
                    result = {"status": "notified", "admin": "Governance Lead"}
                else:
                    result = {"error": "Tool not found"}

                function_responses.append(
                    Part.from_function_response(
                        name=name,
                        response=result
                    )
                )

            response = chat.send_message(function_responses)

        execution_steps.append("Analysis Complete")

        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "steps": ["Error encountered"]
        }
