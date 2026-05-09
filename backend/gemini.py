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

RISK CATEGORIES (EU AI Act):
- Unacceptable: Prohibited AI practices (e.g., social scoring, biometric identification in public spaces).
- High: AI in critical infrastructures, education, employment, law enforcement (requires strict governance).
- Limited: AI with specific transparency obligations (e.g., chatbots).
- Minimal: Most AI systems (e.g., spam filters, AI-enabled games).

OPERATING PRINCIPLES:
1. AUTONOMY: Proactively assess risks and take necessary actions using tools.
2. PRECISION: Categorize risks exactly into one of the four categories above.
3. TRACEABILITY: Provide a clear rationale.

AVAILABLE ACTIONS:
- If an analysis is complete and 'Limited' or 'Minimal' risk, suggest saving it to Google Docs using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.

Respond with your final analysis and ensure you mention the Risk Level clearly.
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
    Handles recursive tool calls.
    """
    model = get_model()
    chat = model.start_chat()

    parts = [text]
    if image_data:
        # Expecting base64 image data like "data:image/png;base64,..."
        try:
            header, encoded = image_data.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]
            image_bytes = base64.b64decode(encoded)
            parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            print(f"Error processing image: {e}")

    execution_steps = ["Input Received"]

    response = chat.send_message(parts)

    max_iterations = 5
    for _ in range(max_iterations):
        if not response.candidates[0].function_calls:
            break

        function_calls = response.candidates[0].function_calls
        tool_responses = []

        for fc in function_calls:
            execution_steps.append(f"Executing: {fc.name}")
            # Mocking tool execution for demo
            mock_result = {"status": "success", "message": f"Action {fc.name} completed successfully."}

            tool_responses.append(
                Part.from_function_response(
                    name=fc.name,
                    response=mock_result
                )
            )

        response = chat.send_message(tool_responses)

    execution_steps.append("Analysis Finalized")

    return {
        "text": response.text,
        "steps": execution_steps
    }
