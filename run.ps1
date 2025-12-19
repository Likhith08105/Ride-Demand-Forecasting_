# Ride Demand Forecasting - Startup Script
# This script will set up the environment and run the application

Write-Host "🚕 Ride Demand Forecasting - Starting Application" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q

# Check if ML models exist
Write-Host "🔍 Verifying ML models..." -ForegroundColor Yellow
$modelsExist = @(
    "model/demand_model.pkl",
    "model/kmeans_model.pkl",
    "model/cluster_scaler.pkl"
)

$allModelsPresent = $true
foreach ($model in $modelsExist) {
    if (Test-Path $model) {
        Write-Host "✓ Found: $model" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $model" -ForegroundColor Red
        $allModelsPresent = $false
    }
}

if (-not $allModelsPresent) {
    Write-Host "⚠️  Some ML models are missing. Training new models..." -ForegroundColor Yellow
    python model/train_model.py
}

# Run the application
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Green
Write-Host "📍 Navigate to: http://localhost:8000" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
