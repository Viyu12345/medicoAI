import openai
from flask import Flask, render_template, request
import os
import requests
import tkinter as tk


app = Flask(__name__)
api_key = "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"
client = openai.OpenAI(api_key=api_key)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('result.html')

def process_image(file):
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'
    files = {'image': file.stream}
    headers = {'X-Api-Key': 'vigHRf35oNq3iOjl1Nl1vQ==cLyltxaWuWE6bQ2D'}
    r = requests.post(api_url, files=files, headers=headers)
    o = r.json()
    extracted_text = ""
    for x in o:
        if "text" in x:
            extracted_text += x["text"] + "\n"
    return extracted_text

@app.route("/process_image", methods=['POST'])
def start():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        extracted_text = process_image(file)
        u = "Please explain the medical reports along with important terminologys in the extracted text of an medical report "+extracted_text
        messages = [{"role": "user", "content": u}]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        model_response = completion.choices[0].message.content
        print(model_response)
        return model_response, 200

def display_text_in_gui(text):
    root = tk.Tk()
    text_label = tk.Label(root, wraplength=400, justify='left', text=text)
    text_label.pack(padx=10, pady=5)
    root.mainloop()

if __name__ == '__main__':
    app.run(debug=True)
