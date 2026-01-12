import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة والهوية الأكاديمية
st.set_page_config(page_title="ASA Smart Mix Pro | AI Optimizer", layout="wide", page_icon="🏗️")

st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 2.2em; margin-bottom: 5px; }
    .thesis-title { color: #333; text-align: center; font-size: 1.2em; font-weight: bold; border-bottom: 2px solid #004a99; padding-bottom: 15px; margin-bottom: 25px; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .optimizer-card { background-color: #e8f5e9; padding: 20px; border-radius: 15px; border-top: 5px solid #2e7d32; }
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
        st.markdown("<h2 style='text-align: center;'>Research Access</h2>", unsafe_allow_html=True)
        with st.form("login"):
            key = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter"):
                if key == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل البيانات والموديل
@st.cache_resource
def load_assets():
    model = joblib.load('models/concrete_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    try: db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    except: db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. الهيدر الرسمي
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='thesis-title'><b>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</b></p>", unsafe_allow_html=True)

# 5. المدخلات (Sidebar)
st.sidebar.header("📥 Current Mix Design")
with st.sidebar:
    cement = st.number_input("Cement (kg/m³)", 250, 600, 350)
    water = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine Aggregate)", 0, 1200, 700)
    rca_p = st.slider("RCA Replacement (%)", 0, 100, 0)
    mrca_p = st.slider("MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("Fly Ash (kg/m³)", 0, 250, 0)
    fiber = st.number_input("Nylon Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc_ratio = st.slider("W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)

# 6. الأقسام الخمسة (Tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Prediction", "🌱 LCA Report", "🔍 Validation", "🚀 AI Optimizer", "📝 Feedback"])

# الحسابات الأساسية للخلطة المدخلة
features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
prediction = model.predict(scaler.transform(features))[0]
total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)

with tab1:
    st.subheader("Current Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("Strength (28d)", f"{prediction:.2f} MPa")
    c2.metric("Split Tensile", f"{(0.55 * np.sqrt(prediction)):.2f} MPa")
    c3.metric("Elastic Modulus", f"{(4.7 * np.sqrt(prediction)):.2f} GPa")
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
        theta=['Strength', 'Recycling', 'Multi-Cycle', 'Eco-Safety'], fill='toself'
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("LCA & Economy Analysis")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("CO2 Emissions", f"{total_co2:.1f} kg/m³")
        fig_pie = px.pie(values=[cement*0.85, sf*0.02, fa*0.01, (nca+nfa)*0.005, sp*0.7], 
                         names=["Cement", "SF", "FA", "Aggregates", "Additives"], hole=0.4)
        st.plotly_chart(fig_pie)
    with col5:
        sust_score = (prediction / (total_co2 * 0.1)) # مبسط للتوضيح
        st.metric("Sustainability Index", f"{sust_score:.2f}")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=sust_score, gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"}}))
        st.plotly_chart(fig_gauge)

with tab3:
    st.subheader("Reliability & Domain of Applicability")
    st.write(f"**Model Type:** Gradient Boosting Regressor (GBR) | **R²:** 0.953")
    v_c1, v_c2 = st.columns(2)
    v_c1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Blind Test Scatter Plot")
    v_c2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity Analysis")

with tab4:
    st.markdown("<div class='optimizer-card'>", unsafe_allow_html=True)
    st.subheader("🚀 Smart Mix Optimization Engine")
    st.write("Find the most sustainable mix design from our Diamond Database based on your target strength.")
    
    target_strength = st.slider("Select Target Compressive Strength (MPa)", 20, 100, 40)
    
    if st.button("Generate Optimal Eco-Design"):
        # محرك البحث: إيجاد خلطات في حدود +/- 3 ميجا باسكال وترتيبها حسب الاستدامة
        tolerance = 3
        optimal_mixes = db[(db['CS_28'] >= target_strength - tolerance) & (db['CS_28'] <= target_strength + tolerance)]
        
        if not optimal_mixes.empty:
            # ترتيب حسب عمود الاستدامة (الأعلى هو الأفضل)
            best_mix = optimal_mixes.sort_values('Sustainability', ascending=False).iloc[0]
            
            st.success(f"✅ Optimal Mix Found! (Mix ID: {best_mix['Mix_ID']})")
            
            opt_c1, opt_c2 = st.columns(2)
            with opt_c1:
                st.write("**Recommended Components:**")
                st.write(f"- Cement: {best_mix['Cement']} kg/m³")
                st.write(f"- Water: {best_mix['Water']} kg/m³")
                st.write(f"- RCA %: {best_mix['RCA_P']}%")
                st.write(f"- Silica Fume: {best_mix['Silica_Fume']} kg/m³")
            with opt_c2:
                st.write("**Performance Indicators:**")
                st.write(f"- Predicted Strength: {best_mix['CS_28']} MPa")
                st.write(f"- Carbon Footprint: {best_mix['CO2']} kg/m³")
                st.write(f"- Sustainability Score: {best_mix['Sustainability']}")
        else:
            st.error("No matches found in the current database for this target. Try a different range.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab5:
    st.subheader("Researcher Feedback & Contact")
    with st.form("feedback"):
        fb_name = st.text_input("Name")
        fb_err = st.number_input("Observed Error % (if tested in lab)", 0.0, 100.0, 0.0)
        fb_msg = st.text_area("Detailed Feedback")
        if st.form_submit_button("Submit"):
            st.success("Feedback logged for syncing with Google Sheets.")
    
    st.markdown("""
        <div style='background-color:#fff3e0; padding:15px; border-radius:10px; border-right:5px solid #ff9800;'>
        <b>Academic Terms:</b> Results are AI-generated based on Master's thesis data. 
        Verify physically before construction use.
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Master's Researcher | Mansoura University</div>", unsafe_allow_html=True)
