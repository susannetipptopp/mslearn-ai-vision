# import to be able to get .env file
from fileinput import filename
from dotenv import load_dotenv
load_dotenv()
# import to be able to use the environment variables
import os # to be able to use the os.getcwd() function to test: print('we are here',os.getcwd())

from flask import Flask, render_template, request, redirect, url_for, flash

import json  # Assuming you're using json to format your response



# environment variables
model_endpoint = os.getenv('VISION_ENDPOINT')
subscription_key = os.getenv('VISION_KEY')

if model_endpoint is None:
    raise ValueError("model_endpoint is not set. Please set it to a valid URL.")

# import to be able to use the REST API
import requests
# import to be able to use the JSON format
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') # Use a secure  key for the session

# This is the path to the directory where uploaded files will be saved
# Ensure this directory exists and your app has write permissions to it
UPLOAD_FOLDER = 'Labfiles/Training/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    print(f"Directory {UPLOAD_FOLDER} does not exist.")
else:
    print(f"Directory {UPLOAD_FOLDER} exists.")

@app.route('/')
def index():
    return render_template('upload.html')  # Assuming your HTML file is named upload_form.html

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    if file:
        # You can add a security check here for file type or file name
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect or respond as necessary, e.g., show a success message or the uploaded image
        flash('File successfully uploaded')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



# Headers and import paratmeters
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}   

params = {'api-version': '2023-02-01-preview',
          'model-name': 'newtest'}

# the path to the image file
# image_path = 'Labfiles/Training/PlantImages/1.jpg'
image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)    




# open the image file

with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# make the post request to the REST API
response = requests.post(model_endpoint, headers=headers, params=params, data=image_data)

# get the JSON response
response_json = response.json()

# print the JSON response
print(json.dumps(response_json, indent=2))

# for all the data in the JSON response send it to the web page


@app.route('/')
def index():
    return render_template('index.html', data=response_json)

if __name__ == '__main__':
    app.run(debug=True)

# to test the path
    
print('we are here',os.getcwd())


