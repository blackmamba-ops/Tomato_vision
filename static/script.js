// Hide the image message initially
window.onload = function() {
    var message = document.getElementById('image-message');
    message.style.display = 'none';
}

function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var preview = document.getElementById('image-preview');
        preview.src = reader.result;

        // Show the image preview
        preview.style.display = 'block';

        // Hide the text message
        var message = document.getElementById('image-message');
        message.style.display = 'none';
    }
    reader.readAsDataURL(event.target.files[0]);

    // Show the text message if no image is selected
    if (event.target.files.length === 0) {
        var message = document.getElementById('image-message');
        message.style.display = 'block';
    }
}

function predict() {
    // Get the image file selected by the user
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];

    // Check if a file is selected
    if (file) {
        // Create a FormData object to send the image file to the server
        var formData = new FormData();
        formData.append('file', file);

        // Send a POST request to the /predict endpoint of your Flask server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Update the prediction result once the response is received
            var predictionResult = document.getElementById('prediction-result');
            predictionResult.innerHTML = 'Prediction: ' + data.predicted_class;
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors if necessary
        });
    } else {
        // If no file is selected, display a message to choose a file
        var predictionResult = document.getElementById('prediction-result');
        predictionResult.innerHTML = 'Please choose a file before predicting.';
    }
}

function scrollToSection(sectionId) {
    var section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
}