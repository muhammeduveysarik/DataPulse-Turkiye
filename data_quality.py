import sqlite3
import pandas as pd

# ==========================================
# 1. SQL VERİTABANINDAN VERİLERİ AL
# ==========================================

connection = sqlite3.connect("weather.db")

df = pd.read_sql_query(
    "SELECT * FROM weather",
    connection
)

connection.close()

print("\n===================================")
print("     DATAPULSE DATA QUALITY")
print("===================================")

print(f"Toplam kayıt: {len(df)}")


# ==========================================
# 2. EKSİK VERİ KONTROLÜ
# ==========================================

missing = df.isnull().sum().sum()

print(f"\nEksik veri sayısı: {missing}")

if missing == 0:
    print("✓ Eksik veri bulunamadı.")
else:
    print("✗ Eksik veriler bulundu!")


# ==========================================
# 3. SICAKLIK KONTROLÜ
# ==========================================

invalid_temperature = df[
    (df["temperature"] < -50) |
    (df["temperature"] > 60)
]

if len(invalid_temperature) == 0:
    print("✓ Sıcaklık değerleri mantıklı.")
else:
    print(
        f"✗ {len(invalid_temperature)} "
        "şüpheli sıcaklık bulundu!"
    )


# ==========================================
# 4. ŞEHİR KONTROLÜ
# ==========================================

city_count = df["city"].nunique()

print(f"\nVeritabanındaki farklı il sayısı: {city_count}")

if city_count == 81:
    print("✓ 81 ilin tamamı mevcut.")
else:
    print("✗ Bazı iller eksik!")


# ==========================================
# 5. DUPLICATE KONTROLÜ
# ==========================================

duplicates = df.duplicated(
    subset=["datetime", "city"]
).sum()

print(f"\nTekrarlı kayıt sayısı: {duplicates}")

if duplicates == 0:
    print("✓ Tekrarlı kayıt bulunamadı.")
else:
    print("✗ Tekrarlı kayıtlar bulundu!")


# ==========================================
# SONUÇ
# ==========================================

print("\n===================================")

if (
    missing == 0
    and len(invalid_temperature) == 0
    and city_count == 81
    and duplicates == 0
):
    print("✓ DATA QUALITY CHECK PASSED")
else:
    print("✗ DATA QUALITY CHECK FAILED")

print("===================================")