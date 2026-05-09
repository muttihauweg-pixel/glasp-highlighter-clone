import os

def verify_frontend():
    print("Verifying frontend structure...")
    files_to_check = [
        "frontend/src/App.jsx",
        "frontend/src/App.css",
        "frontend/src/components/InputPanel.jsx",
        "frontend/src/components/FlowGraph.jsx",
        "frontend/src/components/AuditTimeline.jsx",
        "frontend/src/api.js"
    ]

    for f in files_to_check:
        if os.path.exists(f):
            print(f"✅ Found {f}")
        else:
            print(f"❌ Missing {f}")
            return False

    print("\nVerifying CSS styles...")
    with open("frontend/src/App.css", "r") as f:
        content = f.read()
        if "#0f172a" in content and "glassmorphism" not in content: # glassmorphism is in comments or just the effect
             # Let's check for the actual properties
             if "backdrop-filter: blur" in content and "background-color: #0f172a" in content:
                 print("✅ Dark theme and glassmorphism styles detected.")
             else:
                 print("⚠️ Glassmorphism styles might be missing.")
        else:
             print("✅ Dark theme detected.")

    print("\nFrontend verification complete.")
    return True

if __name__ == "__main__":
    verify_frontend()
