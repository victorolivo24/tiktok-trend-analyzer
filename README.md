🤖 AI-Powered TikTok Trend Analyzer
A full-stack web application that scrapes personalized video recommendations from a user's TikTok Studio account, performs a detailed trend analysis, and uses generative AI to brainstorm new content ideas.

Action Required: Replace the placeholder image link above with a real screenshot of your app's final dashboard! Take a screenshot, upload it to a service like Imgur, and paste the image link.
💡 Problem Solved
For content creators, staying on top of trends within a specific niche is crucial but time-consuming. This tool automates the entire research process. It logs into a creator's account, analyzes the content TikTok is personally recommending to them, and uses that data to provide a clear, actionable brief on what to create next.

✨ Features
Secure Authenticated Scraping: Utilizes session cookies to securely access data from behind a login wall without ever exposing user passwords.
Dynamic Content Handling: Intelligently scrolls the page to load a large, dynamic dataset, ensuring a comprehensive analysis.
Interactive Web Dashboard: A user-friendly interface built with Flask and JavaScript that allows for one-click analysis.
Data Visualization: Uses Chart.js to create clean, easy-to-read bar charts of the top trending hashtags and keywords.
NLP Keyword Analysis: Employs the Natural Language Toolkit (NLTK) to perform keyword extraction on video captions, filtering out common "stop words" to find the most meaningful terms.
AI-Powered Content Strategy: Integrates with the Google Gemini API to synthesize the analyzed data into several distinct, creative, and specific video ideas.
🛠️ Tech Stack
Backend: Python, Flask
Web Scraping: Playwright
Data Analysis: Pandas
NLP: NLTK (Natural Language Toolkit)
AI: Google Generative AI (Gemini)
Frontend: HTML, CSS, JavaScript
Data Visualization: Chart.js
🚀 Setup and Usage
Follow these steps to run the application on your local machine.

1. Clone the Repository:

Bash

git clone [your-github-repo-link]
cd [your-repo-name]
2. Set Up the Environment:

Bash

# Create a virtual environment
python -m venv venv

# Activate it (on Windows PowerShell)
.\venv\Scripts\Activate
3. Install Dependencies:

Bash

# Install all required libraries
pip install Flask playwright pandas nltk google-generativeai

# Run the one-time setup for Playwright to install browser dependencies
playwright install
4. Add Your Credentials:

Cookies: Log into TikTok in your regular browser. Use the "Cookie-Editor" extension to export your cookies as JSON. Save this file in the main project directory as my_cookies.json.
API Key: Create a free API key at Google AI Studio. Set this key as an environment variable on your system named GOOGLE_API_KEY.
5. Run the Application:

Bash

# Launch the Flask web server
python app.py
6. Open the Dashboard:

Open your web browser and navigate to http://127.0.0.1:5000.
Click the "Launch Analysis" button and wait for the results!
