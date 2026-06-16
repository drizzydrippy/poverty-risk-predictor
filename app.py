
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Poverty Risk Predictor",
    page_icon="📊",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}
.metric-card {
    padding: 20px;
    border-radius: 15px;
    background: #1E1E1E;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD MODEL ----------
MODEL_PATH = "poverty_trap_model.pkl"

@st.cache_resource
def load_model():
    if not Path(MODEL_PATH).exists():
        st.error("Model file not found.")
        return None

    try:
        model = joblib.load(MODEL_PATH)
        return model

    except Exception as e:
        st.error(f"Model loading failed: {e}")
        st.info("Run rebuild_model.py to recreate the model using your current sklearn version.")
        return None

model = load_model()

# ---------- HEADER ----------
st.title("📊 Poverty Trap Risk Score Predictor")
st.markdown("Interactive AI-powered poverty risk prediction dashboard")

# ---------- SIDEBAR ----------
st.sidebar.header("User Information")

age = st.sidebar.slider("Age", 18, 70, 30)

education_num = st.sidebar.slider("Education Level (Years)", 1, 16, 10)

hours_per_week = st.sidebar.slider("Hours Worked Per Week", 1, 80, 40)

capital_gain = st.sidebar.number_input("Capital Gain", min_value=0, value=0)

occupation = st.sidebar.selectbox(
    "Occupation",
    [
        "Handlers-cleaners",
        "Other-service",
        "Priv-house-serv",
        "Farming-fishing",
        "Tech-support",
        "Sales",
        "Exec-managerial"
    ]
)

marital_status = st.sidebar.selectbox(
    "Marital Status",
    [
        "Never-married",
        "Separated",
        "Divorced",
        "Married-civ-spouse"
    ]
)

income = st.sidebar.selectbox(
    "Income Category",
    ["<=50K", ">50K"]
)

# ---------- FEATURE ENGINEERING ----------
low_education_risk = 1 if education_num <= 9 else 0
underemployment_risk = 1 if hours_per_week < 30 else 0
wealth_risk = 1 if capital_gain == 0 else 0

low_income_jobs = [
    "Handlers-cleaners",
    "Other-service",
    "Priv-house-serv",
    "Farming-fishing"
]

occupation_risk = 1 if occupation in low_income_jobs else 0

unstable_status = [
    "Never-married",
    "Separated",
    "Divorced"
]

family_instability_risk = 1 if marital_status in unstable_status else 0

# ---------- PREDICT ----------
if st.button("🚀 Predict Poverty Risk"):

    poverty_score = (
        low_education_risk * 20 +
        underemployment_risk * 20 +
        wealth_risk * 15 +
        occupation_risk * 20 +
        family_instability_risk * 10
    )

    if income == "<=50K":
        poverty_score += 35

    if poverty_score >= 70:
        risk = "High Risk"
        recommendation = "Needs urgent financial and employment support."

    elif poverty_score >= 40:
        risk = "Moderate Risk"
        recommendation = "Moderate support and skill development recommended."

    else:
        risk = "Low Risk"
        recommendation = "Financial condition appears relatively stable."

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Predicted Poverty Score", poverty_score)

    with col2:
        st.metric("Risk Category", risk)

    st.progress(min(poverty_score / 100, 1.0))

    st.success(recommendation)

    chart_data = pd.DataFrame({
        "Factor": [
            "Education",
            "Employment",
            "Wealth",
            "Occupation",
            "Family"
        ],
        "Risk Value": [
            low_education_risk * 20,
            underemployment_risk * 20,
            wealth_risk * 15,
            occupation_risk * 20,
            family_instability_risk * 10
        ]
    })

    st.subheader("📈 Risk Factor Contribution")
    st.bar_chart(chart_data.set_index("Factor"))

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Built using Streamlit + Machine Learning")
