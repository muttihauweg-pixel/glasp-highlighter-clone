import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from gemini import analyze_compliance

class TestGovernanceLogic(unittest.TestCase):

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_high_risk(self, mock_start_chat):
        # Setup Mock Chat
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        # Mock Initial Response (Requesting Function Call)
        mock_response_1 = MagicMock()
        mock_candidate_1 = MagicMock()
        mock_call = MagicMock()
        mock_call.name = "notify_governance_admin"
        mock_call.args = {"risk_level": "High", "reason": "Potential medical diagnosis"}
        mock_candidate_1.function_calls = [mock_call]
        mock_response_1.candidates = [mock_candidate_1]

        # Mock Final Response
        mock_response_2 = MagicMock()
        mock_candidate_2 = MagicMock()
        mock_candidate_2.function_calls = []
        mock_response_2.candidates = [mock_candidate_2]
        mock_response_2.text = "RISK: High\nRATIONALE: This request involves medical advice.\nACTION: Admin notified."

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        # Execute
        result = analyze_compliance("Analyze this medical image")

        # Assertions
        self.assertIn("RISK: High", result["text"])
        self.assertEqual(len(result["tool_calls"]), 1)
        self.assertEqual(result["tool_calls"][0]["name"], "notify_governance_admin")

    @patch("gemini.model.start_chat")
    def test_analyze_compliance_minimal_risk(self, mock_start_chat):
        # Setup Mock Chat
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        # Mock Response
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "RISK: Minimal\nRATIONALE: This is a general query.\nRESULT: Safe to proceed."

        mock_chat.send_message.return_value = mock_response

        # Execute
        result = analyze_compliance("What is the capital of France?")

        # Assertions
        self.assertIn("RISK: Minimal", result["text"])
        self.assertEqual(len(result["tool_calls"]), 0)

if __name__ == "__main__":
    unittest.main()
