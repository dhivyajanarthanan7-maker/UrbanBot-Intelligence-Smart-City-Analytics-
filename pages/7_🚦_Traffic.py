import os
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime
import smtplib
from email.message import EmailMessage
from db import get_connection
from model_manager import get_model

MODEL_PATH = "models/Traffic_best.pt"
LOW_THRESHOLD = 8
HIGH_THRESHOLD = 18

st.set_page_config(page_title="Traffic", layout="wide")
st.title("🚦 Traffic Congestion Monitoring")

LOCATIONS = {
    "Chennai":{"T Nagar":(13.0418,80.2341),"Anna Nagar":(13.0850,80.2101),"Guindy":(13.0067,80.2206)},
    "Mumbai":{"Andheri":(19.1197,72.8468),"Bandra":(19.0596,72.8295),"Dadar":(19.0178,72.8478)},
    "Delhi":{"Connaught Place":(28.6315,77.2167),"Saket":(28.5245,77.2066)}
}

VEHICLE_WEIGHTS={
    "car":1.5,"bus":4.0,"truck":4.5,"motorbike":0.6,"auto rickshaw":1.2
}

city=st.selectbox("City",list(LOCATIONS.keys()))
area=st.selectbox("Area",list(LOCATIONS[city].keys()))
lat,lon=LOCATIONS[city][area]

uploaded_image=st.file_uploader("Upload Traffic Image",["jpg","jpeg","png"])

if uploaded_image:

    st.image(uploaded_image,use_container_width=True)

    with st.spinner("Loading Traffic AI model..."):
        model=get_model(MODEL_PATH)

    image=Image.open(uploaded_image).convert("RGB")
    image_np=np.array(image)

    results=model.predict(image_np,conf=0.3,verbose=False)

    img_h,img_w,_=image_np.shape
    image_area=img_h*img_w

    traffic_score=0
    vehicle_count=0

    for box in results[0].boxes:
        cls_id=int(box.cls[0])
        cls_name=model.names[cls_id]
        x1,y1,x2,y2=box.xyxy[0].cpu().numpy()
        box_area=float((x2-x1)*(y2-y1))

        weight=VEHICLE_WEIGHTS.get(cls_name,1.0)
        density=box_area/image_area

        traffic_score+=weight*density*100
        vehicle_count+=1

    traffic_score=round(float(traffic_score),2)

    if traffic_score<=LOW_THRESHOLD:
        level="LOW"
    elif traffic_score<=HIGH_THRESHOLD:
        level="MEDIUM"
    else:
        level="HIGH"

    c1,c2,c3=st.columns(3)
    c1.metric("Vehicles",vehicle_count)
    c2.metric("Score",traffic_score)
    c3.metric("Congestion",level)

    try:
        conn=get_connection()
        cursor=conn.cursor()
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

    st.image(results[0].plot(),use_container_width=True)

else:
    st.info("Upload traffic image")
