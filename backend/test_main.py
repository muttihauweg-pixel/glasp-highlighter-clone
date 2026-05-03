import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

class TestGovernanceAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("main.analyze_compliance")
    def test_process_input_success(self, mock_analyze):
        # Mock Gemini response
        mock_analyze.return_value = {
            "text": "Analysis complete. RISK_ASSESSMENT: MINIMAL. REASON: Safe request.",
            "steps": ["Step 1", "Step 2"]
        }

        response = self.client.post(
            "/process",
            json={"input": "Test request", "image_data": None}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "MINIMAL")
        self.assertIn("hash", data["audit"])
        self.assertEqual(len(data["result"]["steps"]), 2)

    @patch("main.analyze_compliance")
    def test_process_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "DANGER! RISK_ASSESSMENT: HIGH. REASON: Potential bias.",
            "steps": ["Step 1", "Agent Action: notify_governance_admin"]
        }

        response = self.client.post(
            "/process",
            json={"input": "Dangerous request"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "HIGH")
        self.assertTrue(any("notify_governance_admin" in step for step in data["result"]["steps"]))

if __name__ == "__main__":
    unittest.main()
