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
   - ALWAYS include the risk level in your final response in the format "RISK: [Level]".
   - ALWAYS include a brief rationale in the format "RATIONALE: [Reason]".
3. TRACEABILITY: Ensure every decision has a clear rationale for the audit trail.

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

def analyze_compliance(text, image_base64=None):
    """
    Analyzes user input with autonomous agent capabilities and function calling.
    Supports multimodal input (text + image).
    """
    try:
        content = [text]
        if image_base64:
            # Handle base64 data URL
            if "," in image_base64:
                header, data = image_base64.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
            else:
                data = image_base64
                mime_type = "image/png" # Default

            image_part = Part.from_data(
                data=base64.b64decode(data),
                mime_type=mime_type
            )
            content.append(image_part)

        chat = model.start_chat()
        response = chat.send_message(content)

        execution_steps = ["Input Received", "Gemini Analysis Started"]

        # Recursive Function Calling Loop
        iterations = 0
        max_iterations = 5

        while iterations < max_iterations:
            iterations += 1
            function_calls = response.candidates[0].function_calls
            if not function_calls:
                break

            tool_responses = []
            for function_call in function_calls:
                name = function_call.name
                args = function_call.args

                execution_steps.append(f"Tool Call: {name}")

                # Mock tool execution
                if name == "save_to_google_docs":
                    result = {"status": "success", "doc_url": "https://docs.google.com/demo-doc"}
                elif name == "notify_governance_admin":
                    result = {"status": "notified", "admin": "Governance Team"}
                else:
                    result = {"error": "Unknown tool"}

                tool_responses.append(Part.from_function_response(
                    name=name,
                    response=result
                ))

            response = chat.send_message(tool_responses)

        execution_steps.append("Final Policy Verdict Issued")

        # Extract risk level from text
        final_text = response.text
        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", final_text, re.IGNORECASE)
        risk_level = risk_match.group(1).capitalize() if risk_match else "Limited" # Default if not found

        return {
            "text": final_text,
            "steps": execution_steps,
            "risk": risk_level
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error: {str(e)}",
            "steps": ["Error encountered during analysis"],
            "risk": "Minimal"
        }
