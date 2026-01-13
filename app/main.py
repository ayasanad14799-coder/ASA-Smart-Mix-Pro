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

# الرابط المعتمد للربط السحابي (جوجل شيت)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwBM_r1UN07b9zQMhEanoL3yyNYla3MO7Nd1vMaLzBr83vAPpUKJ3kc4YkeggSVbvJ0RQ/exec"

# دالة إرسال البيانات (المطورة للربط السحابي الشامل)
def send_to_google_sheets(payload):
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        if "Success" in response.text:
            return True
        else:
            st.error(f"Google Error: {response.text}")
            return False
    except Exception as e:
        st.error(f"Network Connection Error: {str(e)}")
        return False

# تنسيق CSS احترافي (الخط Times New Roman، التنسيقات، والألوان)
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin-bottom: 5px; }
    .thesis-title { 
        color: #222; 
        text-align: center; 
        font-family: "Times New Roman", Times, serif; 
        font-size: 22px; /* يعادل حجم 16pt */
        font-weight: bold; 
        border-bottom: 3px solid #004a99; 
        padding-bottom: 15px; 
        margin-bottom: 25px; 
        line-height: 1.6; 
    }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .doc-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-right: 6px solid #004a99; margin-bottom: 15px; }
    .optimizer-card { background-color: #f1f8e9; padding: 25px; border-radius: 15px; border: 2px solid #2e7d32; }
    .warning-logic { color: #d32f2f; font-weight: bold; background-color: #ffcdd2; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .footer-text { text-align: center; color: #666; font-size: 0.9em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن وتنسيق الشعارات (شعار يمين وشعار يسار)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("<br>", unsafe_allow_html=True)
        # إنشاء 3 أعمدة داخلية: لوجو يسار، مسافة فارغة، لوجو يمين
        logo_left, spacer, logo_right = st.columns([1, 2.5, 1])
        with logo_left:
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=115)
        with logo_right:
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=115)
        
        st.markdown("<h1 style='text-align: center; color: #004a99; font-weight: bold;'>ASA-Smart-Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)
        
        with st.form("login"):
            key = st.text_input("Enter Access Key", type="password")
            if st.form_submit_button("Start Research Session"):
                if key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Access Denied. Please contact Researcher Aya Sanad.")
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

# 4. الهيدر الرئيسي للصفحة بعد الدخول
st.markdown("<h1 class='main-title'>ASA Smart Mix Pro v2.0</h1>", unsafe_allow_html=True)
st.markdown("<div class='thesis-title'>Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects</div>", unsafe_allow_html=True)

c_info1, c_info2 = st.columns(2)
with c_info1:
    st.markdown("""<div class='doc-card'><b>🎓 Master's Researcher:</b><br>Aya Mohammed Sanad Aboud<br>Faculty of Engineering - Mansoura University</div>""", unsafe_allow_html=True)
with c_info2:
    st.markdown("""<div class='doc-card'><b>👨‍🏫 Under the Supervision of:</b><br>Prof. Ahmed Tahwia<br>Assoc. Prof. Asser El-Sheikh</div>""", unsafe_allow_html=True)

# 5. المدخلات (Sidebar) - الـ 11 متغير بالترتيب الصارم
st.sidebar.header("📋 Mix Constituents")
with st.sidebar:
    st.markdown("---")
    cement = st.number_input("1. Cement (kg/m³)", 200, 600, 350)
    water = st.number_input("2. Water (kg/m³)", 100, 300, 160)
    nca = st.number_input("3. NCA (Natural Coarse)", 0, 1500, 1100)
    nfa = st.number_input("4. NFA (Fine Aggregate)", 0, 1200, 700)
    rca_p = st.slider("5. RCA Replacement (%)", 0, 100, 0)
    mrca_p = st.slider("6. MRCA Replacement (%)", 0, 100, 0)
    sf = st.number_input("7. Silica Fume (kg/m³)", 0, 150, 0)
    fa = st.number_input("8. Fly Ash (kg/m³)", 0, 250, 0)
    fiber = st.number_input("9. Nylon Fiber (kg/m³)", 0.0, 10.0, 0.0)
    wc_ratio = st.slider("10. W/C Ratio", 0.20, 0.80, 0.45)
    sp = st.number_input("11. Superplasticizer (kg/m³)", 0.0, 20.0, 2.0)
    
    if wc_ratio > 0.6 and cement < 310:
        st.markdown("<div class='warning-logic'>⚠️ High W/C ratio detected!</div>", unsafe_allow_html=True)

# 6. محرك التشغيل الرئيسي (The Execution Engine)
st.markdown("---")
col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])
with col_btn_2:
    run_button = st.button("🚀 Run AI Analysis & Generate Report", use_container_width=True)

# الشرط: تظهر النتائج فقط عند الضغط على الزر
if run_button:
    # أ. التنبؤ والحسابات الفنية
    features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
    prediction = model.predict(scaler.transform(features))[0]
    
    sts_val = round(0.55 * np.sqrt(prediction), 2) # الشد
    em_val = round(4.7 * np.sqrt(prediction), 2)  # المرونة
    total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
    total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
    sust_score = (prediction / (total_co2 * total_cost)) * 1000
    rank_val = "A+" if sust_score > 4.5 else "A" if sust_score > 3.5 else "B"

    st.success("✅ Analysis Completed Successfully!")

    # ب. عرض النتائج في التبويبات الخمسة
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📝 Feedback"])

    with tab1:
        st.subheader("Predicted Mechanical Performance")
        c1, c2, c3 = st.columns(3)
        c1.metric("Compressive Strength (28d)", f"{prediction:.2f} MPa")
        c2.metric("Split Tensile (STS)", f"{sts_val} MPa")
        c3.metric("Elastic Modulus (EM)", f"{em_val} GPa")
        
        # زر الربط السحابي (20 عمود بأسماء مطابقة للـ Apps Script)
        if st.button("📤 Sync Full Report to Cloud"):
            payload = {
                "Cement": cement, "Water": water, "NCA": nca, "NFA": nfa, "RCA_P": rca_p, 
                "MRCA_P": mrca_p, "Silica_Fume": sf, "Fly_Ash": fa, "Nylon_Fiber": fiber, 
                "W_C": wc_ratio, "SP": sp, "CS_28": round(float(prediction), 2),
                "STS": sts_val, "EM": em_val, "CO2": round(total_co2, 2), "Cost": round(total_cost, 2),
                "Sustainability": round(sust_score, 5), "Rank": rank_val, "Type": "Manual_Run"
            }
            if send_to_google_sheets(payload): st.success("✅ Recorded in Google Sheets!")
            else: st.error("❌ Sync Failed. Check URL.")

        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
            theta=['Strength', 'Recycled-Agg', 'Multi-Cycle', 'Carbon-Safety'], fill='toself'
        ))
        st.plotly_chart(fig_radar, use_container_width=True)

    with tab2:
        st.subheader("Environmental & Economic Analysis")
        l1, l2 = st.columns(2)
        with l1:
            st.metric("Total CO2 Footprint", f"{total_co2:.1f} kg/m³")
            st.plotly_chart(px.pie(values=[cement*0.85, sf*0.02, fa*0.01, sp*0.7], names=["Cement", "SF", "FA", "SP"], hole=0.4))
        with l2:
            st.metric("Sustainability Index", f"{sust_score:.2f}")
            st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=sust_score, gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"}})))

    with tab3:
        st.subheader("Technical Reliability & Validation")
        st.write("**Domain of Applicability:** Model is valid for CS_28 range [6.4 - 100.5 MPa].")
        v_c1, v_c2 = st.columns(2)
        v_c1.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Model Accuracy Plot (R² ≈ 95.3%)")
        v_c2.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Feature Sensitivity Analysis")

    with tab4:
        st.markdown("<div class='optimizer-card'>", unsafe_allow_html=True)
        st.subheader("🚀 AI-Powered Mix Optimizer")
        req_strength = st.slider("Target Strength (MPa)", 20, 100, 40, key="opt_slider")
        if st.button("Generate Optimal Sustainable Design"):
            res = db[(db['CS_28'] >= req_strength - 3) & (db['CS_28'] <= req_strength + 3)].sort_values('Sustainability', ascending=False)
            if not res.empty:
                best = res.iloc[0]
                st.success(f"🏆 Best Eco-Mix Found: {best['Mix_ID']}")
                st.write(f"Cement: {best['Cement']} | Water: {best['Water']} | RCA: {best['RCA_P']}%")
            else: st.error("No exact matches found in database.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        st.subheader("Researcher Feedback Portal")
        with st.form("fb_form"):
            name = st.text_input("Name")
            err = st.number_input("Observed Lab Error %", 0.0, 100.0, 0.0)
            msg = st.text_area("Feedback/Observations")
            if st.form_submit_button("Submit to Cloud"):
                fb_payload = {"Cement": 0, "Water": 0, "NCA": 0, "NFA": 0, "RCA_P": 0, "MRCA_P": 0, "Silica_Fume": 0, "Fly_Ash": 0, "Nylon_Fiber": 0, "W_C": 0, "SP": 0, "CS_28": err, "STS": 0, "EM": 0, "CO2": 0, "Cost": 0, "Sustainability": 0, "Rank": "N/A", "Type": f"FB: {name} - {msg}"}
                if send_to_google_sheets(fb_payload): st.balloons(); st.success("Feedback Logged!")
                else: st.error("Sync error.")
else:
    # رسالة تظهر قبل ضغط المستخدم على زر Run
    st.info("👈 Please adjust the mix parameters in the sidebar and click 'Run AI Analysis' to see the report.")

# 7. الفوتر النهائي (Footer)
st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Master's Thesis Project | Mansoura University</div>", unsafe_allow_html=True)
