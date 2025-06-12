import asyncio
from playwright.async_api import async_playwright
import os
import json

# Define the path for our cookie file.
# This keeps it organized in our project directory.
COOKIE_FILE = 'my_cookies.json'

async def main():
    async with async_playwright() as p:
        # We will use the chromium browser.
        browser = await p.chromium.launch(headless=False) # headless=False lets us watch
        context = await browser.new_context()

        # --- Check for and load cookies ---
        if os.path.exists(COOKIE_FILE):
            print("Cookie file found. Loading cookies.")
            with open(COOKIE_FILE, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print("Cookies loaded successfully.")
        else:
            print("Cookie file not found. You will need to log in manually the first time.")
            # If no cookies, we'd add manual login logic here later if needed.
            # For now, we are relying on the cookie file.

        # Create a new page in the authenticated context
        page = await context.new_page()

        print("Navigating to TikTok For You page...")
        # Go to the 'For You' page, which is the default tiktok.com URL
        await page.goto("https://www.tiktok.com/foryou", timeout=60000)

        print("Successfully navigated. The page should show your personalized content.")
        print("We will add scraping logic here in the next step.")

        # Keep the browser open for a while so we can see it worked.
        await asyncio.sleep(20)

        # Cleanly close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())