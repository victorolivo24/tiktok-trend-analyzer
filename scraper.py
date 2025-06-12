import asyncio
from playwright.async_api import async_playwright
import os
import json
import pandas as pd
import re

COOKIE_FILE = 'my_cookies.json'
TARGET_URL = "https://www.tiktok.com/tiktokstudio/inspiration/recommended"
OUTPUT_FILE = 'tiktok_final_insights.csv'
SCROLL_ATTEMPTS = 15

def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        if not os.path.exists(COOKIE_FILE):
            print(f"Error: Cookie file '{COOKIE_FILE}' not found."); return
        
        print("Loading cookies...")
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f: cookies = json.load(f)

        valid_same_site_values = ["Strict", "Lax", "None"]; [c.update({"sameSite": "Lax"}) for c in cookies if c.get("sameSite") not in valid_same_site_values]
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        print(f"Navigating to: {TARGET_URL}")
        await page.goto(TARGET_URL, timeout=90000)
        print("Page loaded.")
        
        try:
            container = await page.wait_for_selector('div[data-tt="components_RecommendedVideoList_Container"]', timeout=30000)
            
            print(f"Scrolling {SCROLL_ATTEMPTS} times...")
            for i in range(SCROLL_ATTEMPTS):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await asyncio.sleep(4)
            
            video_cards = await container.query_selector_all('div[data-tt="components_InspirationItemCard_FlexColumn"]')
            print(f"Found {len(video_cards)} videos. Scraping data from main grid...")

            scraped_data = []
            for card in video_cards:
                caption_element = await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]')
                caption = await caption_element.inner_text() if caption_element else ""
                
                view_count_str, like_count_str = "0", "0"
                stat_elements = await card.query_selector_all('div[data-tt="components_InspirationItemCard_FlexRow_6"]')
                if len(stat_elements) > 0 and await stat_elements[0].query_selector('span[data-icon="PlayBold"]'):
                    view_count_element = await stat_elements[0].query_selector('span[data-tt="components_InspirationItemCard_TUXText"]')
                    if view_count_element: view_count_str = await view_count_element.inner_text()
                if len(stat_elements) > 1 and await stat_elements[1].query_selector('span[data-icon="HeartBold"]'):
                    like_count_element = await stat_elements[1].query_selector('span[data-tt="components_InspirationItemCard_TUXText"]')
                    if like_count_element: like_count_str = await like_count_element.inner_text()
                
                hashtags = ", ".join([f"#{tag}" for tag in extract_hashtags(caption)])
                scraped_data.append({'caption': caption.strip(), 'hashtags': hashtags, 'views': view_count_str, 'likes': like_count_str})

            if scraped_data:
                df = pd.DataFrame(scraped_data)
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"\nSUCCESS! Data for {len(df)} videos saved to {OUTPUT_FILE}!")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            print("Process finished.")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())