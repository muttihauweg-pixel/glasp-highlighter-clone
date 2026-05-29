import unittest
from unittest.mock import patch, MagicMock
from backend.gemini import analyze_compliance

class TestComplianceAgent(unittest.TestCase):

    @patch('backend.gemini.get_model')
    def test_analyze_compliance_minimal_risk(self, mock_get_model):
        # Mocking Gemini response
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model

        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "RISK: Minimal\nRATIONALE: This request is safe.\nACTION: save_to_google_docs"
        # Setup candidate parts to break the loop
        mock_response.candidates[0].content.parts = []

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("How to make a cake?")

        self.assertEqual(result["data"]["risk"], "Minimal")
        self.assertIn("Input Received", result["data"]["steps"])
        self.assertIn("Governance Review Finalized", result["data"]["steps"])

    @patch('backend.gemini.get_model')
    def test_analyze_compliance_high_risk(self, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model

        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "RISK: High\nRATIONALE: Credit scoring is high risk under EU AI Act.\nACTION: notify_governance_admin"
        mock_response.candidates[0].content.parts = []

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Build a credit scoring model.")

        self.assertEqual(result["data"]["risk"], "High")
        self.assertIn("Credit scoring", result["data"]["rationale"])

if __name__ == '__main__':
    unittest.main()
