import pandas as pd
from collections import Counter
import re

# --- CONFIGURATION ---
INPUT_FILE = 'tiktok_insights_data.csv'
BARBER_KEYWORDS = [
    'barber', 'haircut', 'hairstyle', 'fade', 'taper', 'burstfade', 
    'lowfade', 'midfade', 'fringe', 'buzzcut', 'mullet'
]

# --- NLTK setup for Keyword Analysis ---
try:
    from nltk.corpus import stopwords
    import nltk
    # Download the stopwords dataset if it's not already present
    try:
        stopwords.words('english')
    except LookupError:
        print("NLTK stopwords not found. Downloading...")
        nltk.download('stopwords')
        print("Download complete.")
    STOP_WORDS = set(stopwords.words('english'))
except ImportError:
    print("NLTK library not found. Please install it by running: pip install nltk")
    STOP_WORDS = set()


def analyze_insights():
    """
    Reads comprehensive scraped data and provides a full report on
    hashtags, keywords, sounds, and video duration for a niche.
    """
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.\n")
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found. Run scraper.py first.")
        return

    # --- 1. Filter data to our niche ---
    keyword_pattern = '|'.join(BARBER_KEYWORDS)
    df_filtered = df[df['caption'].str.contains(keyword_pattern, na=False, case=False)].copy()
    
    if df_filtered.empty:
        print(f"No videos found for your niche. Try different keywords or a larger scrape.")
        return
        
    print(f"Found {len(df_filtered)} videos related to the barbering niche. Generating report...")
    
    # --- 2. Hashtag Analysis ---
    print("\n" + "="*40)
    print("🏆 Top 15 Most Common Hashtags 🏆")
    print("="*40)
    all_hashtags = [tag for tag_list in df_filtered['hashtags'].dropna() for tag in tag_list.split(',') if tag.strip()]
    hashtag_counts = Counter(all_hashtags)
    for hashtag, count in hashtag_counts.most_common(15):
        print(f"  {hashtag.strip().lower()}: {count} times")

    # --- 3. Keyword Analysis ---
    print("\n" + "="*40)
    print("🔑 Top 15 Most Common Keywords (in captions) 🔑")
    print("="*40)
    # Clean and split all captions into words
    all_words = re.findall(r'\b\w+\b', ' '.join(df_filtered['caption'].dropna()).lower())
    # Filter out stop words and our original search keywords
    meaningful_words = [word for word in all_words if word not in STOP_WORDS and word not in BARBER_KEYWORDS and not word.isdigit()]
    keyword_counts = Counter(meaningful_words)
    for keyword, count in keyword_counts.most_common(15):
        print(f"  '{keyword}': {count} times")

    # --- 4. Sound Analysis ---
    print("\n" + "="*40)
    print("🎵 Top 10 Trending Sounds 🎵")
    print("="*40)
    sound_counts = Counter(df_filtered['sound'].dropna())
    for sound, count in sound_counts.most_common(10):
        if sound != "Unknown Sound":
            print(f"  '{sound}': {count} videos")

    # --- 5. Duration Analysis ---
    print("\n" + "="*40)
    print("⏱️ Video Duration Analysis ⏱️")
    print("="*40)
    # Convert duration "M:SS" to seconds for calculation
    def duration_to_seconds(d):
        try:
            parts = d.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except:
            return 0 # Return 0 if conversion fails
    
    df_filtered['duration_seconds'] = df_filtered['duration'].apply(duration_to_seconds)
    valid_durations = df_filtered[df_filtered['duration_seconds'] > 0]
    
    if not valid_durations.empty:
        avg_duration = valid_durations['duration_seconds'].mean()
        print(f"  Average Video Length: {avg_duration:.2f} seconds")
    else:
        print("  Could not calculate average duration.")

if __name__ == "__main__":
    analyze_insights()