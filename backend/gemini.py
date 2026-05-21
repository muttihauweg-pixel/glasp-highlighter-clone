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

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input.
    """
    steps = ["Input Received"]

    contents = [text]
    if image_data:
        # Detect mime type from base64 string
        # Expected format: "data:image/png;base64,..."
        mime_type = "image/jpeg"
        if "image/png" in image_data:
            mime_type = "image/png"

        base64_data = image_data.split(",")[1] if "," in image_data else image_data
        image_part = Part.from_data(
            data=base64.b64decode(base64_data),
            mime_type=mime_type
        )
        contents.append(image_part)
        steps.append("Multimodal Analysis Triggered")

    try:
        chat = model.start_chat()
        response = chat.send_message(contents)
        steps.append("Initial Governance Analysis")

        # Function calling loop
        iterations = 0
        while iterations < 5:
            iterations += 1

            # Check for function calls
            if response.candidates[0].function_calls:
                # Handle parallel tool calls
                tool_responses = []
                for function_call in response.candidates[0].function_calls:
                    name = function_call.name
                    args = function_call.args

                    steps.append(f"Autonomous Action: {name}")

                    # Mock execution
                    if name == "save_to_google_docs":
                        result = {"status": "success", "message": f"Document '{args['title']}' saved successfully."}
                    elif name == "notify_governance_admin":
                        result = {"status": "success", "message": f"Admin notified about {args['risk_level']} risk."}
                    else:
                        result = {"error": "Unknown tool"}

                    tool_responses.append(
                        Part.from_function_response(
                            name=name,
                            response=result
                        )
                    )

                # Send all tool responses back to model
                response = chat.send_message(tool_responses)
            else:
                # No more function calls
                break

        steps.append("Policy Enforcement Finalized")
        return {
            "text": response.text,
            "steps": steps
        }

    except Exception as e:
        error_msg = f"Governance Analysis (Error): {str(e)}"
        return {
            "text": error_msg,
            "steps": steps + ["Analysis Failed"]
        }
