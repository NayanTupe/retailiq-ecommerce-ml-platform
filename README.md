# 🚀 RetailIQ — AI Powered E-commerce Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-orange)
![Status](https://img.shields.io/badge/Project-Production%20Ready-brightgreen)
![Deployment](https://img.shields.io/badge/Live%20SaaS-Active-purple)

---

# 🌐 LIVE LINKS

## 🚀 Backend API (Render)
👉 https://retailiq-api-yzso.onrender.com

## 💻 Frontend Dashboard (Vercel)
👉 https://retailiq-dashboard-frontend.vercel.app/

---

# 🔥 PROJECT OVERVIEW

RetailIQ is a **production-grade AI SaaS platform** that predicts customer churn and provides real-time analytics for e-commerce businesses.

It includes:

✔ Machine Learning Churn Prediction  
✔ Customer Segmentation (KMeans)  
✔ Analytics Dashboard APIs  
✔ React SaaS Frontend  
✔ FastAPI Backend  
✔ Production Deployment (Render + Vercel)

---

# 🎯 BUSINESS PROBLEM

E-commerce businesses face:

- Customer churn prediction issues
- Lack of customer insights
- Poor retention strategies
- Low customer lifetime value

👉 RetailIQ solves this using AI + real-time analytics.

---

# ⚙️ TECH STACK

## Backend
- FastAPI
- Python
- Scikit-learn
- Pandas
- Joblib

## Frontend
- React (Vite)
- Axios
- Framer Motion
- Recharts

## Deployment
- Render (Backend)
- Vercel (Frontend)
- GitHub (Version Control)

---

# 🧠 MACHINE LEARNING PIPELINE

Data Collection
↓
Data Cleaning
↓
Feature Engineering
↓
Model Training (Random Forest)
↓
Model Evaluation
↓
API Deployment (FastAPI)


---

# 🚀 API ENDPOINTS

| Method | Endpoint | Description |
|------|----------|-------------|
| GET | `/` | Health Check |
| GET | `/analytics/summary` | Dashboard KPIs |
| GET | `/analytics/segments` | Customer Segments |
| GET | `/analytics/churn-by-membership` | Churn Analytics |
| POST | `/predict/churn` | Predict Customer Churn |

---

# 🔮 SAMPLE REQUEST

```json
{
  "age": 28,
  "total_spend": 5000,
  "items_purchased": 6,
  "average_rating": 4
}

SAMPLE RESPONSE
{
  "churn_prediction": "No",
  "churn_probability": 29.15,
  "risk_level": "Low Risk"
}


# KEY FEATURES
Real-time ML Prediction API
Business Intelligence Dashboard
Customer Segmentation Engine
Production-ready FastAPI backend
React SaaS UI (Streamlit-like design)
Scalable architecture

SYSTEM ARCHITECTURE

React Frontend (Vercel)
        ↓
FastAPI Backend (Render)
        ↓
Machine Learning Model
        ↓
Feature Engineering Layer

python -m uvicorn api.main:app --reload

🔥 HIGHLIGHTS

✔ End-to-End AI SaaS System
✔ Real Production Deployment
✔ ML Model (Leakage Safe)
✔ FastAPI REST APIs
✔ React Dashboard UI
✔ Scalable Architecture

🚀 FUTURE IMPROVEMENTS
JWT Authentication
User Login System
Real-time streaming analytics
Docker deployment
CI/CD pipeline
Model retraining automation



AUTHOR
Nayan Tupe