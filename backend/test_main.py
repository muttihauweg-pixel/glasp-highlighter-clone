import unittest
from unittest.mock import MagicMock, patch
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestGovernanceAPI(unittest.TestCase):

    @patch("main.analyze_compliance")
    def test_process_input_minimal_risk(self, mock_analyze):
        # Mocking the Gemini response
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: This request is for general information and poses no regulatory risk.",
            "steps": ["Input Received", "Initial Governance Analysis", "Policy Enforcement Finalized"]
        }

        response = client.post(
            "/process",
            json={"input": "Hello, how are you?"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("Initial Governance Analysis", data["result"]["steps"])
        self.assertTrue(data["audit"]["hash"])

    @patch("main.analyze_compliance")
    def test_process_input_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: High\nRATIONALE: The request involves processing sensitive biometrics without clear consent.\nAutonomous Action: notify_governance_admin",
            "steps": ["Input Received", "Initial Governance Analysis", "Autonomous Action: notify_governance_admin", "Policy Enforcement Finalized"]
        }

        response = client.post(
            "/process",
            json={"input": "Scan faces for tracking."}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Autonomous Action: notify_governance_admin", data["result"]["steps"])

if __name__ == "__main__":
    unittest.main()
