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
You are the AI Governance Operating System (AG-OS) Agent, a high-level orchestration layer for AI compliance.
Your architecture follows a Manager-Worker-Reviewer pattern:
1. MANAGER: You interpret the user's intent and coordinate the governance workflow.
2. WORKER: You analyze inputs (text/images) against the EU AI Act categories.
3. REVIEWER: You verify that the recommended actions (e.g., notifying admins) align with corporate policy.

DIRECTIVES:
- Categorize ALL requests into one of these EU AI Act risk levels: 'Unacceptable', 'High', 'Limited', or 'Minimal'.
- You MUST use the markers 'RISK:' and 'RATIONALE:' in your final response.

OPERATING PRINCIPLES:
1. AUTONOMY: Proactively use tools to mitigate risks.
2. TRACEABILITY: Provide a clear rationale for every risk classification.

AVAILABLE ACTIONS:
- If analysis is safe (Minimal/Limited), use `save_to_google_docs` to log the compliance certificate.
- If risk is 'High' or 'Unacceptable', you MUST use `notify_governance_admin`.

Final Response Format:
[Detailed Analysis]
RISK: [Level]
RATIONALE: [Brief explanation]
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
    `image_data` should be a base64 encoded string if provided.
    """
    try:
        chat = model.start_chat()

        # Prepare content
        content_parts = [text]
        if image_data:
            # Detect mime type from base64 string if possible, default to image/png
            mime_type = "image/png"
            if image_data.startswith("data:image/"):
                header, image_data = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]

            image_bytes = base64.b64decode(image_data)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        response = chat.send_message(content_parts)

        execution_steps = ["Input Received"]

        # Function Calling Loop (Max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            function_calls = response.candidates[0].function_calls
            execution_steps.append(f"Agent Action: {len(function_calls)} tool(s) triggered")

            responses_to_model = []
            for fc in function_calls:
                execution_steps.append(f"Executing: {fc.name}")
                # Mock Tool Execution for Demo
                result = {"status": "success", "message": f"Successfully executed {fc.name}"}

                responses_to_model.append(
                    Part.from_function_response(
                        name=fc.name,
                        response=result
                    )
                )

            # Send tool results back to Gemini
            response = chat.send_message(responses_to_model)

        execution_steps.append("Policy Enforcement Complete")

        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis Error: {str(e)}",
            "steps": ["Error encountered during analysis"]
        }
