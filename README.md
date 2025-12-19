# 🚕 Ride Demand Forecasting and Driver Allocation

This project is a **full-stack machine learning application** that predicts **hourly ride demand** based on time and weather-related inputs.  
It provides clear demand insights through a **clean UI, prediction summary, and interactive visualizations**.

The main goal of this project is to understand how **ride-hailing platforms forecast demand** and how such predictions can support **better planning and decision-making**.

---

## 🌐 Live Demo

👉 **Live Application**  
https://<your-render-app-name>.onrender.com

*(Deployed using Docker and Render)*

---

## 🖼️ Application UI Preview

### 🔹 Input Form (Before Prediction)
![Input UI](screenshots/input-ui.png)

### 🔹 Prediction Result with Summary & Visualization
![Output UI](screenshots/output-ui.png)

> The screenshots show the glassmorphism UI, input form, prediction summary, and hourly demand trend chart.

---

## 🔍 What This Project Does

- Accepts **time-based and weather-based inputs**
- Predicts **hourly ride demand**
- Displays:
  - predicted demand (rides/hour)
  - short explanation of the prediction
  - input summary
  - 24-hour demand pattern chart
- Handles invalid inputs with **friendly error messages**

---

## 🧠 Input Features

The model uses the following inputs:

- Year  
- Month  
- Day of Week  
- Hour of Day  
- Temperature (°C)  
- Humidity (%)  
- Wind Speed (km/h)  
- Weather Condition (Clear, Cloudy, Rainy, Fog, Snow)

These features were selected because **ride demand is highly influenced by time patterns and weather conditions**.

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- XGBoost
- Pandas, NumPy

### Frontend
- HTML (Jinja2 Templates)
- Tailwind CSS
- Chart.js

### DevOps
- Docker
- Render
- GitHub

---

## 📊 Machine Learning Model

- Model: **XGBoost Regressor**
- Task: Hourly ride demand prediction
- Model Performance:
  - MAE
  - RMSE
  - R² Score (~86%)

The model was trained on **simulated ride demand data** designed to reflect realistic daily and weather-based patterns.

---

## 📈 Output & Visualization

- Predicted ride demand (rides/hour)
- Human-readable prediction explanation
- Input summary for transparency
- Interactive **24-hour demand trend chart**

This helps users understand **how demand varies throughout the day**.

---

## 🧩 Project Structure
Ride-Demand-Forecasting/
│
├── app/
│ ├── main.py
│ ├── templates/
│ │ └── index.html
│ ├── services/
│ │ ├── predictor.py
│ │ ├── clustering.py
│ │ └── allocation.py
│
├── model/
│ ├── demand_model.pkl
│ ├── kmeans_model.pkl
│ └── cluster_scaler.pkl
│
├── requirements.txt
├── Dockerfile
├── README.md
└── screenshots/


---

## 🚀 Run Locally (Without Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload


Open in browser:

http://127.0.0.1:8000

🐳 Run Using Docker
docker build -t ride-demand-app .
docker run -p 8000:8000 ride-demand-app

☁️ Deployment

The application is containerized using Docker and deployed on Render, making it accessible as a public web service directly from GitHub.

