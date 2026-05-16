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

MANDATORY OUTPUT FORMAT:
Your final response MUST include the following markers:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of why this risk level was chosen]

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

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input.
    """
    try:
        content = [text]
        if image_data:
            # Assuming image_data is base64 string like "data:image/png;base64,..."
            if "," in image_data:
                header, encoded = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                encoded = image_data
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(encoded)
            content.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content)

        tool_calls_executed = []

        # Agentic Loop: Handle potential function calls
        max_iterations = 5
        for _ in range(max_iterations):
            if not response.candidates[0].content.parts[0].function_call:
                break

            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            args = function_call.args

            # Mocking function execution for the demo
            tool_calls_executed.append(f"Tool Executed: {function_name}")

            # Send mock response back to model
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"result": "Action successfully logged and executed by AG-OS system."}
                )
            )

        return {
            "text": response.text,
            "steps": tool_calls_executed
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Error): {str(e)}",
            "steps": ["Error in analysis"]
        }
