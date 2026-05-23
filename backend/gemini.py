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
You are the AI Governance Operating System (AG-OS) Agent.
Your primary directive is to ensure all AI-related requests comply with the EU AI Act and corporate safety policies.

OPERATING PRINCIPLES:
1. AUTONOMY: You proactively assess risks and take necessary actions (like notifying admins or logging results).
2. PRECISION: Categorize risks into 'Unacceptable', 'High', 'Limited', or 'Minimal'.
3. TRACEABILITY: Ensure every decision has a clear rationale for the audit trail.

MANDATORY RESPONSE FORMAT:
Your response MUST include the following markers:
RISK: [Unacceptable | High | Limited | Minimal]
RATIONALE: [Detailed explanation of your assessment]

AVAILABLE ACTIONS:
- If an analysis is complete and safe, you MUST suggest saving it to Google Docs using `save_to_google_docs`.
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
    Analyzes user input with autonomous agent capabilities, multimodality, and function calling.
    """
    try:
        chat = model.start_chat()

        # Prepare content parts
        content_parts = [Part.from_text(text)]

        if image_data:
            # Handle base64 image (data:image/png;base64,...)
            if "," in image_data:
                header, base64_str = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                base64_str = image_data
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(base64_str)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        response = chat.send_message(content_parts)

        # Agentic Execution Flow Logging
        execution_steps = ["Input Received", "Gemini Analysis"]

        # Recursive Function Calling Loop (max 5 iterations for demo safety)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            tool_responses = []
            for function_call in response.candidates[0].function_calls:
                fn_name = function_call.name
                execution_steps.append(f"Executing: {fn_name}")

                # Mock execution results for the agent
                result = {"status": "success", "message": f"Tool {fn_name} executed successfully"}

                tool_responses.append(
                    Part.from_function_response(
                        name=fn_name,
                        response=result
                    )
                )

            # Feed batch of tool responses back to model
            response = chat.send_message(tool_responses)

        final_text = response.text

        # Extract structured data via regex
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", final_text, re.IGNORECASE)
        risk = risk_match.group(1).capitalize() if risk_match else "Minimal"

        execution_steps.append("Policy Enforcement Complete")

        return {
            "text": final_text,
            "risk": risk,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Error during analysis. {str(e)}",
            "risk": "High",
            "steps": ["Input Received", "Analysis Failed"]
        }
