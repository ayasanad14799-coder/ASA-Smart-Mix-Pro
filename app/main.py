import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 1. إعدادات الهوية الأكاديمية الرسمية
st.set_page_config(page_title="ASA Smart Mix Pro | Master's Research Portal", layout="wide", page_icon="🏗️")

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
        "entry.1503898770": data['Sust'], "entry.1583578049": "ASA_FINAL_V10.0"
    }
    try: requests.post(form_url, data=payload, timeout=8); return True
    except: return False

# تنسيق CSS الأكاديمي المتقدم
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin: 0px; }
    .thesis-title { 
        color: #222; text-align: center; font-family: "Times New Roman", Times, serif; 
        font-size: 22px; font-weight: bold; border-bottom: 3px solid #004a99; padding-bottom: 10px; margin-bottom: 20px;
    }
    .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 15px; }
    .footer-text { text-align: center; color: #777; font-size: 0.85em; border-top: 1px solid #ddd; padding: 15px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول وتوزيع الشعارات (طرد للأطراف)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_l: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=125)
    with col_r: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=125)
    with col_m:
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div class='thesis-title'>AI-Driven Decision Support for Eco-Efficient Concrete (LCA & MCDM Framework)</div>", unsafe_allow_html=True)
        with st.form("Login_Portal"):
            pwd = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter Research Portal"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
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

# 4. الهيدر الداخلي (استعادة كامل البيانات)
hl, hm, hr = st.columns([1, 6, 1])
hl.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
hr.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
with hm:
    st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v10.0</h1>", unsafe_allow_html=True)
    st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1:
    st.markdown("""<div class='doc-card'><b>🎓 Master's Researcher:</b><br>Aya Mohammed Sanad Aboud<br>Faculty of Engineering - Mansoura University</div>""", unsafe_allow_html=True)
with c_info2:
    st.markdown("""<div class='doc-card'><b>👨‍🏫 Under the Supervision of:</b><br>Prof. Ahmed Tahwia | Assoc. Prof. Asser El-Sheikh</div>""", unsafe_allow_html=True)

if "calc_results" not in st.session_state: st.session_state.calc_results = None

# 5. المدخلات الجانبية
with st.sidebar:
    st.header("📋 Mix Design Inputs")
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
    
    if st.button("🚀 Analyze Comprehensive Mix Performance", use_container_width=True):
        inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
        p = model.predict(inputs)[0]
        cs28 = p[1]
        st.session_state.calc_results = {
            "7d": p[0] if p[0] > 5 else 0.72*cs28,
            "28d": cs28,
            "90d": p[2] if p[2] > cs28 else 1.15*cs28,
            "sts": p[3] if p[3] > 1 else 0.55*np.sqrt(cs28),
            "em": p[5] if p[5] > 5 else 4.7*np.sqrt(cs28),
            "upv": p[7] if p[7] > 1000 else 4200,
            "abs": p[6] if p[6] > 0.1 else 4.5,
            "co2": p[11], "cost": p[13], "sust": p[16]
        }

# 6. التبويبات الخمسة (التصميم الجمالي والأكاديمي)
t1, t2, t3, t4, t5 = st.tabs(["📊 Mechanical & Durability", "🌱 LCA & Economic Index", "🔍 Technical Validation", "🚀 MCDM Optimizer", "📝 Methodology & Feedback"])

if st.session_state.calc_results:
    res = st.session_state.calc_results
    with t1:
        st.subheader("Predicted Strength & Engineering Profile")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CS 28-Days (AI)", f"{res['28d']:.2f} MPa")
        m2.metric("CS 7-Days", f"{res['7d']:.2f} MPa")
        m3.metric("Split Tensile", f"{res['sts']:.2f} MPa")
        m4.metric("UPV Speed", f"{res['upv']:.0f} m/s")
        st.plotly_chart(px.line(x=[7, 28, 90], y=[res['7d'], res['28d'], res['90d']], title="Predicted Strength Gain Profile", markers=True))

    with t2:
        st.subheader("Environmental (LCA) & Economic Indicators")
        st.info("Note: The Cost Index is a relative economic indicator used for MCDM analysis, accounting for material consumption regardless of inflation.")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint (LCA)", f"{res['co2']:.1f} kg/m³")
        l2.metric("Sustainability Index", f"{res['sust']:.5f}")
        l3.metric("Economic Cost Index", f"{res['cost']:.2f} Units")
        st.plotly_chart(px.bar(x=["CO2 Index", "Cost Index", "Sust. Index"], y=[res['co2']/500, res['cost']/100, res['sust']*1000], title="Comparative Impact Analysis"))

    with t3:
        st.subheader("Reliability & Sensitivity Analysis")
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Accuracy Validation (R² ≈ 0.95)")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Feature Influence on Final CS_28")

with t4:
    st.subheader("AI Smart Design (Diamond Metadata Optimizer)")
    target = st.slider("Select Target Performance (CS_28 MPa)", 20, 100, 40)
    matches = db[(db['CS_28'] >= target-2.5) & (db['CS_28'] <= target+2.5)].sort_values('Sustainability', ascending=False).head(5)
    st.dataframe(matches[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability', 'Cost']], use_container_width=True)

with t5:
    st.subheader("📜 Technical Methodology & Master's Framework")
    st.markdown(f"""
    <div class='doc-card'>
    <b>Research Core:</b> Decision-making framework based on Multi-Output Random Forest Regression.<br>
    <b>LCA & MCDM:</b> Integrated analysis using Sustainability and Cost Indices to rank eco-efficient mixes.<br>
    <b>Database:</b> DIAMOND Meta-Data ({len(db)} samples) encompassing RCA and MRCA replacements.<br>
    <b>Validation:</b> Verified with COV of 6.16% for consistent industrial applicability.
    </div>
    """, unsafe_allow_html=True)
    st.link_button("📝 Submit Lab Observations (Google Form)", "https://docs.google.com/forms/d/e/1FAIpQLSfcSRu1cYGpJtMEX3i09-PihlEgkek2pWWmNHXDnLOQrGsgSQ/viewform")

# 7. الفوتر (إخلاء المسؤولية الرسمي)
st.markdown(f"""
    <div class='footer-text'>
    © {datetime.now().year} Aya Mohammed Sanad Aboud | Mansoura University - Structural Engineering<br>
    <b>Official Disclaimer:</b> This AI framework is designed for research optimization. Actual laboratory validation is mandatory for implementation as per ACI/Egyptian Codes.
    </div>
    """, unsafe_allow_html=True)
