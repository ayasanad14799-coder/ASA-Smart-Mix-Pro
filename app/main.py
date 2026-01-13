import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI Optimizer", layout="wide", page_icon="🏗️")

# دالة إرسال البيانات إلى Google Form (الربط السحري)
def send_to_google_form(data):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfcSRu1cYGpJtMEX3i09-PihlEgkek2pWWmNHXDnLOQrGsgSQ/formResponse"
    
    # ربط الخانات بناءً على الرابط الذي أرسلتِه
    payload = {
        "entry.1599455160": data.get('Cement', 0),
        "entry.359753595": data.get('Water', 0),
        "entry.2089487269": data.get('NCA', 0),
        "entry.581408310": data.get('NFA', 0),
        "entry.402911999": data.get('RCA_P', 0),
        "entry.2027878370": data.get('MRCA_P', 0),
        "entry.834926487": data.get('SF', 0),
        "entry.1854682480": data.get('FA', 0),
        "entry.1224546954": data.get('Fiber', 0),
        "entry.1438579923": data.get('W_C', 0),
        "entry.577250201": data.get('SP', 0),
        "entry.340296413": data.get('Strength', 0),
        "entry.2013040846": data.get('STS', 0),
        "entry.895159496": data.get('EM', 0),
        "entry.422145962": data.get('CO2', 0),
        "entry.1912821133": data.get('Cost', 0),
        "entry.1503898770": data.get('Sustainability', 0),
        "entry.1275091872": data.get('Rank', 'N/A'),
        "entry.1583578049": data.get('Type', 'Manual'),
        "entry.1785868407": "Researcher_Sync"
    }
    try:
        response = requests.post(form_url, data=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

# تنسيق CSS الاحترافي
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; }
    .thesis-title { 
        color: #222; text-align: center; 
        font-family: "Times New Roman", Times, serif; 
        font-size: 22px; font-weight: bold; 
        border-bottom: 3px solid #004a99; padding-bottom: 15px; margin-bottom: 25px;
    }
    .doc-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-right: 6px solid #004a99; margin-bottom: 15px; }
    .optimizer-card { background-color: #f1f8e9; padding: 25px; border-radius: 15px; border: 2px solid #2e7d32; }
    .footer-text { text-align: center; color: #666; font-size: 0.9em; margin-top: 50px; border-top: 1px solid #eee; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 4, 1])
    with col_mid:
        logo_left, spacer, logo_right = st.columns([1, 2.5, 1])
        with logo_left: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=115)
        with logo_right: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=115)
        st.markdown("<h1 style='text-align: center;'>ASA-Smart-Mix Pro</h1>", unsafe_allow_html=True)
        with st.form("login"):
            key = st.text_input("Enter Access Key", type="password")
            if st.form_submit_button("Start Session"):
                if key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الموديل والبيانات
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

# 4. الهيدر
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1:
    st.markdown("<div class='doc-card'><b>🎓 Researcher:</b> Aya Mohammed Sanad Aboud</div>", unsafe_allow_html=True)
with c_info2:
    st.markdown("<div class='doc-card'><b>👨‍🏫 Supervision:</b> Prof. Ahmed Tahwia | Assoc. Prof. Asser El-Sheikh</div>", unsafe_allow_html=True)

# 5. المدخلات (Sidebar)
st.sidebar.header("📋 Mix Constituents")
with st.sidebar:
    cement = st.number_input("Cement (kg/m³)", 200, 600, 350)
    water = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine)", 0, 1200, 700)
    rca_p = st.slider("RCA Replacement (%)", 0, 100, 0)
    mrca_p = st.slider("MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0)
    fa = st.number_input("Fly Ash", 0, 250, 0)
    fiber = st.number_input("Nylon Fiber", 0.0, 10.0, 0.0)
    wc_ratio = st.slider("W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)

# 6. التشغيل والنتائج
st.markdown("---")
col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])
with col_btn_2:
    run_button = st.button("🚀 Run AI Analysis", use_container_width=True)

if run_button:
    features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
    prediction = model.predict(scaler.transform(features))[0]
    
    sts_val = round(0.55 * np.sqrt(prediction), 2)
    em_val = round(4.7 * np.sqrt(prediction), 2)
    total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
    total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
    sust_score = (prediction / (total_co2 * total_cost)) * 1000
    rank_val = "A+" if sust_score > 4.5 else "A" if sust_score > 3.5 else "B"

    st.success("✅ Analysis Completed!")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Mechanical", "🌱 LCA", "🔍 Validation", "🚀 Optimizer", "📝 Feedback"])

    with tab1:
        st.subheader("Performance Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("Strength", f"{prediction:.2f} MPa")
        m2.metric("Tensile", f"{sts_val} MPa")
        m3.metric("Modulus", f"{em_val} GPa")
        
        if st.button("📤 Sync to Research Cloud"):
            data = {
                "Cement": cement, "Water": water, "NCA": nca, "NFA": nfa, "RCA_P": rca_p, "MRCA_P": mrca_p,
                "SF": sf, "FA": fa, "Fiber": fiber, "W_C": wc_ratio, "SP": sp,
                "Strength": round(float(prediction), 2), "STS": sts_val, "EM": em_val,
                "CO2": round(total_co2, 2), "Cost": round(total_cost, 2),
                "Sustainability": round(sust_score, 5), "Rank": rank_val, "Type": "Manual"
            }
            if send_to_google_form(data): st.balloons(); st.success("✅ Synced!")
            else: st.error("❌ Sync Error.")

    with tab4:
        st.markdown("<div class='optimizer-card'>", unsafe_allow_html=True)
        st.subheader("🚀 AI Mix Recommender")
        target = st.slider("Target Strength (MPa)", 20, 100, 40, key="opt_v3")
        if st.button("Generate Top 5 Mixes"):
            matches = db[(db['CS_28'] >= target - 2.5) & (db['CS_28'] <= target + 2.5)]
            if not matches.empty:
                top_5 = matches.sort_values('Sustainability', ascending=False).head(5)
                st.dataframe(top_5[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability']], use_container_width=True)
            else: st.error("No matches.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        with st.form("fb"):
            fb_name = st.text_input("Name")
            fb_msg = st.text_area("Observations")
            if st.form_submit_button("Submit"):
                fb_data = {"Cement": 0, "Water": 0, "NCA": 0, "NFA": 0, "RCA_P": 0, "MRCA_P": 0, "SF": 0, "FA": 0, "Fiber": 0, "W_C": 0, "SP": 0, "Strength": 0, "STS": 0, "EM": 0, "CO2": 0, "Cost": 0, "Sustainability": 0, "Rank": "N/A", "Type": f"FB: {fb_name}-{fb_msg}"}
                if send_to_google_form(fb_data): st.success("Logged!")
else: st.info("👈 Set parameters and click 'Run AI Analysis'.")

st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Mansoura University</div>", unsafe_allow_html=True)
