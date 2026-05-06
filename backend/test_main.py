import unittest
from fastapi.testclient import TestClient
import sys
import os

# Mock vertexai before importing main/gemini to avoid initialization errors
from unittest.mock import MagicMock, patch
sys.modules['vertexai'] = MagicMock()
sys.modules['vertexai.generative_models'] = MagicMock()

from main import app

client = TestClient(app)

class TestGovernanceAPI(unittest.TestCase):

    @patch('main.analyze_compliance')
    def test_process_input_minimal_risk(self, mock_analyze):
        # Mocking Gemini response
        mock_analyze.return_value = {
            "text": "Analysis complete. ```json {\"risk_level\": \"Minimal\", \"rationale\": \"Safe input\"} ```",
            "steps": [{"action": "save_to_google_docs", "params": {"title": "Report"}}]
        }

        response = client.post("/process", json={"input": "Hello world"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("save_to_google_docs", data["result"]["steps"])
        self.assertTrue(len(data["audit"]["hash"]) == 64)

    @patch('main.analyze_compliance')
    def test_process_input_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "Warning! ```json {\"risk_level\": \"High\", \"rationale\": \"Potential bias\"} ```",
            "steps": [{"action": "notify_governance_admin", "params": {"risk_level": "High"}}]
        }

        response = client.post("/process", json={"input": "High risk prompt"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("notify_governance_admin", data["result"]["steps"])

    def test_invalid_base64_image(self):
        # The API should return 400 if base64 decoding fails
        # Using a string that is definitely not valid base64 (contains spaces and special chars that are not padding)
        response = client.post("/process", json={
            "input": "test",
            "image": "not a valid base64 string @#$%"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid image data", response.json()["detail"])

if __name__ == '__main__':
    unittest.main()
