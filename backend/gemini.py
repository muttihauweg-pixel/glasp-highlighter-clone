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
import re

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

MULTIMODAL CAPABILITY:
You can analyze both text and images. If an image is provided (e.g., a UI screenshot), check for dark patterns or manipulative designs prohibited by the EU AI Act.

OUTPUT FORMAT:
Always conclude your analysis with a JSON block containing the risk assessment:
```json
{
  "risk_level": "Unacceptable" | "High" | "Limited" | "Minimal",
  "rationale": "Brief explanation"
}
```
"""

def get_model():
    # Initialize Vertex AI here to allow mocking in tests
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[governance_tools]
    )

def analyze_compliance(text, image_bytes=None, mime_type=None):
    """
    Analyzes user input with autonomous agent capabilities, function calling, and multimodality.
    """
    model = get_model()
    chat = model.start_chat()

    content_parts = [Part.from_text(text)]
    if image_bytes and mime_type:
        content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

    response = chat.send_message(content_parts)

    execution_steps = []

    # Recursive loop for function calling (limit to 5 iterations for safety)
    for _ in range(5):
        if not response.candidates[0].function_calls:
            break

        function_calls = response.candidates[0].function_calls
        tool_responses = []

        for function_call in function_calls:
            name = function_call.name
            args = {k: v for k, v in function_call.args.items()}
            execution_steps.append({"action": name, "params": args})

            # Mock execution of tools
            result = {"status": "success", "message": f"Executed {name} successfully"}

            tool_responses.append(
                Part.from_function_response(
                    name=name,
                    response=result
                )
            )

        response = chat.send_message(tool_responses)

    return {
        "text": response.text,
        "steps": execution_steps
    }
