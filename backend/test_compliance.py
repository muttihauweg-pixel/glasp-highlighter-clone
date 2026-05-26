import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from gemini import analyze_compliance

class TestCompliance(unittest.TestCase):

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_text_only(self, mock_start_chat):
        # Setup mock chat and response
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "RISK: Minimal\nRATIONALE: This is a safe request."
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].function_calls = []

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Hello AI")

        self.assertEqual(result["risk_level"], "Minimal")
        self.assertIn("Minimal", result["response"])
        self.assertIn("Input Received", result["steps"])
        self.assertEqual(mock_chat.send_message.call_count, 1)

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_with_function_call(self, mock_start_chat):
        # Setup mock chat
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        # First response triggers a function call
        mock_response_1 = MagicMock()
        fc = MagicMock()
        fc.name = "save_to_google_docs"
        fc.args = {"title": "Test", "content": "Test content"}
        mock_response_1.candidates = [MagicMock()]
        mock_response_1.candidates[0].function_calls = [fc]

        # Second response is the final text
        mock_response_2 = MagicMock()
        mock_response_2.text = "RISK: Minimal\nRATIONALE: Saved to docs."
        mock_response_2.candidates = [MagicMock()]
        mock_response_2.candidates[0].function_calls = []

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        result = analyze_compliance("Save this safely")

        self.assertEqual(result["risk_level"], "Minimal")
        self.assertIn("Action Triggered: save_to_google_docs", result["steps"])
        self.assertEqual(mock_chat.send_message.call_count, 2)

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_high_risk(self, mock_start_chat):
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "RISK: High\nRATIONALE: This request is dangerous."
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].function_calls = []

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Do something bad")

        self.assertEqual(result["risk_level"], "High")

if __name__ == "__main__":
    unittest.main()
