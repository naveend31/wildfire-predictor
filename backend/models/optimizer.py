def optimize_resources(fires, total_air_tankers=10, total_ground_crews=50):
    """
    A simple continuous allocation heuristic. 
    In a real scenario, this would use PuLP for linear integer programming.
    Given hackathon limits, we do a greedy allocation based on 'threat score'.
    """
    allocations = []
    
    # Calculate a threat score for each fire based on current severity and wind
    scored_fires = []
    total_threat = 0
    for fire in fires:
        threat = (fire["severity"] * 2) + (fire["wind_speed"] * 0.5)
        scored_fires.append({"fire": fire, "threat": threat})
        total_threat += threat
        
    # Sort by threat descending
    scored_fires.sort(key=lambda x: x["threat"], reverse=True)
    
    remaining_tankers = total_air_tankers
    remaining_crews = total_ground_crews
    
    for sf in scored_fires:
        threat_ratio = sf["threat"] / total_threat if total_threat > 0 else 0
        
        # Proportional allocation
        allocate_tankers = int(total_air_tankers * threat_ratio)
        allocate_crews = int(total_ground_crews * threat_ratio)
        
        # Ensure we allocate at least 1 if threat > 0 and resources available
        if allocate_tankers == 0 and remaining_tankers > 0 and sf["threat"] > 5:
            allocate_tankers = 1
        if allocate_crews == 0 and remaining_crews > 0:
            allocate_crews = 1
            
        # Bound limits
        allocate_tankers = min(allocate_tankers, remaining_tankers)
        allocate_crews = min(allocate_crews, remaining_crews)
        
        remaining_tankers -= allocate_tankers
        remaining_crews -= allocate_crews
        
        allocations.append({
            "fire_id": sf["fire"]["id"],
            "air_tankers": allocate_tankers,
            "ground_crews": allocate_crews,
            "threat_score": sf["threat"]
        })
        
    return {
        "allocations": allocations,
        "remaining_tankers": remaining_tankers,
        "remaining_crews": remaining_crews
    }
