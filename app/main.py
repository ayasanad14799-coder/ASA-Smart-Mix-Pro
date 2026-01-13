import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 1. إعدادات الهوية البصرية (UX/UI)
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI Optimizer", layout="wide", page_icon="🏗️")

# دالة الربط السحابي (Google Form)
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
        "entry.1503898770": data['Sust'], "entry.1275091872": data['Rank'],
        "entry.1583578049": data['Type'], "entry.1785868407": "ASA_V5.0_ULTIMATE"
    }
    try:
        requests.post(form_url, data=payload, timeout=8)
        return True
    except: return False

# تنسيق CSS الأكاديمي الرسمي
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin: 0px; }
    .thesis-title { 
        color: #222; text-align: center; font-family: "Times New Roman", Times, serif; 
        font-size: 22px; font-weight: bold; border-bottom: 3px solid #004a99; padding-bottom: 10px; margin-bottom: 20px;
    }
    .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 10px; }
    .footer-text { text-align: center; color: #777; font-size: 0.85em; border-top: 1px solid #ddd; padding: 15px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول وتوزيع الشعارات (طرد للأطراف)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    l_sp, mid_c, r_sp = st.columns([1, 4, 1])
    with l_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=120)
    with r_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=120)
    with mid_c:
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div class='thesis-title'>AI Framework for Multi-Criteria Analysis of Eco-Efficient Concrete</div>", unsafe_allow_html=True)
        with st.form("Login"):
            pwd = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter Research Lab"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الموديل والبيانات
@st.cache_resource
def load_assets():
    model = joblib.load('models/concrete_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';' if ';' in open('data/Trail3_DIAMOND_DATABASE.csv').read() else ',')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. الهيدر الداخلي
h_l, h_m, h_r = st.columns([1, 6, 1])
with h_l: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
with h_r: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
with h_m:
    st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v5.0</h1>", unsafe_allow_html=True)
    st.markdown("<div class='thesis-title'>Comprehensive Technical, Environmental and Economic analysis</div>", unsafe_allow_html=True)

# 5. المدخلات (الـ 11 متغير)
with st.sidebar:
    st.header("📋 Mix Inputs")
    cem = st.number_input("Cement (kg/m³)", 200, 600, 350)
    wat = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine)", 0, 1200, 700)
    rca = st.slider("RCA Replacement (%)", 0, 100, 0)
    mrca = st.slider("MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("Fly Ash (kg/m³)", 0, 250, 0)
    fib = st.number_input("Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc = st.slider("W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)

# 6. التشغيل (التنبؤ المتعدد - Multi-output)
if st.button("🚀 Analyze Comprehensive Mix Performance", use_container_width=True):
    inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
    preds = model.predict(inputs)[0] 
    
    # ربط المخرجات الـ 17 بناءً على تدريب الموديل (Array Mapping)
    # 0:CS_7, 1:CS_28, 2:CS_90, 3:STS, 4:FS, 5:EM, 6:Water_Abs, 7:UPV, 8:Shrinkage, 9:Carb_Depth
    # 11:CO2, 13:Cost, 16:Sustainability
    p_7d, p_28d, p_90d = preds[0], preds[1], preds[2] 
    p_sts, p_fs, p_em  = preds[3], preds[4], preds[5]
    p_abs, p_upv, p_shr, p_carb = preds[6], preds[7], preds[8], preds[9]
    p_co2, p_cost, p_sust = preds[11], preds[13], preds[16]

    tabs = st.tabs(["📊 Mechanical", "🏗️ Durability", "🌱 Economy", "🚀 Optimizer", "📜 Methodology", "📝 Feedback"])

    with tabs[0]:
        st.subheader("Strength & Mechanical Performance")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CS 7-Days", f"{p_7d:.2f} MPa")
        m2.metric("CS 28-Days (AI)", f"{p_28d:.2f} MPa")
        m3.metric("CS 90-Days", f"{p_90d:.2f} MPa")
        m4.metric("Split Tensile", f"{p_sts:.2f} MPa")
        st.plotly_chart(px.line(x=[7, 28, 90], y=[p_7d, p_28d, p_90d], title="Strength Gain Chart", markers=True))
        
        if st.button("📤 Sync Full Report"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "CS_28": round(p_28d, 2), "STS": round(p_sts, 2), "EM": round(p_em, 2), "CO2": round(p_co2, 2), "Cost": round(p_cost, 2), "Sust": round(p_sust, 4), "Rank": "A+", "Type": "AI_Prediction_V5"}
            if send_to_google_form(d): st.balloons(); st.success("✅ Recorded in Cloud Database!")

    with tabs[1]:
        st.subheader("Durability Indices")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("UPV Speed", f"{p_upv:.2f} km/s")
        d2.metric("Water Abs.", f"{p_abs:.2f} %")
        d3.metric("Carb. Depth", f"{p_carb:.2f} mm")
        d4.metric("Elastic Modulus", f"{p_em:.2f} GPa")

    with tabs[4]:
        st.subheader("Technical Methodology")
        st.markdown(f"""
        <div class='doc-card'>
        <b>Algorithm:</b> Random Forest Multi-output Regression<br>
        <b>Database:</b> DIAMOND Database ({len(db)} Samples)<br>
        <b>R² Accuracy:</b> 95.57% | <b>COV:</b> 6.16%
        </div>
        """, unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Accuracy Plot")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity")

# 7. الفوتر مع إخلاء المسؤولية
st.markdown(f"""
    <div class='footer-text'>
    © {datetime.now().year} Aya Mohammed Sanad | Mansoura University<br>
    <b>Disclaimer:</b> This AI tool is for research purposes only. Actual laboratory trials are mandatory for structural implementation.
    </div>
    """, unsafe_allow_html=True)
