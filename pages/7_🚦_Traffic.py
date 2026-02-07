import os
import streamlit as st
import smtplib
from email.message import EmailMessage
from datetime import datetime
from ultralytics import YOLO
from PIL import Image
import numpy as np
import mysql.connector
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ================= CONFIG =================
MODEL_PATH = "models/Traffic_best.pt"

LOW_THRESHOLD = 8
HIGH_THRESHOLD = 18

DB_CONFIG = {
    "host": "localhost",
    "user": "urbanbot_user",
    "password": "UrbanBot@123",
    "database": "urban_bot"
}
# =========================================

# ============ CITY / AREA / GEO DATA ============
LOCATIONS = {
    "Chennai": {
        "T Nagar": (13.0418, 80.2341),
        "Anna Nagar": (13.0850, 80.2101),
        "Guindy": (13.0067, 80.2206)
    },
    "Mumbai": {
        "Andheri": (19.1197, 72.8468),
        "Bandra": (19.0596, 72.8295),
        "Dadar": (19.0178, 72.8478)
    },
    "Delhi": {
        "Connaught Place": (28.6315, 77.2167),
        "Saket": (28.5245, 77.2066)
    },
    "Bangalore": {
        "Whitefield": (12.9698, 77.7499),
        "Electronic City": (12.8452, 77.6600)
    },
    "Hyderabad": {
        "Madhapur": (17.4483, 78.3915),
        "Gachibowli": (17.4401, 78.3489)
    }
}
# ================================================

# ============ VEHICLE WEIGHTS ============
VEHICLE_WEIGHTS = {
    "bicycle": 0.3,
    "motorbike": 0.6,
    "auto rickshaw": 1.2,
    "rickshaw": 1.2,
    "car": 1.5,
    "taxi": 1.5,
    "pickup": 1.8,
    "van": 2.0,
    "suv": 2.0,
    "minibus": 2.5,
    "bus": 4.0,
    "truck": 4.5,
    "ambulance": 3.0,
    "policecar": 3.0
}
# ========================================

# ============ PAGE SETUP ============
st.set_page_config(page_title="Traffic Congestion – UrbanBot", layout="wide")
st.title("🚦 Traffic Congestion Monitoring – UrbanBot")
# ===================================

# ============ LOAD MODEL ============
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()
# ===================================

# ============ DB CONNECTION ============
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
# ======================================

# ============ EMAIL ALERT ============
def send_traffic_alert(city, area, lat, lon, score):
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_RECEIVER:
        st.warning("📧 Email alert skipped (email not configured)")
        return

    msg = EmailMessage()
    msg["Subject"] = "🚨 URBANBOT ALERT: HIGH TRAFFIC CONGESTION"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content(f"""
🚦 HIGH TRAFFIC CONGESTION DETECTED

City        : {city}
Area        : {area}
Latitude    : {lat}
Longitude   : {lon}
Traffic Score : {score}

Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Immediate traffic control required.
— UrbanBot
""")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
    server.quit()
# ===================================

# ============ LOCATION SELECTION ============
st.subheader("📍 Location Details")

city = st.selectbox("City", list(LOCATIONS.keys()))
area = st.selectbox("Area", list(LOCATIONS[city].keys()))

latitude, longitude = LOCATIONS[city][area]

st.info(f"📌 {city} – {area}")
st.text_input("Latitude", latitude, disabled=True)
st.text_input("Longitude", longitude, disabled=True)
# ============================================

# ============ IMAGE INPUT ============
st.subheader("📸 Upload Traffic Image")
uploaded_image = st.file_uploader(
    "Traffic Image",
    type=["jpg", "jpeg", "png"]
)
# ===================================

# ============ MAIN LOGIC ============
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)

    img_h, img_w, _ = image_np.shape
    image_area = img_h * img_w

    results = model.predict(image_np, conf=0.3, verbose=False)

    traffic_score = 0.0
    vehicle_count = 0

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        box_area = float((x2 - x1) * (y2 - y1))

        weight = VEHICLE_WEIGHTS.get(cls_name, 1.0)
        density = box_area / image_area

        traffic_score += weight * density * 100
        vehicle_count += 1

    traffic_score = round(float(traffic_score), 2)

    if traffic_score <= LOW_THRESHOLD:
        level = "LOW"
    elif traffic_score <= HIGH_THRESHOLD:
        level = "MEDIUM"
    else:
        level = "HIGH"

    c1, c2, c3 = st.columns(3)
    c1.metric("🚗 Vehicles", vehicle_count)
    c2.metric("📊 Density Score", traffic_score)
    c3.metric("⚠️ Congestion", level)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO traffic_events
            (city, area, latitude, longitude, vehicle_count, traffic_score, congestion_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            city, area, latitude, longitude,
            vehicle_count, traffic_score, level
        ))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("📦 Data stored in MySQL")

    except Exception as e:
        st.error(f"Database error: {e}")

    if level == "HIGH":
        st.error("🚨 HIGH CONGESTION")
        send_traffic_alert(city, area, latitude, longitude, traffic_score)
    elif level == "MEDIUM":
        st.warning("⚠️ Moderate congestion detected")
    else:
        st.success("✅ Traffic under control")

    st.subheader("📷 Detection Result")
    st.image(results[0].plot(), use_column_width=True)

else:
    st.info("ℹ️ Select location and upload a traffic image")
