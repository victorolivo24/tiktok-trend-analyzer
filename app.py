from flask import Flask, render_template, jsonify
import subprocess
import sys

# Import the function we just created in our analyzer
from analyzer import get_analysis_results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-analysis')
def run_analysis():
    """This route will be called by our webpage."""
    print("Backend: Received request to run analysis...")
    
    # Step 1: Run the scraper.py script using subprocess
    # We use sys.executable to ensure it uses the python from our venv
    print("Backend: Running scraper.py...")
    subprocess.run([sys.executable, "scraper.py"])
    print("Backend: scraper.py finished.")
    
    # Step 2: Run the analyzer function and get the results
    print("Backend: Running analyzer...")
    results = get_analysis_results()
    print("Backend: Analysis complete. Sending results to frontend.")
    
    # Step 3: Return the results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)