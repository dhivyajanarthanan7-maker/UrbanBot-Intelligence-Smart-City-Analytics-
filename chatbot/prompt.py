# chatbot/prompt.py

def build_prompt(question, context):

    context_text = str(context)

    return [
        {
            "role": "system",
            "content": (
                "You are UrbanBot, a Smart City AI Assistant.\n"
                "You MUST answer ONLY using the database results provided.\n"
                "Do NOT invent information.\n"
                "If the database data is empty, say: 'No recent data available.'\n"
                "Always provide a short summary and practical recommendations."
            )
        },
        {
            "role": "user",
            "content": f"""
DATABASE RESULTS:
{context_text}

USER QUESTION:
{question}
"""
        }
    ]
