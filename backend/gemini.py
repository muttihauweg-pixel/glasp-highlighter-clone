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

IMPORTANT: You MUST include the following markers in your final response:
RISK: [Unacceptable | High | Limited | Minimal]
RATIONALE: [Detailed explanation of your decision]
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    """
    try:
        # Prepare parts for multimodal input
        parts = [text]
        if image_data:
            # image_data is expected to be base64 string
            if isinstance(image_data, str) and image_data.startswith("data:"):
                header, base64_str = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
                import base64
                image_bytes = base64.b64decode(base64_str)
                parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(parts)

        execution_steps = ["Initial Analysis Started"]

        # Iterative loop to handle function calls (max 5 iterations)
        for _ in range(5):
            found_call = False
            # Check for function calls in the current response
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        found_call = True
                        call = part.function_call
                        name = call.name
                        args = call.args

                        execution_steps.append(f"Action: {name}")

                        # Mock execution
                        mock_response = {"status": "success", "message": f"Mock executed {name}"}

                        response = chat.send_message(
                            Part.from_function_response(
                                name=name,
                                response=mock_response
                            )
                        )
                        break # Process one call at a time for simplicity in demo

            if not found_call:
                break

        execution_steps.append("Final Policy Decision Reached")
        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Analysis failed. Error: {str(e)}",
            "steps": ["Error encountered"]
        }
