import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Create dummy modules for vertexai
class MockPart:
    @staticmethod
    def from_function_response(name, response):
        return f"PartResponse({name})"
    @staticmethod
    def from_data(data, mime_type):
        return f"PartData({mime_type})"

mock_genai = MagicMock()
mock_genai.Part = MockPart

sys.modules['vertexai'] = MagicMock()
sys.modules['vertexai.generative_models'] = mock_genai

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

class TestGovernanceAgent(unittest.TestCase):

    def setUp(self):
        # Reset gemini module to ensure fresh state for each test
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

    @patch('vertexai.generative_models.GenerativeModel')
    def test_analyze_compliance_text_only(self, mock_model_class):
        import gemini

        mock_model_instance = MagicMock()
        gemini.model = mock_model_instance

        mock_chat = MagicMock()
        mock_model_instance.start_chat.return_value = mock_chat

        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.function_calls = []
        mock_response.candidates = [mock_candidate]
        mock_response.text = "This request is compliant."
        mock_chat.send_message.return_value = mock_response

        result = gemini.analyze_compliance("Test input")

        self.assertIsInstance(result, dict)
        self.assertEqual(result['text'], "This request is compliant.")
        self.assertEqual(len(result['actions']), 0)

    @patch('vertexai.generative_models.GenerativeModel')
    def test_analyze_compliance_with_function_call(self, mock_model_class):
        import gemini

        mock_model_instance = MagicMock()
        gemini.model = mock_model_instance

        mock_chat = MagicMock()
        mock_model_instance.start_chat.return_value = mock_chat

        # First response has a function call
        mock_response1 = MagicMock()
        mock_candidate1 = MagicMock()
        mock_fc = MagicMock()
        mock_fc.name = "notify_governance_admin"
        mock_fc.args = {"risk_level": "High", "reason": "Test reason"}
        mock_candidate1.function_calls = [mock_fc]
        mock_response1.candidates = [mock_candidate1]

        # Second response is the final text
        mock_response2 = MagicMock()
        mock_candidate2 = MagicMock()
        mock_candidate2.function_calls = []
        mock_response2.candidates = [mock_candidate2]
        mock_response2.text = "Admin has been notified of the high risk."

        mock_chat.send_message.side_effect = [mock_response1, mock_response2]

        result = gemini.analyze_compliance("High risk input")

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result['actions']), 1)
        self.assertEqual(result['actions'][0]['name'], "notify_governance_admin")
        self.assertEqual(result['text'], "Admin has been notified of the high risk.")

if __name__ == '__main__':
    unittest.main()
