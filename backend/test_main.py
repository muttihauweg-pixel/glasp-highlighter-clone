import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

class TestGovernanceAPI(unittest.TestCase):

    @patch('main.analyze_compliance')
    def test_process_input_minimal_risk(self, mock_analyze):
        # Mock Gemini response
        mock_analyze.return_value = {
            "text": "Analysis complete. RISK: Minimal. RATIONALE: This request is purely informative and does not involve high-risk AI applications.",
            "steps": ["Input Received", "AI Agent Initialization", "Governance Analysis Finalized"]
        }

        response = client.post("/process", json={"input": "What is the capital of France?"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("purely informative", data["result"]["rationale"])
        self.assertIn("Audit Trail Hash", data["result"]["processed_output"])
        self.assertEqual(len(data["result"]["steps"]), 3)

    @patch('main.analyze_compliance')
    def test_process_input_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "RISK: High. RATIONALE: Biometric identification in public spaces is heavily regulated. Tool Call: notify_governance_admin.",
            "steps": ["Input Received", "Tool Call: notify_governance_admin", "Governance Analysis Finalized"]
        }

        response = client.post("/process", json={"input": "Set up a facial recognition system for the city square."})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Biometric identification", data["result"]["rationale"])

    def test_process_invalid_image(self):
        # Test with malformed base64
        response = client.post("/process", json={
            "input": "test",
            "image": "data:image/png;base64,INVALID_DATA"
        })
        # Should still succeed but might log error (or handle gracefully in our implementation)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
