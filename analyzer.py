import pandas as pd
from collections import Counter

INPUT_FILE = 'tiktok_recommendations.csv'
TARGET_HASHTAG = '#barber'

def analyze_recommendations():
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.")
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found. Run scraper.py first.")
        return

    # --- FINAL, ROBUST Filtering Logic ---
    # Create boolean masks to check both columns, ignoring case.
    mask1 = df['hashtags'].str.contains(TARGET_HASHTAG, na=False, case=False)
    mask2 = df['caption'].str.contains(TARGET_HASHTAG, na=False, case=False)
    
    # Combine the masks: keep a row if the hashtag is in EITHER column.
    df_filtered = df[mask1 | mask2]
    
    if df_filtered.empty:
        print(f"No videos found containing '{TARGET_HASHTAG}'. The algorithm may not have recommended any.")
        return
        
    print(f"\nFound {len(df_filtered)} videos containing '{TARGET_HASHTAG}'. Analyzing...")
    print("-" * 30)

    all_hashtags = []
    for tag_list in df_filtered['hashtags'].dropna():
        # Ensure tags are stripped of whitespace and not empty
        tags = [tag.strip() for tag in tag_list.split(',') if tag.strip()]
        all_hashtags.extend(tags)
    
    hashtag_counts = Counter(all_hashtags)

    print("Most Common Co-occurring Hashtags:")
    for hashtag, count in hashtag_counts.most_common(20):
        print(f"  {hashtag.lower()}: {count} times")

if __name__ == "__main__":
    analyze_recommendations()