from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Use a secure secret key for the session

#UPLOAD_FOLDER = 'Labfiles/Training/UPLOAD_FOLDER'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')


model_endpoint = os.getenv('VISION_ENDPOINT')
subscription_key = os.getenv('VISION_KEY')

if not model_endpoint or not subscription_key:
    raise ValueError("Environment variables for the API are not set.")

@app.route('/')
def index():
    return render_template('start1.html')

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
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    params = {
        'api-version': '2023-02-01-preview',
        'model-name': 'newtest'
    }

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        response = requests.post(model_endpoint, headers=headers, params=params, data=image_data)
        response.raise_for_status()  # Check for HTTP errors
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        flash('Failed to analyze the image: ' + str(e))
        return render_template('error.html', error=str(e))

    return render_template('analysis_result.html', filename=filename, result=response_json, image_path=image_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
