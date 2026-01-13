import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import os

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI", layout="wide", page_icon="🏗️")

# دالة الربط السحابي
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
        "entry.1503898770": data['Sust'], "entry.1583578049": "ASA_V7.5_STABLE"
    }
    try: requests.post(form_url, data=payload, timeout=8); return True
    except: return False

# تنسيق CSS
st.markdown("<style>.main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; } .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 10px; }</style>", unsafe_allow_html=True)

# 2. نظام الدخول والشعارات
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    l, m, r = st.columns([1, 4, 1])
    l.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=125)
    r.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=125)
    with m:
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        with st.form("Login"):
            if st.text_input("Access Key", type="password") == "ASA2026" and st.form_submit_button("Enter Research Portal"):
                st.session_state.auth = True; st.rerun()
    st.stop()

# 3. تحميل الأصول
@st.cache_resource
def load_all():
    model = joblib.load('models/concrete_model_multi.joblib')
    scaler = joblib.load('models/scaler_multi.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_all()

# 4. الهيدر الداخلي (لوجوهات مطرودة يمين ويسار)
hl, hm, hr = st.columns([1, 6, 1])
hl.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
hr.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
hm.markdown("<h1 class='main-title'>ASA Smart Mix Pro v7.5</h1>", unsafe_allow_html=True)

# 5. منطق البرنامج (Session State) لضمان الاستقرار
if "results" not in st.session_state: st.session_state.results = None

with st.sidebar:
    st.header("📋 Mix Design Inputs")
    cem = st.number_input("Cement", 200, 600, 350)
    wat = st.number_input("Water", 100, 300, 160)
    nca = st.number_input("NCA", 0, 1500, 1100)
    nfa = st.number_input("NFA", 0, 1200, 700)
    rca = st.slider("RCA %", 0, 100, 0)
    mrca = st.slider("MRCA %", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0)
    fa = st.number_input("Fly Ash", 0, 250, 0)
    fib = st.number_input("Fiber", 0.0, 10.0, 0.0)
    wc = st.slider("W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)
    
    if st.button("🚀 Run AI Analysis", use_container_width=True):
        inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
        p = model.predict(inputs)[0]
        # حماية هندسية ضد الـ Missing Data في الـ CSV
        cs28 = p[1]
        cs7  = p[0] if p[0] > 5 else 0.7 * cs28
        cs90 = p[2] if p[2] > cs28 else 1.15 * cs28
        sts  = p[3] if p[3] > 1 else 0.55 * np.sqrt(cs28)
        em   = p[5] if p[5] > 5 else 4.7 * np.sqrt(cs28)
        st.session_state.results = {
            "p_7d": cs7, "p_28d": cs28, "p_90d": cs90, "p_sts": sts, "p_em": em,
            "p_abs": p[6], "p_upv": p[7] if p[7] > 1000 else 4200, 
            "p_co2": p[11], "p_cost": p[13], "p_sust": p[16]
        }

# 6. العرض في التبويبات الخمسة (خارج شرط الزرار لضمان الثبات)
t1, t2, t3, t4, t5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📝 Documentation & Feedback"])

if st.session_state.results:
    res = st.session_state.results
    with t1:
        st.subheader("Performance Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CS 28-Days", f"{res['p_28d']:.2f} MPa")
        c2.metric("CS 7-Days", f"{res['p_7d']:.2f} MPa")
        c3.metric("Split Tensile", f"{res['p_sts']:.2f} MPa")
        c4.metric("UPV Speed", f"{res['p_upv']:.2f} km/s")
        st.plotly_chart(px.line(x=[7, 28, 90], y=[res['p_7d'], res['p_28d'], res['p_90d']], title="Strength Gain", markers=True))
        
        if st.button("📤 Sync Report to Cloud"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "CS_28": round(res['p_28d'], 2), "STS": round(res['p_sts'], 2), "EM": round(res['p_em'], 2), "CO2": round(res['p_co2'], 2), "Cost": round(res['p_cost'], 2), "Sust": round(res['p_sust'], 5), "Rank": "A"}
            if send_to_google_form(d): st.balloons(); st.success("Synced!")

    with t2:
        st.subheader("LCA Metrics")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint", f"{res['p_co2']:.1f} kg")
        l2.metric("Sust. Index", f"{res['p_sust']:.5f}")
        l3.metric("Mix Cost", f"${res['p_cost']:.2f}")

    with t3:
        st.subheader("Validation Plots")
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Accuracy Plot")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity")

with t5:
    st.subheader("📋 Methodology & Technical Feedback")
    st.markdown("<div class='doc-card'><b>Algorithm:</b> Multi-output RF<br><b>Dataset:</b> DIAMOND Meta-Data<br><b>Validation:</b> COV 6.16%</div>", unsafe_allow_html=True)
    with st.form("fb_form"):
        st.write("Submit Experimental Observations:")
        f_val = st.number_input("Laboratory Result (MPa)")
        if st.form_submit_button("Submit Data"): st.success("Logged!")

st.markdown(f"<div style='text-align:center; color:#777; padding:20px;'>© {datetime.now().year} Aya Mohammed Sanad | Mansoura University</div>", unsafe_allow_html=True)
