# chatbot/chatbot_logic.py

from .sql_agent import run_query
from .llm_client import ask_llm
from .prompt import build_prompt


def format_rows(rows):
    """Convert SQL rows into readable text for LLM"""
    formatted = []
    for row in rows:
        formatted.append(", ".join(str(col) for col in row))
    return "\n".join(formatted)


def chatbot_response(user_query: str):

    query = user_query.lower()

    try:

        # ---------------- TRAFFIC ----------------
        if any(word in query for word in ["traffic", "jam", "vehicle", "cars", "congestion"]):
            data = run_query("""
                SELECT city, congestion_level, COUNT(*) AS reports
                FROM traffic_events
                GROUP BY city, congestion_level
            """)

        # ---------------- ACCIDENT ----------------
        elif any(word in query for word in ["accident", "crash", "collision"]):
            data = run_query("""
                SELECT city, severity, COUNT(*) AS cases
                FROM accident_events
                GROUP BY city, severity
            """)

        # ---------------- CROWD ----------------
        elif any(word in query for word in ["crowd", "people", "rush"]):
            data = run_query("""
                SELECT city, COUNT(*) AS crowd_events
                FROM crowd_events
                GROUP BY city
            """)

        # ---------------- ROAD DAMAGE ----------------
        elif any(word in query for word in ["road", "pothole", "damage"]):
            data = run_query("""
                SELECT city, area, damage_count, severity
                FROM road_damage_events
                ORDER BY created_at DESC
                LIMIT 10
            """)

        # ---------------- AIR QUALITY ----------------
        elif any(word in query for word in ["air", "aqi", "pollution"]):
            data = run_query("""
                SELECT city, pm25, pm10, no2, so2, co, o3
                FROM air_quality_predictions
                ORDER BY id DESC
                LIMIT 5
            """)

        # ---------------- COMPLAINT ----------------
        elif any(word in query for word in ["complaint", "issue", "problem", "sentiment"]):
            data = run_query("""
                SELECT city, category, sentiment, priority
                FROM citizen_complaints
                ORDER BY created_at DESC
                LIMIT 10
            """)

        else:
            return (
                "I can help with:\n"
                "• Traffic conditions\n"
                "• Accident reports\n"
                "• Air quality (AQI)\n"
                "• Crowd monitoring\n"
                "• Road damage / potholes\n"
                "• Citizen complaints"
            )

        # No database results
        if not data:
            return "No recent data available in the database."

        # Convert rows for AI
        context = format_rows(data)

        # IMPORTANT (fixed order)
        prompt = build_prompt(user_query, context)

        # Ask LLM
        response = ask_llm(prompt)

        return response

    except Exception as e:
        return f"System error: {str(e)}"
