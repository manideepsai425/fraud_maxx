# 💳 Fraud Detection System

A machine learning-powered fraud detection app built with Streamlit and scikit-learn.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
cd backend
python train.py
```

Expected output:
- `model.pkl` - Trained LogisticRegression model
- `scaler.pkl` - StandardScaler for numerical features
- `label_encoders.pkl` - LabelEncoders for categorical features

### 3. Run the App
```bash
streamlit run backend/app.py
```

The app will open at `http://localhost:8501`

## Features

- **Real-time Fraud Detection**: Input transaction details to get instant fraud predictions
- **Risk Scoring**: Probability-based fraud risk assessment (0-100%)
- **Feature Importance**: View SHAP explanations for predictions (optional)

## Input Parameters

**Transaction Details:**
- Amount: Transaction value in dollars
- Type: ATM Withdrawal, Bank Transfer, Bill Payment, Online Purchase, POS Payment
- Time: 24-hour format (0-24)
- Device: Desktop, Mobile, Tablet, Unknown Device
- Location: US cities (Boston, Chicago, Houston, Los Angeles, Miami, New York, San Francisco, Seattle)
- Payment Method: Credit Card, Debit Card, Invalid Method, Net Banking, UPI

**Historical Data:**
- Previous Fraudulent Transactions: Count of prior fraud incidents
- Account Age: Days since account creation
- Transactions in Last 24H: Recent transaction activity

## Model Performance

- Accuracy: ~51% (baseline on imbalanced fraud dataset)
- Optimizer: Grid search with balanced class weights

## File Structure

```
fraud/
├── backend/
│   ├── app.py              # Streamlit web app
│   ├── train.py            # Model training script
│   ├── model.pkl           # Trained model (generated)
│   ├── scaler.pkl          # Feature scaler (generated)
│   └── label_encoders.pkl  # Categorical encoders (generated)
├── dataset/
│   └── Fraud.csv           # Training dataset (51,000 samples)
├── frontend/               # Optional: Frontend components
│   ├── index.html
│   ├── script.js
│   └── style.css
└── requirements.txt        # Python dependencies
```

## Troubleshooting

**Error: "Model or scaler not found"**
- Make sure you've run `python train.py` first

**Error: "SHAP is not installed"**
- The app works without SHAP but shows a warning
- Optional: `pip install shap` for feature explanations

**Error: "Unknown value for [field]"**
- Make sure the selected values match training data categories
- Check the dropdown options are from the valid list
