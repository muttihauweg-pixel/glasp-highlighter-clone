import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.analyze_compliance")
    def test_process_input_text_only(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: Minimal. RATIONALE: All good.",
            "steps": ["Step 1", "Step 2"],
            "risk": "Minimal"
        }

        response = self.client.post("/process", json={"input": "Hello world"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertEqual(data["result"]["steps"], ["Step 1", "Step 2"])
        self.assertIn("hash", data["audit"])

    @patch("main.analyze_compliance")
    def test_process_input_multimodal(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: High. RATIONALE: Image contains sensitive data.",
            "steps": ["Step 1", "Step 2", "Tool Call: notify"],
            "risk": "High"
        }

        response = self.client.post("/process", json={
            "input": "Analyze this",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("hash", data["audit"])

if __name__ == "__main__":
    unittest.main()
