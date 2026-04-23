from fastapi.testclient import TestClient
from main import app
import unittest
from unittest.mock import patch

client = TestClient(app)

class TestGovernanceAPI(unittest.TestCase):
    @patch("main.analyze_compliance")
    def test_process_input_low_risk(self, mock_analyze):
        mock_analyze.return_value = "This request is compliant with EU AI Act. Minimal risk."

        response = client.post("/process", json={"input": "Hello world"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "Low")
        self.assertIn("hash", data["audit"])

    @patch("main.analyze_compliance")
    def test_process_input_high_risk(self, mock_analyze):
        mock_analyze.return_value = "High risk detected. Unauthorized surveillance."

        response = client.post("/process", json={"input": "Facial recognition for surveillance"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["risk"], "High")
        self.assertIn("High risk detected", data["compliance_report"])

if __name__ == "__main__":
    unittest.main()
