import unittest
from fastapi.testclient import TestClient
from main import app
import json
from unittest.mock import patch

client = TestClient(app)

class TestGovernanceAPI(unittest.TestCase):

    @patch('main.analyze_compliance')
    def test_process_text_only(self, mock_analyze):
        # Mock analysis result
        mock_analyze.return_value = {
            "text": "RISK: Minimal\nRATIONALE: This is a simple spam filter.",
            "tool_steps": ["Executing tool: save_to_google_docs"]
        }

        response = client.post(
            "/process",
            json={"input": "Test spam filter request"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("Executing tool: save_to_google_docs", data["result"]["steps"])
        self.assertIn("hash", data["audit"])

    @patch('main.analyze_compliance')
    def test_process_multimodal(self, mock_analyze):
        # Mock analysis result
        mock_analyze.return_value = {
            "text": "RISK: High\nRATIONALE: Biometric analysis detected in screenshot.",
            "tool_steps": ["Executing tool: notify_governance_admin"]
        }

        response = client.post(
            "/process",
            json={
                "input": "Analyze this interface",
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            }
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Executing tool: notify_governance_admin", data["result"]["steps"])

    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Governance OS API"})

if __name__ == "__main__":
    unittest.main()
