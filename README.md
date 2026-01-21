# 🪙 SmartPredict Crypto

A cryptocurrency analysis and clustering web application built entirely through **vibe coding** - created without any prior web development experience or formal coding knowledge. This project demonstrates what's possible when you combine curiosity, AI assistance, and a willingness to learn by doing.

## 🎯 What This App Does

SmartPredict Crypto is a comprehensive cryptocurrency analysis tool that combines machine learning, time series analysis, and clustering algorithms to help users understand crypto market patterns and volatility.

### Core Features

#### 1. **Crypto Price Prediction**
- Predicts next 5 days of cryptocurrency price movements (UP/DOWN)
- Uses **ARIMA-GARCH** model for volatility forecasting
- Employs **Random Forest** classifier for direction prediction
- Calculates **Conditional Volatility (CV)** as the primary feature
- Supports major cryptocurrencies: BTC, ETH, BNB, XRP, ADA, SOL, DOGE, and more
- Real-time data from CoinLore API

#### 2. **Crypto Clustering Analysis**
- Groups cryptocurrencies based on volatility patterns using unsupervised learning
- Two clustering methods:
  - **DTW (Dynamic Time Warping)**: Captures time series shape similarity
  - **Euclidean Distance**: Standard point-to-point comparison
- Interactive **Elbow Plot** with automatic optimal K detection using Kneedle Algorithm
- Cluster evaluation metrics:
  - **Silhouette Score**: Measures cluster cohesion
  - **Davies-Bouldin Index**: Evaluates cluster separation
- PCA visualization for 2D cluster representation

#### 3. **Platform-Based Analysis**
- Analyze cryptocurrencies by blockchain platform:
  - **Ethereum** - ERC-20 tokens
  - **Binance Smart Chain** - BEP-20 tokens
  - **Solana** - SPL tokens
  - **Polygon** - MATIC ecosystem
  - **Avalanche** - AVAX ecosystem
  - **Arbitrum** - Layer 2 tokens
- Compare volatility patterns within the same ecosystem

#### 4. **Interactive Workflow**
- Multi-step clustering process:
  1. Select platform (Ethereum, BSC, Solana, etc.)
  2. Choose specific cryptos or entire platform
  3. Select clustering method (DTW/Euclidean)
  4. View elbow plot with auto-detected optimal K
  5. Analyze clustering results with visualizations

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

## 🧠 How It Works

### Prediction Pipeline
1. **Data Fetching**: Download historical crypto prices from CoinLore API
2. **Log Returns**: Calculate logarithmic returns for stationarity
3. **ARIMA Modeling**: Remove trend and seasonality from returns
4. **GARCH Modeling**: Extract conditional volatility from residuals
5. **Feature Engineering**: Create lag features, technical indicators
6. **Random Forest**: Train classifier on engineered features
7. **Prediction**: Forecast next 5 days with probability scores

### Clustering Pipeline
1. **Data Preparation**: Fetch crypto data for selected platform
2. **CV Calculation**: Compute conditional volatility for each crypto
3. **Normalization**: Z-score standardization across cryptos
4. **Elbow Analysis**: Test K=2 to K=9, calculate inertia
5. **Optimal K Detection**: Kneedle algorithm finds elbow point
6. **Clustering**: Apply DTW or Euclidean KMeans
7. **Evaluation**: Calculate Silhouette Score and Davies-Bouldin Index
8. **Visualization**: PCA reduction to 2D for plotting

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

### Conditional Volatility (CV)
Instead of using raw crypto prices, this app uses **Conditional Volatility** as the primary feature:
- More stable than prices
- Captures market uncertainty
- Better for clustering similar risk profiles
- Derived from GARCH(1,1) model

### Kneedle Algorithm
Automatic elbow detection using geometric approach:
- Normalizes data to [0,1] range
- Calculates perpendicular distance from baseline
- Finds point with maximum distance
- More reliable than derivative methods

### DTW Clustering
Dynamic Time Warping allows:
- Alignment of time series with different phases
- Shape-based similarity matching
- Robust to temporal shifts
- Better for financial time series than Euclidean

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
smartpredict_crypto/
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

### Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Deploy!

### Environment Variables
No environment variables required - the app uses public APIs.

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
