from db import get_connection

def insert_complaint(city, category, department, complaint_text, sentiment, priority):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO citizen_complaints
    (city, category, department, complaint_text, sentiment, priority)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = (
        city,
        category,
        department,
        complaint_text,
        sentiment,
        priority
    )

    cursor.execute(query, data)
    conn.commit()

    cursor.close()
    conn.close()


def fetch_complaints(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT city, category, department, sentiment, priority, created_at
    FROM citizen_complaints
    ORDER BY created_at DESC
    LIMIT %s
    """

    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows
