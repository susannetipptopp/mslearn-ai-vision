# import to be able to get .env file
from dotenv import load_dotenv
load_dotenv()
# import to be able to use the environment variables
import os # to be able to use the os.getcwd() function to test: print('we are here',os.getcwd())

from flask import Flask, render_template, jsonify
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

# Headers and import paratmeters
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}   

params = {'api-version': '2023-02-01-preview',
          'model-name': 'newtest'}

# the path to the image file
image_path = 'Labfiles/Training/PlantImages/1.jpg'

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
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=response_json)

if __name__ == '__main__':
    app.run(debug=True)

# to test the path
    
print('we are here',os.getcwd())


