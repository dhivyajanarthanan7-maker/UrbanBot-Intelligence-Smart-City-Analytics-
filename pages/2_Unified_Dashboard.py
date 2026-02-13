import streamlit as st
import pandas as pd
import mysql.connector
from db import get_connection

# ================= PAGE CONFIG (ONLY ONCE & FIRST) =================
st.set_page_config(
    page_title="Unified City Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart City – Unified Dashboard")
st.caption("Live city status powered by integrated AI modules")
st.divider()

# ================= SAFE DB FETCH FUNCTION =================
def fetch_one(query):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result and result[0] is not None else 0
    except Exception as e:
        st.warning("Database temporarily unavailable...")
        return 0

# ================= KPI METRICS =================
st.subheader("🚨 City Status Overview")

col1, col2, col3, col4, col5 = st.columns(5)

# Accidents today
accidents_today = fetch_one("""
    SELECT COUNT(*) FROM accident_events
    WHERE DATE(created_at) = CURDATE()
""")

# Congested roads
congested_roads = fetch_one("""
    SELECT COUNT(*) FROM traffic_events
    WHERE congestion_level IN ('HIGH', 'SEVERE')
""")

# High crowd zones
high_crowd_zones = fetch_one("""
    SELECT COUNT(*) FROM crowd_events
    WHERE crowd_level IN ('HIGH', 'VERY HIGH')
""")

# Average AQI
avg_aqi = fetch_one("""
    SELECT ROUND(AVG(aqi_value), 1)
    FROM air_quality_predictions
""")

# Complaints
total_complaints = fetch_one("""
    SELECT COUNT(*) FROM citizen_complaints
""")

negative_complaints = fetch_one("""
    SELECT COUNT(*) FROM citizen_complaints
    WHERE sentiment = 'NEGATIVE'
""")

negative_percent = (
    round((negative_complaints / total_complaints) * 100, 1)
    if total_complaints > 0 else 0
)

# Metrics UI
col1.metric("🚑 Accidents Today", accidents_today)
col2.metric("🚦 Congested Roads", congested_roads)
col3.metric("👥 High Crowd Zones", high_crowd_zones)
col4.metric("🌫️ Avg AQI", avg_aqi if avg_aqi else "N/A")
col5.metric("📝 Negative Complaints", f"{negative_percent}%")

st.divider()

# ================= CRITICAL ALERTS =================
st.subheader("⚠️ Critical Alerts")

alerts = []

if accidents_today > 10:
    alerts.append("High number of road accidents detected today")

if congested_roads > 5:
    alerts.append("Severe traffic congestion in multiple areas")

if high_crowd_zones > 3:
    alerts.append("Overcrowding detected in public locations")

if avg_aqi and avg_aqi > 150:
    alerts.append("Poor air quality – public health advisory required")

if negative_percent > 50:
    alerts.append("High negative sentiment in citizen complaints")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No critical alerts at the moment")

st.divider()

# ================= RISK SNAPSHOT =================
st.subheader("📈 Risk Snapshot")

risk_data = {
    "Accidents": min(accidents_today, 5),
    "Traffic": min(congested_roads, 5),
    "Crowd": min(high_crowd_zones, 5),
    "Air Quality": min(int(avg_aqi / 50) if avg_aqi else 0, 5),
    "Sentiment": min(int(negative_percent / 20), 5)
}

df = pd.DataFrame.from_dict(
    risk_data, orient="index", columns=["Risk Level"]
)

st.bar_chart(df)

st.divider()

# ================= SUMMARY =================
st.subheader("🧠 Decision Summary")

st.markdown("""
- Accident and traffic risks are monitored in real time
- Crowd density alerts help prevent unsafe gatherings
- Air quality data drives health advisories
- Citizen complaints highlight service-level issues
""")

st.success("Unified dashboard successfully integrated with live database data.")
