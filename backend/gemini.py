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
You are the AI Governance Operating System (AG-OS) Agent, a multi-agent orchestrator.
You operate using a Manager-Worker-Reviewer hierarchy to ensure all AI-related requests comply with the EU AI Act.

ROLES:
- MANAGER: Analyzes the user intent and plans the governance workflow.
- WORKER: Executes specific policy checks and tool actions.
- REVIEWER: Validates the final assessment against the EU AI Act risk categories.

OPERATING PRINCIPLES:
1. AUTONOMY: Proactively use tools to mitigate risks or log compliance.
2. PRECISION: Categorize risks into 'Unacceptable', 'High', 'Limited', or 'Minimal'.
3. TRACEABILITY: Every decision must have a clear rationale.

RESPONSE FORMAT:
You MUST provide your analysis in the following format:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of the risk assessment]
ACTION: [Action taken or recommended]

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.
"""

def get_model():
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[governance_tools]
    )

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities and recursive function calling.
    """
    model = get_model()

    # Prepare message parts
    parts = [Part.from_text(text)]
    if image_base64:
        try:
            if "," in image_base64:
                header, encoded = image_base64.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
                image_bytes = base64.b64decode(encoded)
            else:
                mime_type = "image/png"
                image_bytes = base64.b64decode(image_base64)
            parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))
        except Exception:
            pass # Fallback to text only if image parsing fails

    execution_steps = ["Input Received", "Orchestrator Analysis Started"]

    try:
        chat = model.start_chat()
        response = chat.send_message(parts)

        # Recursive Function Calling Loop
        max_iterations = 5
        for _ in range(max_iterations):
            if not response.candidates[0].content.parts:
                break

            tool_calls = [part.function_call for part in response.candidates[0].content.parts if part.function_call]

            if not tool_calls:
                break

            responses = []
            for call in tool_calls:
                execution_steps.append(f"Executing: {call.name}")
                # Mock execution for the demo
                result = {"status": "success", "message": f"Action '{call.name}' executed successfully."}
                responses.append(
                    Part.from_function_response(
                        name=call.name,
                        response=result
                    )
                )

            # Send tool results back to the model
            response = chat.send_message(responses)

        full_text = response.text

        # Risk Extraction logic
        risk = "Minimal"
        rationale = "No specific risk identified."
        import re
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", full_text, re.IGNORECASE)
        if risk_match:
            risk = risk_match.group(1).capitalize()

        rationale_match = re.search(r"RATIONALE:\s*(.*?)(?=ACTION:|$)", full_text, re.DOTALL | re.IGNORECASE)
        if rationale_match:
            rationale = rationale_match.group(1).strip()

        execution_steps.append("Governance Review Finalized")

        return {
            "full_response": full_text,
            "data": {
                "risk": risk,
                "rationale": rationale,
                "steps": execution_steps,
                "processed_output": "Governance check and mitigation actions completed."
            }
        }
    except Exception as e:
        return {
            "full_response": f"Governance Analysis (Demo Mode): Error: {str(e)}",
            "data": {
                "risk": "Error",
                "steps": ["Input Received", "Analysis Interrupted"],
                "processed_output": f"Error: {str(e)}"
            }
        }
