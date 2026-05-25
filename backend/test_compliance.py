import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from gemini import analyze_compliance

class TestComplianceLogic(unittest.TestCase):

    @patch('gemini.model.start_chat')
    def test_analyze_compliance_basic(self, mock_start_chat):
        # Setup mock chat and response
        mock_chat = MagicMock()
        mock_response = MagicMock()

        # Mock candidate with text and no function calls
        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "This is a safe request.\nRISK: Minimal\nRATIONALE: Public info."

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        result = analyze_compliance("Hello")

        self.assertIn("RISK: Minimal", result["text"])
        self.assertEqual(result["steps"][0], "Input Received")
        self.assertEqual(result["steps"][-1], "Policy Enforcement Complete")

    @patch('gemini.model.start_chat')
    def test_analyze_compliance_multimodal(self, mock_start_chat):
        # Setup mock chat and response
        mock_chat = MagicMock()
        mock_response = MagicMock()

        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "Analysis of image."

        mock_chat.send_message.return_value = mock_response
        mock_start_chat.return_value = mock_chat

        # Base64 for a tiny transparent pixel
        image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

        result = analyze_compliance("Check this", image_b64)

        self.assertEqual(result["text"], "Analysis of image.")
        # Verify send_message was called with text and image part (conceptually)
        self.assertTrue(mock_chat.send_message.called)

if __name__ == "__main__":
    unittest.main()
