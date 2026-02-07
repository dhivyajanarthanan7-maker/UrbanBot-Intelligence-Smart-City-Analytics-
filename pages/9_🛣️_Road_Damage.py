import streamlit as st
import cv2
import numpy as np
import os
import mysql.connector
from ultralytics import YOLO
from datetime import datetime

# ================= CONFIG =================
MODEL_PATH = "models/road_damage_best.pt"
UPLOAD_DIR = "uploads/road_damage"
CONF_THRESHOLD = 0.25

DB_CONFIG = {
    "host": "localhost",
    "user": "urbanbot_user",
    "password": "UrbanBot@123",
    "database": "urban_bot"
}
# ========================================

os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Road Damage Detection", layout="wide")

st.markdown("""
<h2>🛣️ Road Damage Detection System</h2>
<p style="color:gray;">AI-based pothole & crack detection with smart severity logic</p>
""", unsafe_allow_html=True)

# ================= CITY DATA =================
CITY_DATA = {
    "Chennai": {
        "Anna Nagar": (13.0850, 80.2101),
        "T Nagar": (13.0418, 80.2337),
        "Velachery": (12.9756, 80.2214)
    },
    "Mumbai": {
        "Bandra": (19.0596, 72.8295),
        "Andheri": (19.1136, 72.8697),
        "Dadar": (19.0178, 72.8478)
    },
    "Kolkata": {
        "Howrah": (22.5958, 88.2636),
        "Salt Lake": (22.5726, 88.4315),
        "Garia": (22.4620, 88.3945)
    },
    "Pune": {
        "Hinjewadi": (18.5913, 73.7389),
        "Wakad": (18.5986, 73.7622),
        "Shivajinagar": (18.5308, 73.8475)
    },
    "Bangalore": {
        "Whitefield": (12.9698, 77.7500),
        "Electronic City": (12.8399, 77.6770),
        "Yelahanka": (13.1007, 77.5963)
    },
    "Visakhapatnam": {
        "MVP Colony": (17.7380, 83.3296),
        "Gajuwaka": (17.7006, 83.2160),
        "Maddilapalem": (17.7389, 83.3146)
    }
}
# ============================================

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()
# ============================================

# ================= DB CONNECTION =================
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
# ================================================

left, right = st.columns([1.1, 1])

# ================= LEFT PANEL =================
with left:
    st.subheader("📥 Input Parameters")

    city = st.selectbox("City", list(CITY_DATA.keys()))
    area = st.selectbox("Area / Locality", list(CITY_DATA[city].keys()))

    latitude, longitude = CITY_DATA[city][area]
    st.text_input("Latitude", value=latitude, disabled=True)
    st.text_input("Longitude", value=longitude, disabled=True)

    uploaded_file = st.file_uploader(
        "Upload Road Image",
        type=["jpg", "jpeg", "png"]
    )

    predict_btn = st.button("🚀 Detect Road Damage")

# ================= RIGHT PANEL =================
with right:
    st.subheader("📊 Detection Analysis")

    if uploaded_file and predict_btn:
        image_path = os.path.join(
            UPLOAD_DIR,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        image = cv2.imread(image_path)

        results = model.predict(image, conf=CONF_THRESHOLD, save=False)
        boxes = results[0].boxes
        names = model.names

        detected_classes = []
        if boxes is not None:
            for cls in boxes.cls:
                detected_classes.append(names[int(cls)])

        damage_count = len(detected_classes)
        unique_damages = list(set(detected_classes))

        annotated = results[0].plot()
        st.image(annotated, channels="BGR", use_container_width=True)

        # ================= OPTION-2 SMART SEVERITY =================
        severity = "LOW"

        if "pothole" in unique_damages and damage_count >= 3:
            severity = "HIGH"
        elif "pothole" in unique_damages:
            severity = "MEDIUM"
        elif "crack" in unique_damages and damage_count >= 3:
            severity = "MEDIUM"
        elif damage_count >= 5:
            severity = "HIGH"
        # ==========================================================

        st.markdown("### 📌 Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Damage Count", damage_count)
        c2.metric("Severity", severity)
        c3.metric("Time", datetime.now().strftime("%H:%M:%S"))

        if damage_count == 0:
            st.success("✅ No road damage detected")
        else:
            st.error(f"🚨 {damage_count} damage(s) detected")
            st.markdown("**Detected Types:**")
            for d in unique_damages:
                st.markdown(f"- 🛑 {d.upper()}")

        # ================= SAVE TO MYSQL =================
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO road_damage_events
                (city, area, latitude, longitude, damage_count, damage_types, severity, image_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                area,
                latitude,
                longitude,
                damage_count,
                ", ".join(unique_damages),
                severity,
                os.path.basename(image_path)
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("📦 Data saved to MySQL successfully")

        except Exception as e:
            st.error(f"Database error: {e}")

    else:
        st.info("Upload an image and click **Detect Road Damage**")
