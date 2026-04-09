import math

def calculate_spread_polygon(fire, hours_ahead):
    """
    Simulates simple fire spread using wind vectors.
    Returns a GeoJSON Polygon representing the expected burn area.
    """
    lat = fire["lat"]
    lng = fire["lng"]
    base_radius = fire["base_radius_km"] # current size
    
    # Wind factors
    wind_dir = fire["wind_dir"]
    wind_speed = fire["wind_speed"]
    
    # Simple model: Fire grows radially at a base rate, but strongly in wind direction
    # base spread rate (km/h) based on severity
    base_spread_rate = 0.1 * fire["severity"] 
    
    # Wind driven spread rate (km/h)
    wind_spread_rate = (wind_speed * 0.05) 
    
    # Calculate offset of the fire center due to wind over 'hours_ahead'
    # Wind dir is meteorological (where wind comes from). Spread is opposite.
    spread_dir_rad = math.radians((wind_dir + 180) % 360)
    
    total_wind_dist = wind_spread_rate * hours_ahead
    total_base_dist = base_spread_rate * hours_ahead
    
    # 1 degree lat is approx 111 km. 1 degree lng is approx 111 * cos(lat) km.
    lng_factor = 111.0 * math.cos(math.radians(lat))
    lat_factor = 111.0
    
    # Center of the new ellipse
    center_offset_lat = (total_wind_dist * math.cos(spread_dir_rad)) / lat_factor
    center_offset_lng = (total_wind_dist * math.sin(spread_dir_rad)) / lng_factor
    
    new_center_lat = lat + center_offset_lat
    new_center_lng = lng + center_offset_lng
    
    # Major and minor axis of fire ellipse
    major_axis_km = base_radius + total_base_dist + (total_wind_dist / 2)
    minor_axis_km = base_radius + total_base_dist
    
    # Generate points for a polygon (ellipse approximation)
    points = []
    num_points = 36
    for i in range(num_points):
        angle = math.radians(i * (360 / num_points))
        
        # Calculate point on ellipse before rotation (aligned with axes)
        # We align the major axis with the wind direction
        x_km = minor_axis_km * math.cos(angle)
        y_km = major_axis_km * math.sin(angle)
        
        # Rotate by spread_dir_rad
        rot_x_km = x_km * math.cos(-spread_dir_rad) - y_km * math.sin(-spread_dir_rad)
        rot_y_km = x_km * math.sin(-spread_dir_rad) + y_km * math.cos(-spread_dir_rad)
        
        # Convert offset back to lat/lng
        p_lat = new_center_lat + (rot_y_km / lat_factor)
        p_lng = new_center_lng + (rot_x_km / lng_factor)
        points.append([p_lng, p_lat])
        
    # Close the loop
    points.append(points[0])
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [points]
        },
        "properties": {
            "fire_id": fire["id"],
            "hours_ahead": hours_ahead,
            "severity": fire["severity"]
        }
    }
