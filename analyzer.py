import pandas as pd
from collections import Counter
import re
import os
import google.generativeai as genai

# --- CONFIGURATION ---
# IMPORTANT: PASTE YOUR API KEY HERE
# For a real application, use environment variables, but this is fine for a personal project.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

INPUT_FILE = 'tiktok_final_insights.csv'
BARBER_KEYWORDS = ['barber', 'haircut', 'hairstyle', 'fade', 'taper', 'burstfade', 'lowfade', 'midfade', 'fringe', 'buzzcut', 'mullet']

try:
    from nltk.corpus import stopwords; import nltk
    try: stopwords.words('english')
    except LookupError: nltk.download('stopwords')
    STOP_WORDS = set(stopwords.words('english'))
except ImportError:
    print("NLTK not found. Installing..."); import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"]); from nltk.corpus import stopwords; nltk.download('stopwords'); STOP_WORDS = set(stopwords.words('english'))

def generate_ai_recommendations(top_hashtags, top_keywords):
    """Uses a generative AI to create video ideas based on the data."""
    # This section is unchanged
    print("\n" + "="*50 + "\n🤖 AI-Powered Creative Recommendations 🤖\n" + "="*50)
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are a viral TikTok content strategist for a trendy, modern barbershop.
        I have analyzed competitor videos and have the following data on what is trending:

        Top Trending Hashtags: {', '.join(top_hashtags)}
        Top Trending Keywords: {', '.join(top_keywords)}

        Based ONLY on this data, generate 3 distinct, creative, and specific video ideas that I can film.
        For each idea, provide a catchy "Title Idea" and a "Video Concept" description.
        Make the concepts visual and engaging for a TikTok audience.
        """
        print("Connecting to AI to generate creative ideas... Please wait.")
        response = model.generate_content(prompt)
        print("\nHere are your AI-generated video ideas:\n")
        print(response.text)
    except Exception as e:
        print("\nCould not connect to the AI service."); print(f"Error details: {e}")

def analyze_insights():
    try:
        df = pd.read_csv(INPUT_FILE); print(f"Successfully loaded {len(df)} recommendations from '{INPUT_FILE}'.\n")
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found. Run scraper.py first."); return

    keyword_pattern = '|'.join(BARBER_KEYWORDS)
    df_filtered = df[df['caption'].str.contains(keyword_pattern, na=False, case=False)].copy()
    
    if df_filtered.empty: print(f"No videos found for your niche."); return
    print(f"Found {len(df_filtered)} videos related to the barbering niche. Generating final report...")
    
    # --- Analysis Section ---
    all_hashtags = [tag.strip().lower() for tag_list in df_filtered['hashtags'].dropna() for tag in tag_list.split(',') if tag.strip()]
    hashtag_counts = Counter(all_hashtags)
    top_10_hashtags_list = [item[0] for item in hashtag_counts.most_common(10)]
    
    all_words = re.findall(r'\b\w+\b', ' '.join(df_filtered['caption'].dropna()).lower())
    meaningful_words = [word for word in all_words if word not in STOP_WORDS and word not in BARBER_KEYWORDS and not word.isdigit() and len(word) > 2]
    keyword_counts = Counter(meaningful_words)
    top_10_keywords_list = [item[0] for item in keyword_counts.most_common(10)]

    # --- NEW: Print the rankings first ---
    print("\n" + "="*40 + "\n🏆 Top 15 Most Common Hashtags 🏆\n" + "="*40)
    for hashtag, count in hashtag_counts.most_common(15): print(f"  {hashtag}: {count} times")

    print("\n" + "="*40 + "\n🔑 Top 15 Most Common Keywords 🔑\n" + "="*40)
    for keyword, count in keyword_counts.most_common(15): print(f"  '{keyword}': {count} times")
    # --- End of added section ---

    # --- Generate AI recommendations using the data ---
    if GOOGLE_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("\n" + "!"*50 + "\n!!! ACTION REQUIRED: Please paste your Google AI API key.\n" + "!"*50)
    else:
        generate_ai_recommendations(top_10_hashtags_list, top_10_keywords_list)

if __name__ == "__main__":
    analyze_insights()