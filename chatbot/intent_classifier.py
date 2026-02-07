from .llm_client import ask_llm

def classify_intent(question: str) -> str:

    prompt = f"""
You are an intent classifier for a Smart City AI system.

Classify the user query into ONE of these categories:

traffic
accident
air_quality
crowd
road_damage
complaint

Return ONLY the single word category.

User Question:
{question}
"""

    response = ask_llm([
        {"role": "system", "content": "You only classify the intent."},
        {"role": "user", "content": prompt}
    ], temperature=0)

    return response.lower().strip()
