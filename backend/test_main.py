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
    def test_process_input_text_only(self, mock_analyze):
        # Setup mock
        mock_analyze.return_value = {
            "text": "Risk Level: Minimal\nRationale: This is a safe request.",
            "steps": ["Step 1", "Step 2"]
        }

        response = self.client.post("/process", json={"input": "Hello world"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertEqual(data["result"]["steps"], ["Step 1", "Step 2"])
        self.assertIn("hash", data["audit"])

    @patch("main.analyze_compliance")
    def test_process_input_with_image(self, mock_analyze):
        # Setup mock
        mock_analyze.return_value = {
            "text": "Risk Level: High\nRationale: Facial recognition detected.",
            "steps": ["Step 1", "Executing Tool: notify_governance_admin"]
        }

        response = self.client.post("/process", json={
            "input": "Analyze this face",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Executing Tool", data["result"]["steps"][1])

    def test_regex_parsing_unacceptable(self):
        # Test the regex parsing logic via a mocked call
        with patch("main.analyze_compliance") as mock_analyze:
            mock_analyze.return_value = {
                "text": "Verdict: Dangerous.\nRisk Level: Unacceptable\nRationale: Social scoring is prohibited.",
                "steps": ["Analysis"]
            }
            response = self.client.post("/process", json={"input": "illegal request"})
            self.assertEqual(response.json()["result"]["risk"], "Unacceptable")

if __name__ == "__main__":
    unittest.main()
