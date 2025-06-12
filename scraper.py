import asyncio
from playwright.async_api import async_playwright
import os
import json
import pandas as pd
import re

COOKIE_FILE = 'my_cookies.json'
TARGET_URL = "https://www.tiktok.com/tiktokstudio/inspiration/recommended"
OUTPUT_FILE = 'tiktok_recommendations.csv'
SCROLL_ATTEMPTS = 5

def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        if not os.path.exists(COOKIE_FILE):
            print(f"Error: Cookie file '{COOKIE_FILE}' not found.")
            return
        
        print("Cookie file found...")
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        valid_same_site_values = ["Strict", "Lax", "None"]
        for cookie in cookies:
            if cookie.get("sameSite") not in valid_same_site_values:
                cookie["sameSite"] = "Lax"
        
        await context.add_cookies(cookies)
        print("Cookies loaded.")
        page = await context.new_page()
        
        print(f"Navigating to: {TARGET_URL}")
        await page.goto(TARGET_URL, timeout=90000)
        
        print("Page loaded.")
        
        try:
            container_selector = 'div[data-tt="components_RecommendedVideoList_Container"]'
            container = await page.wait_for_selector(container_selector, timeout=30000)
            
            print(f"Scrolling {SCROLL_ATTEMPTS} times to load more videos...")
            for i in range(SCROLL_ATTEMPTS):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(3)
            
            card_selector = 'div[data-tt="components_InspirationItemCard_FlexColumn"]'
            video_cards = await container.query_selector_all(card_selector)
            print(f"Found {len(video_cards)} videos.")

            scraped_data = []
            for card in video_cards:
                caption = "CAPTION NOT FOUND"
                hashtags_found = []
                image_link = "IMAGE LINK NOT FOUND"
                
                caption_element = await card.query_selector('span[data-tt="components_InspirationItemCard_TruncateText"]')
                if caption_element:
                    caption = await caption_element.inner_text()
                    hashtags_found = extract_hashtags(caption)
                
                image_element = await card.query_selector('img[data-tt="VideoCover_index_img"]')
                if image_element:
                    image_link = await image_element.get_attribute('src')

                scraped_data.append({
                    'caption': caption.strip(),
                    # This line correctly adds the '#' back to each tag
                    'hashtags': ", ".join([f"#{tag}" for tag in hashtags_found]),
                    'image_link': image_link
                })

            if scraped_data:
                df = pd.DataFrame(scraped_data)
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                print(f"\nSUCCESS: Data for {len(df)} videos saved to {OUTPUT_FILE}!")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            print("Process finished.")
            await browser.close()

if __name__ == "__main__":
    try:
        import pandas
    except ImportError:
        print("Installing pandas...")
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    
    asyncio.run(main())