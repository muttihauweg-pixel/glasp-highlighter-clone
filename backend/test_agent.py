import unittest
from unittest.mock import MagicMock, patch
from backend.gemini import analyze_compliance

class TestAgent(unittest.TestCase):

    @patch('backend.gemini.GenerativeModel')
    @patch('backend.gemini.vertexai.init')
    def test_analyze_compliance_text_only(self, mock_init, mock_model_class):
        # Setup mock
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "RISK_ASSESSMENT: Minimal. This is a safe request."
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock(function_call=None)]

        mock_chat.send_message.return_value = mock_response

        # Reset global model for clean test
        import backend.gemini
        backend.gemini._model = None

        # Execute
        result = analyze_compliance("How do I make a cake?")

        # Assert
        self.assertIn("Minimal", result["text"])
        self.assertEqual(len(result["actions"]), 0)
        mock_chat.send_message.assert_called_once()

    @patch('backend.gemini.GenerativeModel')
    @patch('backend.gemini.vertexai.init')
    def test_analyze_compliance_high_risk(self, mock_init, mock_model_class):
        # Setup mock
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        # Turn 1: Function Call
        mock_response_1 = MagicMock()
        mock_fc = MagicMock()
        mock_fc.name = "notify_governance_admin"
        mock_fc.args = {"risk_level": "High", "reason": "Potential bias"}
        mock_response_1.candidates = [MagicMock()]
        # Multi-part message: text + function call
        mock_response_1.candidates[0].content.parts = [
            MagicMock(text="Checking risk...", function_call=None),
            MagicMock(text=None, function_call=mock_fc)
        ]

        # Turn 2: Final Text
        mock_response_2 = MagicMock()
        mock_response_2.text = "RISK_ASSESSMENT: High. Admin notified."
        mock_response_2.candidates = [MagicMock()]
        mock_response_2.candidates[0].content.parts = [MagicMock(function_call=None)]

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        # Reset global model for clean test
        import backend.gemini
        backend.gemini._model = None

        # Execute
        result = analyze_compliance("Create a credit scoring model.")

        # Assert
        self.assertIn("High", result["text"])
        self.assertIn("notify_governance_admin", result["actions"])
        self.assertEqual(mock_chat.send_message.call_count, 2)

if __name__ == '__main__':
    unittest.main()
