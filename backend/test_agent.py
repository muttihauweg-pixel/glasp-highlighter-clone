import unittest
from unittest.mock import MagicMock, patch
from backend.gemini import analyze_compliance
import base64

class TestGovernanceAgent(unittest.TestCase):

    @patch('backend.gemini.get_model')
    def test_analyze_compliance_text_only(self, mock_get_model):
        # Mocking the Gemini response
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model

        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        # Simulate final response with RISK_ASSESSMENT
        mock_response = MagicMock()
        mock_response.text = "Analysis complete. RISK_ASSESSMENT: Minimal"
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock(function_call=None)]

        mock_chat.send_message.return_value = mock_response

        result = analyze_compliance("Test input")

        self.assertIn("RISK_ASSESSMENT: Minimal", result["text"])
        self.assertIn("Input Received", result["steps"])
        self.assertIn("Final Compliance Report Generated", result["steps"])

    @patch('backend.gemini.get_model')
    def test_analyze_compliance_with_tool_call(self, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model

        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        # 1st response: Tool call
        mock_response_1 = MagicMock()
        mock_part_1 = MagicMock()
        mock_part_1.function_call.name = "save_to_google_docs"
        mock_response_1.candidates = [MagicMock()]
        mock_response_1.candidates[0].content.parts = [mock_part_1]

        # 2nd response: Final text
        mock_response_2 = MagicMock()
        mock_response_2.text = "Saved to docs. RISK_ASSESSMENT: Limited"
        mock_response_2.candidates = [MagicMock()]
        mock_response_2.candidates[0].content.parts = [MagicMock(function_call=None)]

        mock_chat.send_message.side_effect = [mock_response_1, mock_response_2]

        result = analyze_compliance("Save this")

        self.assertIn("Tool Use: save_to_google_docs", result["steps"])
        self.assertIn("RISK_ASSESSMENT: Limited", result["text"])

    @patch('backend.gemini.get_model')
    def test_multimodal_input(self, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        mock_chat = MagicMock()
        mock_model.start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_response.text = "Image analyzed. RISK_ASSESSMENT: Minimal"
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock(function_call=None)]
        mock_chat.send_message.return_value = mock_response

        dummy_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

        result = analyze_compliance("What is in this image?", dummy_image)

        self.assertIn("RISK_ASSESSMENT: Minimal", result["text"])
        # Verify Part.from_data was called (internally via send_message args)
        args, _ = mock_chat.send_message.call_args
        content_parts = args[0]
        self.assertEqual(len(content_parts), 2) # Text + Image

if __name__ == '__main__':
    unittest.main()
