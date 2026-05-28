import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from gemini import analyze_compliance

class TestCompliance(unittest.TestCase):

    @patch('gemini.get_model')
    def test_analyze_compliance_text_only(self, mock_get_model):
        # Mocking the model and chat
        mock_model_instance = MagicMock()
        mock_get_model.return_value = mock_model_instance
        mock_chat = mock_model_instance.start_chat.return_value

        # Mock response
        mock_response = MagicMock()
        mock_response.text = "RISK: Minimal\nRATIONALE: Safe request.\nMITIGATION: None."
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].function_calls = []

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Hello")

        self.assertIn("RISK: Minimal", result["text"])
        self.assertEqual(len(result["steps"]), 0)

    @patch('gemini.get_model')
    def test_analyze_compliance_with_tool_call(self, mock_get_model):
        mock_model_instance = MagicMock()
        mock_get_model.return_value = mock_model_instance
        mock_chat = mock_model_instance.start_chat.return_value

        # First response has a function call
        mock_response_1 = MagicMock()
        mock_fc = MagicMock()
        mock_fc.name = "save_to_google_docs"
        mock_fc.args = {"title": "Test", "content": "Content"}
        mock_response_1.candidates = [MagicMock()]
        mock_response_1.candidates[0].function_calls = [mock_fc]

        # Second response (after tool result) is final text
        mock_response_2 = MagicMock()
        mock_response_2.text = "RISK: Minimal\nSaved to docs."
        mock_response_2.candidates = [MagicMock()]
        mock_response_2.candidates[0].function_calls = []

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        result = analyze_compliance("Save this")

        self.assertIn("Tool Call: save_to_google_docs", result["steps"])
        self.assertIn("Saved to docs", result["text"])

if __name__ == '__main__':
    unittest.main()
