import pandas as pd
from collections import Counter
import re

INPUT_FILE = 'tiktok_recommendations.csv'

# --- NEW: Define a list of all keywords we care about ---
# We don't need the '#' here because we'll be searching the raw caption text
BARBER_KEYWORDS = [
    'barber', 'haircut', 'hairstyle', 'fade', 'taper', 
    'burstfade', 'lowfade', 'midfade', 'fringe', 'buzzcut', 'mullet'
]

def analyze_niche_recommendations():
    """
    Reads scraped data, filters for a list of niche keywords,
    and analyzes the most common hashtags within that entire niche.
    """
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.")
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found. Run scraper.py first.")
        return

    # --- FINAL Filtering Logic ---
    # Create a regex pattern that looks for ANY of our keywords.
    # `|` acts as an "OR" operator. `re.IGNORECASE` handles capitalization.
    keyword_pattern = '|'.join(BARBER_KEYWORDS)
    
    # Keep rows where the caption contains any of our keywords
    df_filtered = df[df['caption'].str.contains(keyword_pattern, na=False, case=False)]
    
    if df_filtered.empty:
        print(f"No videos found containing any of the keywords: {BARBER_KEYWORDS}")
        return
        
    print(f"\nFound {len(df_filtered)} videos related to the barbering niche. Analyzing...")
    print("-" * 30)

    all_hashtags = []
    # We use the 'hashtags' column for analysis since it's already clean
    for tag_list in df_filtered['hashtags'].dropna():
        tags = [tag.strip() for tag in tag_list.split(',') if tag.strip()]
        all_hashtags.extend(tags)
    
    hashtag_counts = Counter(all_hashtags)

    print("🏆 Top 20 Most Common Hashtags in Your Niche 🏆")
    for hashtag, count in hashtag_counts.most_common(20):
        print(f"  {hashtag.lower()}: {count} times")

if __name__ == "__main__":
    analyze_niche_recommendations()