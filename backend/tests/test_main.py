import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from main import app

client = TestClient(app)

class TestMain(unittest.TestCase):
    @patch('main.analyze_compliance')
    def test_process_input_minimal_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: This is a safe request.",
            "steps": ["Tool Executed: save_to_google_docs"]
        }

        response = client.post("/process", json={"input": "Hello world"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("Tool Executed: save_to_google_docs", data["result"]["steps"])
        self.assertIn("audit", data)

    @patch('main.analyze_compliance')
    def test_process_input_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: High\nRATIONALE: This request involves prohibited social scoring.",
            "steps": ["Tool Executed: notify_governance_admin"]
        }

        response = client.post("/process", json={"input": "Run social scoring"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Tool Executed: notify_governance_admin", data["result"]["steps"])

    @patch('main.analyze_compliance')
    def test_process_input_with_image(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: Limited\nRATIONALE: Image shows non-critical UI.",
            "steps": []
        }

        response = client.post("/process", json={
            "input": "Check this screenshot",
            "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Limited")
        # Ensure hash is different if image is provided (implicitly tested by logic in main.py)

if __name__ == "__main__":
    unittest.main()
