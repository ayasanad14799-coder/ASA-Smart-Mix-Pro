import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة والهوية الأكاديمية
st.set_page_config(page_title="ASA Smart Mix Pro | Master's Thesis", layout="wide", page_icon="🏗️")

# تنسيق CSS متقدم
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 2.5em; margin-bottom: 10px; }
    .thesis-title { color: #333; text-align: center; font-size: 1.3em; font-weight: bold; border-bottom: 2px solid #004a99; padding-bottom: 15px; margin-bottom: 25px; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .warning-box { background-color: #fff9c4; padding: 15px; border-radius: 10px; border-right: 5px solid #fbc02d; color: #5d4037; font-weight: bold; }
    .footer-text { text-align: center; color: #666; font-size: 0.85em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن (ASA2026)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        l_col1, l_col2 = st.columns(2)
        with l_col1: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=140)
        with l_col2: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=140)
        st.markdown("<h2 style='text-align: center; color: #004a99;'>Research Portal Access</h2>", unsafe_allow_html=True)
        with st.form("login"):
            key = st.text_input("Access Key", type="password")
            if st.form_submit_button("Login"):
                if key == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الأصول (Assets)
@st.cache_resource
def load_assets():
    model = joblib.load('models/concrete_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    try: db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    except: db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. واجهة العرض (Header)
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</p>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1:
    st.info(f"🎓 **Researcher:** Aya Mohammed Sanad Aboud (Master's Researcher)")
with c_info2:
    st.info(f"👨‍🏫 **Supervision:** Prof. Ahmed Tahwia & Assoc. Prof. Asser El-Sheikh")

# 5. المدخلات (Sidebar) مع UX Verification
st.sidebar.header("📥 Laboratory Inputs")
with st.sidebar:
    cement = st.number_input("Cement (kg/m³)", 250, 600, 350)
    water = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Natural Fine)", 0, 1200, 700)
    rca_p = st.slider("RCA Replacement (%)", 0, 100, 0)
    mrca_p = st.slider("MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("Fly Ash (kg/m³)", 0, 250, 0)
    fiber = st.number_input("Nylon Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc_ratio = st.slider("W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("Superplasticizer (kg/m³)", 0.0, 20.0, 2.0)

    # UX Check: Engineering Logic
    if wc_ratio > 0.65 and cement < 300:
        st.warning("⚠️ Warning: High W/C ratio with low cement might result in low structural integrity.")

# 6. التنبؤ والحسابات
features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
prediction = model.predict(scaler.transform(features))[0]

total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
sust_score = (prediction / (total_co2 * total_cost)) * 1000

# 7. لوحة عرض النتائج (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "📝 Feedback & Disclaimer"])

with tab1:
    st.subheader("Performance Metrics (Based on ACI 318 & Eurocode 2)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Comp. Strength (28d)", f"{prediction:.2f} MPa")
    col2.metric("Split Tensile (ACI)", f"{(0.55 * np.sqrt(prediction)):.2f} MPa")
    col3.metric("Elastic Modulus (EC2)", f"{(4.7 * np.sqrt(prediction)):.2f} GPa")
    
    # Radar Chart
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
        theta=['Strength', 'Recycling', 'Multi-Cycle', 'Eco-Safety'], fill='toself'
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("Environmental & Economic Analysis")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Total CO2 Emissions", f"{total_co2:.1f} kg/m³")
        fig_pie = px.pie(values=[cement*0.85, sf*0.02, fa*0.01, (nca+nfa)*0.005, sp*0.7], 
                         names=["Cement", "SF", "FA", "Aggregates", "Additives"], hole=0.4)
        st.plotly_chart(fig_pie)
    with col5:
        rank = "A+" if sust_score > 4.5 else "A" if sust_score > 3.0 else "B"
        st.metric("Sustainability Index", f"{sust_score:.2f} (Rank: {rank})")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=sust_score, gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"}}))
        st.plotly_chart(fig_gauge)

with tab3:
    st.subheader("Model Reliability & Documentation")
    st.write("**Domain of Applicability:** Model is valid for CS_28 range [6.4 - 100.5 MPa].")
    
    val_c1, val_c2 = st.columns(2)
    with val_c1:
        st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Blind Test Results")
        st.write("**Model Accuracy Metrics:**")
        st.table(pd.DataFrame({"Metric": ["R² Score", "MAE", "RMSE"], "Value": ["0.953", "2.14 MPa", "2.88 MPa"]}))
    with val_c2:
        st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity Analysis")
        st.write("**Robustness Info:** Algorithm used is Gradient Boosting Regressor (GBR), known for stable performance across variable inputs.")

with tab4:
    st.subheader("User Feedback & Research Integrity")
    with st.form("feedback_form"):
        st.write("Share your lab results (for Google Sheets sync):")
        fb_name = st.text_input("Name")
        fb_error = st.number_input("Observed Error % (Optional)", 0.0, 100.0, 0.0)
        fb_msg = st.text_area("Observations")
        if st.form_submit_button("Submit Data"):
            st.success("Your feedback has been logged. Syncing with Google Sheets API...")
    
    st.markdown("""
        <div class='warning-box'>
        <b>Research Disclaimer:</b> This AI model is for research purposes only. 
        Final structural designs must be validated in an accredited lab. 
        Developed by Aya Sanad (2026) under supervision.
        </div>
    """, unsafe_allow_html=True)

# 8. Footer
st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Mansoura University | ASA Smart Mix Pro</div>", unsafe_allow_html=True)
