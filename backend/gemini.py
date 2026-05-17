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

OUTPUT FORMAT:
Your final response MUST include these markers:
RISK: [Unacceptable | High | Limited | Minimal]
RATIONALE: [Detailed explanation of the risk assessment]

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
    Analyzes user input with autonomous agent capabilities, function calling, and multimodality.
    """
    try:
        chat = model.start_chat()

        # Prepare content parts (Text + optional Image)
        content_parts = [text]
        if image_base64:
            # Extract mime type if present, else default to image/png
            mime_type = "image/png"
            if "data:" in image_base64 and ";base64," in image_base64:
                mime_type = image_base64.split(":")[1].split(";")[0]
                image_base64 = image_base64.split(",")[1]

            image_part = Part.from_data(
                data=base64.b64decode(image_base64),
                mime_type=mime_type
            )
            content_parts.append(image_part)

        response = chat.send_message(content_parts)

        execution_steps = ["Analysis Initialized"]

        # Recursive Function Calling Loop (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].content.parts:
                break

            tool_calls = [part.function_call for part in response.candidates[0].content.parts if part.function_call]

            if not tool_calls:
                break

            responses = []
            for tool_call in tool_calls:
                step_desc = f"Executing Tool: {tool_call.name}"
                execution_steps.append(step_desc)

                # Mock execution for demo purposes
                # In production, you would call the actual API here
                result = {"status": "success", "message": f"Tool {tool_call.name} executed successfully"}

                responses.append(
                    Part.from_function_response(
                        name=tool_call.name,
                        response=result
                    )
                )

            # Send the tool output back to the model
            response = chat.send_message(responses)

        execution_steps.append("Policy Enforcement Complete")

        return {
            "text": response.text,
            "steps": execution_steps
        }

    except Exception as e:
        # Fallback for environment without credentials or other errors
        return {
            "text": f"RISK: Limited\nRATIONALE: Demo mode active. Analysis for input. (Error: {str(e)})",
            "steps": ["Analysis Initialized", "Fallback Mode Triggered"]
        }
