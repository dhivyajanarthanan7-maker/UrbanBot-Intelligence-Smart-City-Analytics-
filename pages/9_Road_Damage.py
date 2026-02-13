import streamlit as st
import cv2
import numpy as np
import os
from datetime import datetime
from db import get_connection
from model_manager import get_model

UPLOAD_DIR = "uploads/road_damage"
CONF_THRESHOLD = 0.20
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Road Damage Detection", layout="wide")
st.title("🛣️ Road Damage Detection System")

CITY_DATA = {
    "Chennai":{"Anna Nagar":(13.0850,80.2101),"T Nagar":(13.0418,80.2337),"Velachery":(12.9756,80.2214)},
    "Mumbai":{"Bandra":(19.0596,72.8295),"Andheri":(19.1136,72.8697),"Dadar":(19.0178,72.8478)}
}

left,right=st.columns(2)

with left:
    city=st.selectbox("City",list(CITY_DATA.keys()))
    area=st.selectbox("Area",list(CITY_DATA[city].keys()))
    lat,lon=CITY_DATA[city][area]

    uploaded_file=st.file_uploader("Upload Road Image",["jpg","jpeg","png"])
    detect=st.button("Detect Road Damage")

with right:

    if uploaded_file and detect:

        with st.spinner("Loading Road Damage AI model..."):
            model = get_model("road", "models/road_damage_best.pt")

        image_path=os.path.join(UPLOAD_DIR,f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")

        with open(image_path,"wb") as f:
            f.write(uploaded_file.read())

        image=cv2.imread(image_path)

        results=model.predict(image,conf=CONF_THRESHOLD,save=False)
        boxes=results[0].boxes
        names=model.names

        detected=[]
        if boxes is not None:
            for cls in boxes.cls:
                detected.append(names[int(cls)])

        count=len(detected)
        unique=list(set(detected))

        st.image(results[0].plot(),channels="BGR",use_container_width=True)

        severity="LOW"
        if "pothole" in unique and count>=3:
            severity="HIGH"
        elif "pothole" in unique:
            severity="MEDIUM"

        st.metric("Damage Count",count)
        st.metric("Severity",severity)

        try:
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute("""
            INSERT INTO road_damage_events
            (city,area,latitude,longitude,damage_count,damage_types,severity,image_name)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """,(city,area,lat,lon,count,", ".join(unique),severity,os.path.basename(image_path)))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Saved to database")
        except Exception as e:
            st.error(e)

    else:
        st.info("Upload image and click detect")
