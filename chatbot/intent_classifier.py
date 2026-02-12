# chatbot/intent_classifier.py

from .llm_client import ask_llm


def classify_intent(question: str) -> str:

    prompt = f"""
You are an intent classifier for a Smart City AI system.

Classify the user query into EXACTLY ONE of these categories:

traffic
accident
air_quality
crowd
road_damage
complaint

Return ONLY the category word. No explanation.

User Question:
{question}
"""

    response = ask_llm([
        {"role": "system", "content": "You only classify intent. Return one word."},
        {"role": "user", "content": prompt}
    ])

    if not response:
        return "unknown"

    return response.strip().lower()
