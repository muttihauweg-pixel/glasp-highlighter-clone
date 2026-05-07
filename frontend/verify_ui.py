import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:5173")

        # Verify title
        title = await page.title()
        print(f"Page Title: {title}")

        # Check for main elements
        h1_text = await page.inner_text("h1")
        print(f"H1 Text: {h1_text}")

        # Take a screenshot
        await page.screenshot(path="verification_screenshot.png")
        print("Screenshot saved to verification_screenshot.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
