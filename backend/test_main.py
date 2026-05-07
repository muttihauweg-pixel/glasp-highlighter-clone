import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.analyze_compliance")
    def test_process_text_only_low_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "Analysis complete. This request is safe.\nRisk Level: Minimal\nRationale: Standard data analysis.",
            "steps": ["Compliance Analysis"]
        }

        response = self.client.post("/process", json={"input": "Hello AI"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("Compliance Analysis", data["result"]["steps"])
        self.assertIn("hash", data["audit"])

    @patch("main.analyze_compliance")
    def test_process_multimodal_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "High risk detected in image.\nRisk Level: High\nRationale: Facial recognition usage.",
            "steps": ["Compliance Analysis", "Action: notify_governance_admin"]
        }

        response = self.client.post("/process", json={
            "input": "Analyze this image",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Action: notify_governance_admin", data["result"]["steps"])

if __name__ == "__main__":
    unittest.main()
