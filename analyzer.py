import pandas as pd
from collections import Counter
import re

INPUT_FILE = 'tiktok_final_insights.csv'
BARBER_KEYWORDS = ['barber', 'haircut', 'hairstyle', 'fade', 'taper', 'burstfade', 'lowfade', 'midfade', 'fringe', 'buzzcut', 'mullet']

try:
    from nltk.corpus import stopwords; import nltk
    try: stopwords.words('english')
    except LookupError: nltk.download('stopwords')
    STOP_WORDS = set(stopwords.words('english'))
except ImportError:
    print("NLTK not found. Installing..."); import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
    from nltk.corpus import stopwords; nltk.download('stopwords')
    STOP_WORDS = set(stopwords.words('english'))

def convert_to_number(s):
    if not isinstance(s, str): return s
    s = s.lower().strip()
    if 'm' in s: return float(s.replace('m', '')) * 1000000
    if 'k' in s: return float(s.replace('k', '')) * 1000
    try: return float(s)
    except (ValueError, TypeError): return 0

def analyze_insights():
    try:
        df = pd.read_csv(INPUT_FILE); print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.\n")
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found. Run scraper.py first."); return

    keyword_pattern = '|'.join(BARBER_KEYWORDS)
    df_filtered = df[df['caption'].str.contains(keyword_pattern, na=False, case=False)].copy()
    
    if df_filtered.empty: print(f"No videos found for your niche."); return
    print(f"Found {len(df_filtered)} videos related to the barbering niche. Generating final report...")
    
    df_filtered['views_num'] = df_filtered['views'].apply(convert_to_number)
    df_filtered['likes_num'] = df_filtered['likes'].apply(convert_to_number)
    df_sorted_by_views = df_filtered.sort_values(by='views_num', ascending=False)

    print("\n" + "="*40 + "\n🔥 Top 5 Most Viewed Videos 🔥\n" + "="*40)
    for index, row in df_sorted_by_views.head(5).iterrows():
        print(f"  Views: {row['views']} | Likes: {row['likes']}")
        print(f"  Caption: {row['caption'][:80]}...")
        print("-" * 20)

    print("\n" + "="*40 + "\n🏆 Top 15 Most Common Hashtags 🏆\n" + "="*40)
    all_hashtags = [tag.strip().lower() for tag_list in df_filtered['hashtags'].dropna() for tag in tag_list.split(',') if tag.strip()]
    for hashtag, count in Counter(all_hashtags).most_common(15): print(f"  {hashtag}: {count} times")

    print("\n" + "="*40 + "\n🔑 Top 15 Most Common Keywords 🔑\n" + "="*40)
    all_words = re.findall(r'\b\w+\b', ' '.join(df_filtered['caption'].dropna()).lower())
    meaningful_words = [word for word in all_words if word not in STOP_WORDS and word not in BARBER_KEYWORDS and not word.isdigit() and len(word) > 2]
    for keyword, count in Counter(meaningful_words).most_common(15): print(f"  '{keyword}': {count} times")

if __name__ == "__main__":
    analyze_insights()