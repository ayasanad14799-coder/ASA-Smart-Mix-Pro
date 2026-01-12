import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة والهوية الأكاديمية (من كودك الأصلي)
st.set_page_config(page_title="ASA Smart Mix Pro", layout="wide", page_icon="🏗️")

st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .header-container { background-color: #f8f9fa; padding: 25px; border-radius: 15px; border: 2px solid #004a99; text-align: center; margin-bottom: 25px; }
    .doc-card { background-color: #ffffff; padding: 20px; border-radius: 10px; border-right: 6px solid #004a99; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .login-title { color: #004a99; text-align: center; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن (ASA2026) - نفس فكرتك
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        l1, l2 = st.columns(2)
        with l1: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=140)
        with l2: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=140)
        st.markdown("<h2 class='login-title'>ASA Smart Mix Pro: AI Optimizer</h2>", unsafe_allow_html=True)
        with st.form("login"):
            key = st.text_input("Access Key", type="password")
            if st.form_submit_button("Access System"):
                if key == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Incorrect Key.")
    st.stop()

# 3. تحميل الموديل والبيانات
@st.cache_resource
def load_assets():
    model = joblib.load('models/concrete_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
    db = pd.read_csv('data/Trail3_DIAMOND_DATABASE.csv', sep=';')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_assets()

# 4. واجهة البرنامج (Header & Personnel)
st.markdown("<div class='header-container'><h1>ASA Smart Mix Pro v2.0</h1><p><b>Multi-criteria analysis of eco-efficient concrete...</b></p></div>", unsafe_allow_html=True)

# عرض معلومات المشرفين (هامة جداً للمناقشة)
c1, c2 = st.columns(2)
with c1: st.info("🎓 Researcher: Aya Mohammed Sanad Aboud")
with c2: st.info("👨‍🏫 Supervisors: Prof. Ahmed Tahwia & Assoc. Prof. Asser El-Sheikh")

# 5. التبويبات (بما فيها الـ AI Optimizer الجديد)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Prediction", "🌱 Sustainability", "🔍 Validation", "🚀 AI Optimizer", "📝 Feedback"])

# (هنا يوضع الكود البرمجي لكل تبويب كما شرحنا سابقاً)
# ...

st.markdown(f"<p class='footer-text'>© {datetime.now().year} Aya Sanad | Master's Thesis Project</p>", unsafe_allow_html=True)
