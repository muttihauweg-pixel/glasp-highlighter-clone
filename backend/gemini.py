import vertexai
from vertexai.generative_models import GenerativeModel
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "YOUR_PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4")

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-1.5-pro")

def analyze_compliance(text):
    """
    Analyzes the user input against EU AI Act risk categories using Gemini 1.5 Pro.
    """
    prompt = f"""
    You are an AI Governance Expert. Analyze the following user request under EU AI Act risk categories (Unacceptable, High, Limited, Minimal).

    Request: "{text}"

    Return a detailed analysis including:
    1. Risk Level
    2. Compliance Issues
    3. Recommended Mitigations

    Format the output clearly.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback for demo if credentials are not configured
        return f"Governance Analysis (Demo Mode): Analysis for '{text}'. Error or missing credentials: {str(e)}"
