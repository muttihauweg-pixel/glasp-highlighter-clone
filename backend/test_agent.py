import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

# Mock vertexai before importing gemini
with patch('vertexai.init'):
    with patch('vertexai.generative_models.GenerativeModel') as MockModel:
        import gemini

class TestGeminiAgent(unittest.TestCase):

    @patch('gemini.model.start_chat')
    def test_analyze_compliance_text_only(self, mock_start_chat):
        # Setup mock chat and response
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "This is a safe request. Risk: Minimal."
        # No function call
        mock_response.candidates[0].content.parts[0].function_call = None

        mock_chat.send_message.return_value = mock_response

        result = gemini.analyze_compliance("Hello")

        self.assertIn("Minimal", result)
        mock_chat.send_message.assert_called_once()

    @patch('gemini.model.start_chat')
    def test_analyze_compliance_with_function_call(self, mock_start_chat):
        mock_chat = MagicMock()
        mock_start_chat.return_value = mock_chat

        # 1. First response: function call
        mock_fn_call_resp = MagicMock()
        mock_fn_call_part = MagicMock()
        mock_fn_call_part.function_call.name = "save_to_google_docs"
        mock_fn_call_part.function_call.args = {"title": "Test Doc", "content": "Test Content"}
        mock_fn_call_resp.candidates[0].content.parts = [mock_fn_call_part]

        # 2. Second response: final text
        mock_final_resp = MagicMock()
        mock_final_resp.text = "Analysis saved to Google Docs."
        mock_final_resp.candidates[0].content.parts[0].function_call = None

        mock_chat.send_message.side_effect = [mock_fn_call_resp, mock_final_resp]

        result = gemini.analyze_compliance("Save this")

        self.assertEqual(result, "Analysis saved to Google Docs.")
        self.assertEqual(mock_chat.send_message.call_count, 2)

if __name__ == "__main__":
    unittest.main()
