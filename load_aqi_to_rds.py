import pandas as pd
import mysql.connector
import math

print("Reading CSV...")
df = pd.read_csv("data/aqi_data.csv")

def clean(value):
    """Convert NaN to None so MySQL accepts it"""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

print("Connecting to RDS...")
conn = mysql.connector.connect(
    host="database-1.cbggqawg83jt.ap-south-1.rds.amazonaws.com",
    user="admin",
    password="EwHozf1nW6weAyRMi2ep",
    database="urban_bot",
    port=3306,
    auth_plugin="mysql_native_password"
)

cursor = conn.cursor()

insert_query = """
INSERT INTO aqi_locations
(country, state, city, station, last_update, latitude, longitude,
 pollutant_id, pollutant_min, pollutant_max, pollutant_avg)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

print("Uploading rows to RDS... (this may take 1-2 minutes)")

count = 0

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        clean(row.get("country")),
        clean(row.get("state")),
        clean(row.get("city")),
        clean(row.get("station")),
        clean(row.get("last_update")),
        clean(row.get("latitude")),
        clean(row.get("longitude")),
        clean(row.get("pollutant_id")),
        clean(row.get("pollutant_min")),
        clean(row.get("pollutant_max")),
        clean(row.get("pollutant_avg"))
    ))
    count += 1

conn.commit()
cursor.close()
conn.close()

print(f"UPLOAD COMPLETE 🎉  Rows inserted: {count}")
