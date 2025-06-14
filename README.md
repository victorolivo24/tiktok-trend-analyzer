# 🤖 AI-Powered TikTok Trend Analyzer

A full-stack web application that uses an authenticated browser session to scrape personalized video recommendations from a user's TikTok Studio account, performs a detailed trend analysis, and leverages generative AI to brainstorm new content ideas.

---

## 💡 Problem Solved

For content creators, staying on top of trends within a specific niche is crucial but time-consuming. This tool automates the entire market research process. It logs into a creator's account, analyzes the content TikTok is personally recommending to them, and uses that data to provide a clear, actionable brief on what styles and topics are currently performing well.

---

## ✨ Features

- **Secure Authenticated Scraping**: Uses session cookies to securely access data behind login walls, without handling or storing passwords.  
- **Dynamic Content Handling**: Scrolls automatically to collect large sets of data from infinite-scroll feeds.  
- **Interactive Web Dashboard**: Built with Flask and JavaScript for simple one-click analysis and clean results display.  
- **Data Visualization**: Uses Chart.js to render animated bar charts of trending hashtags and keywords.  
- **NLP Keyword Extraction**: Uses NLTK to extract meaningful terms from video captions, filtering out common stop words.  
- **AI-Powered Content Strategy**: Uses Google Gemini API to turn trends into detailed video content ideas.  
- **Toggleable Views**: Charts for quick summaries + expandable lists for raw data inspection.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **Web Scraping**: Playwright  
- **Data Analysis**: Pandas  
- **NLP**: NLTK  
- **AI**: Google Generative AI (Gemini)  
- **Frontend**: HTML, CSS, JavaScript  
- **Data Viz**: Chart.js

---

## 🚀 Setup and Usage

### Step 1: Initial Setup

**Clone the repository:**
git clone https://github.com/victorolivo24/tiktok-trend-analyzer.git
cd tiktok-trend-analyzer

Create and activate a virtual environment:
python -m venv venv
# On Windows PowerShell
.\venv\Scripts\Activate

Install dependencies:
pip install -r requirements.txt
playwright install

Step 2: Authentication (One-Time Setup)
API Key
Go to Google AI Studio and create a free API key.

Set the key as an environment variable:

GOOGLE_API_KEY=your_api_key_here

TikTok Session Cookies
Install the Cookie-Editor browser extension (Chrome/Firefox).

Log in to your TikTok account.

Open Cookie-Editor → Export → Export as JSON.

Create a file my_cookies.json in the root folder.

Paste the copied cookies and save the file.

✅ This file is .gitignored to stay private.

Step 3: Run the App
Launch the Flask server:

bash
Copy
Edit
python app.py
Open the dashboard:

Go to http://127.0.0.1:5000

Click "Launch Analysis" and see your results!

📂 Project Structure
graphql
Copy
Edit
/
├── app.py              # Flask backend
├── scraper.py          # Scrapes TikTok Studio
├── analyzer.py         # Performs trend analysis + AI generation
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend UI
├── my_cookies.json     # TikTok session cookies (private)
└── .gitignore          # Files to ignore
