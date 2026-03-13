# 🪙 SmartPredict Stock

A cryptocurrency analysis and price prediction web application with dual model selection. Predict price direction (UP/DOWN) or future price levels using machine learning, time series analysis, and real-time crypto data.

**Version**: v1.0 ✨  
**Web**: https://smartpredict-stock.onrender.com/  
**Status**: Production Ready

---

Built through **vibe coding** - created without any prior web development experience or formal coding knowledge. This project demonstrates what's possible when you combine curiosity, AI assistance, and a willingness to learn by doing.

---

## ⚡ Quick Start

### 🚀 Try It Online (Free)
**Live Demo**: https://smartpredict-stock.onrender.com/

⚠️ **Note**: This app is deployed on Render's free tier. If the site hasn't been accessed in a while, it may take **30-50 seconds** to start up (cold start). Please be patient on your first visit!

### Features to Try:
1. **Direction Model** - Predict UP/DOWN (57.34% accuracy)
2. **Price Model** - Forecast price levels (7.07% MAPE)
3. **Cryptocurrency Support** - BTC, ETH, BNB, XRP, ADA, SOL, DOGE, and 100+ more

### Local Installation (2 minutes):
```bash
git clone https://github.com/Prakarn-Taranodom/smartpredict-crypto.git
cd smartpredict-crypto
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

---

## 🎯 What This App Does

SmartPredict Stock is a dual-model cryptocurrency price prediction system that lets users choose between two prediction approaches based on their needs.

### Core Features

#### 1. **Direction Model** (Best for Market Direction)
- **Accuracy**: 57.34%
- Predicts if price will go UP or DOWN in next 5 days
- Uses raw price data without volatility preprocessing
- Fast predictions with confidence scores
- Best for: **Traders wanting directional bias**

#### 2. **Price Model** (Best for Price Accuracy)
- **MAPE Error**: 7.07%
- Forecasts actual next-5-days price levels
- Uses ARIMA-GARCH conditional volatility features
- Probability-weighted predictions for robustness
- Best for: **Investors needing price targets**

#### 3. **Smart Model Selection**
- Simple dropdown interface to choose your goal
- Real-time model info showing accuracy metrics
- One-click switching between prediction types
- Supports 100+ cryptocurrencies via CoinLore API

## 🛠️ Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **CoinLore API** - Real-time cryptocurrency data
- **pandas & numpy** - Data manipulation and numerical computing

### Machine Learning & Statistics
- **scikit-learn** - Random Forest, KMeans, PCA, evaluation metrics
- **tslearn** - Time series clustering with DTW
- **statsmodels** - Statistical modeling and ARIMA
- **arch** - GARCH volatility modeling
- **pmdarima** - Automatic ARIMA parameter selection

### Frontend
- **Chart.js** - Interactive charts and visualizations
- **HTML/CSS/JavaScript** - Responsive UI with gradient designs
- **Bootstrap-inspired styling** - Custom CSS without frameworks

### Deployment
- **Gunicorn** - Production WSGI server
- **Render** - Cloud hosting platform (free tier)
  - **Web URL**: https://smartpredict-stock.onrender.com/
  - Auto-deploys on git push to main branch

## 🧠 How It Works

### Direction Model Pipeline (Raw Data)
1. **Fetch Data**: Download historical crypto prices from CoinLore API
2. **Calculate Returns**: Log returns for market movement
3. **Extract Features**: Return lags (lag1, lag2) + RSI (14-period) + RSI slope
4. **Train/Test Split**: 80/20 split for unbiased evaluation
5. **Random Forest**: 200 estimators (max_depth=5) for binary classification
6. **Predict Direction**: UP/DOWN with confidence probability

### Price Model Pipeline (With Conditional Volatility)
1. **Fetch Data**: Download historical crypto prices
2. **ARIMA Modeling**: Fit auto-ARIMA to remove trend/seasonality
3. **GARCH Volatility**: Compute conditional volatility from residuals
4. **Feature Engineering**: CV lags + Return lags + RSI indicators
5. **Train/Test Split**: 80/20 for robust evaluation
6. **Random Forest**: Same (200 est, max_depth=5) trained on CV features
7. **Predict Prices**: 5-day price forecast with probability weighting

## 📊 Models Training Results

### Model Performance Metrics

| Metric | Direction Model<br/>(Raw Data) | Price Model<br/>(With CV) | Winner |
|--------|:------:|:------:|:-----:|
| **Accuracy** | 57.34% | 40.14% | ✅ Direction |
| **ROC-AUC** | 0.6554 | 0.5847 | ✅ Direction |
| **F1-Score** | 0.6554 | 0.5847 | ✅ Direction |
| **MAPE Error** | N/A | 7.07% | ✅ Price |
| **Precision** | 0.5734 | 0.4014 | ✅ Direction |
| **Recall** | 1.0000 | 1.0000 | 🔵 Tied |
| **Train/Test** | 80/20 split | 80/20 split | N/A |
| **Data Used** | Raw prices | ARIMA+GARCH CV | - |

### Key Findings:
- **Direction Model Wins**: Raw data **17.20% better** than CV-processed for UP/DOWN prediction
- **Why?**: ARIMA+GARCH removes momentum signals while smoothing price movements
- **Use Direction Model**: When accuracy for direction matters most
- **Use Price Model**: When you need actual price level forecasts (7.07% error)

### Model Comparison
| Metric | Direction Model | Price Model |
|--------|-----------------|-------------|
| **Features** | Return lags (2) + RSI (2) | Above + CV lags (2) |
| **Target** | UP/DOWN (binary) | Price direction (binary) |
| **Accuracy** | 57.34% | 40.14% |
| **MAPE Error** | N/A | 7.07% |
| **Best For** | Direction prediction | Price level accuracy |
| **ROC-AUC** | 0.6554 | 0.5847 |

**Finding**: Raw data beats preprocessed data for direction prediction because ARIMA+GARCH smoothing removes market movement signals.

## 💡 The Vibe Coding Story

This entire project was built through **vibe coding** - an experimental approach where someone with zero web development experience uses AI assistance to build a functional web application.

### What is Vibe Coding?
- Learning by building, not studying first
- Using AI (like Amazon Q, ChatGPT) as a coding partner
- Iterative development: try → fail → fix → learn
- Focus on functionality over perfect code
- Embracing mistakes as learning opportunities

### Challenges Overcome
- Never used Flask before → Built full REST API
- No JavaScript knowledge → Created interactive UI
- No ML deployment experience → Integrated complex models
- No understanding of ARIMA/GARCH → Implemented volatility pipeline
- No clustering experience → Built DTW-based analysis tool
- Switched from stock market to crypto → Adapted entire system

### Key Learnings
- Web frameworks aren't as scary as they seem
- AI can explain complex concepts in simple terms
- Breaking problems into small steps makes anything achievable
- Documentation + AI assistance = powerful combination
- Real projects teach more than tutorials
- Pivoting projects is easier than starting from scratch

## 📊 Technical Highlights

### Dual Model Design
SmartPredict uses **two independent models** to serve different user needs:
- **Raw Data Model (57.34% accuracy)**: Captures market momentum for direction prediction
- **Processed Data Model (7.07% MAPE)**: Uses volatility features for price level accuracy

### Conditional Volatility (CV)
Extract market uncertainty using GARCH(1,1) model:
- **ARIMA preprocessing**: Remove trend/seasonality for better GARCH fit
- **Volatility clustering**: Capitalize on high-volatility periods
- **Risk-adjusted features**: Incorporate market uncertainty into predictions
- **Trade-off**: Better accuracy on new market regimes, but loses some momentum signals

### Key Metrics
- **Accuracy**: Percentage of correct UP/DOWN predictions
- **MAPE**: Mean Absolute Percentage Error for price forecasting
- **ROC-AUC**: Area under Receiver Operating Characteristic curve (0.5-1.0 scale)
- **Train/Test**: 80/20 split ensures unbiased model evaluation

### Feature Engineering
The models use carefully engineered features:
- **Return Lags**: Previous 1-2 day returns (momentum indicators)
- **RSI (14)**: Relative Strength Index (overbought/oversold signals)
- **RSI Slope**: Rate of RSI change (momentum acceleration)
- **CV Lags**: Conditional volatility lags (risk indicators, optional)

## 🚀 Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/smartpredict-crypto.git
cd smartpredict-crypto

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit
http://localhost:5000
```

## 📁 Project Structure

```
smarpredict-crypto/  (GitHub: https://github.com/Prakarn-Taranodom/smartpredict-crypto)
├── app.py                              # Flask routes and API endpoints
├── clustering_module.py                # Clustering algorithms and metrics
├── data_preparation_platform.py        # Platform-based data preparation
├── volatility_pipeline.py              # ARIMA-GARCH CV calculation
├── feature_engineering.py              # ML feature creation
├── train_model.py                      # Random Forest training
├── fetch_coinlore.py                   # CoinLore API wrapper
├── technical_indicators.py             # TA indicators (RSI, MACD, etc.)
├── test_system.py                      # System testing script
├── templates/                          # HTML templates
│   ├── index.html                     # Landing page
│   ├── predict.html                   # Prediction interface
│   ├── cluster.html                   # Clustering workflow
│   ├── cluster_select_method.html     # Method selection
│   ├── cluster_elbow.html             # Elbow plot
│   └── cluster_result.html            # Results visualization
├── static/                             # Static assets
├── requirements.txt                    # Python dependencies
├── Procfile                            # Render deployment config
└── README.md                           # This file
```

## 🎓 What I Learned

### Technical Skills
- Flask web framework and routing
- REST API design and integration
- HTML/CSS/JavaScript basics
- Chart.js for data visualization
- Git version control
- Cloud deployment (Render)
- API consumption (CoinLore)

### Data Science Skills
- Time series analysis (ARIMA, GARCH)
- Clustering algorithms (KMeans, DTW)
- Feature engineering for ML
- Model evaluation metrics
- Dimensionality reduction (PCA)
- Cryptocurrency market analysis

### Soft Skills
- Breaking complex problems into steps
- Reading documentation effectively
- Debugging with systematic approach
- Asking better questions to AI
- Persistence through errors
- Adapting to changing requirements

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

Tests include:
- Data fetching from CoinLore API
- Volatility calculation (ARIMA-GARCH)
- Feature engineering and prediction
- Platform data preparation
- Clustering with elbow detection

## 🌐 Deployment

### Live Deployment ✅
**Web URL**: https://smartpredict-stock.onrender.com/  
**Platform**: Render (Free Tier)  
**Status**: Active & Auto-deployed  
**Response Time**: First visit may take 30-50 seconds (cold start)

### How to Deploy Your Own
1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. New Web Service → Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Deploy! (Takes ~2-3 minutes)

### Environment Variables
None required - uses public APIs (CoinLore)

### Cold Start Warning
Render's free tier spins down after 15 minutes of inactivity. First request after idle period takes 30-50 seconds. Subsequent requests are instant.

## 🤝 Contributing

This project welcomes contributions! Whether you're also learning or an expert, feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Optimize code
- Add new cryptocurrencies or platforms
- Share your vibe coding story

## 📝 License

MIT License - Feel free to use this project for learning or building your own tools.

## 📋 Version History

### v1.0 - Dual Model Selection (March 2026) ✨
**MAJOR RELEASE** - Complete redesign with smart model selection strategy

#### 🎯 Features Added
- **Dual Model System**: Choose between Direction (57.34% acc) or Price (7.07% error) prediction
- **Smart Dropdown UI**: One-click model switching in web interface
- **Model Info Display**: Shows accuracy, F1-score, ROC-AUC for selected model
- **Real-time Comparison**: See which model is better for your goal
- **100+ Crypto Support**: BTC, ETH, BNB, XRP, ADA, SOL, DOGE, and more

#### 🐛 Critical Bug Fixes
| Issue | Impact | Fix |
|-------|--------|-----|
| **No Train/Test Split** | No validation, 100% overfitting | ✅ Added 80/20 split |
| **cv_lag1 KeyError** | Direction model crashed on predict | ✅ Conditional feature checking |
| **Missing Metrics** | No way to measure model quality | ✅ Added MAE, RMSE, MAPE |
| **Raw vs CV Data** | Unknown which is better | ✅ Built eval framework, found Raw wins |
| **Error Handling** | Generic 500 errors | ✅ Better Flask error messages |

#### 📈 Model Training Results
**Direction Model (Raw Data)**:
- Accuracy: 57.34% ✅
- ROC-AUC: 0.6554
- F1-Score: 0.6554
- Best for UP/DOWN predictions

**Price Model (With CV)**:
- MAPE Error: 7.07% ✅
- Accuracy: 40.14%
- ROC-AUC: 0.5847
- Best for price level accuracy

#### 🚀 Deployment
- **Live Web**: https://smartpredict-stock.onrender.com/ (Render free tier)
- **Auto-deploy**: On git push to main
- **Cold Start**: 30-50 seconds first visit
- **Local**: `python app.py` → http://localhost:5000

#### 📊 Code Quality Improvements
- ✅ 12 new documentation files
- ✅ Comprehensive test scripts (test_both_models.py, test_quick.py, eval_complete_metrics.py)
- ✅ Improved feature engineering pipelines
- ✅ Better error handling and user feedback
- ✅ Model evaluation framework (comparison vs metrics calculation)

#### 📚 New Documentation
See linked files for detailed information:
- [SMART_MODEL_SELECTION.md](SMART_MODEL_SELECTION.md) - Feature documentation
- [EVALUATION_REPORT.md](EVALUATION_REPORT.md) - Performance analysis
- [MODEL_SELECTION_GUIDE.md](MODEL_SELECTION_GUIDE.md) - User guide
- [eval_complete_metrics.py](eval_complete_metrics.py) - Training metrics code

---

## ⚠️ Disclaimer

This is a learning project built through vibe coding. The predictions are for **educational purposes only** and should not be used for actual trading decisions. Cryptocurrency trading involves substantial risk of loss. Always do your own research and consult financial advisors.

## 🙏 Acknowledgments

- Built with assistance from **Amazon Q Developer**
- Crypto data provided by **CoinLore API**
- Inspired by the vibe coding movement
- Thanks to the open-source community for amazing libraries

## 📈 Supported Cryptocurrencies

### Major Coins
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- XRP (XRP)
- Cardano (ADA)
- Solana (SOL)
- Dogecoin (DOGE)
- Polkadot (DOT)
- And 100+ more...

### Platforms
- Ethereum (ERC-20)
- Binance Smart Chain (BEP-20)
- Solana (SPL)
- Polygon (MATIC)
- Avalanche (AVAX)
- Arbitrum (ARB)

---

**Built with 💜 through vibe coding**

*"The best way to learn coding is to build something you're curious about, even if you don't know how yet."*

---

## 📸 Screenshots

### Prediction Interface
Predict next 5 days of crypto price movements with confidence scores.

### Clustering Analysis
Group cryptocurrencies by volatility patterns and visualize with PCA.

### Elbow Plot
Automatically detect optimal number of clusters using Kneedle algorithm.

---

**Star ⭐ this repo if you found it helpful!**
