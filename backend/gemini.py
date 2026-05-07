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
At the end of your analysis, ALWAYS include:
Risk Level: [Unacceptable/High/Limited/Minimal]
Rationale: [Brief explanation]

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs for record-keeping using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.

Respond in a professional, authoritative tone.
"""

def get_model():
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return GenerativeModel(
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
        model = get_model()
        chat = model.start_chat()

        content_parts = [Part.from_text(text)]
        if image_data:
            # Handle base64 image data
            if "," in image_data:
                header, base64_data = image_data.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                base64_data = image_data
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(base64_data)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        response = chat.send_message(content_parts)

        execution_steps = ["Compliance Analysis"]

        # Agentic Loop (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].function_calls:
                break

            # Record tool steps
            for fc in response.candidates[0].function_calls:
                execution_steps.append(f"Action: {fc.name}")

            # In a demo, we mock the tool results
            tool_results = []
            for fc in response.candidates[0].function_calls:
                tool_results.append(
                    Part.from_function_response(
                        name=fc.name,
                        response={"result": "Success: Operation completed and logged."}
                    )
                )

            response = chat.send_message(tool_results)

        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {
            "text": f"Governance Analysis (Error Mode): {str(e)}",
            "steps": ["Error encountered during analysis"]
        }
