from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from flask import Flask, redirect, url_for, request, render_template, session

import os, uuid, json, requests


# from dotenv import load_dotenv
# load_dotenv()


app = Flask (__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def helloWorld():
    imageSelected = request.form['ImageSelected']

    # key = os.environ['KEY']
    # endpoint = os.environ['ENDPOINT']
    # location = os.environ['LOCATION']

    key = "8a54f9fab78f41929264d9581a0d0e22"
    endpoint = "https://colour-palette.cognitiveservices.azure.com/"
    # endpoint = "https://westeurope.api.cognitive.microsoft.com/"
    location = "westeurope"

    path = '/vision/v3.1/analyze'
    constructedURL = endpoint + path

    headers = {'Ocp-Apim-Subscription-Key': key}
    params = {'visualFeatures': 'Color'}
    data = {'url': str(imageSelected)}

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    response = requests.post(constructedURL, headers=headers, params=params, json=data)
    response.raise_for_status()
    analysis = response.json()

    return render_template(
        'palette.html',
        ImageSelected=str(imageSelected),
        dominantCOLOURS=analysis['color']['dominantColors'],
        accentCOLOUR=analysis['color']['accentColor'],
        blackWHITE=analysis['color']['isBWImg']
    )

