# 🚀 Deployment Guide - Stress Analyzer Web Application

Complete guide for deploying your stress analyzer web application to production servers.

---

## 📦 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ All code in the `webapp` folder
- ✅ `.gitignore` file configured
- ✅ `requirements.txt` with all dependencies
- ✅ `Procfile` for Heroku/cloud platforms
- ✅ `runtime.txt` specifying Python version
- ✅ `env.example` for environment variables
- ✅ Model file hosted separately (if needed)

---

## 📁 What to Upload to GitHub

### Include in Repository:
```
webapp/
├── .gitignore              ✅ Include
├── app.py                  ✅ Include
├── run.py                  ✅ Include
├── requirements.txt        ✅ Include
├── Procfile               ✅ Include
├── runtime.txt            ✅ Include
├── env.example            ✅ Include
├── README.md              ✅ Include
├── DEPLOYMENT.md          ✅ Include
├── static/                ✅ Include
├── templates/             ✅ Include
└── uploads/.gitkeep       ✅ Include
```

### Exclude from Repository (in .gitignore):
```
❌ shape_predictor_68_face_landmarks.dat  (99 MB - too large)
❌ uploads/* (except .gitkeep)
❌ __pycache__/
❌ *.pyc
❌ .env (sensitive data)
❌ RUN_WEBAPP.bat (Windows-specific)
```

---

## 🔧 Step 1: Prepare for GitHub

### 1. Initialize Git (if not done)

```bash
cd webapp
git init
```

### 2. Create .env for Local Development

```bash
# Copy example file
cp env.example .env

# Edit .env with your values
# NEVER commit .env to GitHub!
```

### 3. Add Remote Repository

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/stress-analyzer-webapp.git
```

### 4. Commit and Push

```bash
# Add all files (respects .gitignore)
git add .

# Commit
git commit -m "Initial commit: Stress analyzer web application"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 📥 Handling the Large Model File

The `shape_predictor_68_face_landmarks.dat` file (99 MB) is too large for GitHub.

### Option 1: GitHub Releases (Recommended)

1. Create a release on GitHub
2. Upload the `.dat` file as a release asset
3. Update README with download link

### Option 2: External Hosting

Host the file on:
- **Google Drive**: Public link
- **Dropbox**: Public link
- **AWS S3**: Public bucket
- **Your server**: Direct download link

### Update README.md

Add this section:

```markdown
## 📥 Required: Download Model File

The facial landmark model is required but not included in the repository.

**Download:** [shape_predictor_68_face_landmarks.dat](YOUR_LINK_HERE)

Place the file in the project root directory.
```

---

## 🌐 Deployment Platforms

### Option 1: Heroku (Easy, Free Tier Available)

**Steps:**

1. **Create Heroku Account**
   - Sign up at https://heroku.com

2. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Login to Heroku**
   ```bash
   heroku login
   ```

4. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ```

6. **Add Buildpacks** (if needed for dlib)
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   ```

7. **Deploy**
   ```bash
   git push heroku main
   ```

8. **Upload Model File**
   - Use Heroku ephemeral filesystem or
   - Host on S3 and update PREDICTOR_PATH

9. **Open App**
   ```bash
   heroku open
   ```

**Note:** Heroku's free tier may have limitations with the 99 MB model file.

---

### Option 2: Render (Modern, Free Tier)

**Steps:**

1. **Sign up at** https://render.com

2. **New Web Service**
   - Connect your GitHub repository
   - Render auto-detects Python/Flask

3. **Configure**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

4. **Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-key>
   ```

5. **Deploy**
   - Render auto-deploys on push to main

**Model File Handling:**
- Upload via Render dashboard, or
- Host externally and set PREDICTOR_PATH

---

### Option 3: Railway (Simple Deployment)

**Steps:**

1. **Sign up at** https://railway.app

2. **New Project → Deploy from GitHub**
   - Select your repository

3. **Railway Auto-Configures**
   - Detects Python automatically
   - Uses Procfile

4. **Add Environment Variables**
   - In Railway dashboard settings

5. **Deploy**
   - Automatic deployment

---

### Option 4: DigitalOcean App Platform

**Steps:**

1. **Create App**
   - From GitHub repository

2. **Configure**
   - Type: Web Service
   - Build Command: Auto-detected
   - Run Command: `gunicorn app:app`

3. **Environment Variables**
   - Add in settings

4. **Deploy**
   - Automatic

---

### Option 5: AWS Elastic Beanstalk

**Steps:**

1. **Install AWS CLI and EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize**
   ```bash
   eb init -p python-3.10 stress-analyzer
   ```

3. **Create Environment**
   ```bash
   eb create stress-analyzer-env
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

5. **Set Environment Variables**
   ```bash
   eb setenv FLASK_ENV=production SECRET_KEY=your-key
   ```

---

### Option 6: Google Cloud App Engine

**Steps:**

1. **Create `app.yaml`**
   ```yaml
   runtime: python310
   entrypoint: gunicorn -b :$PORT app:app
   
   env_variables:
     FLASK_ENV: 'production'
     SECRET_KEY: 'your-secret-key'
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

---

### Option 7: Azure App Service

**Steps:**

1. **Create Web App**
   - Python 3.10 runtime

2. **Configure Deployment**
   - GitHub Actions or Azure DevOps

3. **Set Environment Variables**
   - In Configuration settings

4. **Deploy**
   - Push to GitHub (auto-deploy)

---

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Download model file (or mount as volume)
# RUN wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 \
#     && bunzip2 shape_predictor_68_face_landmarks.dat.bz2

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

### Build and Run

```bash
# Build image
docker build -t stress-analyzer .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  stress-analyzer
```

### Deploy to Docker Hub

```bash
docker tag stress-analyzer your-username/stress-analyzer
docker push your-username/stress-analyzer
```

---

## 🔐 Security Considerations

### 1. Environment Variables

**Never commit these to GitHub:**
- `SECRET_KEY`
- Database credentials
- API keys
- Passwords

### 2. Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Production Settings

```python
# In production:
FLASK_ENV=production
DEBUG=False
```

### 4. HTTPS

- Use HTTPS in production (most platforms provide free SSL)
- Update URLs to use `https://`

### 5. Rate Limiting

Consider adding Flask-Limiter:

```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    ...
```

---

## 📊 Performance Optimization

### 1. Gunicorn Workers

```bash
gunicorn --workers 4 --threads 2 app:app
```

### 2. File Upload Limits

Already configured in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 3. Caching (Optional)

Add Flask-Caching for better performance.

---

## 🔍 Monitoring & Logs

### Heroku Logs

```bash
heroku logs --tail
```

### Render Logs

- View in Render dashboard

### Docker Logs

```bash
docker logs <container-id>
```

---

## 🧪 Testing Before Deployment

### Local Testing

```bash
# Set production mode locally
export FLASK_ENV=production
python app.py
```

### Test Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Upload test
curl -X POST -F "image=@test_image.jpg" http://localhost:5000/analyze
```

---

## 📝 Post-Deployment Checklist

After deployment:

- ✅ Test `/` - main page loads
- ✅ Test `/health` - returns healthy status
- ✅ Test image upload
- ✅ Test camera capture (requires HTTPS)
- ✅ Check environment variables are set
- ✅ Verify model file is accessible
- ✅ Check logs for errors
- ✅ Test on mobile devices
- ✅ Verify HTTPS is working

---

## 🆘 Troubleshooting

### Model File Not Found

**Solution:**
1. Upload model file to server
2. Or host externally and update `PREDICTOR_PATH`

### Import Errors (dlib)

**Solution:**
```bash
# Install system dependencies first
apt-get install build-essential cmake libopenblas-dev
pip install dlib
```

### Port Already in Use

**Solution:**
- Platform assigns PORT automatically
- Use `PORT` environment variable

### 413 Request Entity Too Large

**Solution:**
- Increase `MAX_CONTENT_LENGTH` in `app.py`
- Configure server (nginx/apache) file upload limits

### Camera Not Working

**Solution:**
- Camera requires HTTPS (not HTTP)
- Ensure SSL certificate is configured

---

## 🎉 Success!

Your application is now deployed and accessible online!

**Next Steps:**
- Share the URL with users
- Monitor performance
- Collect feedback
- Scale as needed

---

## 📞 Support Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **Heroku Docs**: https://devcenter.heroku.com/
- **Gunicorn Docs**: https://docs.gunicorn.org/
- **Docker Docs**: https://docs.docker.com/

---

**Happy Deploying! 🚀**

© 2025 Stress Analyzer - Healthcare Technology

