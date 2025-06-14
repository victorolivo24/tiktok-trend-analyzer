import pandas as pd
from collections import Counter
import re
import os
import google.generativeai as genai

# --- CONFIGURATION ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INPUT_FILE = 'tiktok_studio_insights.csv'
BARBER_KEYWORDS = ['barber', 'haircut', 'hairstyle', 'fade', 'taper', 'burstfade', 'lowfade', 'midfade', 'fringe', 'buzzcut', 'mullet']

try:
    from nltk.corpus import stopwords
    import nltk
    try: stopwords.words('english')
    except LookupError: nltk.download('stopwords')
    STOP_WORDS = set(stopwords.words('english'))
except ImportError:
    # This block is for auto-installation if NLTK is missing
    print("NLTK library not found. Installing..."); import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"]); from nltk.corpus import stopwords; nltk.download('stopwords'); STOP_WORDS = set(stopwords.words('english'))

def generate_ai_recommendations(top_hashtags, top_keywords):
    """Generates AI recommendations and returns them as a string."""
    if not GOOGLE_API_KEY:
        return "Google API Key not found. Please set the environment variable."
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are a viral TikTok content strategist for a trendy barbershop.
        Based on this data from trending videos:
        Top Hashtags: {', '.join(top_hashtags)}
        Top Keywords: {', '.join(top_keywords)}
        Generate 3 distinct, creative, and specific video ideas. For each idea, provide a "Title Idea" and a "Video Concept".
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not connect to the AI service. Error: {e}"

def get_analysis_results():
    """
    This is our main logic function. It reads the CSV and returns a dictionary of results.
    """
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
    hashtag_counts = Counter(all_hashtags).most_common(15)
    
    all_words = re.findall(r'\b\w+\b', ' '.join(df_filtered['caption'].dropna()).lower())
    meaningful_words = [word for word in all_words if word not in STOP_WORDS and word not in BARBER_KEYWORDS and not word.isdigit() and len(word) > 2]
    keyword_counts = Counter(meaningful_words).most_common(15)
    
    # --- AI Recs ---
    top_10_hashtags = [item[0] for item in hashtag_counts[:10]]
    top_10_keywords = [item[0] for item in keyword_counts[:10]]
    ai_recs = generate_ai_recommendations(top_10_hashtags, top_10_keywords)
    
    return {
        "hashtags": hashtag_counts,
        "keywords": keyword_counts,
        "ai_recs": ai_recs
    }

# This block allows us to still run 'python analyzer.py' directly if we want
if __name__ == "__main__":
    results = get_analysis_results()
    if "error" in results:
        print(results["error"])
    else:
        print("\n" + "="*40 + "\n🏆 Top 15 Most Common Hashtags 🏆\n" + "="*40)
        for hashtag, count in results['hashtags']: print(f"  {hashtag}: {count} times")
        
        print("\n" + "="*40 + "\n🔑 Top 15 Most Common Keywords 🔑\n" + "="*40)
        for keyword, count in results['keywords']: print(f"  '{keyword}': {count} times")
        
        print("\n" + "="*50 + "\n🤖 AI-Powered Creative Recommendations 🤖\n" + "="*50)
        print(results['ai_recs'])