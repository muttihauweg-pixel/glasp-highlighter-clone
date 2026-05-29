import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import base64

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from gemini import process_listing

class TestSellingExpert(unittest.TestCase):

    @patch('gemini.get_model')
    def test_process_listing_step1(self, mock_get_model):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        # Mock step 1 response
        mock_response.text = "Das ist ein schönes Foto! Bitte lade noch ein Foto von der Rückseite hoch. Ist das Gerät voll funktionsfähig?"
        mock_candidate = MagicMock()
        mock_part = MagicMock()
        mock_part.function_call = None
        mock_candidate.content.parts = [mock_part]
        mock_response.candidates = [mock_candidate]

        # Test with mock image
        mock_image = "data:image/jpeg;base64," + base64.b64encode(b"fake image data").decode()
        result = process_listing("Hier ist mein iPhone", mock_image)

        self.assertEqual(result['step'], "Foto-Regie")
        self.assertIn("Rückseite", result['text'])

    @patch('gemini.get_model')
    def test_process_listing_final_step(self, mock_get_model):
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()

        mock_get_model.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat
        mock_chat.send_message.return_value = mock_response

        # Mock final listing response
        mock_response.text = "### 💥 Super iPhone 13\n---\n**📊 STRATEGIE:** Festpreis\n**Beschreibung:** Tolles Teil!"
        mock_candidate = MagicMock()
        mock_part = MagicMock()
        mock_part.function_call = None
        mock_candidate.content.parts = [mock_part]
        mock_response.candidates = [mock_candidate]

        result = process_listing("Bereit für den Text", None)

        self.assertEqual(result['step'], "Fertiges Inserat")
        self.assertIn("Super iPhone 13", result['text'])

if __name__ == '__main__':
    unittest.main()
