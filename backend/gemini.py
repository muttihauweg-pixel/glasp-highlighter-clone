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
1. AUTONOMY: Proactively assess risks and take necessary actions (notifying admins or logging results).
2. PRECISION: Categorize risks into 'Unacceptable', 'High', 'Limited', or 'Minimal' based on EU AI Act criteria.
3. TRACEABILITY: Ensure every decision has a clear rationale for the audit trail.

EU AI ACT RISK CATEGORIES:
- UNACCEPTABLE: Social scoring, biometric identification (real-time), dark pattern manipulation. (ACTION: MUST NOTIFY ADMIN)
- HIGH: Critical infrastructure, education, employment, law enforcement, migration. (ACTION: MUST NOTIFY ADMIN)
- LIMITED: Chatbots (transparency obligations), emotion recognition. (ACTION: SAVE TO DOCS)
- MINIMAL: AI-enabled games, spam filters. (ACTION: SAVE TO DOCS)

OUTPUT FORMAT:
Your final response MUST include the following structured markers for the backend to parse:
RISK: [Category]
RATIONALE: [Detailed explanation of your decision]

AVAILABLE ACTIONS:
- Use `save_to_google_docs` for 'Minimal' or 'Limited' risk interactions to maintain a compliance record.
- Use `notify_governance_admin` for 'High' or 'Unacceptable' risk interactions to trigger human oversight.

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
    Supports multimodal input (text + images) and autonomous tool loops.
    """
    try:
        parts = [text]

        if image_data:
            # Extract mime type and base64 data
            mime_type_match = re.search(r'data:(.*?);base64,', image_data)
            if mime_type_match:
                mime_type = mime_type_match.group(1)
                base64_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(base64_data)
                parts.append(Part.from_data(data=image_bytes, mime_type=mime_type))

        chat = model.start_chat()
        response = chat.send_message(parts)

        tool_steps = []
        max_iterations = 5

        for _ in range(max_iterations):
            if not response.candidates[0].content.parts:
                break

            function_calls = [p.function_call for p in response.candidates[0].content.parts if p.function_call]

            if not function_calls:
                break

            responses = []
            for fc in function_calls:
                # Simulate tool execution for the demo
                tool_steps.append(f"Executing tool: {fc.name}")
                mock_response = {"status": "success", "message": f"Tool {fc.name} executed successfully"}

                responses.append(Part.from_function_response(
                    name=fc.name,
                    response=mock_response
                ))

            response = chat.send_message(responses)

        return {
            "text": response.text,
            "tool_steps": tool_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error: {str(e)}",
            "tool_steps": []
        }
