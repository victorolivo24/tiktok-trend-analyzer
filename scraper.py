import asyncio
from playwright.async_api import async_playwright
import os
import json

# Define the path for our cookie file.
COOKIE_FILE = 'my_cookies.json'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        if os.path.exists(COOKIE_FILE):
            print("Cookie file found. Loading and cleaning cookies.")
            with open(COOKIE_FILE, 'r') as f:
                cookies = json.load(f)

            # --- NEW: Clean the cookies before loading them ---
            # This loop fixes the 'sameSite' issue.
            valid_same_site_values = ["Strict", "Lax", "None"]
            for cookie in cookies:
                if cookie.get("sameSite") not in valid_same_site_values:
                    # If sameSite is invalid, set it to a sensible default like "Lax"
                    print(f"Fixing invalid sameSite value: '{cookie.get('sameSite')}'")
                    cookie["sameSite"] = "Lax"
            # --- End of new cleaning block ---

            await context.add_cookies(cookies)
            print("Cookies loaded successfully.")
        else:
            print("Cookie file not found. You will need to log in manually.")

        page = await context.new_page()

        print("Navigating to TikTok For You page...")
        await page.goto("https://www.tiktok.com/foryou", timeout=60000)

        print("Successfully navigated. The page should show your personalized content.")
        print("We will add scraping logic here in the next step.")

        await asyncio.sleep(20)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())