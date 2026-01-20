# SmartPredict Stock - Deployment Guide

## Deploy to Render (Free)

### Steps:

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Name: `smartpredict-stock`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Instance Type: `Free`
   - Click "Create Web Service"

4. **Wait for deployment** (5-10 minutes)
   - Render will automatically build and deploy
   - Your app will be live at: `https://smartpredict-stock.onrender.com`

### Important Notes:

- **Free tier limitations:**
  - App sleeps after 15 minutes of inactivity
  - First request after sleep takes 30-60 seconds to wake up
  - 750 hours/month free

- **Security:**
  - Never commit API keys or secrets
  - Use Render's Environment Variables for sensitive data

- **Performance:**
  - Free tier has limited CPU/RAM
  - Consider upgrading for production use

### Alternative Free Hosting:

1. **Railway** - https://railway.app (500 hours/month free)
2. **Fly.io** - https://fly.io (Free tier available)
3. **PythonAnywhere** - https://www.pythonanywhere.com (Limited free tier)

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000
