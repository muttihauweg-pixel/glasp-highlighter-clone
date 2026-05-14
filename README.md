# 🚀 AI Governance OS (AG-OS)
### *Bridging the Gap Between Innovation and Regulation*

[![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini%201.5%20Pro-blue?logo=google-gemini)](https://deepmind.google/technologies/gemini/)
[![GCP Native](https://img.shields.io/badge/Deployment-Cloud%20Run-orange?logo=google-cloud)](https://cloud.google.com/run)

---

## 🌪 The Problem
As AI scaling accelerates, organizations face a **compliance wall**. The **EU AI Act** and global regulations make manual AI oversight impossible. Enterprises are stuck between:
- **Innovation Paralysis**: Slowing down deployment for manual checks.
- **Regulatory Risk**: Deploying unvetted AI and risking multi-million Euro fines.

## 🛡 The Solution: AG-OS
**AG-OS** is the world's first autonomous AI Governance Operating System. It sits between your users and your AI models, providing a real-time, verifiable safety layer.

### ✨ Key Features
- **🧠 Autonomous Agentic Workflow**: Powered by **Gemini 1.5 Pro**, AG-OS uses a recursive function-calling loop to autonomously analyze, mitigate, and document risks.
- **📷 Multimodal Governance**: Analyze not just text, but also screenshots, UI mockups, and system diagrams for compliance.
- **⚡ Proactive Mitigation**: Automatically triggers `notify_governance_admin` for high-risk requests or logs compliant reports via `save_to_google_docs`.
- **🧾 Immutable Audit Trail**: Generates a cryptographic SHA-256 hash for every interaction (including image data), ensuring 100% traceability for regulators.
- **🎨 High-Fidelity Dashboard**: A modern, glassmorphism React interface visualizing the agent's internal "thought process" and multi-step execution flow.

---

## 🛠 Tech Stack
- **Frontend**: React (Vite), CSS3 (Custom Dashboard UI)
- **Backend**: FastAPI (Python 3.10)
- **AI Engine**: Vertex AI (Gemini 1.5 Pro)
- **Deployment**: Docker + GCP Cloud Run

---

## 🚀 Get Started in 60 Seconds

### 1. Prerequisites
- [Google Cloud SDK](https://cloud.google.com/sdk) installed.
- Vertex AI API enabled.

### 2. Run Local Demo
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

---

## 📈 Roadmap: Scaling to 10/10
- [ ] **Multi-Model Support**: Integration with Anthropic & OpenAI via Vertex Model Garden.
- [ ] **Automated Remediation**: AI-powered rewriting of non-compliant prompts.
- [ ] **Enterprise Connectors**: Full integration with Jira, Slack, and SAP.

---

### **"Governance is no longer a bottleneck. It's a competitive advantage."**
*Join the future of safe AI at [ai-governance-os.demo](https://ai-governance-os-xyz.a.run.app)*
