import pandas as pd
import matplotlib.pyplot as plt

# Veriyi oku
df = pd.read_csv("weather_data.csv")

# datetime sütununu gerçek tarih-saat tipine çevir
df["datetime"] = pd.to_datetime(df["datetime"])

# Sadece İstanbul verilerini al
istanbul = df[df["city"] == "Istanbul"].copy()

# Tarihe göre sırala
istanbul = istanbul.sort_values("datetime")

print("İstanbul kayıt sayısı:", len(istanbul))

print(
    istanbul[
        ["datetime", "city", "temperature"]
    ].to_string(index=False)
)

# Zaman serisi grafiği
plt.figure(figsize=(10, 6))

plt.plot(
    istanbul["datetime"],
    istanbul["temperature"],
    marker="o"
)

plt.title("İstanbul Sıcaklık Değişimi")
plt.xlabel("Zaman")
plt.ylabel("Sıcaklık (°C)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()