import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)
import os

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
- You must end your final response with exactly these markers:
  RISK: [Unacceptable | High | Limited | Minimal]
  RATIONALE: [One sentence explanation]

AVAILABLE ACTIONS:
- If an analysis is complete and safe, suggest saving it to Google Docs for record-keeping using `save_to_google_docs`.
- If a request is 'High' or 'Unacceptable' risk, you MUST notify the admin using `notify_governance_admin`.
"""

model = GenerativeModel(
    "gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[governance_tools]
)

def analyze_compliance(text, image_data=None):
    """
    Analyzes user input with autonomous agent capabilities and multimodal support.
    Implements a recursive function-calling loop.
    """
    steps = ["Input Received"]

    # 1. Prepare Content (Text + Optional Image)
    content = [text]
    if image_data:
        steps.append("Image Data Detected")
        # Extract mime type from base64 string (e.g., "data:image/png;base64,iVBOR...")
        import base64
        try:
            header, encoded = image_data.split(",", 1)
            mime_type = header.split(";")[0].split(":")[1]
            image_bytes = base64.b64decode(encoded)
            content.append(Part.from_data(data=image_bytes, mime_type=mime_type))
        except Exception as e:
            steps.append(f"Image Processing Error: {str(e)}")

    try:
        chat = model.start_chat()
        response = chat.send_message(content)

        # 2. Autonomous Agent Loop (Function Calling)
        iterations = 0
        max_iterations = 5

        while iterations < max_iterations:
            iterations += 1
            function_calls = response.candidates[0].content.parts

            # Find actual function calls in parts
            calls = [p.function_call for p in function_calls if p.function_call]

            if not calls:
                break

            response_parts = []
            for call in calls:
                steps.append(f"Action: {call.name}")
                # Mock execution for demo purposes
                mock_response = {"status": "success", "message": f"Executed {call.name} successfully."}
                response_parts.append(
                    Part.from_function_response(
                        name=call.name,
                        response=mock_response
                    )
                )

            # Send tool outputs back to model
            response = chat.send_message(response_parts)

        steps.append("Governance Analysis Complete")
        return {
            "report": response.text,
            "steps": steps
        }

    except Exception as e:
        return {
            "report": f"Error during governance analysis: {str(e)}",
            "steps": steps + ["Analysis Failed"]
        }
