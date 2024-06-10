import os
from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
import mediapipe as mp
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

def detect_gaze(landmarks, frame):
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']

    left_eye_center = np.mean(left_eye, axis=0).astype(int)
    right_eye_center = np.mean(right_eye, axis=0).astype(int)

    if left_eye_center[0] < right_eye_center[0]:
        return "Focused"
    else:
        return "Not Focused"

def process_frame(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data.split(",")[1])))
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = {
                'left_eye': [(int(pt.x * frame.shape[1]), int(pt.y * frame.shape[0])) for pt in face_landmarks.landmark[133:144]],
                'right_eye': [(int(pt.x * frame.shape[1]), int(pt.y * frame.shape[0])) for pt in face_landmarks.landmark[362:373]]
            }
            for pt in face_landmarks.landmark:
                x, y = int(pt.x * frame.shape[1]), int(pt.y * frame.shape[0])
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            gaze = detect_gaze(landmarks, frame)
            cv2.putText(frame, gaze, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/process_frame', methods=['POST'])
def process_frame_route():
    data = request.json
    image_data = data['image']
    frame = process_frame(image_data)
    return jsonify({'image': frame})

@app.route('/')
def index():
    return render_template('client.html')

# This block is optional for Google Cloud Run but useful for local development.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
