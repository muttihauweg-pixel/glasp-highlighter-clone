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

# Vertex AI initialization is handled within the analysis function for better mockability

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
You are the AI Governance Operating System (AG-OS) Agent, a specialized compliance entity designed to enforce the EU AI Act.

CORE DIRECTIVE:
Analyze the user's AI request and any provided visual context to determine its risk category.

RISK CATEGORIES (EU AI Act):
- UNACCEPTABLE: Prohibited practices (e.g., social scoring, real-time remote biometric ID).
- HIGH: Significant risk to health, safety, or fundamental rights (e.g., recruitment, credit scoring, justice).
- LIMITED: Specific transparency risks (e.g., chatbots, deepfakes).
- MINIMAL: All other AI systems.

OPERATING PROTOCOL:
1. Identify the core application area.
2. If risk is 'HIGH' or 'UNACCEPTABLE', you MUST call `notify_governance_admin`.
3. If the request is compliant, suggest `save_to_google_docs` for the audit trail.
4. MANDATORY: Your response MUST end with the tag 'RISK_ASSESSMENT: [CATEGORY]' where [CATEGORY] is one of the four mentioned above.

Respond in a professional, authoritative tone. Be concise.
"""

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    """
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[governance_tools]
        )

        content_parts = [text]

        if image_data:
            # Handle base64 image
            if "," in image_data:
                header, base64_str = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                base64_str = image_data
                mime_type = "image/png" # Default

            image_bytes = base64.b64decode(base64_str)
            content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(content_parts)

        # Recursive function calling loop (with parallel tool use support)
        steps = []
        max_iterations = 5
        iterations = 0

        while response.candidates[0].function_calls and iterations < max_iterations:
            iterations += 1
            tool_responses = []

            for function_call in response.candidates[0].function_calls:
                function_name = function_call.name
                args = function_call.args

                steps.append(f"Tool Use: {function_name}({dict(args)})")

                # For the demo, we simulate tool execution
                tool_result = f"Successfully executed {function_name}"

                tool_responses.append(
                    Part.from_function_response(
                        name=function_name,
                        response={"content": tool_result}
                    )
                )

            response = chat.send_message(tool_responses)

        return {
            "text": response.text,
            "steps": steps
        }
    except Exception as e:
        return f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error: {str(e)}"
