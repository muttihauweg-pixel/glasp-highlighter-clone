import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from gemini import analyze_compliance

class TestHappyAssistant(unittest.TestCase):

    @patch('gemini.get_model')
    def test_analyze_compliance_success(self, mock_get_model):
        # Mock model and response
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        # Set up mock response content in German
        mock_response.text = "JOY SCORE: 95\nHAPPINESS RATIONALE: Diese Kamera ist vintage und toll!\nRECOMMENDATION: Kauf sie!"
        mock_candidate = MagicMock()
        mock_part = MagicMock()
        mock_part.function_call = None
        mock_candidate.content.parts = [mock_part]
        mock_response.candidates = [mock_candidate]

        result = analyze_compliance("vintage kamera")

        self.assertEqual(result['joy_score'], "95")
        self.assertIn("vintage und toll", result['rationale'])
        self.assertIn("Kauf sie!", result['text'])
        self.assertIn("Fröhliche Antwort generiert", result['steps'])

    @patch('gemini.get_model')
    def test_analyze_compliance_error_handling(self, mock_get_model):
        mock_get_model.side_effect = Exception("Vertex AI Fehler")

        result = analyze_compliance("test")

        self.assertEqual(result['joy_score'], "50")
        self.assertIn("Fehler: Vertex AI Fehler", result['text'])
        self.assertIn("Wiederherstellung mit Positivität", result['steps'])

if __name__ == '__main__':
    unittest.main()
