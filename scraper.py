import asyncio
from playwright.async_api import async_playwright
import os
import json
import pandas as pd
import re

# --- CONFIGURATION ---
COOKIE_FILE = 'my_cookies.json'
TARGET_URL = "https://www.tiktok.com/tiktokstudio/inspiration/recommended"
OUTPUT_FILE = 'tiktok_insights_data.csv' # New, final output file
SCROLL_ATTEMPTS = 15 # Set how many times to scroll

def extract_hashtags(text):
    """Finds all hashtags in a string, returns a list of strings without the '#'"""
    return re.findall(r"#(\w+)", text)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        if not os.path.exists(COOKIE_FILE):
            print(f"Error: Cookie file '{COOKIE_FILE}' not found.")
            return
        
        print("Loading cookies...")
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        valid_same_site_values = ["Strict", "Lax", "None"]
        for cookie in cookies:
            if cookie.get("sameSite") not in valid_same_site_values:
                cookie["sameSite"] = "Lax"
        
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        print(f"Navigating to: {TARGET_URL}")
        await page.goto(TARGET_URL, timeout=90000)
        print("Page loaded.")
        
        try:
            container = await page.wait_for_selector('div[data-tt="components_RecommendedVideoList_Container"]', timeout=30000)
            
            print(f"Scrolling {SCROLL_ATTEMPTS} times...")
            for i in range(SCROLL_ATTEMPTS):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(3)
            
            video_cards = await container.query_selector_all('div[data-tt="components_InspirationItemCard_FlexColumn"]')
            print(f"Found {len(video_cards)} videos to scrape.")

            scraped_data = []
            for card in video_cards:
                # Scrape data points, with defaults if not found
                caption = (await (await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]')) .inner_text()) if await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]') else ""
                
                # --- NEW: Scrape Duration and Sound ---
                # These selectors are based on common structures and your screenshot
                duration_element = await card.query_selector('div[data-tt="VideoCover_index_Absolute"] span')
                duration = await duration_element.inner_text() if duration_element else "0:00"

                sound_element = await card.query_selector('div[data-tt="components_InspirationItemCard_FlexRow"] > span')
                sound = await sound_element.inner_text() if sound_element else "Unknown Sound"
                
                hashtags_found = extract_hashtags(caption)
                
                scraped_data.append({
                    'caption': caption.strip(),
                    'hashtags': ", ".join([f"#{tag}" for tag in hashtags_found]),
                    'sound': sound.strip(),
                    'duration': duration.strip()
                })

            if scraped_data:
                df = pd.DataFrame(scraped_data)
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"\nSUCCESS: Data for {len(df)} videos saved to {OUTPUT_FILE}!")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            print("Scraping process finished.")
            await browser.close()

if __name__ == "__main__":
    try:
        import pandas
    except ImportError:
        print("Installing pandas...")
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    
    asyncio.run(main())