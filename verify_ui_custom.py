import os

def check_file_content(filepath, search_strings):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False

    with open(filepath, 'r') as f:
        content = f.read()

    all_found = True
    for s in search_strings:
        if s in content:
            print(f"✅ Found '{s}' in {filepath}")
        else:
            print(f"❌ Could NOT find '{s}' in {filepath}")
            all_found = False
    return all_found

def verify_ui():
    print("Verifying Frontend UI Updates...")

    # Check InputPanel
    input_panel_ok = check_file_content("frontend/src/components/InputPanel.jsx", [
        "Governance Control Center",
        "file-upload",
        "image-preview",
        "FileReader"
    ])

    # Check App.css
    css_ok = check_file_content("frontend/src/App.css", [
        "glassmorphism",
        "radial-gradient",
        "risk-unacceptable",
        "backdrop-filter"
    ])

    # Check FlowGraph
    flow_graph_ok = check_file_content("frontend/src/components/FlowGraph.jsx", [
        "Agentic Execution Flow",
        "risk-badge",
        "result.steps.map"
    ])

    if input_panel_ok and css_ok and flow_graph_ok:
        print("\n✨ Frontend UI Verification PASSED")
    else:
        print("\n⚠️ Frontend UI Verification FAILED")

if __name__ == "__main__":
    verify_ui()
