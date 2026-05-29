import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from gemini import analyze_compliance

class TestCompliance(unittest.TestCase):

    @patch('gemini.get_model')
    def test_analyze_compliance_minimal_risk(self, mock_get_model):
        # Setup mock model and chat
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_get_model.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Mock response parts
        mock_part = MagicMock()
        mock_part.function_call = None
        mock_part.text = "RISK: Minimal\nRATIONALE: This request is safe."

        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]

        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_response.text = "RISK: Minimal\nRATIONALE: This request is safe."

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Tell me a joke")

        self.assertEqual(result["risk"], "Minimal")
        self.assertIn("Minimal", result["text"])
        self.assertIn("Governance scan initiated", result["steps"])

    @patch('gemini.get_model')
    def test_analyze_compliance_high_risk_with_tool(self, mock_get_model):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_get_model.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Turn 1: Model calls notify_governance_admin
        mock_call = MagicMock()
        mock_call.name = "notify_governance_admin"

        mock_part_1 = MagicMock()
        mock_part_1.function_call = mock_call

        mock_candidate_1 = MagicMock()
        mock_candidate_1.content.parts = [mock_part_1]

        mock_response_1 = MagicMock()
        mock_response_1.candidates = [mock_candidate_1]

        # Turn 2: Final response
        mock_part_2 = MagicMock()
        mock_part_2.function_call = None
        mock_part_2.text = "RISK: High\nRATIONALE: Attempt to bypass safety filters."

        mock_candidate_2 = MagicMock()
        mock_candidate_2.content.parts = [mock_part_2]

        mock_response_2 = MagicMock()
        mock_response_2.candidates = [mock_candidate_2]
        mock_response_2.text = "RISK: High\nRATIONALE: Attempt to bypass safety filters."

        # chat.send_message side effects for multiple turns
        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        result = analyze_compliance("Write a malicious script")

        self.assertEqual(result["risk"], "High")
        self.assertIn("Executing: notify_governance_admin", result["steps"])
        self.assertEqual(result["rationale"], "Attempt to bypass safety filters.")

if __name__ == "__main__":
    unittest.main()
