import asyncio
from playwright.async_api import async_playwright
import os
import json
import pandas as pd
import re

# --- CONFIGURATION ---
COOKIE_FILE = 'my_cookies.json'
TARGET_URL = "https://www.tiktok.com/tiktokstudio/inspiration/recommended"
OUTPUT_FILE = 'tiktok_final_insights.csv' # Note: Analyzer reads this file
SCROLL_ATTEMPTS = 15

def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # Set to True for faster, background scraping

        # --- FIX FOR FRESH DATA ---
        # Create a new, isolated browser context for each run.
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            java_script_enabled=True,
            # This tells the browser to ignore its cache for this session
            storage_state=None 
        )
        
        if not os.path.exists(COOKIE_FILE):
            print(f"Error: Cookie file '{COOKIE_FILE}' not found."); return
        
        print("Loading and cleaning cookies...")
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f: cookies = json.load(f)
        valid_same_site_values = ["Strict", "Lax", "None"]; [c.update({"sameSite": "Lax"}) for c in cookies if c.get("sameSite") not in valid_same_site_values]
        
        # Add cookies to our fresh context
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        print(f"Navigating to TikTok Studio page: {TARGET_URL}")
        await page.goto(TARGET_URL, timeout=90000, wait_until="domcontentloaded")
        print("Page loaded.")
        
        try:
            container = await page.wait_for_selector('div[data-tt="components_RecommendedVideoList_Container"]', timeout=30000)
            
            print(f"Scrolling {SCROLL_ATTEMPTS} times to gather a large dataset...")
            for i in range(SCROLL_ATTEMPTS):
                print(f"  Scroll attempt {i + 1}/{SCROLL_ATTEMPTS}...")
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await asyncio.sleep(3)
            
            video_cards = await container.query_selector_all('div[data-tt="components_InspirationItemCard_FlexColumn"]')
            print(f"Found {len(video_cards)} videos. Scraping data...")

            scraped_data = []
            for card in video_cards:
                caption_element = await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]')
                caption = await caption_element.inner_text() if caption_element else ""
                
                views_element = await card.query_selector('div[data-tt="components_InspirationItemCard_FlexRow_6"] span[data-tt="components_InspirationItemCard_TUXText"]')
                views = await views_element.inner_text() if views_element else "0"
                
                hashtags = ", ".join([f"#{tag}" for tag in extract_hashtags(caption)])
                scraped_data.append({'caption': caption.strip(), 'hashtags': hashtags, 'views': views})

            if scraped_data:
                df = pd.DataFrame(scraped_data)
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"\nSUCCESS! Data for {len(df)} videos saved to {OUTPUT_FILE}!")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            print("Scraping process finished.")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())