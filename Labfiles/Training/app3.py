from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import requests
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Use a secure secret key for the session

UPLOAD_FOLDER = 'Labfiles/Training/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your environment variables for the API
model_endpoint = os.getenv('VISION_ENDPOINT')
subscription_key = os.getenv('VISION_KEY')

# Ensure you have the model endpoint and key before starting
if not model_endpoint or not subscription_key:
    raise ValueError("Environment variables for the API are not set.")



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    # After saving the file, redirect to the analysis route
    return redirect(url_for('analyze_image', filename=filename))

@app.route('/analyze/<filename>')
def analyze_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Prepare headers and params for the API call
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    params = {
        'api-version': '2023-02-01-preview',
        'model-name': 'newtest'
    }

    # Read the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Make the API call
    response = requests.post(model_endpoint, headers=headers, params=params, data=image_data)
    response_json = response.json()

    # Print the JSON response
    print(json.dumps(response_json, indent=2))

    # Display the results in the analysis_result.html template
    return render_template('analysis_result.html', result=response_json, image_path=image_path)
