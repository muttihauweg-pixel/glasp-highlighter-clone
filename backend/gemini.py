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
You are the AI Governance Operating System (AG-OS) Agent, a specialized compliance layer built on Gemini 1.5 Pro.
Your mission is to evaluate AI interactions against the EU AI Act and enterprise safety standards.

RISK CATEGORIZATION (EU AI ACT):
- UNACCEPTABLE: Cognitive behavioral manipulation, social scoring, real-time biometric ID in public, etc. (MUST NOTIFY ADMIN)
- HIGH: Critical infrastructure, educational/vocational training, employment, essential services, law enforcement. (MUST NOTIFY ADMIN)
- LIMITED: Chatbots (transparency required), deepfakes, emotion recognition. (LOG TO DOCS)
- MINIMAL: AI-enabled video games, spam filters, etc. (LOG TO DOCS)

OPERATING PRINCIPLES:
1. MANDATORY MARKERS: You MUST always include 'RISK: [Level]' and 'RATIONALE: [Reasoning]' in your final response.
2. PROACTIVE TOOL USE:
   - Use `notify_governance_admin` for HIGH and UNACCEPTABLE risks immediately.
   - Use `save_to_google_docs` for ALL completed analyses to maintain an official record.
3. MULTIMODAL ANALYSIS: Analyze any provided images (screenshots, system architectures, data flows) with the same rigor as text.

RESPONSE FORMAT:
Your response should be professional, concise, and structured for an executive audit.

Example:
RISK: High
RATIONALE: The request involves processing biometric data for recruitment purposes, which falls under the 'High-Risk' category of the EU AI Act.
[Detailed Analysis...]
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
    Returns a dict with the final response and the tool execution steps.
    """
    try:
        chat = model.start_chat()

        content = [text]
        if image_data:
            # Handle data URL if present
            if "," in image_data:
                header, image_data = image_data.split(",", 1)
                mime_type = header.split(":")[1].split(";")[0]
            else:
                mime_type = "image/jpeg" # Default

            image_part = Part.from_data(
                data=base64.b64decode(image_data),
                mime_type=mime_type
            )
            content.append(image_part)

        response = chat.send_message(content)

        execution_steps = ["Initial Analysis Started"]
        if image_data:
            execution_steps[0] = "Multimodal Analysis Started (Image + Text)"

        # Simple loop to handle function calls (max 5 iterations)
        for _ in range(5):
            if not response.candidates[0].content.parts[0].function_call:
                break

            function_call = response.candidates[0].content.parts[0].function_call
            fn_name = function_call.name
            fn_args = function_call.args

            execution_steps.append(f"Tool Call: {fn_name}")

            # Mock execution of the function
            # In a real app, you would call the actual API here
            mock_response = {"status": "success", "message": f"Executed {fn_name} successfully"}

            # Send the tool output back to the model
            response = chat.send_message(
                Part.from_function_response(
                    name=fn_name,
                    response=mock_response
                )
            )

        execution_steps.append("Final Governance Decision Rendered")

        return {
            "text": response.text,
            "steps": execution_steps
        }
    except Exception as e:
        return {
            "text": f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error: {str(e)}",
            "steps": ["Error encountered during analysis"]
        }
