# Stress Analyzer Web Application

A modern web-based interface for facial stress detection using advanced computer vision and the Facial Action Coding System (FACS).

## 🌟 Features

- **Web-Based Interface**: Access from any browser on your network
- **Image Upload**: Analyze photos with facial stress detection
- **Real-Time Camera Capture**: Use your webcam directly in the browser
- **Detailed Analysis**: Get stress scores (0-10 scale) with professional interpretations
- **Action Unit Metrics**: View detailed FACS Action Unit values
- **Modern UI**: Responsive, beautiful design that works on desktop and mobile
- **No Installation Required**: Just Python and a web browser

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Webcam (optional, for camera capture feature)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Python Packages
- Flask (web framework)
- OpenCV (computer vision)
- dlib (facial landmark detection)
- NumPy (numerical operations)
- Pillow (image processing)

## 🚀 Quick Start

### Method 1: Using the Batch File (Windows - Easiest)

1. Double-click `RUN_WEBAPP.bat`
2. Wait for the server to start
3. Open your browser to `http://localhost:5000`
4. Enjoy!

### Method 2: Manual Setup

1. **Navigate to the webapp directory:**
   ```bash
   cd webapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the facial landmark model:**
   - Download: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
   - Extract the `.bz2` file
   - Place `shape_predictor_68_face_landmarks.dat` in the `webapp` folder

4. **Run the application:**
   ```bash
   python app.py
   ```
   Or:
   ```bash
   python run.py
   ```

5. **Open your browser:**
   - Navigate to: `http://localhost:5000`
   - Or from another device on your network: `http://YOUR_IP:5000`

## 📁 Project Structure

```
webapp/
├── app.py                  # Flask backend application
├── run.py                  # Application runner script
├── requirements.txt        # Python dependencies
├── RUN_WEBAPP.bat         # Windows launcher script
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Application styling
│   └── js/
│       └── app.js         # Frontend JavaScript
├── uploads/               # Temporary upload folder (auto-created)
└── shape_predictor_68_face_landmarks.dat  # Model file (download separately)
```

## 🎯 How to Use

### Upload an Image
1. Click "Upload Image" button
2. Select a photo with a clear, front-facing face
3. Image will appear in the display area
4. Click "Analyze Current Image" to see results

### Capture from Camera
1. Click "Capture from Camera" button
2. Allow camera access when prompted
3. Position your face in the frame
4. Click "Take Photo" when ready
5. Click "Analyze Current Image" to see results

### Understanding Results
- **Stress Score**: 0-10 scale (0 = very low stress, 10 = very high stress)
- **Interpretation**: Professional description of stress level
- **Action Units**: Detailed facial muscle activation metrics

## 🔧 Configuration

### Change Port
Edit `app.py` (line ~280):
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to your desired port
```

### Enable/Disable Debug Mode
Edit `app.py` (line ~280):
```python
app.run(debug=False, host='0.0.0.0', port=5000)  # Set debug=False for production
```

### Change Max Upload Size
Edit `app.py` (line ~18):
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB (change as needed)
```

## 🌐 Network Access

### Access from Other Devices
1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`

2. On another device on the same network:
   - Open browser to: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

### Firewall Configuration
If you can't access from other devices:
- Windows: Allow Python through Windows Firewall
- Or temporarily disable firewall for testing

## 🛡️ Security Notes

### Development vs Production
- This app uses Flask's development server (good for local/testing)
- For production deployment, use a proper WSGI server:
  - Gunicorn (Linux/Mac)
  - Waitress (Windows)
  - uWSGI
  - Or deploy to cloud platforms (Heroku, AWS, Azure, etc.)

### Best Practices
- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Implement authentication if deployed publicly
- Validate and sanitize all inputs
- Monitor upload folder size
- Implement rate limiting for public deployments

## 📊 Technical Details

### How It Works
1. **Frontend**: HTML/CSS/JavaScript handles UI and camera access
2. **Image Capture**: JavaScript captures frames from webcam or file upload
3. **Backend**: Flask receives images and processes them
4. **Detection**: dlib detects faces and extracts 68 facial landmarks
5. **Analysis**: Custom algorithm computes Action Unit metrics
6. **Scoring**: Weighted calculation produces stress score (0-10)
7. **Results**: JSON response sent back to frontend for display

### Action Units (FACS)
The application uses the Facial Action Coding System:
- AU4: Brow lowerer
- AU5: Upper lid raiser
- AU6: Cheek raiser
- AU7: Lid tightener
- AU9: Nose wrinkler
- AU10: Upper lip raiser
- AU15: Lip corner depressor
- AU17: Chin raiser
- AU23: Lip tightener
- AU24: Lip pressor
- AU31: Jaw clencher
- AU42_44: Squint/blink

## 🐛 Troubleshooting

### Port Already in Use
```bash
Error: Address already in use
```
**Solution**: Change port in `app.py` or kill the process using port 5000

### Camera Not Working
**Solutions**:
- Ensure browser has camera permissions
- Use HTTPS for non-localhost access (browsers restrict camera on HTTP)
- Try a different browser (Chrome recommended)
- Check if another app is using the camera

### Model File Error
```
WARNING: shape_predictor_68_face_landmarks.dat not found!
```
**Solution**: Download and extract the model file (see Quick Start step 3)

### No Face Detected
**Solutions**:
- Ensure good lighting
- Face should be front-facing
- Move closer to camera
- Remove obstructions (sunglasses, masks)

### Installation Errors (dlib)
dlib can be tricky to install. If you get errors:

**Windows**:
```bash
pip install cmake
pip install dlib
```

**Mac (with Homebrew)**:
```bash
brew install cmake
pip install dlib
```

**Linux**:
```bash
sudo apt-get install cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

### Slow Analysis
- Large images take longer to process
- First analysis may be slower (model initialization)
- Consider resizing very large images before upload

## 🚀 Deployment Options

### Local Network (LAN)
- Already configured! Just use `http://YOUR_IP:5000`

### Cloud Deployment

**Heroku**:
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

**AWS / Azure / Google Cloud**:
- Package as Docker container
- Deploy to Elastic Beanstalk / App Service / App Engine

**Render / Railway / Vercel**:
- Connect GitHub repository
- Auto-deploy on push

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t stress-analyzer .
docker run -p 5000:5000 stress-analyzer
```

## 📝 API Endpoints

### `GET /`
Main application page

### `POST /analyze`
Analyze uploaded or captured image

**Request** (multipart/form-data):
```
image: <file>
```

**Request** (JSON):
```json
{
  "imageData": "data:image/jpeg;base64,..."
}
```

**Response**:
```json
{
  "success": true,
  "score": 4.25,
  "interpretation": "Low Stress — Slight muscle activation...",
  "au_values": {
    "AU4": 0.0823,
    "AU5": 0.0651,
    ...
  }
}
```

### `GET /health`
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🎨 Customization

### Modify UI Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #3498db;  /* Change to your color */
    --accent-color: #e74c3c;   /* Change to your color */
    ...
}
```

### Add New Features
- Extend `app.py` for new endpoints
- Modify `templates/index.html` for UI changes
- Update `static/js/app.js` for new interactions

## 📄 License

This project uses:
- Flask (BSD License)
- OpenCV (Apache 2.0)
- dlib (Boost Software License)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions:
- Check this README first
- Review troubleshooting section
- Check browser console for errors (F12)
- Check terminal/console for backend errors

## 🎉 Enjoy!

You now have a fully functional web-based stress analyzer. Use it responsibly and enjoy exploring facial stress detection!

---

**Built with ❤️ using Flask, OpenCV, and dlib**

*Last Updated: November 11, 2025*

