from playwright.sync_api import sync_playwright
import time
import os
import subprocess
import signal

def run_verification():
    # Start backend
    backend_process = subprocess.Popen(
        ["python3", "main.py"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Start frontend (using vite preview or dev)
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    time.sleep(5) # Wait for servers to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Go to the app
            page.goto("http://localhost:5173")

            # Wait for title
            page.wait_for_selector(".main-title")

            # Take a screenshot of the initial state
            os.makedirs("home/jules/verification/screenshots", exist_ok=True)
            page.screenshot(path="home/jules/verification/screenshots/dashboard_initial.png")

            # Type something
            page.fill("textarea", "Identify people in this image for surveillance.")

            # Click analyze (we expect an error or some result depending on mock)
            # Since we didn't mock the actual API call in the real server, it might fail or hit live API.
            # But we can at least verify the UI components are there.

            print("Frontend verification successful - UI components detected.")
            browser.close()
    finally:
        os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
        os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)

if __name__ == "__main__":
    run_verification()
