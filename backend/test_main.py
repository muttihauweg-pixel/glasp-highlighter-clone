import unittest
from fastapi.testclient import TestClient
from main import app
import json

class TestGovernanceAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "AI Governance OS API"})

    def test_process_input_text_only(self):
        # We mock the analyze_compliance in a real scenario,
        # but here we test the API structure and response parsing logic.
        payload = {
            "input": "Analyze a low-risk chatbot application."
        }
        response = self.client.post("/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("result", data)
        self.assertIn("risk", data["result"])
        self.assertIn("audit", data)
        self.assertIn("hash", data["audit"])

    def test_process_input_multimodal(self):
        payload = {
            "input": "Check this architecture diagram for compliance.",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        }
        response = self.client.post("/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("result", data)
        self.assertTrue(len(data["audit"]["hash"]) > 0)

if __name__ == "__main__":
    unittest.main()
