🤖 AI-Powered TikTok Trend Analyzer
A full-stack web application that uses an authenticated browser session to scrape personalized video recommendations from a user's TikTok Studio account, performs a detailed trend analysis, and leverages generative AI to brainstorm new content ideas.

💡 Problem Solved
For content creators, staying on top of trends within a specific niche is crucial but time-consuming. This tool automates the entire market research process. It logs into a creator's account, analyzes the content TikTok is personally recommending to them, and uses that data to provide a clear, actionable brief on what styles and topics are currently performing well.

✨ Features
Secure Authenticated Scraping: Utilizes user-provided session cookies to securely access personalized data from behind a login wall without handling or storing passwords.
Dynamic Content Handling: Automatically scrolls the page to gather a large, dynamic dataset from "infinite scroll" style feeds, ensuring a comprehensive analysis.
Interactive Web Dashboard: A user-friendly interface built with Flask and JavaScript that allows for one-click analysis and displays results in a clean, modern layout.
Data Visualization: Uses Chart.js to create animated, easy-to-read bar charts of the top trending hashtags and keywords.
NLP Keyword Extraction: Employs the Natural Language Toolkit (NLTK) to perform keyword extraction on video captions, filtering out common "stop words" to find the most meaningful terms.
AI-Powered Content Strategy: Integrates with the Google Gemini API to synthesize the analyzed data into several distinct, creative, and specific video ideas.
Toggleable Views: The dashboard provides a clean visual summary with charts, plus "Show/Hide Full List" buttons for a deeper dive into the raw data.
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

Step 1: Initial Setup
Clone the Repository:

Bash

git clone https://github.com/victorolivo24/tiktok-trend-analyzer.git
cd tiktok-trend-analyzer
Create and Activate Virtual Environment:

Bash

# Create the environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate
Install Dependencies:
This project uses a requirements.txt file to manage all libraries.

Bash

# Ensure you have a requirements.txt file with Flask, playwright, pandas, nltk, and google-generativeai
pip install -r requirements.txt

# Run the one-time setup for Playwright to install browser dependencies
playwright install
Step 2: Authentication (One-Time Setup)
This application requires credentials to access your personalized TikTok data.

API Key:

Create a free API key at Google AI Studio.
Securely set this key as an Environment Variable on your system named GOOGLE_API_KEY.
TikTok Session Cookies:

Install a browser extension called "Cookie-Editor" (available for Chrome/Firefox).
Open your browser and log in to your TikTok account.
Click the Cookie-Editor extension icon and choose "Export" -> "Export as JSON".
In the root of the project folder, create a new file named my_cookies.json.
Paste the copied cookie data into this file and save it. The .gitignore file is configured to keep this file private.
Step 3: Run the Application
Launch the Flask Web Server:

Bash

python app.py
Open the Dashboard:

Open your web browser and navigate to http://127.0.0.1:5000.
Click the "Launch Analysis" button and see the results!
📂 Project Structure
/
├── app.py              # The Flask backend server
├── scraper.py          # The Playwright script for scraping data
├── analyzer.py         # The script for data analysis and AI integration
├── requirements.txt    # List of Python dependencies
├── templates/
│   └── index.html      # The HTML/CSS/JS for the frontend dashboard
├── my_cookies.json     # (Ignored by Git) Your personal session cookies
└── .gitignore          # Specifies files for Git to ignore
