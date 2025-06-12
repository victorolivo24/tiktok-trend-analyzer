import pandas as pd
from collections import Counter

# Define the input file from our scraper and the target hashtag
INPUT_FILE = 'tiktok_recommendations.csv'
TARGET_HASHTAG = '#barber'

def analyze_recommendations():
    """
    Reads the scraped data, filters for a specific hashtag,
    and analyzes the frequency of all other hashtags in that niche.
    """
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.")
    except FileNotFoundError:
        print(f"Error: The input file '{INPUT_FILE}' was not found.")
        print("Please run the scraper.py script first to generate the data.")
        return

    # --- Filtering Logic ---
    # We need to handle cases where the 'hashtags' column might be empty (NaN)
    df_filtered = df[df['hashtags'].str.contains(TARGET_HASHTAG, na=False)]
    
    if df_filtered.empty:
        print(f"No videos found with the '{TARGET_HASHTAG}' hashtag in the current dataset.")
        return
        
    print(f"\nFound {len(df_filtered)} videos with the '{TARGET_HASHTAG}' hashtag. Analyzing...")
    print("-" * 30)

    # --- Hashtag Frequency Analysis ---
    all_hashtags = []
    # Go through the 'hashtags' column of our FILTERED data
    for tag_list in df_filtered['hashtags'].dropna():
        # Split the string of tags "tag1, tag2, tag3" into a list ['tag1', 'tag2', 'tag3']
        tags = [tag.strip() for tag in tag_list.split(',')]
        all_hashtags.extend(tags)
    
    # Count the occurrences of each hashtag
    hashtag_counts = Counter(all_hashtags)

    print("Most Common Hashtags in Barber-Related Videos:")
    # Print the 15 most common hashtags and their counts
    for hashtag, count in hashtag_counts.most_common(15):
        print(f"  {hashtag}: {count} times")

if __name__ == "__main__":
    analyze_recommendations()