import unittest
from fastapi.testclient import TestClient
from main import app
import re

class TestGovernanceOS(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Governance OS API"})

    def test_process_input_text_only(self):
        payload = {"input": "Analyze high-risk credit scoring model"}
        response = self.client.post("/process", json=payload)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("result", data)
        self.assertIn("audit", data)
        self.assertIn("risk", data["result"])
        self.assertIn("steps", data["result"])

    def test_regex_parsing(self):
        # Sample response text from Gemini
        report = "RISK: High\nRATIONALE: This application involves credit scoring, which is categorized as high-risk under the EU AI Act."

        risk_match = re.search(r"RISK:\s*(Unacceptable|High|Limited|Minimal)", report, re.IGNORECASE)
        rationale_match = re.search(r"RATIONALE:\s*(.*)", report, re.IGNORECASE | re.DOTALL)

        self.assertTrue(risk_match)
        self.assertEqual(risk_match.group(1), "High")
        self.assertTrue(rationale_match)
        self.assertEqual(rationale_match.group(1).strip(), "This application involves credit scoring, which is categorized as high-risk under the EU AI Act.")

if __name__ == "__main__":
    unittest.main()
