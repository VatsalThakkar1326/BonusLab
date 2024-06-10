## link to my application : https://face-gazzer-u64ezt75sq-uc.a.run.app


### A Structured Guide to Recreate Your Flask Application and Deploy it to Google Cloud Run

#### Step 1: Environment Setup

First, ensure you have Python 3.10 installed. Then, set up a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### Step 2: Install Dependencies

Create a `requirements.txt` file with all the necessary packages:

```
Flask
opencv-python
mediapipe
numpy
Pillow
gunicorn
```

Install them using pip:

```bash
pip install -r requirements.txt
```

#### Step 3: Flask Application

Your Flask application will serve as the backend server. Here's a detailed breakdown:

##### 3.1. Import Libraries

Start by importing the necessary libraries:

```python
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import base64
from io import BytesIO
from PIL import Image
```

##### 3.2. Initialize Flask and Mediapipe

Initialize the Flask app and Mediapipe for face mesh detection:

```python
app = Flask(__name__)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
```

##### 3.3. Define Helper Functions

Define functions to process the image and detect the gaze:

```python
def detect_gaze(landmarks, frame):
    # ... gaze detection logic ...

def process_frame(image_data):
    # ... frame processing logic ...
```

##### 3.4. Define Routes

Set up the routes to handle requests:

```python
@app.route('/process_frame', methods=['POST'])
def process_frame_route():
    # ... logic to handle frame processing ...

@app.route('/')
def index():
    return render_template('client.html')
```

##### 3.5. Run the Application

Include a block to run the app, especially useful for local development:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

#### Step 4: Client-Side Code

The client-side code will interact with the user's webcam and send frames to the server.

##### 4.1. HTML Structure

Create an HTML file with video and image elements to display the webcam feed and processed frames:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Video Feed</title>
</head>
<body>
    <h1>Video Feed</h1>
    <video id="video" width="640" height="480" autoplay></video>
    <canvas id="canvas" width="640" height="480" style="display: none;"></canvas>
    <img id="processed-video" width="640" height="480" />
    <!-- Include JavaScript file -->
    <script src="client.js"></script>
</body>
</html>
```

##### 4.2. JavaScript Logic (`client.js`)

Write a JavaScript file named `client.js` to handle webcam access and frame transmission:

```javascript
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const processedVideo = document.getElementById('processed-video');

// Access the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
    })
    .catch(err => {
        console.error("Error accessing webcam: " + err);
    });

// Send frames to the server
function sendFrame() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');
    fetch('/process_frame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        processedVideo.src = 'data:image/jpeg;base64,' + data.image;
    })
    .catch(err => {
        console.error('Error sending frame: ' + err);
    });
}

// Send a frame every 100ms
setInterval(sendFrame, 100);
```

This JavaScript code will capture frames from the webcam and send them to the Flask server for processing. The processed frames are then displayed on the webpage.

#### Step 5: Dockerize the Application

Create a Dockerfile to containerize your application. Here's an example snippet:

```Dockerfile
FROM python:3.10-slim
# ... rest of the Dockerfile
```

#### Step 6: Build the Docker Image

Build your Docker image with the following command:

```bash
docker build -t myapp .
```

#### Step 7: Test Locally

Before deploying, test the Docker container locally:

```bash
docker run -p 8080:8080 myapp
```

#### Step 8: Deploy to Google Cloud Run

##### 8.1. Google Cloud SDK Setup

Ensure that you have the Google Cloud SDK installed and initialized on your machine. If not, download and install it, then authenticate with your Google account:

```bash
gcloud auth login
```

##### 8.2. Configure Project ID

Set your Google Cloud project ID as the default for the `gcloud` command-line tool:

```bash
gcloud config set project PROJECT_ID
```

Replace `PROJECT_ID` with your actual Google Cloud project ID.

##### 8.3. Build the Container Image

Build your container image using Cloud Build and submit it to Google Container Registry:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/myapp
```

This command will package your application, upload it to Google Cloud, and build the Docker image.

##### 8.4. Deploy the Image to Cloud Run

Deploy the newly built image to Google Cloud Run:

```bash
gcloud run deploy --image gcr.io/PROJECT_ID/myapp --platform managed
```

During the deployment process, you will be prompted to select a region, allow unauthenticated invocations, and other configuration options.

#### Step 9: Access the Application

##### 9.1. Find the Service URL

After deployment, Google Cloud Run will provide you with a URL to access your service. You can also find this URL in the Cloud Run dashboard or by using the following command:

```bash
gcloud run services describe myapp --platform managed --format "value(status.url)"
```

##### 9.2. Open the Application

Open the provided URL in a web browser to interact with your deployed Flask application. The URL will look something like this:

```
https://myapp-xyz-uc.a.run.app
```

##### 9.3. Monitor and Manage

You can monitor the status of your application, view logs, and manage your service through the Google Cloud Console.

--- 

This guide provides a structured approach to recreate your Flask application and deploy it to Google Cloud Run. Each step is clearly outlined with necessary commands and
