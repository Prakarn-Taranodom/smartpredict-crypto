# SmartPredict Stock

A simple stock clustering web app built with vibe coding, created without prior web development experience

## Features

- Stock price prediction using ARIMA-GARCH and Random Forest
- Stock clustering analysis with DTW and Euclidean distance
- Interactive elbow plot for optimal cluster selection
- Conditional Volatility (CV) analysis
- Support for NASDAQ-100, SET-50, SET-100, S&P 500
- Cryptocurrency prediction support (BTC-USD, ETH-USD, etc.)

## Deploy to Render (Free)

### Steps:

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect this GitHub repository
   - Settings:
     - Name: `smartpredict-stock`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Instance Type: `Free`
   - Click "Create Web Service"

3. **Wait for deployment** (5-10 minutes)
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

## Tech Stack

- Flask (Web Framework)
- yfinance (Stock Data)
- scikit-learn (Machine Learning)
- tslearn (Time Series Clustering)
- ARIMA-GARCH (Volatility Modeling)
- Chart.js (Visualization)
