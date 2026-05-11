import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    Content
)
import os
import json

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
You MUST always include the following markers in your final response:
RISK: [Unacceptable/High/Limited/Minimal]
RATIONALE: [Detailed explanation of your governance decision]

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

def analyze_compliance(text, image_bytes=None, mime_type=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodality if image_bytes is provided.
    """
    steps = ["Input Received", "AI Agent Initialization"]

    contents = []
    if image_bytes and mime_type:
        contents.append(Part.from_data(data=image_bytes, mime_type=mime_type))
        steps.append("Image Data Processed")

    contents.append(text)

    try:
        chat = model.start_chat()
        response = chat.send_message(contents)

        # Agentic Loop for Function Calling
        iterations = 0
        max_iterations = 5

        while response.candidates[0].content.parts[0].function_call and iterations < max_iterations:
            iterations += 1
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name

            steps.append(f"Tool Call: {function_name}")

            # Mocking the actual tool execution for the demo
            # In a real app, you would execute the code here
            if function_name == "save_to_google_docs":
                args = function_call.args
                tool_result = f"Document '{args.get('title')}' successfully created in Google Docs."
            elif function_name == "notify_governance_admin":
                args = function_call.args
                tool_result = f"Governance administrator notified of {args.get('risk_level')} risk. Ticket #GOV-{iterations}42 generated."
            else:
                tool_result = f"Successfully executed {function_name}"

            # Send the result back to the model
            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"result": tool_result}
                )
            )

        steps.append("Governance Analysis Finalized")

        return {
            "text": response.text,
            "steps": steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Error): {str(e)}",
            "steps": steps + ["Analysis Failed"]
        }
