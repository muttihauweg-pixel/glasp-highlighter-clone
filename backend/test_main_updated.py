import unittest
from unittest.mock import MagicMock, patch
import json
from fastapi.testclient import TestClient
import sys
import os

# Ensure backend is in path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from main import app
import gemini

class TestGOSBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("gemini.model")
    @patch("gemini.vertexai.init")
    def test_process_input_success(self, mock_init, mock_model):
        # Mocking Gemini's response
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        # Mock final response with RISK and RATIONALE
        mock_response = MagicMock()
        mock_response.text = "RISK: Minimal\nRATIONALE: This request is safe for execution.\n\nEverything looks good."
        # No function calls in the first response for this test
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].function_calls = []

        mock_chat.send_message.return_value = mock_response

        payload = {
            "input": "How can I improve my startup pitch?",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        }

        response = self.client.post("/process", json=payload)

        data = response.json()
        if response.status_code != 200:
            print(f"Error response: {data}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("steps", data["result"])
        self.assertEqual(data["result"]["processed_output"], "This request is safe for execution.")
        self.assertIn("hash", data["audit"])

    @patch("gemini.model")
    @patch("gemini.vertexai.init")
    def test_process_input_high_risk_function_calling(self, mock_init, mock_model):
        # Mocking Gemini's response with function calling
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        # 1st response: Function call
        mock_fc = MagicMock()
        mock_fc.name = "notify_governance_admin"
        mock_fc.args = {"risk_level": "High", "reason": "Potential biometric data usage."}

        mock_response_1 = MagicMock()
        mock_response_1.candidates = [MagicMock()]
        mock_response_1.candidates[0].function_calls = [mock_fc]

        # 2nd response: Final text after function response
        mock_response_2 = MagicMock()
        mock_response_2.text = "RISK: High\nRATIONALE: Biometric identification is strictly regulated under the EU AI Act.\n\nAdministrator has been notified."
        mock_response_2.candidates = [MagicMock()]
        mock_response_2.candidates[0].function_calls = []

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        payload = {
            "input": "Identify people from this video feed."
        }

        response = self.client.post("/process", json=payload)

        data = response.json()
        if response.status_code != 200:
            print(f"Error response: {data}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Tool Call: notify_governance_admin", str(data["result"]["steps"]))
        self.assertIn("Biometric identification", data["result"]["processed_output"])

if __name__ == "__main__":
    unittest.main()
