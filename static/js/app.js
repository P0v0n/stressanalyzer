// Stress Analyzer Web Application - Frontend JavaScript

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const cameraBtn = document.getElementById('cameraBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const takePhotoBtn = document.getElementById('takePhotoBtn');
const cancelCameraBtn = document.getElementById('cancelCameraBtn');

const placeholder = document.getElementById('placeholder');
const previewImage = document.getElementById('previewImage');
const cameraVideo = document.getElementById('cameraVideo');
const captureCanvas = document.getElementById('captureCanvas');
const cameraControls = document.getElementById('cameraControls');

const scoreValue = document.getElementById('scoreValue');
const progressBar = document.getElementById('progressBar');
const interpretationText = document.getElementById('interpretationText');
const auList = document.getElementById('auList');
const loadingOverlay = document.getElementById('loadingOverlay');

// State
let currentImageData = null;
let cameraStream = null;
let isCameraMode = false;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Stress Analyzer initialized');
    
    // Setup event listeners
    fileInput.addEventListener('change', handleFileSelect);
    cameraBtn.addEventListener('click', startCamera);
    takePhotoBtn.addEventListener('click', capturePhoto);
    cancelCameraBtn.addEventListener('click', stopCamera);
    analyzeBtn.addEventListener('click', analyzeImage);
});

// Handle file upload
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return;
    }

    // Read and display image
    const reader = new FileReader();
    reader.onload = function(e) {
        displayImage(e.target.result);
        currentImageData = file;
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);

    // Stop camera if active
    if (cameraStream) {
        stopCamera();
    }
}

// Display image
function displayImage(imageSrc) {
    placeholder.style.display = 'none';
    cameraVideo.style.display = 'none';
    previewImage.src = imageSrc;
    previewImage.style.display = 'block';
    isCameraMode = false;
}

// Start camera
async function startCamera() {
    try {
        // Request camera access
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });

        cameraStream = stream;
        cameraVideo.srcObject = stream;
        
        // Show camera video
        placeholder.style.display = 'none';
        previewImage.style.display = 'none';
        cameraVideo.style.display = 'block';
        cameraControls.style.display = 'flex';
        
        isCameraMode = true;
        analyzeBtn.disabled = true;

    } catch (error) {
        console.error('Camera access error:', error);
        showError('Unable to access camera. Please ensure camera permissions are granted.');
    }
}

// Capture photo from camera
function capturePhoto() {
    if (!cameraStream) return;

    // Set canvas size to video size
    captureCanvas.width = cameraVideo.videoWidth;
    captureCanvas.height = cameraVideo.videoHeight;

    // Draw current video frame to canvas
    const ctx = captureCanvas.getContext('2d');
    ctx.drawImage(cameraVideo, 0, 0);

    // Get image data
    const imageDataUrl = captureCanvas.toDataURL('image/jpeg', 0.95);
    
    // Display captured image
    displayImage(imageDataUrl);
    currentImageData = imageDataUrl;
    analyzeBtn.disabled = false;

    // Stop camera
    stopCamera();
}

// Stop camera
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    cameraVideo.style.display = 'none';
    cameraControls.style.display = 'none';
    isCameraMode = false;
}

// Analyze image
async function analyzeImage() {
    if (!currentImageData) {
        showError('No image to analyze');
        return;
    }

    // Show loading overlay
    loadingOverlay.style.display = 'flex';
    analyzeBtn.disabled = true;

    try {
        let response;

        if (typeof currentImageData === 'string') {
            // Base64 image data (from camera)
            response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    imageData: currentImageData
                })
            });
        } else {
            // File upload
            const formData = new FormData();
            formData.append('image', currentImageData);

            response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
        }

        const result = await response.json();

        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || 'Analysis failed');
        }

    } catch (error) {
        console.error('Analysis error:', error);
        showError('Error analyzing image. Please try again.');
    } finally {
        loadingOverlay.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

// Display analysis results
function displayResults(result) {
    // Update score
    scoreValue.textContent = result.score.toFixed(1);
    
    // Update progress bar
    const scorePercent = (result.score / 10) * 100;
    progressBar.style.width = scorePercent + '%';
    
    // Update interpretation
    interpretationText.textContent = result.interpretation;
    
    // Update Action Units
    auList.innerHTML = '';
    for (const [au, value] of Object.entries(result.au_values)) {
        const auItem = document.createElement('div');
        auItem.className = 'au-item';
        auItem.innerHTML = `
            <span class="au-name">${au}</span>
            <span class="au-value">${value.toFixed(4)}</span>
        `;
        auList.appendChild(auItem);
    }

    // Animate results
    scoreValue.style.animation = 'none';
    setTimeout(() => {
        scoreValue.style.animation = 'fadeIn 0.5s ease';
    }, 10);
}

// Show error message
function showError(message) {
    alert('Error: ' + message);
    console.error(message);
}

// Utility: Convert data URL to blob
function dataURLtoBlob(dataURL) {
    const arr = dataURL.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (cameraStream) {
        stopCamera();
    }
});

// Handle window resize for responsive design
window.addEventListener('resize', function() {
    if (cameraStream && cameraVideo.style.display === 'block') {
        // Adjust camera video size if needed
        console.log('Window resized');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Space to analyze
    if (e.code === 'Space' && !analyzeBtn.disabled && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        analyzeImage();
    }
    
    // Escape to stop camera
    if (e.code === 'Escape' && cameraStream) {
        stopCamera();
    }
});

console.log('✅ Stress Analyzer frontend loaded successfully');

