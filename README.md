**Ride Demand Forecasting**

A compact, interview-ready internal tool that predicts hourly ride demand using a trained XGBoost model and clusters areas into demand zones. The app is built for internal operations (dispatch/fleet planning), not for end users.

**Why this project**: it demonstrates a full end-to-end ML workflow — feature engineering, model inference, a lightweight backend API, and a polished frontend that visualizes predictions. It's intentionally simple and production-conscious (no overclaims).

**Key Features**
- **Prediction**: XGBoost model predicts rides/hour from time & weather features.
- **Zone classification**: K-Means classifies zones into Low/Medium/High demand.
- **Frontend**: Single-page UI (Tailwind + Chart.js) that submits inputs and shows results.
- **Backend**: FastAPI serves the UI and prediction API (`/predict`), plus `/history` for in-memory recent predictions.
- **In-memory history**: Keeps last 10 predictions (timestamp, inputs, prediction, zone) — no DB required for now.

**Project Layout (important files)**
- `app/main.py` — FastAPI app and endpoints (`/`, `/predict`, `/history`).
- `app/templates/index.html` — Pre-built frontend (DO NOT modify unless you want UX changes).
- `app/services/predictor.py` — Loads `model/demand_model.pkl` and predicts.
- `app/services/clustering.py` — Loads `model/kmeans_model.pkl` and `model/cluster_scaler.pkl`.
- `model/` — Pre-trained model files (included): `demand_model.pkl`, `kmeans_model.pkl`, `cluster_scaler.pkl`.
- `requirements.txt` — Python dependencies.

**What I removed**
- `run.ps1` — a Windows convenience script. You asked to remove it; the project runs fine with the commands below.

**Quick Start (local, Windows PowerShell)**

1. Open PowerShell and activate the venv (if you have one):

```powershell
cd "C:\Users\nares\Downloads\RESUME\Ride Demand Forecasting"
.\venv\Scripts\Activate.ps1
```

2. Install dependencies (first time only):

```powershell
pip install -r requirements.txt
```

3. Start the FastAPI server:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

4. Open: `http://localhost:8000`

**Quick Start (Linux/macOS / generic)**

```bash
cd "<path-to-project>"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**How to use the app**
- Fill the form on the page (year, month, day_of_week, hour, temperature, humidity, wind_speed, weather condition).
- Click **Predict Demand** — the frontend calls `/predict` and shows:
  - Predicted rides/hour
  - Zone classification
  - Input summary and an hourly demand chart
- Recent predictions appear in the "Recent Predictions" section (in-memory history). The history is returned by `/history`.

**Notes about predictions**
- The model uses a simulated `distance_km` (random 3–12 km) because the UI does not collect distance. This is a conscious design choice for the MVP. You can replace it by adding a distance input if you want more deterministic behavior.
- Predictions are produced by the included `model/demand_model.pkl` — do not overwrite unless retraining intentionally.

**API reference (quick)**
- `GET /` — returns the UI
- `POST /predict` — expects JSON body with the input fields (see `app/main.py` `PredictionRequest`) and returns prediction result JSON
- `GET /history` — returns last (up to 10) predictions stored in memory

Example `POST /predict` payload (JSON):

```json
{
  "year": 2024,
  "month": 12,
  "day_of_week": 4,
  "hour": 18,
  "temperature": 25.0,
  "humidity": 65.0,
  "wind_speed": 5.0,
  "weather_condition": "Clear"
}
```

**Why this is a good interview/portfolio piece**
- Shows an end-to-end ML pipeline (data → model → serving → frontend) without overclaiming.
- Demonstrates practical engineering: API design, templating, front-end visualization, and lightweight state management (in-memory history).
- Easy to explain and extend (add DB later, add logging/metrics, or dockerize).

**Next realistic improvements (resume-friendly)**
- Add model metrics page (MAE/RMSE & feature importance) — shows ML evaluation skills.
- Persist predictions to a simple DB (SQLite/Postgres) — shows persistence & analytics.
- Add Dockerfile + `docker-compose.yml` for containerized testing and simple deployment.

If you want, I can add a concise `Dockerfile` and `docker-compose.yml` (no complex stacks) so the project is container-ready — this is small, realistic, and very resume-friendly.

**Contributing & contact**
- If you modify model files, update `app/services/predictor.py` accordingly.
- Keep `app/templates/index.html` design intact unless you want UI changes (logic hooks used by JS depend on specific element IDs).

---

If you'd like, I can also create a short `README` section showing one or two example predictions and model performance numbers (if you want to run `model/train_model.py` and output metrics). Want me to add a minimal `Dockerfile` next?