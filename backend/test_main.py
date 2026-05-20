import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main import app

class TestGovernanceAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.analyze_compliance")
    def test_process_input_minimal_risk(self, mock_analyze):
        # Mock Gemini response
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: This is a safe request.\nDetailed analysis here.",
            "steps": ["Step 1", "Step 2"]
        }

        response = self.client.post("/process", json={"input": "Hello AI"})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertEqual(data["result"]["rationale"], "This is a safe request.")
        self.assertIn("hash", data["audit"])
        self.assertEqual(data["result"]["steps"], ["Step 1", "Step 2"])

    @patch("main.analyze_compliance")
    def test_process_input_high_risk(self, mock_analyze):
        # Mock Gemini response for high risk
        mock_analyze.return_value = {
            "text": "RISK: High\nRATIONALE: Biometric identification detected.\nDetailed analysis here.",
            "steps": ["Step 1", "Tool Call: notify_governance_admin"]
        }

        response = self.client.post("/process", json={"input": "Scan faces"})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Biometric identification", data["result"]["rationale"])

    @patch("main.analyze_compliance")
    def test_multimodal_request(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: Image analyzed successfully.",
            "steps": ["Multimodal Analysis Started"]
        }

        test_image_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        response = self.client.post("/process", json={
            "input": "What is in this image?",
            "image": test_image_b64
        })

        self.assertEqual(response.status_code, 200)
        mock_analyze.assert_called_once()
        # Verify image was passed to analyze_compliance
        self.assertEqual(mock_analyze.call_args[0][1], test_image_b64)

if __name__ == "__main__":
    unittest.main()
