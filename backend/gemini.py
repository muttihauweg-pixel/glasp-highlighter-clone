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

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs for record-keeping using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.

IMPORTANT: ALWAYS include 'RISK_ASSESSMENT: <level>' in your final response.
"""

def get_model():
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
    model = get_model()
    chat = model.start_chat()

    content_parts = [Part.from_text(text)]

    if image_data:
        # Assuming image_data is a base64 string with header like "data:image/png;base64,..."
        if "," in image_data:
            header, base64_str = image_data.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]
        else:
            base64_str = image_data
            mime_type = "image/png" # Default

        image_bytes = base64.b64decode(base64_str)
        content_parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

    response = chat.send_message(content_parts)

    execution_steps = ["Input Received", "Initial Analysis"]

    # Agentic Loop for Function Calling
    max_iterations = 5
    for _ in range(max_iterations):
        function_call = None
        # Check if the last response part has a function call
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        if not function_call:
            break

        function_name = function_call.name
        execution_steps.append(f"Tool Use: {function_name}")

        # Mocking tool execution results
        if function_name == "save_to_google_docs":
            api_response = {"status": "success", "doc_id": "mock-doc-123"}
        elif function_name == "notify_governance_admin":
            api_response = {"status": "delivered", "priority": "high"}
        else:
            api_response = {"error": "Unknown tool"}

        # Send the function response back to the model
        response = chat.send_message(
            Part.from_function_response(
                name=function_name,
                response=api_response
            )
        )

    execution_steps.append("Final Compliance Report Generated")

    return {
        "text": response.text,
        "steps": execution_steps
    }
