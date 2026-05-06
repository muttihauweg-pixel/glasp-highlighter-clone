from playwright.sync_api import Page, expect, sync_playwright

def test_ui_verification(page: Page):
    page.goto("http://localhost:5173")
    expect(page.locator("h1")).to_have_text("AI Governance OS")
    page.get_by_placeholder("Enter AI request or describe a system for audit...").fill("I want to build a credit scoring system.")
    analyze_btn = page.get_by_role("button", name="Analyze Compliance")
    expect(analyze_btn).to_be_visible()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_ui_verification(page)
            print("UI Verification Passed")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
