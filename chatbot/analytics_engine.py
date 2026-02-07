from .sql_agent import execute_query

# =========================================================
# ACCIDENT INSIGHTS
# =========================================================
def get_accident_insights():

    query = """
    SELECT city, area, severity, COUNT(*) as total_cases
    FROM accident_events
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, area, severity
    ORDER BY total_cases DESC
    """

    return execute_query(query)


# =========================================================
# TRAFFIC INSIGHTS
# =========================================================
def get_traffic_insights():

    query = """
    SELECT city, area, 
           AVG(vehicle_count) as avg_vehicle_count,
           AVG(traffic_score) as avg_traffic_score,
           congestion_level,
           COUNT(*) as records
    FROM traffic_events
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, area, congestion_level
    ORDER BY avg_traffic_score DESC
    """

    return execute_query(query)


# =========================================================
# AIR QUALITY INSIGHTS
# =========================================================
def get_aqi_insights():

    query = """
    SELECT city, area,
           ROUND(AVG(pm25),2) as avg_pm25,
           ROUND(AVG(pm10),2) as avg_pm10,
           ROUND(AVG(aqi_value),2) as avg_aqi,
           aqi_category
    FROM air_quality_predictions
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, area, aqi_category
    ORDER BY avg_aqi DESC
    """

    return execute_query(query)


# =========================================================
# CROWD INSIGHTS
# =========================================================
def get_crowd_insights():

    query = """
    SELECT city, area, landmark,
           AVG(crowd_count) as avg_crowd,
           MAX(crowd_count) as peak_crowd,
           crowd_level,
           COUNT(*) as observations
    FROM crowd_events
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, area, landmark, crowd_level
    ORDER BY peak_crowd DESC
    """

    return execute_query(query)


# =========================================================
# ROAD DAMAGE INSIGHTS
# =========================================================
def get_road_damage_insights():

    query = """
    SELECT city, area,
           SUM(damage_count) as total_damages,
           severity,
           COUNT(*) as reports
    FROM road_damage_events
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, area, severity
    ORDER BY total_damages DESC
    """

    return execute_query(query)


# =========================================================
# CITIZEN COMPLAINT SENTIMENT
# =========================================================
def get_complaint_insights():

    query = """
    SELECT city,
           category,
           department,
           sentiment,
           priority,
           COUNT(*) as total_complaints
    FROM citizen_complaints
    WHERE DATE(created_at) = CURDATE()
    GROUP BY city, category, department, sentiment, priority
    ORDER BY total_complaints DESC
    """

    return execute_query(query)
