import os
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import smtplib
from email.message import EmailMessage
from db import get_connection
from model_manager import get_model

# ================= MODEL CONFIG =================
MODEL_NAME = "traffic"
MODEL_PATH = "models/traffic_best.pt"   # MUST match your models folder

LOW_THRESHOLD = 8
HIGH_THRESHOLD = 18

st.set_page_config(page_title="Traffic", layout="wide")
st.title("🚦 Traffic Congestion Monitoring")

# ================= EMAIL CONFIG =================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email_alert(subject, body):
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_RECEIVER:
        st.info("📧 Email alerts disabled")
        return

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

    except Exception:
        st.warning("Email failed (safe to ignore)")

# ================= LOCATIONS =================
LOCATIONS = {
    "Chennai":{
        "T Nagar":(13.0418,80.2341),
        "Anna Nagar":(13.0850,80.2101),
        "Guindy":(13.0067,80.2206)
    },
    "Mumbai":{
        "Andheri":(19.1197,72.8468),
        "Bandra":(19.0596,72.8295),
        "Dadar":(19.0178,72.8478)
    },
    "Delhi":{
        "Connaught Place":(28.6315,77.2167),
        "Saket":(28.5245,77.2066)
    }
}

VEHICLE_WEIGHTS = {
    "car":1.5,
    "bus":4.0,
    "truck":4.5,
    "motorbike":0.6,
    "auto rickshaw":1.2
}

# ================= UI INPUT =================
city = st.selectbox("City", list(LOCATIONS.keys()))
area = st.selectbox("Area", list(LOCATIONS[city].keys()))
lat, lon = LOCATIONS[city][area]

uploaded_image = st.file_uploader("Upload Traffic Image", ["jpg","jpeg","png"])

# ================= MAIN =================
if uploaded_image:

    st.image(uploaded_image, use_container_width=True)

    # LOAD MODEL (FIXED)
    with st.spinner("Loading Traffic AI model..."):
        model = get_model(MODEL_NAME, MODEL_PATH)

    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)

    results = model.predict(image_np, conf=0.3, verbose=False)

    img_h, img_w, _ = image_np.shape
    image_area = img_h * img_w

    traffic_score = 0
    vehicle_count = 0

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        box_area = float((x2-x1)*(y2-y1))

        weight = VEHICLE_WEIGHTS.get(cls_name, 1.0)
        density = box_area / image_area

        traffic_score += weight * density * 100
        vehicle_count += 1

    traffic_score = round(float(traffic_score), 2)

    # ================= CONGESTION LOGIC (UNCHANGED) =================
    if traffic_score <= LOW_THRESHOLD:
        level = "LOW"
    elif traffic_score <= HIGH_THRESHOLD:
        level = "MEDIUM"
    else:
        level = "HIGH"

    c1, c2, c3 = st.columns(3)
    c1.metric("Vehicles", vehicle_count)
    c2.metric("Score", traffic_score)
    c3.metric("Congestion", level)

    # ================= DATABASE SAVE (UNCHANGED) =================
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO traffic_events
        (city,area,latitude,longitude,vehicle_count,traffic_score,congestion_level)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,(city,area,lat,lon,vehicle_count,traffic_score,level))

        conn.commit()
        cursor.close()
        conn.close()

        st.success("Stored in DB")

    except Exception as e:
        st.error(e)

    # ================= EMAIL ALERT (UNCHANGED) =================
    if level == "HIGH":
        send_email_alert(
            "🚨 UrbanBot Traffic Alert",
            f"City: {city}\nArea: {area}\nCongestion Level: {level}\nTraffic Score: {traffic_score}"
        )

    st.image(results[0].plot(), use_container_width=True)

else:
    st.info("Upload traffic image")
