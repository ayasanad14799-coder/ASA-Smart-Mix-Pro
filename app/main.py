import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 1. إعدادات الصفحة والهوية الأكاديمية الرسمية
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI Optimizer", layout="wide", page_icon="🏗️")

# دالة إرسال البيانات إلى Google Form (الربط المضمون 100%)
def send_to_google_form(data):
    # رابط الإرسال الخاص بالاستمارة بتاعتك
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfcSRu1cYGpJtMEX3i09-PihlEgkek2pWWmNHXDnLOQrGsgSQ/formResponse"
    
    # خريطة البيانات بناءً على الرابط اللي بعتيه (الـ Entry IDs)
    payload = {
        "entry.1599455160": data['Cement'],
        "entry.359753595": data['Water'],
        "entry.2089487269": data['NCA'],
        "entry.581408310": data['NFA'],
        "entry.402911999": data['RCA_P'],
        "entry.2027878370": data['MRCA_P'],
        "entry.834926487": data['SF'],
        "entry.1854682480": data['FA'],
        "entry.1224546954": data['Fiber'],
        "entry.1438579923": data['W_C'],
        "entry.577250201": data['SP'],
        "entry.340296413": data['Strength'],
        "entry.2013040846": data['STS'],
        "entry.895159496": data['EM'],
        "entry.422145962": data['CO2'],
        "entry.1912821133": data['Cost'],
        "entry.1503898770": data['Sustainability'],
        "entry.1275091872": data['Rank'],
        "entry.1583578049": data['Type'],
        "entry.1785868407": "Researcher_Sync" # خانة التوثيق الأخيرة
    }
    
    try:
        response = requests.post(form_url, data=payload)
        return response.status_code == 200
    except:
        return False

# تنسيق CSS احترافي (الخط Times New Roman، التنسيقات، والألوان)
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin-bottom: 5px; }
    .thesis-title { 
        color: #222; 
        text-align: center; 
        font-family: "Times New Roman", Times, serif; 
        font-size: 22px; 
        font-weight: bold; 
        border-bottom: 3px solid #004a99; 
        padding-bottom: 15px; 
        margin-bottom: 25px; 
        line-height: 1.6; 
    }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .doc-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-right: 6px solid #004a99; margin-bottom: 15px; }
    .optimizer-card { background-color: #f1f8e9; padding: 25px; border-radius: 15px; border: 2px solid #2e7d32; }
    .footer-text { text-align: center; color: #666; font-size: 0.9em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن وتنسيق الشعارات
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("<br>", unsafe_allow_html=True)
        logo_left, spacer, logo_right = st.columns([1, 2.5, 1])
        with logo_left: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=115)
        with logo_right: st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=115)
        
        st.markdown("<h1 style='text-align: center; color: #004a99; font-weight: bold;'>ASA-Smart-Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)
        
        with st.form("login"):
            key = st.text_input("Enter Access Key", type="password")
            if st.form_submit_button("Start Research Session"):
                if key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 3. تحميل الأصول والموديل
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

# 4. الهيدر الرئيسي
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c
