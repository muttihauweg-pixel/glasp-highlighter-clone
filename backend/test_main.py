import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from main import app

class TestAGOS(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("gemini.model.start_chat")
    def test_process_text_only(self, mock_start_chat):
        # Mock Gemini response
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "RISK: Minimal\nRATIONALE: This is a safe request."

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        response = self.client.post("/process", json={"input": "Hello AG-OS"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("safe request", data["result"]["rationale"])
        self.assertIn("hash", data["audit"])

    @patch("gemini.model.start_chat")
    def test_process_multimodal(self, mock_start_chat):
        # Mock Gemini response
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "RISK: High\nRATIONALE: Image contains sensitive data."

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        # Mock image data
        image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

        response = self.client.post("/process", json={
            "input": "Analyze this image",
            "image": image_b64
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("sensitive data", data["result"]["rationale"])

    @patch("gemini.model.start_chat")
    def test_function_calling_loop(self, mock_start_chat):
        # Mock Gemini responses for loop
        mock_chat = MagicMock()

        # 1st response: Trigger function call
        resp1 = MagicMock()
        cand1 = MagicMock()
        func_call = MagicMock()
        func_call.name = "notify_governance_admin"
        cand1.function_calls = [func_call]
        resp1.candidates = [cand1]

        # 2nd response: Final text
        resp2 = MagicMock()
        cand2 = MagicMock()
        cand2.function_calls = []
        resp2.candidates = [cand2]
        resp2.text = "RISK: High\nRATIONALE: Admin notified."

        mock_chat.send_message.side_effect = [resp1, resp2]
        mock_start_chat.return_value = mock_chat

        response = self.client.post("/process", json={"input": "Dangerous request"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        # Check if "Action: notify_governance_admin" is in steps
        self.assertTrue(any("notify_governance_admin" in step for step in data["result"]["steps"]))

if __name__ == "__main__":
    unittest.main()
