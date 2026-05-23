import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from main import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.analyze_compliance")
    def test_process_input_success(self, mock_analyze):
        # Setup mock
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: All good.",
            "risk": "Minimal",
            "steps": ["Input Received", "Gemini Analysis", "Policy Enforcement Complete"]
        }

        # Test request
        response = self.client.post("/process", json={"input": "Hello", "image": None})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("audit", data)
        self.assertIn("compliance_report", data)
        self.assertEqual(data["result"]["steps"], ["Input Received", "Gemini Analysis", "Policy Enforcement Complete"])

    @patch("main.analyze_compliance")
    def test_process_input_with_image(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: Limited\nRATIONALE: Image contains text.",
            "risk": "Limited",
            "steps": ["Input Received", "Gemini Analysis", "Policy Enforcement Complete"]
        }

        # Fake base64 image
        fake_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

        response = self.client.post("/process", json={"input": "What is this?", "image": fake_image})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Limited")

if __name__ == "__main__":
    unittest.main()
