import os
import streamlit as st
import smtplib
from email.message import EmailMessage
from ultralytics import YOLO
from datetime import datetime
import cv2
import numpy as np
from db import get_connection

# ================= ENV VARIABLES =================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ================= EMAIL FUNCTION =================
def send_email_alert(subject, body):
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_RECEIVER:
        st.info("📧 Email alerts disabled (credentials not set)")
        return False

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return True

    except Exception:
        st.warning("📧 Email alert failed (safe to ignore)")
        return False

# ================= CONFIG =================
MODEL_PATH = "models/accident_best.pt"
CONF_THRESHOLD = 0.25

st.set_page_config(page_title="Accident – UrbanBot", layout="wide")
st.title("🚑 Accident Detection System")

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# ================= CITY DATA =================
CITY_DATA = {
    "Chennai": ["Guindy", "T Nagar", "Velachery", "Tambaram"],
    "Bangalore": ["Electronic City", "Whitefield"],
    "Mumbai": ["Andheri", "Kurla"],
    "Delhi": ["Dwarka", "Rohini", "Karol Bagh"],
    "Hyderabad": ["Gachibowli", "Kukatpally"]
}

# ================= UI =================
col1, col2 = st.columns(2)

with col1:
    city = st.selectbox("City", CITY_DATA.keys())
    area = st.selectbox("Area", CITY_DATA[city])
    image_file = st.file_uploader(
        "Upload Accident Image",
        ["jpg", "jpeg", "png"]
    )

with col2:
    st.subheader("Detection Preview")
    preview = st.empty()

# ================= MAIN LOGIC =================
if image_file and st.button("🚨 Detect Accident"):

    img_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    results = model.predict(image, conf=CONF_THRESHOLD)
    boxes = results[0].boxes
    vehicle_count = len(boxes)

    avg_conf = float(boxes.conf.mean()) if vehicle_count > 0 else 0.0

    # ===== SEVERITY LOGIC =====
    if vehicle_count == 0:
        severity = "No Accident"
    elif vehicle_count == 1:
        severity = "Minor"
    elif vehicle_count == 2:
        severity = "Moderate"
    else:
        severity = "Severe"

    # ===== METRICS =====
    c1, c2, c3 = st.columns(3)
    c1.metric("🚗 Vehicles", vehicle_count)
    c2.metric("📊 Confidence", f"{avg_conf:.2f}")
    c3.metric("🚦 Severity", severity)

    # ===== PREVIEW =====
    annotated = results[0].plot()
    preview.image(annotated, channels="BGR", use_container_width=True)

    # ===== SAVE TO MYSQL (MATCHES YOUR TABLE) =====
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO accident_events
            (city, area, severity, confidence_score, image_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            city,
            area,
            severity,
            avg_conf,
            image_file.name
        ))

        conn.commit()
        cur.close()
        conn.close()

        st.success("✅ Accident data saved to MySQL")

    except Exception as e:
        st.error(f"Database error: {e}")

    # ===== EMAIL ALERT (WORKING) =====
    if severity in ["Moderate", "Severe"]:
        send_email_alert(
            "🚨 UrbanBot Accident Alert",
            f"""
City: {city}
Area: {area}
Severity: {severity}
Confidence: {avg_conf:.2f}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        )

else:
    st.info("ℹ️ Upload an image and click Detect Accident")
