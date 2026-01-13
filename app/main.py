import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime
import os

# 1. إعدادات الهوية الأكاديمية الرسمية
st.set_page_config(page_title="ASA Smart Mix Pro | Final Dissertation Portal", layout="wide", page_icon="🏗️")

# دالة الربط السحابي (Google Form) - لضمان تسجيل كل تجارب المستخدم
def send_to_google_form(data):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfcSRu1cYGpJtMEX3i09-PihlEgkek2pWWmNHXDnLOQrGsgSQ/formResponse"
    payload = {
        "entry.1599455160": data['Cement'], "entry.359753595": data['Water'],
        "entry.2089487269": data['NCA'], "entry.581408310": data['NFA'],
        "entry.402911999": data['RCA_P'], "entry.2027878370": data['MRCA_P'],
        "entry.834926487": data['SF'], "entry.1854682480": data['FA'],
        "entry.1224546954": data['Fiber'], "entry.1438579923": data['W_C'],
        "entry.577250201": data['SP'], "entry.340296413": data['CS_28'],
        "entry.2013040846": data['STS'], "entry.895159496": data['EM'],
        "entry.422145962": data['CO2'], "entry.1912821133": data['Cost'],
        "entry.1503898770": data['Sust'], "entry.1583578049": "ASA_V10_FINAL_CERTIFIED"
    }
    try:
        requests.post(form_url, data=payload, timeout=5)
        return True
    except: return False

# تنسيق CSS الأكاديمي الفاخر (Times New Roman)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin: 0px; }
    .thesis-title { 
        color: #222; text-align: center; font-family: 'Times New Roman', serif; 
        font-size: 22px; font-weight: bold; border-bottom: 3px solid #004a99; padding-bottom: 10px; margin-bottom: 25px;
    }
    .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 15px; }
    .stMetric { background-color: #ffffff; border-radius: 10px; border: 1px solid #eee; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .footer-text { text-align: center; color: #777; font-size: 0.85em; border-top: 1px solid #ddd; padding: 20px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن (ASA2026)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    l, c, r = st.columns([1, 3, 1])
    with c:
        st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=150)
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><b>Secure Access to Master's Research Portal</b></p>", unsafe_allow_html=True)
        with st.form("Login"):
            pwd = st.text_input("Research Access Key", type="password")
            if st.form_submit_button("Authenticate"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الأصول التقنية
@st.cache_resource
def load_all():
    model = joblib.load('models/concrete_model_multi.joblib')
    scaler = joblib.load('models/scaler_multi.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';' if ';' in open('data/Trail3_DIAMOND_DATABASE.csv').read() else ',')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_all()

# 4. الهيدر الداخلي (استعادة برستيج الجامعة)
hl, hm, hr = st.columns([1, 6, 1])
hl.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
hr.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
with hm:
    st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v10.0</h1>", unsafe_allow_html=True)
    st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

info1, info2 = st.columns(2)
with info1: st.markdown("<div class='doc-card'><b>🎓 Researcher:</b> Aya M. Sanad Aboud<br>Faculty of Engineering - Mansoura University</div>", unsafe_allow_html=True)
with info2: st.markdown("<div class='doc-card'><b>👨‍🏫 Supervision:</b> Prof. Ahmed Tahwia & Assoc. Prof. Asser El-Sheikh</div>", unsafe_allow_html=True)

# 5. المدخلات (Sidebar)
with st.sidebar:
    st.header("📋 Laboratory Mix Design")
    cem = st.number_input("Cement (kg/m³)", 200, 600, 350)
    wat = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine Aggregate)", 0, 1200, 700)
    rca = st.slider("RCA Replacement %", 0, 100, 0)
    mrca = st.slider("MRCA Replacement %", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0)
    fa = st.number_input("Fly Ash", 0, 250, 0)
    fib = st.number_input("Nylon Fiber", 0.0, 10.0, 0.0)
    wc = st.slider("W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)
    
    # تحذير نطاق الصلاحية (Applicability Domain)
    if wc > 0.6 or cem < 300:
        st.warning("⚠️ Warning: Outside optimal structural range (20-80 MPa).")

# 6. التنبؤ وتوزيع النتائج (Multi-output Mapping)
if st.button("🚀 Run Comprehensive MCDM & LCA Analysis", use_container_width=True):
    inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
    p = model.predict(inputs)[0]
    
    # مخرجات النموذج الـ 17 بناءً على الترتيب العلمي لرسالتك
    res = {
        "7d": p[0], "28d": p[1], "90d": p[2], "sts": p[3], "fs": p[4], 
        "em": p[5], "abs": p[6], "upv": p[7], "carb": p[9], "co2": p[11], 
        "cost_idx": p[13], "sust": p[16]
    }

    t1, t2, t3, t4, t5 = st.tabs(["📊 Technical", "🛡️ Durability", "🌱 LCA & Economy", "🔍 Reliability", "🚀 Optimizer"])

    with t1:
        st.subheader("Mechanical Performance Profile")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CS 28d", f"{res['28d']:.2f} MPa")
        col2.metric("Flexural", f"{res['fs']:.2f} MPa")
        col3.metric("Split Tensile", f"{res['sts']:.2f} MPa")
        col4.metric("Elastic Modulus", f"{res['em']:.2f} GPa")
        
        # منحنى تطور المقاومة (أساسي للرسالة)
        fig_gain = px.line(x=[7, 28, 90], y=[res['7d'], res['28d'], res['90d']], 
                          title="Strength Gain Curve", markers=True, labels={'x':'Days', 'y':'Strength (MPa)'})
        st.plotly_chart(fig_gain, use_container_width=True)

    with t2:
        st.subheader("Durability & Physical Indices")
        d1, d2, d3 = st.columns(3)
        d1.metric("Water Absorption", f"{res['abs']:.2f} %")
        d2.metric("Carbonation Depth", f"{res['carb']:.2f} mm")
        d3.metric("UPV Speed", f"{res['upv']:.0f} m/s")
        st.info("💡 Durability parameters indicate long-term structural integrity in harsh environments.")

    with t3:
        st.subheader("LCA & Economic Decision (MCDM)")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint", f"{res['co2']:.1f} kg/m³")
        l2.metric("Relative Cost Index", f"{res['cost_idx']:.2f}")
        l3.metric("Sustainability Score", f"{res['sust']:.4f}")
        
        # رادار MCDM للموازنة بين المعايير
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[res['28d']/100, (100-rca)/100, (600-res['co2'])/600, (150-res['cost_idx'])/150],
            theta=['Technical (CS)', 'Recycling (RCA)', 'Environmental (CO2)', 'Economic (Cost)'], fill='toself'
        ))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        if st.button("📤 Sync Report to Cloud"):
            if send_to_google_form({'Cement':cem,'Water':wat,'NCA':nca,'NFA':nfa,'RCA_P':rca,'MRCA_P':mrca,'SF':sf,'FA':fa,'Fiber':fib,'W_C':wc,'SP':sp,'CS_28':res['28d'],'STS':res['sts'],'EM':res['em'],'CO2':res['co2'],'Cost':res['cost_idx'],'Sust':res['sust']}):
                st.balloons(); st.success("✅ Synced to Research Cloud!")

    with t4:
        st.subheader("Model Reliability & Validation")
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="R² = 0.953 Validation")
        with v2:
            st.write("**Scientific Integrity Metrics:**")
            st.table(pd.DataFrame({"Metric": ["R² Score", "COV (Stability)", "MAE"], "Value": ["0.953", "6.16%", "2.14 MPa"]}))
            st.success("Model demonstrates high robustness for Master's research validation.")

    with t5:
        st.subheader("AI Mix Optimizer")
        target = st.slider("Target CS (MPa)", 20, 80, 40)
        matches = db[(db['CS_28'] >= target-3) & (db['CS_28'] <= target+3)].sort_values('Sustainability', ascending=False).head(5)
        st.write("Best Sustainable Mixes from Experimental Database:")
        st.dataframe(matches[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability']], use_container_width=True)

# 7. الفوتر الرسمي
st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Structural Engineering Department | Mansoura University<br>This tool represents the computational framework of the Master's Thesis. Actual laboratory validation is mandatory.</div>", unsafe_allow_html=True)
