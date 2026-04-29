import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini import analyze_compliance

class TestAgent(unittest.TestCase):

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_text_only(self, mock_start_chat):
        # Mocking the chat and response
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_candidate = MagicMock()

        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "This request is safe and follows EU AI Act guidelines."

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        result = analyze_compliance("How do I make a cake?")

        self.assertEqual(result["risk_level"], "Minimal")
        self.assertIn("Input Received", result["steps"])
        self.assertIn("Policy Enforcement Complete", result["steps"])
        self.assertEqual(result["report"], mock_response.text)

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_with_function_call(self, mock_start_chat):
        # Mocking the chat and sequential responses
        mock_chat = MagicMock()

        # 1. First response with a function call
        mock_response_1 = MagicMock()
        mock_candidate_1 = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "notify_governance_admin"
        mock_function_call.args = {"risk_level": "High", "reason": "Potential biometric data usage"}
        mock_candidate_1.function_calls = [mock_function_call]
        mock_response_1.candidates = [mock_candidate_1]

        # 2. Second response (final text)
        mock_response_2 = MagicMock()
        mock_candidate_2 = MagicMock()
        mock_candidate_2.function_calls = []
        mock_response_2.candidates = [mock_candidate_2]
        mock_response_2.text = "Admin notified. High-risk application flagged."

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]
        mock_start_chat.return_value = mock_chat

        result = analyze_compliance("Analyze this biometric identification system.")

        self.assertEqual(result["risk_level"], "High")
        self.assertTrue(any("Admin Notified" in s for s in result["steps"]))
        self.assertIn("Admin notified. High-risk application flagged.", result["report"])

if __name__ == "__main__":
    unittest.main()
