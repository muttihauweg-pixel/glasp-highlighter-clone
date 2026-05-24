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

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs for record-keeping using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.

RESPONSE FORMAT:
You MUST include the following markers in your response:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of the risk assessment]

Then, proceed with any tool calls or final summary.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input (text + optional image).
    """
    try:
        content_parts = [text]
        if image_data:
            # Assume image_data is a base64 string
            if "base64," in image_data:
                header, image_data = image_data.split("base64,")
                mime_type = header.split(":")[1].split(";")[0]
            else:
                mime_type = "image/jpeg" # Default

            image_bytes = base64.b64decode(image_data)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        execution_steps = ["User Request Received"]

        # Recursive function calling loop (limit to 5 iterations)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            # Collect all function responses for the current turn
            function_responses = []
            for function_call in response.candidates[0].function_calls:
                name = function_call.name
                params = {k: v for k, v in function_call.args.items()}
                execution_steps.append(f"Tool Call: {name}({params})")

                # Mock execution for demo
                mock_result = f"Success: {name} executed."

                function_responses.append(
                    Part.from_function_response(
                        name=name,
                        response={"result": mock_result}
                    )
                )

            # Send all responses back in a single message
            response = chat.send_message(function_responses)

        # Safely access text if available
        try:
            final_text = response.text
        except ValueError:
            # Fallback if no text is returned (e.g., only tool calls)
            final_text = "Analysis completed with autonomous actions."

        # Extract risk and rationale for structured output
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", final_text, re.I)
        rationale_match = re.search(r"RATIONALE:\s*(.*?)(?=\n\n|\n[A-Z]+:|$)", final_text, re.S | re.I)

        risk = risk_match.group(1).capitalize() if risk_match else "Unknown"
        rationale = rationale_match.group(1).strip() if rationale_match else final_text

        execution_steps.append("Analysis Finalized")

        return {
            "full_response": final_text,
            "risk": risk,
            "rationale": rationale,
            "steps": execution_steps
        }

    except Exception as e:
        return {
            "full_response": f"Error: {str(e)}",
            "risk": "Error",
            "rationale": str(e),
            "steps": ["Error encountered"]
        }
