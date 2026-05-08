import os

def verify_ui():
    print("🚀 Starting UI Verification...")

    # Check if critical components exist
    required_files = [
        "frontend/src/App.css",
        "frontend/src/components/FlowGraph.jsx",
        "frontend/src/components/InputPanel.jsx"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            print(f"❌ Missing {file}")
            return False

    # Read App.css to verify glassmorphism and background
    with open("frontend/src/App.css", "r") as f:
        content = f.read()
        if "#0f172a" in content and "backdrop-filter" in content:
            print("✅ Glassmorphism and background color verified in App.css")
        else:
            print("❌ App.css does not contain expected styles")
            return False

    # Read FlowGraph.jsx to verify risk colors
    with open("frontend/src/components/FlowGraph.jsx", "r") as f:
        content = f.read()
        if "#ff4d4d" in content and "#00ff00" in content:
            print("✅ Risk level colors verified in FlowGraph.jsx")
        else:
            print("❌ FlowGraph.jsx does not contain expected colors")
            return False

    print("🎉 UI Verification Complete: All checks passed!")
    return True

if __name__ == "__main__":
    verify_ui()
