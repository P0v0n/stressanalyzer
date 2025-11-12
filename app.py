"""
Stress Analyzer Web Application
Flask-based web interface for facial stress detection
"""
import os
import base64
import cv2
import dlib
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import io
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Path to dlib predictor
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"

# Initialize dlib detector and predictor
try:
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    model_loaded = True
except Exception as e:
    detector = None
    predictor = None
    model_loaded = False
    print(f"Error loading dlib model: {e}")


# ----------------------------
# Utility functions
# ----------------------------
def euclidean(p1, p2):
    """Calculate Euclidean distance between two points"""
    return np.linalg.norm(np.array(p1) - np.array(p2))


def get_landmarks_from_frame(frame):
    """Extract 68 landmarks from an image frame. Returns list of (x,y) or None."""
    if detector is None or predictor is None:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None

    face = faces[0]
    landmarks = predictor(gray, face)
    return [(p.x, p.y) for p in landmarks.parts()]


def compute_au_metrics(landmarks):
    """Compute Action Unit metrics from facial landmarks"""
    face_width = euclidean(landmarks[0], landmarks[16])
    au = {}

    au["AU4"] = euclidean(landmarks[21], landmarks[22]) / face_width
    au["AU5"] = (euclidean(landmarks[37], landmarks[41]) + euclidean(landmarks[43], landmarks[47])) / (2 * face_width)
    au["AU6"] = (euclidean(landmarks[36], landmarks[48]) + euclidean(landmarks[45], landmarks[54])) / (2 * face_width)
    au["AU7"] = (euclidean(landmarks[38], landmarks[40]) + euclidean(landmarks[44], landmarks[46])) / (2 * face_width)
    au["AU9"] = euclidean(landmarks[27], landmarks[33]) / face_width
    au["AU10"] = euclidean(landmarks[33], landmarks[51]) / face_width
    au["AU15"] = ((landmarks[48][1] + landmarks[54][1]) / 2 - landmarks[51][1]) / face_width
    au["AU17"] = euclidean(landmarks[57], landmarks[8]) / face_width
    au["AU23"] = euclidean(landmarks[48], landmarks[54]) / face_width
    au["AU24"] = euclidean(landmarks[62], landmarks[66]) / face_width
    au["AU31"] = euclidean(landmarks[5], landmarks[11]) / face_width
    au["AU42_44"] = (euclidean(landmarks[37], landmarks[41]) + euclidean(landmarks[43], landmarks[47])) / (2 * face_width)

    return au


# Baseline values (neutral)
NEUTRAL_BASELINE = {
    "AU4": 0.070, "AU5": 0.060, "AU6": 0.250, "AU7": 0.060,
    "AU9": 0.130, "AU10": 0.090, "AU15": 0.030, "AU17": 0.180,
    "AU23": 0.390, "AU24": 0.015, "AU31": 0.480, "AU42_44": 0.055
}


def compute_stress_score(au_values, baseline=NEUTRAL_BASELINE):
    """Compute stress score from Action Unit values"""
    deviations = {}
    weights = {
        "AU4": 0.15, "AU5": 0.10, "AU6": 0.05, "AU7": 0.15,
        "AU9": 0.05, "AU10": 0.05, "AU15": 0.05, "AU17": 0.10,
        "AU23": 0.15, "AU24": 0.05, "AU31": 0.05, "AU42_44": 0.05
    }

    total_weight = sum(weights.values())
    weighted_sum = 0

    for au, value in au_values.items():
        if au in baseline:
            base_val = baseline[au] if baseline[au] != 0 else 1e-6
            diff = abs(value - baseline[au]) / base_val
            deviations[au] = diff
            weighted_sum += diff * weights[au]

    normalized_score = min((weighted_sum / total_weight) * 10, 10)
    return round(normalized_score, 2), deviations


def interpret_stress_level(score):
    """Interpret stress level from score"""
    if score <= 2:
        return "Very Low Stress — Calm or relaxed facial state"
    elif score <= 4:
        return "Low Stress — Slight muscle activation (mild focus or alertness)"
    elif score <= 6:
        return "Moderate Stress — Noticeable brow or lip tension detected"
    elif score <= 8:
        return "High Stress — Strong facial tension across brow, eyes, and jaw"
    else:
        return "Very High Stress — Intense emotional arousal, possible strain or fatigue"


def decode_base64_image(base64_string):
    """Decode base64 image string to OpenCV image"""
    # Remove data URI prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64
    img_data = base64.b64decode(base64_string)
    img_array = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    return img


# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', model_loaded=model_loaded)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded or captured image"""
    if not model_loaded:
        return jsonify({
            'success': False,
            'error': 'Facial landmark model not loaded. Please ensure shape_predictor_68_face_landmarks.dat is in the application folder.'
        }), 500

    try:
        # Get image from request
        if 'image' in request.files:
            # File upload
            file = request.files['image']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400
            
            # Read image
            img_bytes = file.read()
            img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
        elif 'imageData' in request.json:
            # Base64 image data (from camera)
            base64_data = request.json['imageData']
            img = decode_base64_image(base64_data)
            
        else:
            return jsonify({'success': False, 'error': 'No image provided'}), 400

        if img is None:
            return jsonify({'success': False, 'error': 'Failed to decode image'}), 400

        # Get landmarks
        landmarks = get_landmarks_from_frame(img)
        if landmarks is None:
            return jsonify({
                'success': False,
                'error': 'No face detected in the image. Please ensure the face is clearly visible and front-facing.'
            }), 400

        # Compute AU metrics and stress score
        au_values = compute_au_metrics(landmarks)
        score, deviations = compute_stress_score(au_values)
        interpretation = interpret_stress_level(score)

        # Format AU values for display
        au_display = {au: round(value, 4) for au, value in au_values.items()}

        return jsonify({
            'success': True,
            'score': score,
            'interpretation': interpretation,
            'au_values': au_display
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded
    })


if __name__ == '__main__':
    # Check if model file exists
    if not os.path.exists(PREDICTOR_PATH):
        print("\n" + "="*70)
        print("WARNING: shape_predictor_68_face_landmarks.dat not found!")
        print("="*70)
        print("\nThe facial landmark model file is required for the application to work.")
        print("\nDownload it from:")
        print("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        print("\nExtract the .bz2 file and place the .dat file in the 'webapp' folder.")
        print("\nThe application will start but won't be able to analyze images.")
        print("="*70 + "\n")
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment variable (False in production)
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "="*70)
    print("STRESS ANALYZER WEB APPLICATION")
    print("="*70)
    print("\nStarting server...")
    print(f"\nAccess the application at: http://localhost:{port}")
    print(f"Environment: {'Development' if debug else 'Production'}")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)

