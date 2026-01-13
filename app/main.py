import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 1. إعدادات الهوية البصرية والأكاديمية
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI Optimizer", layout="wide", page_icon="🏗️")

# دالة الربط السحابي (Google Form) لتوثيق 20 خانة بحثية
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
        "entry.1583578049": data['Type'], "entry.1785868407": "ASA_V6_MULTI_FINAL"
    }
    try:
        requests.post(form_url, data=payload, timeout=8)
        return True
    except: return False

# تنسيق CSS الأكاديمي الرسمي (Times New Roman)
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
    with l_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=125)
    with r_sp: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=125)
    with mid_c:
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA Smart Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div class='thesis-title'>AI-Driven Framework for Eco-Efficient Concrete Optimization</div>", unsafe_allow_html=True)
        with st.form("Login"):
            pwd = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter Research Lab"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الموديل والبيانات (الـ 36 عمود)
@st.cache_resource
def load_assets():
    # تأكدي من تسمية الملفات في GitHub كما يلي:
    model = joblib.load('models/concrete_model_multi.joblib')
    scaler = joblib.load('models/scaler_multi.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';' if ';' in open('data/Trail3_DIAMOND_DATABASE.csv').read() else ',')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. الهيدر الداخلي (شعارات متباعدة)
h_l, h_m, h_r = st.columns([1, 6, 1])
with h_l: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=100)
with h_r: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=100)
with h_m:
    st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v6.0</h1>", unsafe_allow_html=True)
    st.markdown("<div class='thesis-title'>Multi-criteria Analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

# 5. المدخلات (الـ 11 متغير)
with st.sidebar:
    st.header("📋 Mix Design Inputs")
    cem = st.number_input("Cement (kg/m³)", 200, 600, 350)
    wat = st.number_input("Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("NCA (Coarse)", 0, 1500, 1100)
    nfa = st.number_input("NFA (Fine)", 0, 1200, 700)
    rca = st.slider("RCA Replacement (%)", 0, 100, 0)
    mrca = st.slider("MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("Silica Fume", 0, 150, 0)
    fa = st.number_input("Fly Ash", 0, 250, 0)
    fib = st.number_input("Nylon Fiber", 0.0, 10.0, 0.0)
    wc = st.slider("W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("Superplasticizer", 0.0, 20.0, 2.0)

# 6. التنبؤ والحسابات (Multi-output Mapping) [ضمان عدم الترحيل]
if st.button("🚀 Analyze Comprehensive Mix Performance", use_container_width=True):
    inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
    preds = model.predict(inputs)[0] 
    
    # ربط المخرجات الـ 17 بناءً على ترتيب الـ Targets في كود كولاب
    p_7d, p_28d, p_90d = preds[0], preds[1], preds[2] 
    p_sts, p_fs, p_em  = preds[3], preds[4], preds[5]
    p_abs, p_upv, p_shr, p_carb = preds[6], preds[7], preds[8], preds[9]
    p_co2, p_cost, p_sust = preds[11], preds[13], preds[16]
    p_rank = "A+" if p_sust > 4.5 else "A" if p_sust > 3.5 else "B"

    # التبويبات الخمسة المعتمدة
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📝 Feedback & Methodology"])

    with tab1:
        st.subheader("Predicted Mechanical & Durability Performance")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CS 28-Days", f"{p_28d:.2f} MPa")
        m2.metric("CS 7-Days", f"{p_7d:.2f} MPa")
        m3.metric("Split Tensile", f"{p_sts:.2f} MPa")
        m4.metric("UPV Speed", f"{p_upv:.2f} km/s")
        
        d1, d2, d3 = st.columns(3)
        d1.metric("Elastic Modulus", f"{p_em:.2f} GPa")
        d2.metric("Water Abs.", f"{p_abs:.2f} %")
        d3.metric("CS 90-Days", f"{p_90d:.2f} MPa")

        st.plotly_chart(px.line(x=[7, 28, 90], y=[p_7d, p_28d, p_90d], title="AI-Predicted Strength Evolution Curve", markers=True))
        
        if st.button("📤 Sync Full Report to Research Cloud"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "CS_28": round(p_28d, 2), "STS": round(p_sts, 2), "EM": round(p_em, 2), "CO2": round(p_co2, 2), "Cost": round(p_cost, 2), "Sust": round(p_sust, 4), "Rank": p_rank, "Type": "AI_Multi_Prediction"}
            if send_to_google_form(d): st.balloons(); st.success("✅ Recorded in Cloud Database!")

    with tab2:
        st.subheader("Environmental & Economic Analysis")
        l1, l2, l3 = st.columns(3)
        l1.metric("CO2 Footprint", f"{p_co2:.1f} kg/m³")
        l2.metric("Sustainability Index", f"{p_sust:.3f}")
        l3.metric("Estimated Cost", f"${p_cost:.2f}")

    with tab3:
        st.subheader("Technical Reliability & Validation")
        st.write(f"**Domain:** Model valid for CS_28 range [{db['CS_28'].min()} - {db['CS_28'].max()} MPa].")
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Accuracy Validation (R² ≈ 95.5%)")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity Analysis (Variable Influence)")

    with tab4:
        st.subheader("AI Smart Mix Recommender")
        target_s = st.slider("Select Target Strength", 20, 100, 40)
        matches = db[(db['CS_28'] >= target_s-2.5) & (db['CS_28'] <= target_s+2.5)].sort_values('Sustainability', ascending=False).head(5)
        st.dataframe(matches[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability']], use_container_width=True)

    with tab5:
        st.subheader("📋 Technical Documentation & Methodology")
        st.markdown(f"""
        <div class='doc-card'>
        <b>Algorithm:</b> Random Forest Multi-output Regression (Selected for its superior handling of non-linear structural data)<br>
        <b>Database:</b> DIAMOND Metadata Repository ({len(db)} samples)<br>
        <b>COV:</b> 6.16% (Demonstrating high stability across raw material sources)<br>
        <b>Applicability Domain:</b> Optimized for eco-friendly concrete mixes (20-80 MPa)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        with st.form("fb"):
            st.write("Share experimental lab results to improve the model:")
            lab_s = st.number_input("Actual Strength (MPa)")
            if st.form_submit_button("Submit Feedback"): st.success("Feedback Logged!")

# 7. الفوتر مع إخلاء المسؤولية
st.markdown(f"""
    <div class='footer-text'>
    © {datetime.now().year} Aya Mohammed Sanad Aboud | Mansoura University - Structural Engineering Dept.<br>
    <b>Disclaimer:</b> This AI tool is for research and design. Actual laboratory trials are mandatory for structural implementation as per official codes.
    </div>
    """, unsafe_allow_html=True)
