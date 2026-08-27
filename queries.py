import sqlite3
import pandas as pd

# Veritabanına bağlan
connection = sqlite3.connect("weather.db")

# SQL sorgumuz
query = """
SELECT city, temperature, datetime
FROM weather AS w
WHERE datetime = (
    SELECT MAX(datetime)
    FROM weather
    WHERE city = w.city
)
ORDER BY temperature DESC
LIMIT 10;
"""

# SQL sorgusunu çalıştır
result = pd.read_sql_query(query, connection)

connection.close()

print("\nEN SICAK 10 IL\n")
print(result.to_string(index=False))