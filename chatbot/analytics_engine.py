from .sql_agent import execute_query

# -------- Accident --------
def get_accident_insights():
    query = """
    SELECT city, area, severity, COUNT(*) as total_cases
    FROM accident_events
    WHERE DATE(created_at)=CURDATE()
    GROUP BY city, area, severity
    ORDER BY total_cases DESC
    """
    return execute_query(query)

# -------- Traffic --------
def get_traffic_insights():
    query = """
    SELECT city, area,
           AVG(vehicle_count) avg_vehicle,
           AVG(traffic_score) avg_score,
           congestion_level
    FROM traffic_events
    WHERE DATE(created_at)=CURDATE()
    GROUP BY city, area, congestion_level
    ORDER BY avg_score DESC
    """
    return execute_query(query)

# -------- AQI --------
def get_aqi_insights():
    query = """
    SELECT city, area,
           ROUND(AVG(aqi_value),2) avg_aqi,
           aqi_category
    FROM air_quality_predictions
    WHERE DATE(created_at)=CURDATE()
    GROUP BY city, area, aqi_category
    ORDER BY avg_aqi DESC
    """
    return execute_query(query)

# -------- Crowd --------
def get_crowd_insights():
    query = """
    SELECT city, area,
           AVG(crowd_count) avg_crowd,
           MAX(crowd_count) peak
    FROM crowd_events
    WHERE DATE(created_at)=CURDATE()
    GROUP BY city, area
    ORDER BY peak DESC
    """
    return execute_query(query)

# -------- Road Damage --------
def get_road_damage_insights():
    query = """
    SELECT city, area,
           SUM(damage_count) damages,
           severity
    FROM road_damage_events
    WHERE DATE(created_at)=CURDATE()
    GROUP BY city, area, severity
    ORDER BY damages DESC
    """
    return execute_query(query)
