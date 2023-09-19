from flask import Flask, redirect, url_for, request, render_template, session
import os, uuid, json, requests
from PIL import Image
import openai
import pytesseract
from tkinter import filedialog
import tkinter as tk

from dotenv import load_dotenv
load_dotenv()

app = Flask (__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def generateImage():
    prompt = request.form['prompt']

    openai.api_type = "azure"
    openai.api_base = os.environ['api_base']
    openai.api_version = os.environ['api_version']
    openai.api_key = os.environ['api_key']

    response = openai.Image.create(
        prompt=prompt,
        size='1024x1024',
        n=1
    )

    response = response
    image_url = response["data"][0]["url"]
    
    return render_template(
        'image-gen.html',
        prompt=prompt,
        image_url=image_url)

# def colourPicker():
#     imageSelected = request.form['ImageSelected']

#     key = os.environ['KEY']
#     endpoint = os.environ['ENDPOINT']
#     location = os.environ['LOCATION']

#     path = '/vision/v3.1/analyze'
#     constructedURL = endpoint + path

#     headers = {'Ocp-Apim-Subscription-Key': key}
#     params = {'visualFeatures': 'Color'}
#     data = {'url': str(imageSelected)}

#     headers = {
#         'Ocp-Apim-Subscription-Key': key,
#         'Ocp-Apim-Subscription-Region': location,
#         'Content-type': 'application/json',
#         'X-ClientTraceId': str(uuid.uuid4())
#     }

#     response = requests.post(constructedURL, headers=headers, params=params, json=data)
#     response.raise_for_status()
#     analysis = response.json()

#     return render_template(
#         'palette.html',
#         ImageSelected=str(imageSelected),
#         dominantCOLOURS=analysis['color']['dominantColors'],
#         accentCOLOUR=analysis['color']['accentColor'],
#         blackWHITE=analysis['color']['isBWImg']
#     )

# def upload_image():
#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename()
#     return file_path

# def image_to_notes(file_path, notes_path):
#     # Load the image
#     image = Image.open(file_path)

#     # Extract text from the image using pytesseract
#     text = pytesseract.image_to_string(image)

#     # Open the JSON file for appending
#     with open(notes_path, "a") as notes_file:
#         # Append a new note object to the JSON file
#         note = {"file_path": file_path, "text": text}
#         json.dump(note, notes_file)
#         notes_file.write("\n")
