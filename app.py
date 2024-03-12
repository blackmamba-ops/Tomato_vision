from flask import Flask, request, jsonify, render_template, send_from_directory
from tensorflow.keras.models import load_model
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import urllib.request

app = Flask(__name__)

# Load the machine learning model
model = load_model('Tomato_model.h5')

# Define the mapping of class indices to class names
class_names = {
    0: "Your tomato plant is diagnosed with Early Blight.",
    1: 'Tomato mosaic virus',
    2: 'Your tomato plant is diagnosed with Target Spot',
    3: 'Your tomato plant is Healthy',
    4: 'Your tomato plant is diagnosed with Bacterial spot'
}

# Function to download a file from a URL
def download_file(url, filename):
    urllib.request.urlretrieve(url, filename)

# Function for leaf detection
def leaf_detection(image_path):
    # Read input image
    img = cv2.imread(image_path)

    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Count the number of green pixels
    green_pixel_count = cv2.countNonZero(mask)

    # Set a threshold for considering an image as containing a leaf
    leaf_pixel_threshold = 10000

    # Return result based on green pixel count
    if green_pixel_count > leaf_pixel_threshold:
        return "Leaf detected"
    else:
        return "No leaf detected"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        # Get the image file from the request
        file = request.files["file"]
        
        # Save the file temporarily
        file_path = "temp_image.jpg"
        file.save(file_path)
        
        # Check if image contains a leaf
        leaf_result = leaf_detection(file_path)
        print("Leaf Detection Result:", leaf_result)  # Debug statement

        # If leaf is detected, proceed with prediction
        if leaf_result == "Leaf detected":
            # Read the image file
            img = plt.imread(file_path)
            
            # Resize the image to match the input shape of the model
            img_resized = resize(img, (150, 150, 3))
            
            # Expand dimensions to match the input shape of the model
            img_resized = np.expand_dims(img_resized, axis=0)
            
            # Make prediction
            prediction = model.predict(img_resized)
            predicted_class_index = np.argmax(prediction)
            predicted_class_name = class_names.get(predicted_class_index, 'Unknown')
            print("Prediction Result:", predicted_class_name)  # Debug statement
            return jsonify({"predicted_class": predicted_class_name})
        else:
            return jsonify({"predicted_class": "No leaf detected"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    # Run the Flask application
    app.run(port=5000)
