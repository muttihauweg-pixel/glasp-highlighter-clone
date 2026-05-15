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

    @patch('main.analyze_compliance')
    def test_process_input_success(self, mock_analyze):
        # Setup mock
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: This is a safe request.",
            "steps": ["Step 1", "Step 2"]
        }

        response = self.client.post("/process", json={"input": "Hello world"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertEqual(data["result"]["rationale"], "This is a safe request.")
        self.assertIn("hash", data["audit"])
        self.assertEqual(data["result"]["steps"], ["Step 1", "Step 2"])

    @patch('main.analyze_compliance')
    def test_process_input_high_risk(self, mock_analyze):
        # Setup mock
        mock_analyze.return_value = {
            "text": "RISK: High\nRATIONALE: Potential for bias in credit scoring.",
            "steps": ["Step 1", "Action: notify_governance_admin"]
        }

        response = self.client.post("/process", json={"input": "Create credit scoring model"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("High", data["result"]["risk"])

if __name__ == '__main__':
    unittest.main()
