import asyncio
from playwright.async_api import async_playwright
import os
import json
import pandas as pd
import re

# Define the path for our cookie file.
COOKIE_FILE = 'my_cookies.json'
TARGET_URL = "https://www.tiktok.com/tiktokstudio/inspiration/recommended"
OUTPUT_FILE = 'tiktok_recommendations.csv'

def extract_hashtags(text):
    """Uses regular expressions to find all hashtags in a string."""
    return re.findall(r"#(\w+)", text)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        if not os.path.exists(COOKIE_FILE):
            print(f"Error: Cookie file '{COOKIE_FILE}' not found.")
            return
        
        print("Cookie file found. Loading cookies.")
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        valid_same_site_values = ["Strict", "Lax", "None"]
        for cookie in cookies:
            if cookie.get("sameSite") not in valid_same_site_values:
                cookie["sameSite"] = "Lax"
        
        await context.add_cookies(cookies)
        print("Cookies loaded successfully.")

        page = await context.new_page()
        
        print(f"Navigating to: {TARGET_URL}")
        await page.goto(TARGET_URL, timeout=90000)
        
        print("Page loaded. Looking for recommended videos...")
        
        try:
            video_list_container_selector = 'div[data-tt="components_RecommendedVideoList_Container"]'
            container = await page.wait_for_selector(video_list_container_selector, timeout=30000)
            print("Found the main video list container.")

            # --- NEW AND IMPROVED LOGIC ---
            # Now that we have the container, we specifically wait for a video card to appear INSIDE it.
            video_card_selector = 'div[data-tt="components_InspirationItemCard_FlexColumn"]'
            print("Waiting for video cards to load inside the container...")
            await container.wait_for_selector(video_card_selector, timeout=15000) # Wait up to 15s for the first card
            
            video_cards = await container.query_selector_all(video_card_selector)
            print(f"SUCCESS: Found {len(video_cards)} video cards on the page.")
            # --- END OF NEW LOGIC ---

            if not video_cards:
                print("No video cards found after waiting. Exiting.")
                return

            scraped_data = []
            for i, card in enumerate(video_cards):
                caption = "CAPTION NOT FOUND"
                hashtags = []
                image_link = "IMAGE LINK NOT FOUND"
                
                caption_element = await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]')
                if caption_element:
                    caption = await caption_element.inner_text()
                    hashtags = extract_hashtags(caption)
                
                image_element = await card.query_selector('img[data-tt="VideoCover_index_img"]')
                if image_element:
                    image_link = await image_element.get_attribute('src')

                scraped_data.append({
                    'caption': caption.strip(),
                    'hashtags': ", ".join(hashtags),
                    'image_link': image_link
                })

            if scraped_data:
                print(f"\nScraping complete. Saving {len(scraped_data)} items to {OUTPUT_FILE}")
                df = pd.DataFrame(scraped_data)
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"Data saved successfully to {OUTPUT_FILE}!")
                print("\n--- Scraped Data ---")
                print(df)
                print("--------------------")

        except Exception as e:
            print(f"\nAn error occurred during scraping: {e}")
            print("The script will now pause so you can inspect the page manually.")
            await page.pause()

        finally:
            print("\nProcess finished. Closing browser.")
            await browser.close()

if __name__ == "__main__":
    try:
        import pandas
    except ImportError:
        print("Pandas library not found. Installing...")
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    
    asyncio.run(main())