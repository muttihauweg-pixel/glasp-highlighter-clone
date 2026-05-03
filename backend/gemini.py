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

At the end of your response, you MUST include a summary in this exact format:
RISK_ASSESSMENT: [Risk Level]
REASON: [Short Reason]
"""

# Initialize Model outside to avoid re-init in loop if possible,
# but keep it flexible for structured output if needed later.
model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities, function calling, and multimodality.
    """
    try:
        # Re-initialize to ensure fresh state if needed, though start_chat usually handles it.
        # However, to be extra safe with tool state/history:
        current_model = GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[governance_tools]
        )

        content_parts = [Part.from_text(text)]

        if image_data:
            if "," in image_data:
                header, base64_str = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                base64_str = image_data
                mime_type = "image/png"

            image_bytes = base64.b64decode(base64_str)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = current_model.start_chat()
        response = chat.send_message(content_parts)

        execution_steps = ["User Input Received"]

        iterations = 0
        max_iterations = 5

        while response.candidates[0].content.parts[0].function_call and iterations < max_iterations:
            iterations += 1
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name

            execution_steps.append(f"Agent Action: {function_name}")

            # Mock Tool Execution
            if function_name == "save_to_google_docs":
                result = {"status": "success", "doc_url": "https://docs.google.com/example"}
            elif function_name == "notify_governance_admin":
                result = {"status": "notified", "admin": "Governance Board"}
            else:
                result = {"error": "Unknown tool"}

            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response=result
                )
            )

        execution_steps.append("Final Policy Decision")

        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Analysis failed. Error: {str(e)}",
            "steps": ["Input Received", "Error Encountered"]
        }
