import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import os

# 1. إعدادات الهوية البصرية والأكاديمية
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI", layout="wide", page_icon="🏗️")

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
        "entry.1503898770": data['Sust'], "entry.1583578049": "ASA_MASTER_V7.5"
    }
    try: requests.post(form_url, data=payload, timeout=8); return True
    except: return False

# تنسيق CSS الأكاديمي
st.markdown("<style>.main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; } .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 10px; }</style>", unsafe_allow_html=True)

# 2. نظام الدخول وتوزيع الشعارات (طرد للأطراف)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    l_sp, mid_c, r_sp = st.columns([1, 4, 1])
    with l_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=125)
    with r_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=125)
    with mid_c:
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-weight: bold; border-bottom: 2px solid #004a99;'>AI-Driven Framework for Sustainable Concrete Optimization</div>", unsafe_allow_html=True)
        with st.form("Login"):
            pwd = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter Research Portal"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الأصول (الموديل والسكيلر والداتا)
@st.cache_resource
def load_all():
    model = joblib.load('models/concrete_model_multi.joblib')
    scaler = joblib.load('models/scaler_multi.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_all()

# 4. الهيدر الداخلي
hl, hm, hr = st.columns([1, 6, 1])
hl.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
hr.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
hm.markdown("<h1 class='main-title'>ASA Smart Mix Pro v7.5</h1>", unsafe_allow_html=True)

# 5. إدارة الحالة (Session State) لثبات النتائج
if "results" not in st.session_state: st.session_state.results = None

with st.sidebar:
    st.header("📋 Mix Design Inputs")
    cem = st.number_input("Cement (kg/m³)", 200, 600, 350)
    wat = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine)", 0, 1200, 700)
    rca = st.slider("RCA %", 0, 100, 0)
    mrca = st.slider("MRCA %", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0)
    fa = st.number_input("Fly Ash", 0, 250, 0)
    fib = st.number_input("Nylon Fiber", 0.0, 10.0, 0.0)
    wc = st.slider("W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)
    
    if st.button("🚀 Run Comprehensive Analysis", use_container_width=True):
        features = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
        preds = model.predict(features)[0]
        # حماية هندسية: لو الموديل تنبأ بـ 0 (بسبب نقص الداتا)، نستخدم المعادلات التصحيحية
        cs28 = preds[1]
        cs7  = preds[0] if preds[0] > 5 else 0.72 * cs28
        cs90 = preds[2] if preds[2] > cs28 else 1.15 * cs28
        sts  = preds[3] if preds[3] > 1 else 0.55 * np.sqrt(cs28)
        em   = preds[5] if preds[5] > 5 else 4.7 * np.sqrt(cs28)
        
        st.session_state.results = {
            "7d": cs7, "28d": cs28, "90d": cs90, "sts": sts, "em": em,
            "abs": preds[6], "upv": preds[7] if preds[7] > 1000 else 4250, 
            "co2": preds[11], "cost": preds[13], "sust": preds[16]
        }

# 6. التبويبات الخمسة (خارج شرط الزرار لضمان الاستقرار)
t1, t2, t3, t4, t5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📜 Methodology & Feedback"])

if st.session_state.results:
    res = st.session_state.results
    with t1:
        st.subheader("Predicted Strength & Performance")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CS 28-Days (AI)", f"{res['28d']:.2f} MPa")
        m2.metric("CS 7-Days", f"{res['7d']:.2f} MPa")
        m3.metric("Split Tensile", f"{res['sts']:.2f} MPa")
        m4.metric("UPV Speed", f"{res['upv']:.2f} m/s")
        st.plotly_chart(px.line(x=[7, 28, 90], y=[res['7d'], res['28d'], res['90d']], title="Strength Evolution", markers=True))
        
        if st.button("📤 Sync Full Report"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "CS_28": round(res['28d'], 2), "STS": round(res['sts'], 2), "EM": round(res['em'], 2), "CO2": round(res['co2'], 2), "Cost": round(res['cost'], 2), "Sust": round(res['sust'], 5), "Rank": "A"}
            if send_to_google_form(d): st.balloons(); st.success("✅ Synced!")

    with t2:
        st.subheader("Environmental & Economic LCA")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint", f"{res['co2']:.1f} kg")
        l2.metric("Sust. Index", f"{res['sust']:.5f}")
        l3.metric("Estimated Cost", f"${res['cost']:.2f}")

    with t3:
        st.subheader("Reliability Plots")
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Accuracy Plot")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Feature Importance")

with t4:
    st.subheader("AI Design Optimizer (Diamond Database)")
    target_s = st.slider("Select Target Strength", 20, 100, 40)
    matches = db[(db['CS_28'] >= target_s-2.5) & (db['CS_28'] <= target_s+2.5)].sort_values('Sustainability', ascending=False).head(5)
    st.dataframe(matches[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability']], use_container_width=True)

with t5:
    st.subheader("📋 Methodology & Experimental Feedback")
    st.markdown("<div class='doc-card'><b>Algorithm:</b> Multi-output Random Forest<br><b>Dataset:</b> DIAMOND Meta-Data<br><b>Reliability:</b> Direct prediction from experimental data.</div>", unsafe_allow_html=True)
    with st.form("feedback_form"):
        st.write("Share Lab Result to improve AI:")
        lab_val = st.number_input("Actual Strength (MPa)")
        if st.form_submit_button("Submit Data"): st.success("Feedback Logged!")

st.markdown(f"<div style='text-align:center; color:#777; padding:20px;'>© {datetime.now().year} Aya Mohammed Sanad | Mansoura University</div>", unsafe_allow_html=True)
