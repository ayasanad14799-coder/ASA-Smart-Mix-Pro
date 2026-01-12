import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة والهوية الأكاديمية الرسمية
st.set_page_config(page_title="ASA Smart Mix Pro | Master's Thesis", layout="wide", page_icon="🏗️")

# تنسيق CSS احترافي (الهوية الأكاديمية لجامعة المنصورة)
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .header-container { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 2px solid #004a99; text-align: center; margin-bottom: 25px; }
    .doc-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-right: 6px solid #004a99; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .legend-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 15px; font-size: 0.9em; }
    .footer-text { text-align: center; color: #666; font-size: 0.85em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن (ASA2026) وشعارات الكلية
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        l_col1, l_col2 = st.columns(2)
        with l_col1:
            # رابط لوجو الجامعة من مجلد docs
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=140)
        with l_col2:
            # رابط لوجو الكلية من مجلد docs
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=140)
        
        st.markdown("<h2 style='text-align: center; color: #004a99;'>ASA-Smart-Mix Pro: Research Portal</h2>", unsafe_allow_html=True)
        with st.form("login_gate"):
            access_key = st.text_input("Enter Access Key", type="password")
            if st.form_submit_button("Access System"):
                if access_key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Access Denied. Unauthorized entry.")
    st.stop()

# 3. تحميل الموديل والبيانات (المسارات الاحترافية الجديدة)
@st.cache_resource
def load_assets():
    model = joblib.load('models/concrete_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    try:
        db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    except:
        db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. واجهة العرض الرئيسية والهوية البحثية
st.markdown("""
    <div class='header-container'>
        <h1 style='color: #004a99;'>ASA Smart Mix Pro v2.0</h1>
        <p style='font-style: italic; font-size: 1.1em;'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</p>
    </div>
    """, unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1:
    st.markdown(f"""<div class='doc-card'><b>🎓 Master's Researcher:</b><br>Aya Mohammed Sanad Aboud<br>Construction Engineering Dept.</div>""", unsafe_allow_html=True)
with c_info2:
    st.markdown(f"""<div class='doc-card'><b>👨‍🏫 Under the Supervision of:</b><br>Prof. Ahmed Tahwia<br>Assoc. prof. Asser El-Sheikh</div>""", unsafe_allow_html=True)

# 5. المدخلات الـ 11 (Sidebar)
st.sidebar.header("📥 Experimental Design Inputs")
with st.sidebar:
    st.markdown("<div class='legend-box'><b>Note:</b> Accurate inputs ensure 95.3% prediction reliability.</div>", unsafe_allow_html=True)
    cement = st.number_input("1. Cement (kg/m³)", 200, 600, 350)
    water = st.number_input("2. Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("3. NCA (Natural Coarse Agg.)", 0, 1500, 1100)
    nfa = st.number_input("4. NFA (Natural Fine Agg.)", 0, 1200, 700)
    rca_p = st.slider("5. RCA Replacement (%)", 0, 100, 0)
    mrca_p = st.slider("6. MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("7. Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("8. Fly Ash (kg/m³)", 0, 250, 0)
    fiber = st.number_input("9. Nylon Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc_ratio = st.slider("10. W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("11. Superplasticizer (kg/m³)", 0.0, 20.0, 2.0)

# 6. التنبؤ والحسابات
features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
prediction = model.predict(scaler.transform(features))[0]

total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
sust_score = (prediction / (total_co2 * total_cost)) * 1000

# 7. الأقسام الأربعة (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["Mechanical Performance", "Eco-Environmental LCA", "Model Reliability", "Feedback & Ethics"])

with tab1:
    st.subheader("📊 Predicted Mechanical Output")
    col1, col2, col3 = st.columns(3)
    col1.metric("Compressive Strength", f"{prediction:.2f} MPa")
    col2.metric("Est. Split Tensile", f"{(0.55 * np.sqrt(prediction)):.2f} MPa")
    col3.metric("Est. Elastic Modulus", f"{(4.7 * np.sqrt(prediction)):.2f} GPa")
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
        theta=['Strength', 'Recycling', 'Multi-Cycle', 'CO2 Saving'], fill='toself'
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("🌱 Sustainability & Economic Analysis")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Total CO2 Footprint", f"{total_co2:.1f} kg/m³")
        fig_pie = px.pie(values=[cement*0.85, sf*0.02, fa*0.01, (nca+nfa)*0.005, sp*0.7], 
                         names=["Cement", "Silica Fume", "Fly Ash", "Aggregates", "Additives"], hole=0.4)
        st.plotly_chart(fig_pie)
    with col5:
        rank = "A+" if sust_score > 4.5 else ("A" if sust_score > 3.5 else "B")
        st.metric("Sustainability Index", f"{sust_score:.2f} (Rank: {rank})")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=sust_score, gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"}}))
        st.plotly_chart(fig_gauge)

with tab3:
    st.subheader("🔍 Technical Validation & Reliability")
    v_col1, v_col2 = st.columns(2)
    # روابط الصور المستخرجة من كولاب والموجودة في docs
    v_col1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Model Accuracy Validation (R² ≈ 95.3%)")
    v_col2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Variables Importance (Sensitivity Analysis)")
    
    st.subheader("📍 Closest Laboratory Matches")
    db['diff'] = abs(db['CS_28'] - prediction)
    st.table(db.sort_values('diff').head(3)[['Mix_ID', 'CS_28', 'Sustainability', 'CO2']])

with tab4:
    st.subheader("📝 User Feedback & Ethics")
    with st.form("feedback_form"):
        st.write("Share your observations or lab results:")
        fb_user = st.text_input("Name")
        fb_msg = st.text_area("Feedback")
        if st.form_submit_button("Submit"):
            st.success("Feedback received for the 2026 cycle.")
    
    st.markdown("""
        <div class='disclaimer-box'>
        <b>Professional Disclaimer:</b> This tool is a research outcome of the Master's thesis titled "Multi-criteria analysis of eco-efficient concrete...". 
        Predictions are guidance for preliminary design. Laboratory verification is required for structural applications.
        </div>
    """, unsafe_allow_html=True)

# 8. التذييل
st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | ASA Smart Mix Pro | Final Research Interface 2026</div>", unsafe_allow_html=True)
