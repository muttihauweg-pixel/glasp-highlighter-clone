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
import re

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")

# Initialize Vertex AI
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
except Exception:
    pass # Handle cases where credentials might not be available during initialization

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

MANDATORY RESPONSE FORMAT:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of the risk assessment]

Respond in a professional, authoritative tone.
"""

def get_model():
    return GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[governance_tools]
    )

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input and recursive tool execution.
    """
    model = get_model()
    chat = model.start_chat()

    inputs = [text]

    # Multimodal support (Step 2 will refine this, but adding placeholder logic here)
    if image_base64:
        try:
            if "base64," in image_base64:
                header, encoded = image_base64.split("base64,")
                mime_type = header.split(":")[1].split(";")[0]
            else:
                encoded = image_base64
                mime_type = "image/png"

            image_bytes = base64.b64decode(encoded)
            inputs.append(Part.from_data(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            execution_steps.append(f"Image decode error: {str(e)}")

    execution_steps = ["Governance scan initiated"]

    try:
        response = chat.send_message(inputs)

        # Recursive function-calling loop
        iterations = 0
        while iterations < 5:
            function_calls = []
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_calls.append(part.function_call)

            if not function_calls:
                break

            execution_steps.append(f"Analyzing {len(function_calls)} governance actions...")

            responses = []
            for call in function_calls:
                execution_steps.append(f"Executing: {call.name}")
                # Mock implementation for demo
                result = {"status": "success", "message": f"Action '{call.name}' logged in audit trail."}
                responses.append(Part.from_function_response(
                    name=call.name,
                    response=result
                ))

            response = chat.send_message(responses)
            iterations += 1

        final_text = response.text

        # Risk & Rationale Parsing (Step 3 will refine this)
        risk = "Minimal"
        rationale = "No specific risk markers found."

        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", final_text, re.IGNORECASE)
        if risk_match:
            risk = risk_match.group(1).capitalize()

        rationale_match = re.search(r"RATIONALE:\s*(.*)", final_text, re.IGNORECASE | re.DOTALL)
        if rationale_match:
            rationale = rationale_match.group(1).strip()

        return {
            "text": final_text,
            "risk": risk,
            "rationale": rationale,
            "steps": execution_steps
        }

    except Exception as e:
        return {
            "text": f"Error during analysis: {str(e)}",
            "risk": "High",
            "rationale": "System error during governance check.",
            "steps": execution_steps + ["Analysis failed"]
        }
