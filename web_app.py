from flask import Flask, render_template, request, redirect, url_for
from modules.authentication import authenticate
from modules.proposal_generator import generate_cover_letter
from modules.upwork_calls import get_job_details
import re

app = Flask(__name__)

client = authenticate()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_job_url():
    job_url = request.form['job_url']

    # Extract the job ID from the URL using a regular expression
    match = re.search(r'~[0-9a-zA-Z]{18}', job_url)
    if match:
        job_id = match.group()
    else:
        error = "Invalid Upwork job URL"
        return render_template('index.html', error=error)

    try:
        job = get_job_details(client, job_id)
        cover_letter = generate_cover_letter(job['profile']['op_description'])
    except Exception as e:
        error = f"Error: {str(e)}"
        return render_template('index.html', error=error)

    return render_template('index.html', cover_letter=cover_letter)

if __name__ == '__main__':
    app.run(debug=True)