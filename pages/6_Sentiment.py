import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
from db import get_connection
import nltk

nltk.download("vader_lexicon")

st.set_page_config(
    page_title="Citizen Complaint AI",
    layout="centered"
)

st.title("🧠 Citizen Complaint AI")
st.caption("Automated sentiment analysis & priority routing for smart cities")

sia = SentimentIntensityAnalyzer()

# ---------------- SENTIMENT LOGIC ----------------
def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "POSITIVE", "LOW"
    elif score <= -0.05:
        return "NEGATIVE", "HIGH"
    else:
        return "NEUTRAL", "MEDIUM"

# ---------------- DB INSERT ----------------
def insert_complaint(city, category, department, text, sentiment, priority):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO citizen_complaints
        (city, category, department, complaint_text, sentiment, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (city, category, department, text, sentiment, priority))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- UI ----------------
st.subheader("📌 Register Complaint")

city = st.selectbox(
    "City",
    ["Chennai", "Delhi", "Hyderabad", "Bangalore", "Mumbai"]
)

category = st.selectbox(
    "Category",
    ["Water", "Road", "Electricity", "Garbage", "Traffic"]
)

department = st.text_input(
    "Department",
    value=f"{category} Department"
)

complaint_text = st.text_area(
    "Complaint Description",
    height=120
)

submit = st.button("🚀 Submit Complaint")

if submit:
    if complaint_text.strip() == "":
        st.error("Complaint description cannot be empty")
    else:
        sentiment, priority = analyze_sentiment(complaint_text)
        insert_complaint(city, category, department, complaint_text, sentiment, priority)

        st.success("✅ Complaint successfully registered")

        st.markdown("### 📊 Analysis Result")
        st.markdown(f"**Sentiment:** `{sentiment}`")
        st.markdown(f"**Priority:** `{priority}`")
