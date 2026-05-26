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
You are the AI Governance Operating System (AG-OS) Agent, a multi-agent orchestration layer designed to ensure AI safety and compliance.
Your architecture consists of three specialized internal personas:

1. MANAGER: Coordinates the governance workflow, analyzes the intent of the user input, and plans the necessary compliance checks.
2. WORKER: Executes specific tool calls, such as notifying administrators or generating documentation.
3. REVIEWER: Conducts a final audit of the proposed actions against the EU AI Act and corporate policy.

OPERATING PRINCIPLES:
- AUTONOMY: Proactively trigger tools based on risk assessment.
- PRECISION: You MUST categorize the final risk into exactly one of these levels: 'Unacceptable', 'High', 'Limited', or 'Minimal'.
- TRACEABILITY: Provide a clear rationale for every decision.

OUTPUT FORMAT:
You must conclude your analysis with the following markers:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of your governance decision]

MANDATORY ACTIONS:
- For 'High' or 'Unacceptable' risk: You MUST call `notify_governance_admin`.
- For 'Minimal' or 'Limited' risk: You should offer to `save_to_google_docs` if it's a formal report or significant result.

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
    Supports multimodal input (text + image) and recursive tool execution.
    """
    try:
        content_parts = [text]
        steps = ["Input Received"]

        if image_data:
            if "," in image_data:
                header, base64_str = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                base64_str = image_data
                mime_type = "image/png"

            image_bytes = base64.b64decode(base64_str)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))
            steps.append("Image Data Processed")

        chat = model.start_chat()
        steps.append("Compliance Analysis Initialized")

        response = chat.send_message(content_parts)

        # Recursive function calling loop
        for _ in range(5):  # Max 5 iterations
            if not response.candidates[0].function_calls:
                break

            function_calls = response.candidates[0].function_calls
            tool_responses = []

            for function_call in function_calls:
                name = function_call.name
                params = function_call.args
                steps.append(f"Action Triggered: {name}")

                # Mock execution of tools for the demo
                result = {"status": "success", "message": f"Simulated execution of {name}"}

                tool_responses.append(
                    Part.from_function_response(
                        name=name,
                        response=result
                    )
                )

            # Send tool results back to model
            response = chat.send_message(tool_responses)

        final_text = response.text
        steps.append("Policy Enforcement Finalized")

        # Robust extraction of risk and rationale
        risk_match = re.search(r"RISK:\s*(\w+)", final_text, re.IGNORECASE)

        if risk_match:
            risk_level = risk_match.group(1).capitalize()
            # Validate against our standard set
            if risk_level not in ["Unacceptable", "High", "Limited", "Minimal"]:
                risk_level = None
        else:
            risk_level = None

        # Fallback to keyword search if marker is missing or invalid
        if not risk_level:
            if "unacceptable" in final_text.lower(): risk_level = "Unacceptable"
            elif "high" in final_text.lower(): risk_level = "High"
            elif "limited" in final_text.lower(): risk_level = "Limited"
            else: risk_level = "Minimal"

        return {
            "response": final_text,
            "risk_level": risk_level,
            "steps": steps
        }
    except Exception as e:
        return {
            "response": f"Governance Analysis Error: {str(e)}",
            "risk_level": "Unknown",
            "steps": ["Error encountered"]
        }
