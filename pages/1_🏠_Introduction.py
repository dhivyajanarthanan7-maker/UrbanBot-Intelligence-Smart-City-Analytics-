import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Introduction – UrbanBot",
    page_icon="🏙️",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style="margin-bottom:0;">🏙️ UrbanBot – Smart City Intelligence Platform</h1>
    <p style="color:gray; font-size:16px;">
    AI-driven urban monitoring, analytics, and decision support system
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- INTRO SECTION ----------------
st.markdown(
    """
    ## 📌 Project Introduction

    Rapid urbanization has significantly increased challenges in modern cities, including  
    **traffic congestion, road infrastructure damage, accidents, air pollution, crowd management,
    and citizen dissatisfaction**.

    Traditional monitoring systems rely heavily on **manual reporting and delayed response mechanisms**,
    which are often inefficient in handling real-time urban issues.

    **UrbanBot** addresses these challenges by providing a **centralized, AI-powered smart city
    intelligence platform** that enables authorities to **monitor, analyze, and respond proactively**
    to critical urban events.
    """
)

# ---------------- PROBLEM STATEMENT ----------------
st.markdown(
    """
    ## ❗ Problem Statement

    City administrations face the following key issues:

    - 🚦 Lack of real-time traffic congestion monitoring  
    - 🛣️ Delayed detection of road damage such as potholes and cracks  
    - 🚑 Late identification of accidents and emergency situations  
    - 🌫️ Inadequate air quality analysis for public safety  
    - 👥 Poor crowd density management during peak hours or events  
    - 🧠 Limited insight into citizen complaints and sentiments  

    These challenges often lead to **slow response times, increased accidents, infrastructure decay,
    and reduced quality of urban life**.
    """
)

# ---------------- SOLUTION OVERVIEW ----------------
st.markdown(
    """
    ## 💡 Proposed Solution – UrbanBot

    **UrbanBot** is an integrated **Smart City Intelligence System** that leverages:

    - **Computer Vision** for image-based detection  
    - **Machine Learning & Deep Learning** for prediction and classification  
    - **Natural Language Processing (NLP)** for sentiment analysis  
    - **MySQL Database** for structured data storage and analytics  
    - **Email Alert System** for real-time emergency notifications  

    The platform consolidates multiple urban monitoring modules into a **single unified dashboard**,
    enabling faster decision-making and proactive governance.
    """
)

# ---------------- MODULES ----------------
st.markdown(
    """
    ## 🧩 Core Modules

    - 🚦 **Traffic Congestion Monitoring**  
      Detects vehicle density from images and classifies congestion levels.

    - 🛣️ **Road Damage Detection**  
      Identifies potholes, cracks, and road defects using YOLO-based computer vision.

    - 🚑 **Accident Detection System**  
      Detects accidents from images and sends automated email alerts.

    - 🌫️ **Air Quality Analysis**  
      Predicts AQI levels and categorizes pollution severity.

    - 👥 **Crowd Density Estimation**  
      Estimates crowd levels to assist in public safety management.

    - 🧠 **Citizen Sentiment Analysis**  
      Analyzes complaints and feedback using NLP techniques.

    - 🤖 **AI Chatbot**  
      Assists city administrators with insights and queries.
    """
)

# ---------------- TECHNOLOGY STACK ----------------
st.markdown(
    """
    ## ⚙️ Technology Stack

    **Frontend**
    - Streamlit (Interactive Dashboard)

    **AI & ML**
    - YOLOv8 (Object Detection)
    - CNN / LSTM Models
    - NLP & Sentiment Analysis Models

    **Backend**
    - Python
    - MySQL Database
    - SMTP Email Alert System

    **Deployment**
    - Modular Streamlit Pages
    """
)

# ---------------- OBJECTIVES ----------------
st.markdown(
    """
    ## 🎯 Project Objectives

    - Enable **real-time urban monitoring**
    - Reduce **response time** during emergencies
    - Improve **infrastructure maintenance planning**
    - Enhance **public safety and city efficiency**
    - Provide **data-driven insights** for administrators
    """
)

# ---------------- IMPACT ----------------
st.markdown(
    """
    ## 🌍 Impact & Use Cases

    - Smart traffic control and congestion mitigation  
    - Early accident detection and emergency response  
    - Efficient road maintenance planning  
    - Improved air quality awareness  
    - Safer crowd management during events  
    - Better understanding of citizen sentiment  

    UrbanBot contributes towards building **safer, smarter, and more sustainable cities**.
    """
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <center>
    <small>
    UrbanBot – Smart City Intelligence Platform  
    <br>
    Final Year Project / Capstone System
    </small>
    </center>
    """,
    unsafe_allow_html=True
)
