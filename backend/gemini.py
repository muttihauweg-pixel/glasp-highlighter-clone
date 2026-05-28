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

# Initialize Vertex AI (wrapped to allow testing without credentials)
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception:
    pass

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
1. AGENTIC HIERARCHY:
   - MANAGER: Orchestrate the analysis workflow.
   - WORKER: Analyze input (text/images) for compliance risks.
   - REVIEWER: Verify findings and trigger mitigation tools.

2. PRECISION CATEGORIZATION (EU AI Act):
   - 'Unacceptable': Prohibited (e.g., social scoring).
   - 'High': Significant risk to health/safety/rights.
   - 'Limited': Transparency risks.
   - 'Minimal': Low risk.

3. MANDATORY OUTPUT FORMAT:
   Every response MUST include:
   RISK: [Category]
   RATIONALE: [Why this category was chosen]
   MITIGATION: [Actions taken/recommended]

AVAILABLE ACTIONS:
- `save_to_google_docs`: Save analysis for audit.
- `notify_governance_admin`: Urgent escalation for High/Unacceptable risks.

Respond with authority and precision.
"""

def get_model():
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[governance_tools]
    )

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities, multimodality, and function calling.
    """
    try:
        content_parts = [text]

        if image_base64:
            # Handle base64 image data
            if "," in image_base64:
                header, data = image_base64.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                data = image_base64
                mime_type = "image/png" # Default

            image_part = Part.from_data(
                data=base64.b64decode(data),
                mime_type=mime_type
            )
            content_parts.append(image_part)

        model = get_model()
        chat = model.start_chat()
        response = chat.send_message(content_parts)

        tool_steps = []

        # Simple Agentic Loop (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            function_responses = []
            for function_call in response.candidates[0].function_calls:
                tool_name = function_call.name
                tool_args = function_call.args
                tool_steps.append(f"Tool Call: {tool_name}")

                # Mock execution results
                if tool_name == "save_to_google_docs":
                    result = {"status": "success", "doc_id": "doc_12345"}
                elif tool_name == "notify_governance_admin":
                    result = {"status": "notified", "priority": "high"}
                else:
                    result = {"error": "unknown tool"}

                function_responses.append(
                    Part.from_function_response(
                        name=tool_name,
                        response=result
                    )
                )

            # Send all tool results back to the model in one turn
            response = chat.send_message(function_responses)

        return {
            "text": response.text,
            "steps": tool_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "steps": ["Error encountered"]
        }
