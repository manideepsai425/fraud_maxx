import os
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

try:
    import shap
    shap_available = True
except ImportError:
    shap_available = False

# ============================================================================
# PAGE CONFIGURATION - PREMIUM FINTECH STYLE
# ============================================================================
st.set_page_config(
    page_title="Fraud Detection | Premium AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ============================================================================
# IPHONE-STYLE GLASSMORPHISM UI
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Colors - Apple iPhone iOS */
    :root {
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --glass-hover: rgba(255, 255, 255, 0.15);
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --success-glow: #34C759;
        --danger-glow: #FF3B30;
        --warning-glow: #FF9500;
        --blur-amount: 15px;
    }
    
    /* Base Styles - Dark Theme */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        color: white;
    }
    
    /* Smooth Page Load Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    [data-testid="stAppViewContainer"] {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: white;
    }
    
    /* Premium Glass Card - iPhone Style */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--blur-amount));
        -webkit-backdrop-filter: blur(var(--blur-amount));
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: var(--glass-hover);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4),
                    inset 0 1px 1px rgba(255, 255, 255, 0.2);
        transform: translateY(-4px);
    }
    
    /* Header - Glowing Title */
    .premium-header {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 2.5rem 0;
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: white;
        text-shadow: 0 0 40px rgba(52, 199, 89, 0.3);
        animation: fadeIn 1s ease-out;
    }
    
    .premium-subheader {
        text-align: center;
        font-size: 1rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
        animation: fadeIn 1.2s ease-out;
    }
    
    /* Input Section Styling */
    .input-section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.2rem;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: 0.3px;
    }
    
    .input-section-icon {
        font-size: 1.4rem;
        opacity: 0.9;
    }
    
    /* Custom Input Styling - Glass Effect */
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] select,
    [data-testid="stSlider"] input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        color: white !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stNumberInput"] input::placeholder,
    [data-testid="stSelectbox"] select::placeholder {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stSelectbox"] select:focus,
    [data-testid="stSlider"] input:focus {
        border-color: var(--success-glow) !important;
        box-shadow: 0 0 0 3px rgba(52, 199, 89, 0.2),
                    inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Glowing Button - iPhone Style */
    .stButton > button {
        background: rgba(52, 199, 89, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 14px 32px;
        font-size: 0.95rem;
        font-weight: 600;
        color: white;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        min-height: 50px;
        box-shadow: 0 0 0 rgba(52, 199, 89, 0.5),
                    inset 0 1px 1px rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover {
        background: rgba(52, 199, 89, 1);
        box-shadow: 0 0 30px rgba(52, 199, 89, 0.6),
                    inset 0 1px 2px rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result Card - Safe (Green Glow) */
    .result-safe {
        background: rgba(52, 199, 89, 0.12);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(52, 199, 89, 0.5);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 0 50px rgba(52, 199, 89, 0.25),
                    inset 0 1px 1px rgba(255, 255, 255, 0.1);
        animation: glassSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Result Card - Fraud (Red Glow) */
    .result-fraud {
        background: rgba(255, 59, 48, 0.12);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(255, 59, 48, 0.5);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 0 50px rgba(255, 59, 48, 0.25),
                    inset 0 1px 1px rgba(255, 255, 255, 0.1);
        animation: glassSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes glassSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Badge Styling */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 0.75rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .badge-safe {
        background: rgba(52, 199, 89, 0.3);
        color: #34C759;
        box-shadow: 0 0 20px rgba(52, 199, 89, 0.3);
    }
    
    .badge-fraud {
        background: rgba(255, 59, 48, 0.3);
        color: #FF3B30;
        box-shadow: 0 0 20px rgba(255, 59, 48, 0.3);
    }
    
    /* Metric Cards - Glass */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        background: var(--glass-hover);
        transform: translateY(-6px);
        box-shadow: 0 12px 48px rgba(52, 199, 89, 0.2),
                    inset 0 1px 1px rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #34C759;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 0 20px rgba(52, 199, 89, 0.3);
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin-top: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    
    /* Animated Progress Bar - Glass */
    .progress-container {
        margin: 2rem 0;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: white;
    }
    
    .progress-bar {
        height: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #34C759 0%, #FF3B30 100%);
        border-radius: 10px;
        animation: glowFill 1.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(52, 199, 89, 0.5);
    }
    
    @keyframes glowFill {
        from { width: 0; filter: brightness(1.2); }
        to { width: inherit; filter: brightness(1); }
    }
    
    /* Divider - Subtle Gradient */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        margin: 2rem 0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.5) 0%, rgba(30, 41, 59, 0.5) 100%);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    
    .sidebar-title {
        font-size: 1rem;
        font-weight: 700;
        color: #34C759;
        margin-bottom: 0.75rem;
        text-shadow: 0 0 15px rgba(52, 199, 89, 0.3);
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin: 2.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.3px;
    }
    
    /* Info Box - Glass Alert */
    .info-box {
        background: rgba(52, 199, 89, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(52, 199, 89, 0.3);
        border-radius: 14px;
        padding: 1.2rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
        box-shadow: 0 0 30px rgba(52, 199, 89, 0.1),
                    inset 0 1px 1px rgba(255, 255, 255, 0.08);
    }
    
    /* Text Styling */
    .secondary-text {
        color: var(--text-secondary);
        font-weight: 400;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL & PREPROCESSORS
# ============================================================================
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "model.pkl")
scaler_path = os.path.join(base_dir, "scaler.pkl")
encoders_path = os.path.join(base_dir, "label_encoders.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(encoders_path, "rb") as f:
        label_encoders = pickle.load(f)
except FileNotFoundError as e:
    st.error(f"Error: Required file not found: {e}")
    st.info("Please ensure train.py has been executed in the backend directory.")
    st.stop()

# ============================================================================
# PREMIUM SIDEBAR - FINTECH STYLE
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class='sidebar-card'>
        <div class='sidebar-title'>About This Platform</div>
        <p class='secondary-text'>
        Advanced AI-powered fraud detection system using machine learning to protect transactions in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='sidebar-card'>
        <div class='sidebar-title'>Quick Guide</div>
        <p class='secondary-text'>
        <strong>1.</strong> Enter transaction details<br>
        <strong>2.</strong> Review all information<br>
        <strong>3.</strong> Click Predict button<br>
        <strong>4.</strong> Analyze results & confidence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Model Stats
    st.markdown("""
    <div class='sidebar-card'>
        <div class='sidebar-title'>Model Metrics (Random Forest)</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", "94.87%")
    with col2:
        st.metric("Precision", "33.33%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Recall", "1.36%")
    with col2:
        st.metric("F1 Score", "2.61%")
    
    st.metric("ROC AUC Score", "53.19%")
    st.metric("Training Size", "40,800 transactions")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class='sidebar-card'>
        <div class='sidebar-title'>Portfolio</div>
        <p class='secondary-text'>
        <strong>Built with:</strong> Streamlit, scikit-learn, SHAP<br><br>
        <strong>Model:</strong> Logistic Regression<br><br>
        <strong>Purpose:</strong> Real-time fraud detection
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PREMIUM HEADER
# ============================================================================
st.markdown("<div class='premium-header'>Fraud Detection AI</div>", unsafe_allow_html=True)
st.markdown("<div class='premium-subheader'>Advanced machine learning for transaction security</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================================
# INPUT SECTION - GLASSMORPHIC CARDS
# ============================================================================
st.markdown("<div class='section-header'>📋 Transaction Details</div>", unsafe_allow_html=True)

# Transaction Information
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='input-section-title'><span class='input-section-icon'>💰</span>Amount & Type</div>", unsafe_allow_html=True)
    
    transaction_amount = st.number_input(
        "Transaction Amount (USD)",
        value=100.0,
        min_value=0.0,
        max_value=100000.0,
        step=10.0,
        key="amount",
        label_visibility="collapsed"
    )
    
    transaction_type = st.selectbox(
        "Transaction Type",
        ["ATM Withdrawal", "Bank Transfer", "Bill Payment", "Online Purchase", "POS Payment"],
        key="type",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div class='input-section-title'><span class='input-section-icon'>⏰</span>Time & Device</div>", unsafe_allow_html=True)
    
    time_of_transaction = st.slider(
        "Transaction Time (24h format)",
        min_value=0.0,
        max_value=24.0,
        value=12.0,
        step=0.5,
        key="time",
        label_visibility="collapsed"
    )
    
    device_used = st.selectbox(
        "Device Used",
        ["Desktop", "Mobile", "Tablet", "Unknown Device"],
        key="device",
        label_visibility="collapsed"
    )

# Location & Payment
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='input-section-title'><span class='input-section-icon'>📍</span>Location</div>", unsafe_allow_html=True)
    
    location = st.selectbox(
        "Transaction City",
        ["Boston", "Chicago", "Houston", "Los Angeles", "Miami", "New York", "San Francisco", "Seattle"],
        key="location",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div class='input-section-title'><span class='input-section-icon'>💳</span>Payment Method</div>", unsafe_allow_html=True)
    
    payment_method = st.selectbox(
        "Payment Method",
        ["Credit Card", "Debit Card", "Invalid Method", "Net Banking", "UPI"],
        key="payment",
        label_visibility="collapsed"
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Account History
st.markdown("<div class='section-header'>📊 Account History</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    previous_fraud = st.number_input(
        "Previous Fraud Incidents",
        value=0,
        min_value=0,
        max_value=100,
        key="prev_fraud",
        label_visibility="collapsed"
    )

with col2:
    account_age = st.number_input(
        "Account Age (days)",
        value=365,
        min_value=0,
        max_value=10000,
        key="account_age",
        label_visibility="collapsed"
    )

with col3:
    transactions_24h = st.number_input(
        "Transactions (24h)",
        value=5,
        min_value=0,
        max_value=500,
        key="trans_24h",
        label_visibility="collapsed"
    )

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ============================================================================
# PREMIUM PREDICT BUTTON
# ============================================================================
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button(
        "ANALYZE TRANSACTION",
        use_container_width=True,
        type="primary",
        key="predict_btn"
    )

# ============================================================================
# RESULTS SECTION
# ============================================================================
if predict_button:
    # Loading animation
    with st.spinner("🔍 Analyzing transaction..."):
        import time
        time.sleep(0.5)  # Smooth animation
        
        # Prepare features
        features_dict = {
            'Transaction_Amount': transaction_amount,
            'Transaction_Type': transaction_type,
            'Time_of_Transaction': time_of_transaction,
            'Device_Used': device_used,
            'Location': location,
            'Previous_Fraudulent_Transactions': previous_fraud,
            'Account_Age': account_age,
            'Number_of_Transactions_Last_24H': transactions_24h,
            'Payment_Method': payment_method
        }

        features_df = pd.DataFrame([features_dict])

        # Encode
        categorical_cols = ['Transaction_Type', 'Device_Used', 'Location', 'Payment_Method']
        try:
            for col in categorical_cols:
                features_df[col] = label_encoders[col].transform(features_df[col])
        except ValueError as e:
            st.error(f"Invalid input: {str(e)}")
            st.stop()

        # Scale
        numerical_cols = ['Transaction_Amount', 'Time_of_Transaction', 'Previous_Fraudulent_Transactions', 
                          'Account_Age', 'Number_of_Transactions_Last_24H']
        features_df[numerical_cols] = scaler.transform(features_df[numerical_cols])

        # Reorder
        feature_order = ['Transaction_Amount', 'Transaction_Type', 'Time_of_Transaction', 'Device_Used', 'Location', 
                         'Previous_Fraudulent_Transactions', 'Account_Age', 'Number_of_Transactions_Last_24H', 'Payment_Method']
        features_df = features_df[feature_order]

        # Predict
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0][1]

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>🎯 Analysis Results</div>", unsafe_allow_html=True)

    # Result Card
    if prediction == 1:
        st.markdown(f"""
        <div class='result-fraud'>
            <h2 style='color: #FF3B30; margin: 0;'>FRAUD ALERT</h2>
            <div class='badge badge-fraud'>High Risk Transaction</div>
            <p style='margin-top: 1rem; color: white;'>This transaction shows patterns consistent with fraudulent activity</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='result-safe'>
            <h2 style='color: #34C759; margin: 0;'>TRANSACTION SAFE</h2>
            <div class='badge badge-safe'>Low Risk</div>
            <p style='margin-top: 1rem; color: white;'>This transaction appears to be legitimate</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>""" + ("FRAUD" if prediction == 1 else "SAFE") + """</div>
            <div class='metric-label'>Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{probability*100:.1f}%</div>
            <div class='metric-label'>Fraud Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{max(probability, 1-probability)*100:.1f}%</div>
            <div class='metric-label'>Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Animated Progress Bar
    risk_percentage = probability * 100
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-label'>
            <span>Fraud Risk Probability</span>
            <span style='color: #34C759; font-weight: 700;'>{risk_percentage:.1f}%</span>
        </div>
        <div class='progress-bar'>
            <div class='progress-fill' style='width: {risk_percentage}%'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Transaction Summary
    st.markdown("<div class='section-header'>📝 Transaction Summary</div>", unsafe_allow_html=True)
    
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.markdown(f"""
        <div class='glass-card'>
            <p><strong>Amount:</strong> <span style='color: #34C759;'>${transaction_amount:,.2f}</span></p>
            <p><strong>Type:</strong> {transaction_type}</p>
            <p><strong>Time:</strong> {int(time_of_transaction)}:00</p>
            <p><strong>Device:</strong> {device_used}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown(f"""
        <div class='glass-card'>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Payment:</strong> {payment_method}</p>
            <p><strong>Account Age:</strong> {account_age} days</p>
            <p><strong>Recent Transactions:</strong> {transactions_24h} in 24h</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # SHAP Explanation
    st.markdown("<div class='section-header'>🔬 Feature Importance</div>", unsafe_allow_html=True)

    if not shap_available:
        st.markdown("""
        <div class='info-box'>
        SHAP library not installed. Install with: <code>pip install shap</code> for ML interpretability analysis.
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            with st.spinner("Generating SHAP analysis..."):
                explainer = shap.Explainer(model, features_df)
                shap_values = explainer(features_df)
                
                fig, ax = plt.subplots(figsize=(12, 5))
                fig.patch.set_facecolor('none')
                ax.set_facecolor('#0a0e27')
                plt.tight_layout()
                shap.plots.waterfall(shap_values[0], show=False)
                st.pyplot(fig, use_container_width=True, transparent=True)
                
                st.markdown("""
                <div class='info-box'>
                <strong>How to read this chart:</strong> Each bar shows how features impact the prediction. Red increases fraud risk, blue decreases it.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.info(f"Could not generate SHAP explanation: {str(e)}")

    # Recommendation
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>💡 Recommendation</div>", unsafe_allow_html=True)
    
    if prediction == 1:
        st.markdown("""
        <div style='background: rgba(255, 59, 48, 0.15); backdrop-filter: blur(10px); border: 1px solid rgba(255, 59, 48, 0.3); border-radius: 16px; padding: 1.5rem; box-shadow: 0 0 30px rgba(255, 59, 48, 0.1);'>
        <strong style='color: #FF3B30;'>BLOCK TRANSACTION</strong> - Request additional verification from customer. Review recent activity patterns.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(52, 199, 89, 0.15); backdrop-filter: blur(10px); border: 1px solid rgba(52, 199, 89, 0.3); border-radius: 16px; padding: 1.5rem; box-shadow: 0 0 30px rgba(52, 199, 89, 0.1);'>
        <strong style='color: #34C759;'>APPROVE TRANSACTION</strong> - Process normally. Continue monitoring for pattern changes.
        </div>
        """, unsafe_allow_html=True)

