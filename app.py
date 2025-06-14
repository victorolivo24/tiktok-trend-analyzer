from flask import Flask, render_template

# Create an instance of the Flask class
app = Flask(__name__)

# Define a "route" for the main page
@app.route('/')
def index():
    # This function will run when someone visits the homepage
    # It will look for a file named 'index.html' in a 'templates' folder
    return render_template('index.html')

# This allows you to run the app directly from the command line
if __name__ == '__main__':
    app.run(debug=True)