import random
import uuid

def generate_mock_fires(num_fires=5, center_lat=38.5, center_lng=-121.0, spread=2.0):
    """
    Generates mock active fires around a central latitude/longitude.
    By default, near Sacramento, CA area for demonstration.
    """
    fires = []
    for _ in range(num_fires):
        lat = center_lat + random.uniform(-spread, spread)
        lng = center_lng + random.uniform(-spread, spread)
        
        # Base severity from 1 to 10
        severity = random.randint(1, 10)
        
        # Wind direction in degrees (0-360), speed in km/h
        wind_dir = random.uniform(0, 360)
        wind_speed = random.uniform(5, 45)
        
        fires.append({
            "id": str(uuid.uuid4()),
            "lat": lat,
            "lng": lng,
            "severity": severity,
            "wind_dir": wind_dir,
            "wind_speed": wind_speed,
            "name": f"Mock Fire {random.randint(100, 999)}",
            "base_radius_km": severity * 0.5 # Current size
        })
    return fires

# Pre-generate a static set for the session so it doesn't jump around
ACTIVE_FIRES = generate_mock_fires()

def get_active_fires():
    return ACTIVE_FIRES
