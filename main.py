import requests
import csv
import sqlite3
import time
from datetime import datetime

# ==========================================
# AYARLAR
# ==========================================

MAX_RETRY = 3
WAIT_TIME = 2

# ==========================================
# 1. ŞEHİRLERİ OKU
# ==========================================

with open("cities.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    cities = list(reader)

print(f"\n{len(cities)} il bulundu.")
print("Hava durumu verileri toplanıyor...\n")

# ==========================================
# 2. SQL VERİTABANINA BAĞLAN
# ==========================================

connection = sqlite3.connect("weather.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    temperature REAL NOT NULL
)
""")

connection.commit()

# ==========================================
# 3. 81 İLİN VERİSİNİ ÇEK
# ==========================================

successful = 0
failed = 0

for city in cities:

    city_name = city["city"]
    latitude = float(city["latitude"])
    longitude = float(city["longitude"])

    url = (
        "http://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m"
    )

    city_success = False

    # ======================================
    # RETRY SİSTEMİ
    # ======================================

    for attempt in range(1, MAX_RETRY + 1):

        try:
            print(
                f"→ {city_name} "
                f"(Deneme {attempt}/{MAX_RETRY})"
            )

            # EXTRACT
            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            # TRANSFORM
            temperature = float(
                data["current"]["temperature_2m"]
            )

            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # LOAD → SQL
            cursor.execute(
                """
                INSERT INTO weather
                (
                    datetime,
                    city,
                    latitude,
                    longitude,
                    temperature
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    now,
                    city_name,
                    latitude,
                    longitude,
                    temperature
                )
            )

            connection.commit()

            print(
                f"✓ {city_name}: "
                f"{temperature} °C → SQL'e kaydedildi"
            )

            successful += 1
            city_success = True

            # Başarılıysa tekrar denemeyi bırak
            break

        except Exception as error:

            print(
                f"✗ {city_name} "
                f"{attempt}. denemede başarısız."
            )

            print(f"  Hata: {error}")

            # Son deneme değilse bekle
            if attempt < MAX_RETRY:
                print(
                    f"  {WAIT_TIME} saniye sonra "
                    f"tekrar deneniyor..."
                )

                time.sleep(WAIT_TIME)

    # 3 denemenin tamamı başarısızsa
    if not city_success:
        failed += 1

        print(
            f"❌ {city_name}: "
            f"{MAX_RETRY} deneme de başarısız."
        )

# ==========================================
# 4. SONUÇ
# ==========================================

cursor.execute(
    "SELECT COUNT(*) FROM weather"
)

total_records = cursor.fetchone()[0]

connection.close()

print("\n===================================")
print("       DATAPULSE ETL RAPORU")
print("===================================")
print(f"✓ Başarılı: {successful}")
print(f"✗ Başarısız: {failed}")
print(f"🗄️ SQL toplam kayıt: {total_records}")
print("===================================")
print("ETL Pipeline tamamlandı!")