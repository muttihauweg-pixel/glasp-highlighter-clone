import unittest
from unittest.mock import MagicMock, patch
from backend.gemini import analyze_compliance, handle_function_call

class TestGovernanceAgent(unittest.TestCase):

    def test_handle_function_call_save_docs(self):
        mock_call = MagicMock()
        mock_call.name = "save_to_google_docs"
        mock_call.args = {"title": "Test Doc", "content": "Test Content"}

        result = handle_function_call(mock_call)
        self.assertEqual(result["status"], "success")
        self.assertIn("Test Doc", result["message"])

    def test_handle_function_call_notify_admin(self):
        mock_call = MagicMock()
        mock_call.name = "notify_governance_admin"
        mock_call.args = {"risk_level": "High", "reason": "Test Reason"}

        result = handle_function_call(mock_call)
        self.assertEqual(result["status"], "notified")

    @patch('backend.gemini.model.start_chat')
    def test_analyze_compliance_text_only(self, mock_start_chat):
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "RISK LEVEL: Minimal. Everything is fine."
        # Ensure the candidate response doesn't trigger function calls
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].function_call = None

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        result = analyze_compliance("Hello")
        self.assertIn("Minimal", result)
        mock_chat.send_message.assert_called_once_with(["Hello"])

    @patch('backend.gemini.model.start_chat')
    def test_analyze_compliance_multimodal(self, mock_start_chat):
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "RISK LEVEL: Low. Image analyzed."
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].function_call = None

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        image_bytes = b"fake_image_data"
        mime_type = "image/png"

        result = analyze_compliance("Analyze this", image_bytes, mime_type)
        self.assertIn("Image analyzed", result)

        # Check that send_message was called with text and a Part object
        args, _ = mock_chat.send_message.call_args
        self.assertEqual(len(args[0]), 2)
        self.assertEqual(args[0][0], "Analyze this")

if __name__ == "__main__":
    unittest.main()
