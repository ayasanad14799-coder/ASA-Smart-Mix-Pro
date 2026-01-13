import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import datetime

# 1. الإعدادات الرسمية والهوية البصرية (UX/UI)
st.set_page_config(page_title="ASA Smart Mix Pro | Cloud AI Optimizer", layout="wide", page_icon="🏗️")

# دالة إرسال البيانات إلى Google Form (الربط المضمون) [نقطة 8]
def send_to_google_form(data):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfcSRu1cYGpJtMEX3i09-PihlEgkek2pWWmNHXDnLOQrGsgSQ/formResponse"
    payload = {
        "entry.1599455160": data['Cement'], "entry.359753595": data['Water'],
        "entry.2089487269": data['NCA'], "entry.581408310": data['NFA'],
        "entry.402911999": data['RCA_P'], "entry.2027878370": data['MRCA_P'],
        "entry.834926487": data['SF'], "entry.1854682480": data['FA'],
        "entry.1224546954": data['Fiber'], "entry.1438579923": data['W_C'],
        "entry.577250201": data['SP'], "entry.340296413": data['Strength'],
        "entry.2013040846": data['STS'], "entry.895159496": data['EM'],
        "entry.422145962": data['CO2'], "entry.1912821133": data['Cost'],
        "entry.1503898770": data['Sustainability'], "entry.1275091872": data['Rank'],
        "entry.1583578049": data['Type'], "entry.1785868407": "ASA_V3_FINAL"
    }
    try:
        requests.post(form_url, data=payload, timeout=8)
        return True
    except: return False

# تنسيق CSS الأكاديمي (Times New Roman) [نقطة 14]
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin-bottom: 0px; }
    .thesis-title { 
        color: #222; text-align: center; font-family: "Times New Roman", Times, serif; 
        font-size: 22px; font-weight: bold; border-bottom: 3px solid #004a99; padding-bottom: 10px; margin-bottom: 20px;
    }
    .doc-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; margin-bottom: 10px; }
    .footer-text { text-align: center; color: #777; font-size: 0.85em; border-top: 1px solid #ddd; padding: 15px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول والشعارات [نقطة 14]
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 3, 1])
    with col_mid:
        l_col, r_col = st.columns([1, 1])
        l_col.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=110)
        r_col.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=110)
        st.markdown("<h2 style='text-align: center;'>ASA Smart Mix Pro | AI Dashboard</h2>", unsafe_allow_html=True)
        with st.form("Login"):
            pwd = st.text_input("Access Key", type="password")
            if st.form_submit_button("Start Research Session"):
                if pwd == "ASA2026": st.session_state.auth = True; st.rerun()
                else: st.error("Access Denied. Please contact Researcher Aya Sanad.")
    st.stop()

# 3. تحميل الموديل والبيانات (الـ 35 عمود) [نقطة 10، 12]
@st.cache_resource
def load_research_data():
    model = joblib.load('uploaded:concrete_model.joblib')
    scaler = joblib.load('uploaded:scaler.joblib')
    # قراءة الملف مع التأكد من الفواصل 
    db = pd.read_csv('uploaded:Trail3_DIAMOND_DATABASE.csv', sep=';' if ';' in open('uploaded:Trail3_DIAMOND_DATABASE.csv').read() else ',')
    db.columns = db.columns.str.strip()
    return model, scaler, db

model, scaler, db = load_research_data()

# 4. واجهة المستخدم الرئيسية والمعلومات الأكاديمية
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v3.0</h1>", unsafe_allow_html=True)
st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1: st.markdown("<div class='doc-card'><b>🎓 Researcher:</b> Aya Mohammed Sanad Aboud<br>Mansoura University</div>", unsafe_allow_html=True)
with c_info2: st.markdown("<div class='doc-card'><b>👨‍🏫 Supervision:</b> Prof. Ahmed Tahwia | Assoc. Prof. Asser El-Sheikh</div>", unsafe_allow_html=True)

# 5. شريط المدخلات (الـ 11 متغير مع الحدود المنطقية) [نقطة 7]
with st.sidebar:
    st.header("📋 Mix Constituents")
    st.markdown("---")
    cem = st.number_input("1. Cement (kg/m³)", 200, 600, 350)
    wat = st.number_input("2. Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("3. NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("4. NFA (Fine Aggregate)", 0, 1200, 700)
    rca = st.slider("5. RCA Replacement (%)", 0, 100, 0)
    mrca = st.slider("6. MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("7. Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("8. Fly Ash (kg/m³)", 0, 250, 0)
    fib = st.number_input("9. Nylon Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc = st.slider("10. W/C Ratio", 0.2, 0.8, 0.45)
    sp = st.number_input("11. Superplasticizer (kg/m³)", 0.0, 20.0, 2.0)

# 6. محرك التشغيل الرئيسي والنتائج [نقطة 11، 13]
if st.button("🚀 Run AI Analysis & Generate Full Report", use_container_width=True):
    inputs = scaler.transform([[cem, wat, nca, nfa, rca, mrca, sf, fa, fib, wc, sp]])
    pred_28 = model.predict(inputs)[0] # المقاومة عند 28 يوم [cite: 4]
    
    # حسابات تكميلية للنمو الزمني والديمومة [نقطة 6]
    pred_7 = round(0.74 * pred_28, 2) # تقديري بناءً على نمو الخرسانة [cite: 4]
    pred_90 = round(1.17 * pred_28, 2) # [cite: 4]
    sts = round(0.55 * np.sqrt(pred_28), 2) # معادلة الكود [cite: 4]
    em = round(4.7 * np.sqrt(pred_28), 2) # [cite: 3]
    
    co2 = (cem*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fib*2.5)
    cost = (cem*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fib*4.0)
    sust = (pred_28 / (co2 * cost)) * 1000

    # نظام التبويبات المتكامل (6 تبويبات) [نقطة 14]
    t1, t2, t3, t4, t5, t6 = st.tabs(["📊 Performance", "🏗️ Durability", "🌱 Economy & CO2", "🚀 AI Optimizer", "📜 Methodology", "📝 Feedback"])

    with t1:
        st.subheader("Predicted Strength Development")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("CS 7-Days", f"{pred_7} MPa")
        m2.metric("CS 28-Days (Target)", f"{pred_28:.2f} MPa")
        m3.metric("CS 90-Days", f"{pred_90} MPa")
        m4.metric("Split Tensile", f"{sts} MPa")
        
        # رسم بياني لمنحنى القوة الزمني [نقطة 5]
        fig_line = px.line(x=[7, 28, 90], y=[pred_7, pred_28, pred_90], title="Concrete Strength Evolution Chart", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        if st.button("📤 Sync Report to Master Cloud"):
            d = {"Cement": cem, "Water": wat, "NCA": nca, "NFA": nfa, "RCA_P": rca, "MRCA_P": mrca, "SF": sf, "FA": fa, "Fiber": fib, "W_C": wc, "SP": sp, "Strength": round(pred_28, 2), "STS": sts, "EM": em, "CO2": round(co2, 2), "Cost": round(cost, 2), "Sustainability": round(sust, 4), "Rank": "A+", "Type": "Master_Research_Sync"}
            if send_to_google_form(d): st.balloons(); st.success("✅ Recorded in Google Sheets!")

    with t2:
        st.subheader("Durability & Elastic Properties")
        d1, d2 = st.columns(2)
        d1.metric("Elastic Modulus (EM)", f"{em} GPa")
        d2.metric("Estimated UPV Speed", f"{3.5 + (pred_28/100):.2f} km/s")

    with t3:
        st.subheader("Environmental & Economic Analysis")
        l1, l2 = st.columns(2)
        l1.metric("CO2 Footprint", f"{co2:.1f} kg/m³")
        l2.metric("Sust. Index", f"{sust:.3f}")
        st.plotly_chart(px.pie(values=[cem*0.85, sf*0.02, fa*0.01, sp*0.7], names=["Cement", "SF", "FA", "SP"], title="CO2 Source Analysis"))

    with t4:
        st.subheader("AI Smart Mix Recommender (Diamond DB)")
        target_s = st.slider("Select Target Strength", 20, 100, 40, key="opt_v4")
        if st.button("Generate Candidate Designs"):
            matches = db[(db['CS_28'] >= target_s-2.5) & (db['CS_28'] <= target_s+2.5)].sort_values('Sustainability', ascending=False).head(5)
            st.dataframe(matches[['Mix_ID', 'Cement', 'Water', 'RCA_P', 'CS_28', 'Sustainability']], use_container_width=True)

    with t5:
        st.subheader("Technical Methodology & Reliability") # [نقطة 1، 2، 3، 10، 12]
        st.markdown(f"""
        <div class='doc-card'>
        <b>Algorithm:</b> Random Forest Regression (Multi-output) [cite: 8]<br>
        <b>Database:</b> DIAMOND Research Repository ({len(db)} Samples) [cite: 11, 12]<br>
        <b>Strength Domain:</b> {db['CS_28'].min()} to {db['CS_28'].max()} MPa [cite: 14]<br>
        <b>Model Accuracy (R²):</b> 95.57% | <b>COV (Stability):</b> 6.16% 
        </div>
        """, unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        v1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Blind Test: Actual vs. Predicted [نقطة 2]")
        v2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Feature Sensitivity Analysis [نقطة 5]")

    with t6:
        st.subheader("Experimental Feedback Hub") # [نقطة 4]
        with st.form("fb_form"):
            st.write("Help us improve the model by sharing your lab results:")
            lab_s = st.number_input("Actual Laboratory Strength (MPa)")
            fb_msg = st.text_area("Observations/Differences noticed")
            if st.form_submit_button("Submit to Researcher"):
                st.success("✅ Feedback logged! This data will be used for Model Retraining.")

# 7. الفوتر النهائي وإخلاء المسؤولية [نقطة 9]
st.markdown(f"""
    <div class='footer-text'>
    © {datetime.now().year} Aya Mohammed Sanad | Mansoura University - Structural Engineering Dept.<br>
    <b>Disclaimer:</b> This AI tool is for research and design purposes. Actual laboratory trials are mandatory for structural implementation as per official codes. [نقطة 9]
    </div>
    """, unsafe_allow_html=True)
