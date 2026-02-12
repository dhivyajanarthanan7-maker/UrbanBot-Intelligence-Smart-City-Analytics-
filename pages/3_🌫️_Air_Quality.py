import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from db import get_connection

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Air Quality AI Insights", layout="wide")

st.title("🌫️ Air Quality AI Insights")
st.caption("Dataset-driven AQI prediction, monitoring & comparison")

# ================= LOAD DATASET =================
@st.cache_data(ttl=600)
def load_dataset():
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()

        df = pd.read_sql("SELECT * FROM aqi_locations", conn)
        conn.close()

        df = df.dropna(subset=["state", "city", "station"])
        df.columns = df.columns.str.lower()

        return df

    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


df = load_dataset()

if df.empty:
    st.warning("Database not connected yet. Please check RDS.")
    st.stop()

# ================= LOCATION =================
st.subheader("📍 Location Selection")

col1, col2, col3 = st.columns(3)

state = col1.selectbox("State", sorted(df["state"].unique()))
cities = df[df["state"] == state]["city"].unique()
city = col2.selectbox("City", sorted(cities))
areas = df[df["city"] == city]["station"].unique()
area = col3.selectbox("Monitoring Station / Area", sorted(areas))

location_df = df[
    (df["state"] == state) &
    (df["city"] == city) &
    (df["station"] == area)
]

lat = location_df["latitude"].iloc[0]
lon = location_df["longitude"].iloc[0]

st.info(f"📌 {city}, {state} | 🌐 {lat}, {lon}")

# ================= POLLUTANTS =================
st.markdown("---")
st.subheader("🧪 Pollutant Inputs")

pollutants = ["pm2.5", "pm10", "no2", "so2", "co", "ozone", "nh3"]
values = {}

cols = st.columns(3)

for i, pol in enumerate(pollutants):
    pol_df = location_df[location_df["pollutant_id"].str.lower() == pol]

    if not pol_df.empty:
        options = sorted(pol_df["pollutant_avg"].dropna().unique())
        values[pol.upper()] = cols[i % 3].selectbox(pol.upper(), options)
    else:
        values[pol.upper()] = 0.0
        cols[i % 3].warning(f"{pol.upper()} data not available")

# ================= AQI CALCULATION =================
def calculate_aqi(pollutant_values):

    valid_values = [v for v in pollutant_values.values() if v is not None]

    if not valid_values:
        return None, "NO DATA", "#95a5a6"

    aqi = round(max(valid_values), 2)

    if aqi <= 50:
        return aqi, "GOOD", "#2ecc71"
    elif aqi <= 100:
        return aqi, "MODERATE", "#f1c40f"
    elif aqi <= 200:
        return aqi, "POOR", "#e67e22"
    else:
        return aqi, "SEVERE", "#e74c3c"

# ================= BUTTON =================
st.markdown("---")

if st.button("⚡ Predict AQI Level", use_container_width=True):

    aqi_value, category, color = calculate_aqi(values)

    if aqi_value is None:
        st.warning("No valid pollutant values.")
        st.stop()

    # ---------- SHOW RESULT ----------
    st.markdown("## 📊 AQI Result")

    c1, c2 = st.columns(2)
    c1.metric("AQI Value", round(aqi_value, 2))
    c2.markdown(f"<h3 style='color:{color};'>⚠ {category}</h3>", unsafe_allow_html=True)

    donut_df = pd.DataFrame({
        "Pollutant": list(values.keys()),
        "Value": list(values.values())
    })

    fig = px.pie(donut_df, names="Pollutant", values="Value", hole=0.55, title="Pollutant Contribution")
    st.plotly_chart(fig, use_container_width=True)

    # ---------- SAVE TO DATABASE ----------
    try:
        conn = get_connection()

        if conn is None:
            st.warning("Database not connected. Prediction not saved.")
        else:
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO air_quality_predictions
            (city, area, pm25, pm10, no2, so2, co, o3, nh3, aqi_value, aqi_category)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(insert_query, (
                city, area,
                values["PM2.5"], values["PM10"], values["NO2"],
                values["SO2"], values["CO"], values["OZONE"],
                values["NH3"], aqi_value, category
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ AQI prediction saved successfully")

    except Exception as e:
        st.error(f"Error saving prediction: {e}")
