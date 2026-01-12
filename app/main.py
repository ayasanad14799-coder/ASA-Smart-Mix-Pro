import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# 1. إعدادات الصفحة والهوية الأكاديمية
st.set_page_config(page_title="ASA-Smart-Mix Pro | Master's Thesis", layout="wide", page_icon="🏗️")

# تنسيق الـ CSS للهوية الأكاديمية
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .header-container { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 2px solid #004a99; text-align: center; margin-bottom: 25px; }
    .doc-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-right: 6px solid #004a99; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .legend-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 15px; font-size: 0.9em; }
    .footer-text { text-align: center; color: #666; font-size: 0.85em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن (ASA2026)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        l_col1, l_col2 = st.columns(2)
        with l_col1: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/2692812d3d7d64c3ea237f8e877675f896bce834/LOGO.png", width=140)
        with l_col2: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/2692812d3d7d64c3ea237f8e877675f896bce834/OIP.jfif", width=140)
        st.markdown("<h2 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro: Access Control</h2>", unsafe_allow_html=True)
        with st.form("login_gate"):
            access_key = st.text_input("Enter Access Key", type="password")
            if st.form_submit_button("Enter System"):
                if access_key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Unauthorized Entry.")
    st.stop()

# 3. تحميل الموديل والبيانات (تعديل المسارات للهيكل الجديد)
@st.cache_resource
def load_assets():
    # المسارات الجديدة بناءً على هيكل المجلدات
    model_path = 'models/concrete_model.joblib'
    scaler_path = 'models/scaler.joblib'
    db_path = 'data/Trail3_DIAMOND_DATABASE.csv'
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    try:
        db = pd.read_csv(db_path, sep=';')
    except:
        db = pd.read_csv(db_path)
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. الواجهة الرئيسية والهوية البحثية
st.markdown("""
    <div class='header-container'>
        <h1 style='color: #004a99;'>ASA Smart Mix Pro v2.0</h1>
        <p style='font-style: italic; font-size: 1.1em;'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</p>
    </div>
    """, unsafe_allow_html=True)

# تفاصيل المشرفين والباحثة
c_info1, c_info2 = st.columns(2)
with c_info1:
    st.markdown(f"""<div class='doc-card'><b>🎓 Master's Researcher:</b><br>Aya Mohammed Sanad Aboud<br>Construction Engineering Dept.</div>""", unsafe_allow_html=True)
with c_info2:
    st.markdown(f"""<div class='doc-card'><b>👨‍🏫 Supervisors:</b><br>Prof. Ahmed Tahwia<br>Assoc. Prof. Asser El-Sheikh</div>""", unsafe_allow_html=True)

# 5. المدخلات الـ 11 (القائمة الجانبية)
st.sidebar.header("📥 Laboratory Input Parameters")
with st.sidebar:
    st.markdown("<div class='legend-box'><b>Note:</b> Accurate inputs ensure 95.3% prediction reliability.</div>", unsafe_allow_html=True)
    cement = st.number_input("1. Cement (kg/m³)", 200, 600, 350)
    water = st.number_input("2. Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("3. NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("4. NFA (Natural Fine)", 0, 1200, 700)
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

# الحسابات الاقتصادية والبيئية
total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
sust_score = (prediction / (total_co2 * total_cost)) * 1000

# 7. الأقسام الأربعة للمناقشة
tab1, tab2, tab3, tab4 = st.tabs(["Mechanical Performance", "LCA & Economy", "Validation Graphs", "Support"])

with tab1:
    st.subheader("📊 Mechanical Assessment Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Compressive Strength", f"{prediction:.2f} MPa")
    col2.metric("Est. Split Tensile", f"{(0.55 * np.sqrt(prediction)):.2f} MPa")
    col3.metric("Est. Elastic Modulus", f"{(4.7 * np.sqrt(prediction)):.2f} GPa")
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
        theta=['Strength', 'Eco-Agg', 'Multi-Cycle', 'CO2 Saving'], fill='toself'
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("🌱 Environmental & Economic (LCA)")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Total CO2 Emissions", f"{total_co2:.1f} kg/m³")
        fig_pie = px.pie(values=[cement*0.85, sf*0.02, fa*0.01, (nca+nfa)*0.005, sp*0.7], 
                         names=["Cement", "SF", "FA", "Aggregates", "Additives"], hole=0.4)
        st.plotly_chart(fig_pie)
    with col5:
        st.metric("Sustainability Index", f"{sust_score:.2f}")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=sust_score, gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"}}))
        st.plotly_chart(fig_gauge)

with tab3:
    st.subheader("🔍 Technical Verification")
    v1, v2 = st.columns(2)
    # ملاحظة: تأكدي من وجود هذه الصور في جيت هوب
    v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/2ddbd240c3eeae0e4603f535d2089f80cf940ea6/accuracy_plot.png", caption="Model Accuracy Validation")
    v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/2ddbd240c3eeae0e4603f535d2089f80cf940ea6/feature_importance.png", caption="Variables Importance")
    
    st.subheader("📍 Closest Experimental Benchmarks")
    db['diff'] = abs(db['CS_28'] - prediction)
    st.table(db.sort_values('diff').head(3)[['Mix_ID', 'CS_28', 'Sustainability', 'CO2']])

with tab4:
    st.subheader("📝 Disclaimer")
    st.info("This software is a research tool for preliminary guidance. Laboratory verification is mandatory for final structural designs.")
    st.write("For support or inquiries: [Your Email Here]")

# 8. التذييل النهائي
st.markdown(f"""<div class='footer-text'>© {datetime.now().year} Aya M. Sanad Aboud | ASA Smart Mix Pro | Mansoura University</div>""", unsafe_allow_html=True)
