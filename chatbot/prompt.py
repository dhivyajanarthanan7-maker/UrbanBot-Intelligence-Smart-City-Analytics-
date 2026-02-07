def build_prompt(context, question):
    return [
        {
            "role": "system",
            "content": (
                "You are UrbanBot, a Smart City AI Assistant. "
                "Answer ONLY using the provided database data. "
                "If data is insufficient, clearly say so."
            )
        },
        {
            "role": "user",
            "content": f"""
DATABASE DATA:
{context}

QUESTION:
{question}

Provide a clear summary and recommendations.
"""
        }
    ]

