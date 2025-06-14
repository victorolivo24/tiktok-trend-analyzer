import pandas as pd
from collections import Counter
import re
import os
import google.generativeai as genai

# --- CONFIGURATION ---
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
    if not GOOGLE_API_KEY:
        return "Google API Key not found. Please set the environment variable."
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are a viral TikTok content strategist for a trendy barbershop.
        Based on this data from trending videos:
        Top Trending Hashtags: {', '.join(top_hashtags)}
        Top Trending Keywords: {', '.join(top_keywords)}
        Generate 3 distinct, creative, and specific video ideas that I can film.
        For each idea, provide a catchy "Title Idea" and a "Video Concept" description.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not connect to the AI service. Error: {e}"

def get_analysis_results():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        return {"error": f"'{INPUT_FILE}' not found. Run scraper.py first."}

    keyword_pattern = '|'.join(BARBER_KEYWORDS)
    df_filtered = df[df['caption'].str.contains(keyword_pattern, na=False, case=False)].copy()
    
    if df_filtered.empty:
        return {"error": "No videos found for your niche in the data."}
    
    # --- Analysis ---
    all_hashtags = [tag.strip().lower() for tag_list in df_filtered['hashtags'].dropna() for tag in tag_list.split(',') if tag.strip()]
    hashtag_counts = Counter(all_hashtags).most_common(10) # Top 10 for the chart
    
    all_words = re.findall(r'\b\w+\b', ' '.join(df_filtered['caption'].dropna()).lower())
    meaningful_words = [word for word in all_words if word not in STOP_WORDS and word not in BARBER_KEYWORDS and not word.isdigit() and len(word) > 2]
    keyword_counts = Counter(meaningful_words).most_common(10) # Top 10 for the chart
    
    top_hashtags_for_ai = [item[0] for item in hashtag_counts]
    top_keywords_for_ai = [item[0] for item in keyword_counts]
    ai_recs = generate_ai_recommendations(top_hashtags_for_ai, top_keywords_for_ai)
    
    return {
        "total_videos_analyzed": len(df_filtered), # <-- THE NEW DATA POINT
        "hashtags": hashtag_counts,
        "keywords": keyword_counts,
        "ai_recs": ai_recs
    }

if __name__ == "__main__":
    results = get_analysis_results()
    print(results)