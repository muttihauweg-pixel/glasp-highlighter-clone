import unittest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Governance OS API"})

    @patch("main.analyze_compliance")
    def test_process_input(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "Analysis complete. Risk Level: Minimal. Everything looks fine.",
            "steps": ["Input Received", "Compliance Check", "Analysis Finalized"]
        }

        payload = {"input": "Test request", "image": None}
        response = self.client.post("/process", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Minimal")
        self.assertIn("hash", data["audit"])
        self.assertEqual(data["result"]["steps"], ["Input Received", "Compliance Check", "Analysis Finalized"])

    @patch("main.analyze_compliance")
    def test_process_high_risk(self, mock_analyze):
        mock_analyze.return_value = {
            "text": "This request is dangerous. Risk Level: High. Admin notified.",
            "steps": ["Input Received", "Executing: notify_governance_admin", "Analysis Finalized"]
        }

        payload = {"input": "Dangerous request", "image": "data:image/png;base64,mock"}
        response = self.client.post("/process", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("Executing: notify_governance_admin", data["result"]["steps"])

if __name__ == "__main__":
    unittest.main()
