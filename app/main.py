import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime
import os

# 1. إعدادات الهوية البصرية
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
        "entry.1503898770": data['Sust'], "entry.1583578049": "ASA_V7_FINAL"
    }
    try: requests.post(form_url, data=payload, timeout=8); return True
    except: return False

# تنسيق CSS الأكاديمي (Times New Roman)
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

# 4. الهيدر الداخلي
hl, hm, hr = st.columns([1, 6, 1])
hl.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
hr.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
hm.markdown("<h1 class='main-title'>ASA Smart Mix Pro v7.0</h1>", unsafe_allow_html=True)
hm.markdown("<p style='text-align: center; font-weight: bold;'>Technical, Environmental and Economic analysis of Eco-efficient concrete</p>", unsafe_allow_html=True)

# 5. المدخلات
with st.sidebar:
    st.header("📋 Mix Inputs")
    cem = st.number_input("Cement", 200, 600, 350); wat = st.number_input("Water", 100, 300, 160)
    nca = st.number_input("NCA", 0, 1500, 1100); nfa = st.number_input("NFA", 0, 1200, 700)
    rca = st.slider("RCA %", 0, 100, 0); mrca = st.slider("MRCA %", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0); fa = st.number_input("Fly Ash", 0, 250, 0)
    fib = st.number_input("Fiber", 0.0, 10.0, 0.0); wc = st.slider("W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)

# 6. التنبؤ والمنطق الهجين (Hybrid Logic) لمنع "العبط"
if st.button("🚀 Analyze Comprehensive Mix Performance", use_container_width=True):
    inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
    preds = model.predict(inputs)[0]
    
    # تصحيح ترحيل الأعمدة (بناءً على ملفك الـ CSV)
    p_28d = preds[1]
    # منطق حماية: لو الموديل تنبأ بـ 0 لـ 7 و 90 يوم (بسبب نقص الداتا)، استخدم المعادلات الهندسية
    p_7d = preds[0] if preds[0] > 5 else round(0.7 * p_28d, 2)
    p_90d = preds[2] if preds[2] > 5 else round(1.15 * p_28d, 2)
    p_sts = preds[3] if preds[3] > 1 else round(0.55 * np.sqrt(p_28d), 2)
    p_em = preds[5] if preds[5] > 5 else round(4.7 * np.sqrt(p_28d), 2)
    p_upv = preds[7] if preds[7] > 1000 else round(3500 + (p_28d * 20), 0)
    
    # مخرجات الـ LCA
    p_co2, p_cost, p_sust = preds[11], preds[13], preds[16]
    p_rank = "A+" if p_sust > 0.005 else "A" if p_sust > 0.001 else "B"

    # التبويبات الخمسة المعتمدة
    t1, t2, t3, t4, t5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📝 Methodology & Feedback"])

    with t1:
        st.subheader("Predicted Engineering Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CS 28-Days (AI)", f"{p_28d:.2f} MPa")
        c2.metric("CS 7-Days", f"{p_7d:.2f} MPa")
        c3.metric("Split Tensile", f"{p_sts:.2f} MPa")
        c4.metric("Elastic Modulus", f"{p_em:.2f} GPa")
        st.plotly_chart(px.line(x=[7, 28, 90], y=[p_7d, p_28d, p_90d], title="Strength Gain Profile", markers=True))
        if st.button("📤 Sync Report"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "CS_28": round(p_28d, 2), "STS": p_sts, "EM": p_em, "CO2": round(p_co2, 2), "Cost": round(p_cost, 2), "Sust": round(p_sust, 5), "Rank": p_rank, "Type": "AI_Master_V7"}
            if send_to_google_form(d): st.success("✅ Synced to Research Cloud!")

    with t2:
        st.subheader("Environmental & Economic Analysis")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint", f"{p_co2:.1f} kg/m³")
        l2.metric("Sust. Index", f"{p_sust:.5f} (Rank: {p_rank})")
        l3.metric("Estimated Cost", f"${p_cost:.2f}")

    with t5:
        st.subheader("📋 Technical Documentation & Methodology")
        st.markdown(f"""
        <div class='doc-card'>
        <b>Algorithm:</b> Multi-output Random Forest Regression<br>
        <b>Validation:</b> Learned from {len(db)} experimental samples<br>
        <b>Hybrid Logic:</b> Application uses engineering growth factors for missing temporal data to ensure logical consistency.
        </div>
        """, unsafe_allow_html=True)
        with st.form("fb"):
            st.write("Share experimental results:")
            if st.form_submit_button("Submit"): st.success("Feedback Logged.")

st.markdown(f"<div style='text-align:center; color:#777; padding:20px;'>© {datetime.now().year} Aya Mohammed Sanad | Mansoura University</div>", unsafe_allow_html=True)
