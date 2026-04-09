from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from data.mock_generator import get_active_fires
from models.spread_model import calculate_spread_polygon
from models.optimizer import optimize_resources

app = FastAPI(title="Spatio-Temporal Wildfire Predictor API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/fires")
def get_fires():
    """Return the current active fires."""
    return get_active_fires()

@app.get("/api/simulate")
def simulate_spread(hours: int = Query(..., ge=0, le=24)):
    """Return spread polygons based on requested +hours."""
    fires = get_active_fires()
    features = []
    for fire in fires:
        poly_feature = calculate_spread_polygon(fire, hours)
        features.append(poly_feature)
        
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/api/optimize")
def get_optimization(tankers: int = 10, crews: int = 50):
    """Return resource distribution to current active fires."""
    fires = get_active_fires()
    return optimize_resources(fires, total_air_tankers=tankers, total_ground_crews=crews)

from fastapi.staticfiles import StaticFiles
import os

# Serve the static frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
