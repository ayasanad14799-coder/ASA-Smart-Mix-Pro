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

# رابط الـ Google Apps Script للربط السحابي (الذي استخرجتِه)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwzWjzzmOs6dkEGvonbqatvG_vMTWTFV02OPBl8iO_f4WYQNGHdz6VZPh9e8nWdWHq0Gg/exec"

# دالة إرسال البيانات إلى Google Sheets
def send_to_google_sheets(payload):
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.status_code == 200
    except:
        return False

# تنسيق CSS احترافي لضبط الهوية البصرية (البولد، الألوان، والتقسيم)
st.markdown("""
    <style>
    .main-title { color: #004a99; text-align: center; font-weight: bold; font-size: 3em; margin-bottom: 5px; }
    .thesis-title { color: #222; text-align: center; font-size: 1.45em; font-weight: bold; border-bottom: 3px solid #004a99; padding-bottom: 15px; margin-bottom: 25px; line-height: 1.6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #004a99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .doc-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-right: 6px solid #004a99; margin-bottom: 15px; }
    .optimizer-card { background-color: #f1f8e9; padding: 25px; border-radius: 15px; border: 2px solid #2e7d32; }
    .warning-logic { color: #d32f2f; font-weight: bold; background-color: #ffcdd2; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .footer-text { text-align: center; color: #666; font-size: 0.9em; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الدخول الآمن وتنسيق الشعارات (المتناظر يمين ويسار)
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col_l, col_mid, col_r = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("<br>", unsafe_allow_html=True)
        # تنسيق الشعارات: واحد أقصى اليسار والآخر أقصى اليمين
        logo_left, spacer, logo_right = st.columns([1, 3, 1])
        with logo_left:
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/LOGO.png", width=125)
        with logo_right:
            st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/OIP.jfif", width=125)
        
        st.markdown("<h1 style='text-align: center; color: #004a99;'>ASA-Smart-Mix Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: bold;'>🔒 Secure Master's Research Portal</p>", unsafe_allow_html=True)
        
        with st.form("login"):
            key = st.text_input("Access Key", type="password")
            if st.form_submit_button("Enter Research System"):
                if key == "ASA2026":
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Access Denied. Please contact Researcher Aya Sanad.")
    st.stop()

# 3. تحميل الأصول (المسارات الاحترافية الجديدة)
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

# 4. واجهة العرض الرئيسية والهوية الأكاديمية
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
    
    # تحذير UX للمنطق الهندسي (نقطة 11 و 13)
    if wc_ratio > 0.6 and cement < 310:
        st.markdown("<div class='warning-logic'>⚠️ High W/C ratio with low Cement content detected!</div>", unsafe_allow_html=True)

# 6. التنبؤ والحسابات الأساسية
features = np.array([[cement, water, nca, nfa, rca_p, mrca_p, sf, fa, fiber, wc_ratio, sp]])
prediction = model.predict(scaler.transform(features))[0]

# معادلات الأثر البيئي والاقتصادي
total_co2 = (cement*0.85 + sf*0.02 + fa*0.01 + (nca+nfa)*0.005 + sp*0.7 + fiber*2.5)
total_cost = (cement*0.1 + sf*0.25 + fa*0.03 + nca*0.015 + nfa*0.012 + sp*1.5 + fiber*4.0)
sust_score = (prediction / (total_co2 * total_cost)) * 1000

# 7. الأقسام الخمسة (Tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Mechanical Results", "🌱 LCA & Economy", "🔍 Reliability & Validation", "🚀 AI Optimizer", "📝 Feedback"])

with tab1:
    st.subheader("Predicted Mechanical Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("Compressive Strength (28d)", f"{prediction:.2f} MPa")
    c2.metric("Split Tensile (ACI 318)", f"{(0.55 * np.sqrt(prediction)):.2f} MPa")
    c3.metric("Elastic Modulus (EC2)", f"{(4.7 * np.sqrt(prediction)):.2f} GPa")
    
    # زر رفع البيانات للشيت تلقائياً
    if st.button("🚀 Log Mix to Research Cloud"):
        payload = {
            "cement": cement, "water": water, "nca": nca, "nfa": nfa, "rca_p": rca_p, 
            "mrca_p": mrca_p, "sf": sf, "fa": fa, "fiber": fiber, "wc_ratio": wc_ratio, 
            "sp": sp, "prediction": round(float(prediction), 2), "total_co2": round(float(total_co2), 2), 
            "type": "Manual_Prediction"
        }
        if send_to_google_sheets(payload): st.success("✅ Mix Successfully Synced to Google Sheets!")
        else: st.error("❌ Sync Failed. Check Connection.")

    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[prediction/100, (100-rca_p)/100, (100-mrca_p)/100, (600-total_co2)/600],
        theta=['Strength', 'Recycled-Agg', 'Multi-Cycle', 'Carbon-Safety'], fill='toself'
    ))
    st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.subheader("Environmental Impact (LCA)")
    col_lca1, col_lca2 = st.columns(2)
    with col_lca1:
        st.metric("Total CO2 Footprint", f"{total_co2:.1f} kg/m³")
        st.plotly_chart(px.pie(values=[cement*0.85, sf*0.02, fa*0.01, sp*0.7, fiber*2.5], 
                               names=["Cement", "SF", "FA", "SP", "Fiber"], hole=0.4))
    with col_lca2:
        rank = "A+" if sust_score > 4.5 else "A" if sust_score > 3.5 else "B"
        st.metric("Sustainability Index", f"{sust_score:.2f} (Rank: {rank})")
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=sust_score, 
                                               gauge={'axis': {'range': [0, 6]}, 'bar': {'color': "#004a99"},
                                                      'steps': [{'range': [0, 2], 'color': "red"}, {'range': [2, 4], 'color': "yellow"}, {'range': [4, 6], 'color': "green"}]})))

with tab3:
    st.subheader("Technical Reliability & Validation")
    st.write("**Domain of Applicability:** Model is valid for CS_28 range [6.4 - 100.5 MPa].")
    v_c1, v_c2 = st.columns(2)
    with v_c1:
        st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/accuracy_plot.png", caption="Blind Test Results (R² ≈ 95.3%)")
        st.table(pd.DataFrame({"Metric": ["R² Score", "RMSE", "MAE"], "Value": ["0.953", "2.88 MPa", "2.14 MPa"]}))
    with v_c2:
        st.image("https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix-Pro/main/docs/feature_importance.png", caption="Sensitivity Analysis (Variable Influence)")
        st.info("💡 The model demonstrates high Robustness; minimal input variations result in logically consistent transitions in strength.")

with tab4:
    st.markdown("<div class='optimizer-card'>", unsafe_allow_html=True)
    st.subheader("🚀 AI-Powered Optimizer (Design Recommender)")
    st.write("Find the most sustainable mix from the Diamond Database (1,243 mixes) based on your target strength.")
    req_strength = st.slider("Target Strength (MPa)", 20, 100, 40)
    if st.button("Generate Optimal Sustainable Mix"):
        res = db[(db['CS_28'] >= req_strength - 3) & (db['CS_28'] <= req_strength + 3)].sort_values('Sustainability', ascending=False)
        if not res.empty:
            best = res.iloc[0]
            st.success(f"🏆 Optimal Eco-Mix Identified: {best['Mix_ID']}")
            o1, o2 = st.columns(2)
            with o1:
                st.write("**Recommended Mix (kg/m³):**")
                st.write(f"Cement: {best['Cement']} | Water: {best['Water']}")
                st.write(f"RCA: {best['RCA_P']}% | Silica Fume: {best['Silica_Fume']}")
            with o2:
                st.write("**Sustainability Metrics:**")
                st.write(f"CO2: {best['CO2']} kg/m³ | Sustainability Index: {best['Sustainability']}")
        else: st.error("No exact match found. Try a different range.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab5:
    st.subheader("Research Feedback Portal")
    with st.form("feedback"):
        u_name = st.text_input("Name (Researcher/Visitor)")
        u_err = st.number_input("Observed Error % (Laboratory vs AI)", 0.0, 100.0, 0.0)
        u_msg = st.text_area("Observations/Feedback")
        if st.form_submit_button("Submit to Researcher Cloud"):
            fb_payload = {"cement": 0, "water": 0, "nca": 0, "nfa": 0, "rca_p": 0, "mrca_p": 0, "sf": 0, "fa": 0, "fiber": 0, "wc_ratio": 0, "sp": 0, "prediction": u_err, "total_co2": 0, "type": f"FEEDBACK: {u_name} - {u_msg}"}
            if send_to_google_sheets(fb_payload):
                st.balloons(); st.success("Thank you! Feedback synced to Google Sheets.")
            else: st.error("Sync Failed.")

st.markdown(f"<div class='footer-text'>© {datetime.now().year} Aya Mohammed Sanad Aboud | Master's Thesis Project | Mansoura University</div>", unsafe_allow_html=True)
