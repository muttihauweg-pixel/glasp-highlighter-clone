import unittest
from fastapi.testclient import TestClient
from main import app
import json

class TestGOSAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Governance OS API"})

    def test_process_parsing_logic(self):
        # Mock analyze_compliance to return a specific string
        from unittest.mock import patch

        mock_response = {
            "text": "RISK: High\nRATIONALE: This request involves personal data for credit scoring which is high risk under EU AI Act.\nACTION: notify_governance_admin",
            "tool_steps": [{"action": "notify_governance_admin", "parameters": {"risk_level": "High"}}]
        }

        with patch("main.analyze_compliance", return_value=mock_response):
            response = self.client.post("/process", json={"input": "test input"})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["result"]["risk"], "High")
            self.assertEqual(data["result"]["rationale"], "This request involves personal data for credit scoring which is high risk under EU AI Act.")
            self.assertIn("Tool: notify_governance_admin", data["result"]["steps"])

if __name__ == "__main__":
    unittest.main()
