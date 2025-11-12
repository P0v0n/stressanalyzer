# 🚀 Quick Guide: Deploy to GitHub

Simple step-by-step guide to upload your stress analyzer to GitHub and deploy it.

---

## 📁 Step 1: What's Included

Your `webapp` folder is now **deployment-ready** with these files:

```
webapp/
├── .gitignore              ✅ Excludes unnecessary files
├── app.py                  ✅ Production-ready Flask app
├── requirements.txt        ✅ With gunicorn & python-dotenv
├── Procfile               ✅ For Heroku/cloud deployment
├── runtime.txt            ✅ Python 3.10.5
├── env.example            ✅ Environment variable template
├── DEPLOYMENT.md          ✅ Full deployment guide
├── README.md              ✅ Documentation
├── static/                ✅ CSS & JavaScript
├── templates/             ✅ HTML files
└── uploads/.gitkeep       ✅ Keeps uploads folder in git
```

---

## 🚀 Step 2: Upload to GitHub

### Option A: Using Git Command Line

```bash
# 1. Navigate to webapp folder
cd C:\Users\PAWAN\Downloads\fer\webapp

# 2. Initialize git (if not already)
git init

# 3. Add all files (respects .gitignore)
git add .

# 4. Commit
git commit -m "Initial commit: Healthcare stress analyzer web app"

# 5. Create repository on GitHub
# Go to https://github.com/new
# Create a new repository (e.g., "stress-analyzer-webapp")

# 6. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/stress-analyzer-webapp.git

# 7. Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. File → Add Local Repository
3. Select the `webapp` folder
4. Commit changes
5. Publish repository to GitHub

---

## 📥 Step 3: Handle the Model File

The `shape_predictor_68_face_landmarks.dat` file (99 MB) is **automatically excluded** by `.gitignore`.

### Host it separately:

#### Option 1: GitHub Releases
1. Go to your GitHub repo
2. Click "Releases" → "Create a new release"
3. Upload `shape_predictor_68_face_landmarks.dat` as an asset
4. Get the download URL

#### Option 2: Google Drive
1. Upload the file to Google Drive
2. Make it publicly accessible
3. Get the direct download link

#### Option 3: Dropbox
1. Upload to Dropbox
2. Share and get public link

### Update README

Add this to your README.md:

```markdown
## 📥 Download Required Model File

Download the facial landmark model (99 MB):
- **Link**: [YOUR_LINK_HERE]
- **File**: `shape_predictor_68_face_landmarks.dat`
- **Place in**: Project root directory

Or download from official source:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
```

---

## 🌐 Step 4: Deploy to Cloud

Your app is ready to deploy to:

### Quick Deploy Options:

#### 🟣 Heroku (Easiest)

```bash
# Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku main

# Open app
heroku open
```

#### 🟢 Render (Modern)

1. Go to https://render.com
2. New → Web Service
3. Connect your GitHub repo
4. Render auto-configures everything
5. Add environment variables in dashboard
6. Deploy!

#### 🔵 Railway (Simple)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables
5. Deploy automatically!

---

## 🔐 Step 5: Configure Environment Variables

For any platform, set these:

```bash
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ Verification

After deployment, test these:

1. **Main page**: `https://your-app.com/`
2. **Health check**: `https://your-app.com/health`
3. **Upload image** and analyze
4. **Camera capture** (requires HTTPS)

---

## 📝 Files Explained

### `.gitignore`
- Excludes large files (model)
- Excludes temporary files
- Excludes sensitive data (.env)

### `Procfile`
```
web: gunicorn app:app
```
Tells Heroku/Render how to run your app.

### `runtime.txt`
```
python-3.10.5
```
Specifies Python version.

### `requirements.txt`
Updated with:
- `gunicorn` - Production server
- `python-dotenv` - Environment variables

### `app.py`
Updated with:
- Environment variable support
- Production-ready configuration
- PORT handling for cloud platforms

### `env.example`
Template for environment variables.
Copy to `.env` for local development.

---

## 🎯 What's Excluded from GitHub

Thanks to `.gitignore`, these won't be uploaded:

- ❌ `shape_predictor_68_face_landmarks.dat` (99 MB)
- ❌ `uploads/` folder contents
- ❌ `__pycache__/` and `.pyc` files
- ❌ `.env` file (sensitive)
- ❌ `RUN_WEBAPP.bat` (Windows-specific)

---

## 🆘 Common Issues

### Issue: "Repository too large"
**Solution**: Model file is excluded. If you see this, run:
```bash
git rm --cached shape_predictor_68_face_landmarks.dat
git commit -m "Remove large model file"
```

### Issue: "Module not found" on deployment
**Solution**: Ensure `requirements.txt` is complete:
```bash
pip freeze > requirements.txt
```

### Issue: "Application error" on Heroku
**Solution**: Check logs:
```bash
heroku logs --tail
```

---

## 🎉 You're Ready!

Your stress analyzer is now:
- ✅ On GitHub (version controlled)
- ✅ Deployment-ready (Procfile, runtime.txt)
- ✅ Production-configured (environment variables)
- ✅ Properly structured (.gitignore)
- ✅ Documented (README, DEPLOYMENT.md)

---

## 📚 Next Steps

1. **Push to GitHub** (Step 2)
2. **Host model file** (Step 3)
3. **Choose platform** (Step 4)
4. **Deploy** (5 minutes!)
5. **Share your app** 🎊

---

## 📖 Detailed Documentation

For comprehensive deployment instructions, see:
- **DEPLOYMENT.md** - Full deployment guide
- **README.md** - Application documentation
- **QUICK_START.txt** - Local development guide

---

**Need help?** Check DEPLOYMENT.md for platform-specific instructions!

Happy deploying! 🚀

© 2025 Stress Analyzer - Healthcare Technology

