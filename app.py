from flask import Flask, request, render_template, send_from_directory
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Display uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Load AI Model
print("Loading AI model...")
model = MobileNetV2(weights="imagenet")
print("Model loaded successfully!")

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Image Metadata
    img_info = Image.open(filepath)
    width, height = img_info.size
    file_size = round(os.path.getsize(filepath) / (1024 * 1024), 2)

    # Process Image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)

    # Top 3 Predictions
    results = decode_predictions(predictions, top=3)[0]

    prediction = results[0][1].replace("_", " ").title()
    confidence = results[0][2] * 100

    top_predictions = ""

    for item in results:
        label = item[1].replace("_", " ").title()
        score = item[2] * 100

        top_predictions += f"""
        <div style="margin:15px 0;">
            <div style="display:flex;justify-content:space-between;">
                <span>{label}</span>
                <span>{score:.2f}%</span>
            </div>

            <div style="
                width:100%;
                height:12px;
                background:rgba(255,255,255,0.2);
                border-radius:10px;
                overflow:hidden;
                margin-top:5px;
            ">
                <div style="
                    width:{score:.2f}%;
                    height:100%;
                    background:white;
                ">
                </div>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>AI Vision Pro</title>

<style>

* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Segoe UI',sans-serif;
}}

body {{
    background:linear-gradient(-45deg,#667eea,#764ba2,#6a11cb,#2575fc);
    background-size:400% 400%;
    animation:gradient 12s ease infinite;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:30px;
}}

@keyframes gradient {{
    0%{{background-position:0% 50%;}}
    50%{{background-position:100% 50%;}}
    100%{{background-position:0% 50%;}}
}}

.card {{
    width:800px;
    background:rgba(255,255,255,0.15);
    backdrop-filter:blur(15px);
    padding:30px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0 8px 32px rgba(0,0,0,0.2);
}}

img {{
    width:320px;
    border-radius:15px;
    margin:20px 0;
}}

.result {{
    background:rgba(255,255,255,0.12);
    padding:20px;
    border-radius:15px;
    margin-top:20px;
}}

.bar {{
    width:100%;
    height:20px;
    background:rgba(255,255,255,0.2);
    border-radius:20px;
    overflow:hidden;
    margin-top:10px;
}}

.fill {{
    height:100%;
    width:{confidence:.2f}%;
    background:white;
}}

.info-card {{
    margin-top:20px;
    padding:15px;
    border-radius:12px;
    background:rgba(255,255,255,0.1);
}}

.btn {{
    display:inline-block;
    margin-top:25px;
    padding:12px 25px;
    background:white;
    color:#6a11cb;
    text-decoration:none;
    border-radius:10px;
    font-weight:bold;
}}

.btn:hover {{
    opacity:0.9;
}}

</style>
</head>

<body>

<div class="card">

<h1>🤖 AI Vision Pro</h1>

<img src="/uploads/{file.filename}" alt="Uploaded Image">

<div class="result">

<h2>{prediction}</h2>

<h3>Confidence: {confidence:.2f}%</h3>

<div class="bar">
    <div class="fill"></div>
</div>

<div class="info-card">

    <h3>📷 Image Details</h3>

    <p><b>File:</b> {file.filename}</p>

    <p><b>Dimensions:</b> {width} × {height}</p>

    <p><b>Size:</b> {file_size} MB</p>

</div>

<h3 style="margin-top:25px;">🏆 Top 3 Predictions</h3>

{top_predictions}

</div>

<a href="/" class="btn">
Analyze Another Image
</a>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)