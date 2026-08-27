import sqlite3
import pandas as pd

# CSV dosyasındaki verileri oku
df = pd.read_csv("weather_data.csv")

# SQLite veritabanını oluştur / bağlan
connection = sqlite3.connect("weather.db")

# Verileri "weather" isimli SQL tablosuna aktar
df.to_sql(
    "weather",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("✅ Veriler SQL veritabanına aktarıldı!")
print(f"✅ Toplam {len(df)} kayıt eklendi.")
print("✅ weather.db oluşturuldu.")