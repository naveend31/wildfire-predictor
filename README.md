# Spatio-Temporal Wildfire Predictor & Optimizer 🔥🗺️

A Spatio-Temporal Big Data model designed to predict the 12-hour spread trajectory of active wildfires and optimize the deployment of national firefighting resources. Built natively with Python (FastAPI) and an interactive Vanilla JS / Leaflet dashboard to handle complex geospatial visualizations seamlessly.

## 🚀 Hackathon Problem Statement Addressed

Developed a Big Data model that integrates real-time satellite imagery (MODIS/VIIRS proxies), localized weather forecasts (wind vectors/speeds), and historical fire behavior to predict active wildfire trajectories. Includes a mathematical optimization component that recommends the allocation of limited national firefighting resources (air tankers, ground crews) directly to the highest-threat zones to minimize property damage and save lives.

## ✨ Key Features

1. **Spatio-Temporal Simulation Engine**: A mathematical backend model written in Python that takes current active fire radii and extrapolates geometric spread polygons over a 12-hour horizon based on wind speed and directional data.
2. **Resource Optimization Engine**: Ranks incoming active fires based on a continuous "Threat Score" (derived from size and wind multipliers) and dynamically allocates a finite pool of Air Tankers and Ground Crews utilizing proportional allocation mathematics.
3. **Interactive "Dark Mode" Dashboard**: A premium, responsive UI featuring dynamic sliders, real-time fetching, Leaflet Map integration, and custom CartoDB dark tiling.
4. **No Node.js Required**: The entire application is served natively from a Python FastAPI backend acting as both the API and the static file server for maximum deployment simplicity.

## 🛠️ Technology Stack

- **Backend / API Engine**: Python 3.13, FastAPI, Uvicorn
- **Spatial Mathematics**: `shapely`, `geojson`
- **Dashboard / Frontend**: HTML5, CSS3 (Custom Glassmorphism Design), Vanilla JavaScript (ES6)
- **Mapping**: Leaflet.js

## ⚙️ Installation & Running Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/wildfire-predictor.git
   cd wildfire-predictor/backend
   ```

2. **Set up Python Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Engine**
   ```bash
   python app.py
   ```

5. **Interact**
   Open your browser and navigate to `http://localhost:8000` to view the Spatio-Temporal Interface.
