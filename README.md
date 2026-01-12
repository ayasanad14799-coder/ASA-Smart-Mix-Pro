# 🏗️ ASA Smart Mix Pro (v2.0)
### **AI-Powered Multi-Criteria Optimization for Eco-Efficient Concrete**

<div align="center">

![Logo](https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/main/LOGO.png)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**Advanced Predictive Model for Sustainable Concrete using Gradient Boosting Regression**

[العربية](README.md) | [English](README_EN.md)

</div>

---

## 🎓 Research Identity | الهوية البحثية
* **Researcher:** Aya Mohammed Sanad Aboud
* **Supervisors:** * Prof. Ahmed Tahwia
  * Assoc. Prof. Asser El-Sheikh
* **Thesis Title:** Multi-criteria analysis of eco-efficient concrete from Technical, Environmental and Economic aspects.
* **Institution:** Mansoura University - Faculty of Engineering.

---

## 📊 Scientific Validation | التحقق العلمي
Below are the performance metrics of the AI model based on the "Diamond Database" (1,243 mixes):

<div align="center">
  <img src="https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/main/accuracy_plot.png" width="400" alt="Accuracy Plot">
  <img src="https://raw.githubusercontent.com/ayasanad14799-coder/ASA-Smart-Mix2/main/feature_importance.png" width="400" alt="Feature Importance">
</div>

* **Prediction Accuracy (R²):** 95.3%
* **Key Influencers:** Cement, W/C Ratio, and Silica Fume.

---

## 🔬 Study Variables | المتغيرات المدروسة (11 Inputs)
Unlike standard models, this system analyzes 11 critical parameters:
1. **Cement** | 2. **Water** | 3. **NCA** | 4. **NFA**
5. **RCA Replacement (%)** | 6. **MRCA Replacement (%)**
7. **Silica Fume** | 8. **Fly Ash** | 9. **Nylon Fiber**
10. **W/C Ratio** | 11. **Superplasticizer**

---

## 📁 Project Structure | هيكل المشروع
```text
ASA-Smart-Mix-Pro/
├── app/              # Web Interface (main.py)
├── data/             # Diamond Database (CSV)
├── models/           # Trained Models (.joblib)
├── docs/             # Laboratory Photos & Methodology
└── requirements.txt  # Libraries (Streamlit, Scikit-learn, etc.)
🚀 How to Run | طريقة التشغيل
# Clone the repository
git clone [https://github.com/ayasanad14799-coder/ASA-Smart-Mix-Pro.git](https://github.com/ayasanad14799-coder/ASA-Smart-Mix-Pro.git)
# Install dependencies
pip install -r requirements.txt
# Run the app
streamlit run app/main.py
© 2026 Aya Sanad | Master's Thesis Project
