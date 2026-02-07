from .sql_agent import run_query
from .llm_client import ask_llm
from .prompt import build_prompt

def chatbot_response(user_query):
    query = user_query.lower()

    try:
        # 🚦 TRAFFIC
        if "traffic" in query:
            data = run_query("""
                SELECT city, congestion_level, COUNT(*) AS count
                FROM traffic_events
                GROUP BY city, congestion_level
            """)

        # 🚑 ACCIDENT
        elif "accident" in query:
            data = run_query("""
                SELECT city, severity, COUNT(*) AS count
                FROM accident_events
                GROUP BY city, severity
            """)

        # 👥 CROWD
        elif "crowd" in query:
            data = run_query("""
                SELECT city, COUNT(*) AS crowd_events
                FROM crowd_events
                GROUP BY city
            """)

        # 🛣️ ROAD DAMAGE
        elif "road" in query or "pothole" in query:
            data = run_query("""
                SELECT city, area, damage_count, severity
                FROM road_damage_events
                ORDER BY created_at DESC
                LIMIT 10
            """)

        # 🌫️ AIR QUALITY
        elif "air" in query or "aqi" in query:
            data = run_query("""
                SELECT city, pm25, pm10, no2, so2, co, o3
                FROM air_quality_predictions
                ORDER BY id DESC
                LIMIT 5
            """)

        # 🧾 COMPLAINTS / SENTIMENT
        elif "complaint" in query or "sentiment" in query:
            data = run_query("""
                SELECT city, category, sentiment, priority
                FROM citizen_complaints
                ORDER BY created_at DESC
                LIMIT 10
            """)

        else:
            return "Please ask about traffic, accidents, air quality, crowd, road damage, or complaints."

        if not data:
            return "No data available in the database for this query."

        context = "\n".join(str(row) for row in data)
        prompt = build_prompt(context, user_query)
        return ask_llm(prompt)

    except Exception as e:
        return f"Database error: {str(e)}"
