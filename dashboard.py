import streamlit as st
import pandas as pd
import sqlite3

# ==================================================
# SAYFA AYARLARI
# ==================================================

st.set_page_config(
    page_title="DataPulse Türkiye",
    page_icon="🌡️",
    layout="wide"
)

# ==================================================
# SQL VERİTABANINA BAĞLAN
# ==================================================

connection = sqlite3.connect("weather.db")

# Artık CSV DEĞİL, SQL'den veri çekiyoruz
query = """
SELECT
    city,
    temperature,
    latitude,
    longitude,
    datetime
FROM weather;
"""

df = pd.read_sql_query(query, connection)

connection.close()

# ==================================================
# VERİ TEMİZLEME
# ==================================================

df["temperature"] = pd.to_numeric(
    df["temperature"],
    errors="coerce"
)

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df["datetime"] = pd.to_datetime(
    df["datetime"],
    errors="coerce"
)

df = df.dropna()

# Her ilin en güncel ölçümü
latest_df = (
    df.sort_values("datetime")
    .drop_duplicates(
        subset="city",
        keep="last"
    )
    .copy()
)

# ==================================================
# BAŞLIK
# ==================================================

st.title("🇹🇷 DataPulse Türkiye")

st.write(
    "Türkiye'nin 81 ilinden toplanan hava durumu "
    "verilerinin SQL tabanlı analiz dashboard'u."
)

st.success(
    f"🗄️ SQL veritabanından {len(df)} kayıt yüklendi."
)

st.divider()

# ==================================================
# GENEL İSTATİSTİKLER
# ==================================================

hottest = latest_df.loc[
    latest_df["temperature"].idxmax()
]

coldest = latest_df.loc[
    latest_df["temperature"].idxmin()
]

average = latest_df["temperature"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔥 En Sıcak İl",
        hottest["city"],
        f"{hottest['temperature']:.1f} °C"
    )

with col2:
    st.metric(
        "❄️ En Soğuk İl",
        coldest["city"],
        f"{coldest['temperature']:.1f} °C"
    )

with col3:
    st.metric(
        "🌡️ Türkiye Ortalaması",
        f"{average:.1f} °C"
    )

with col4:
    st.metric(
        "📍 Takip Edilen İl",
        len(latest_df)
    )

# ==================================================
# EN SICAK 10
# ==================================================

st.divider()
st.subheader("🔥 En Sıcak 10 İl")

top10 = latest_df.nlargest(
    10,
    "temperature"
)

st.bar_chart(
    top10.set_index("city")["temperature"]
)

# ==================================================
# EN SOĞUK 10
# ==================================================

st.divider()
st.subheader("❄️ En Soğuk 10 İl")

bottom10 = latest_df.nsmallest(
    10,
    "temperature"
)

st.bar_chart(
    bottom10.set_index("city")["temperature"]
)

# ==================================================
# TÜRKİYE HARİTASI
# ==================================================

st.divider()
st.subheader("🗺️ Türkiye Sıcaklık Haritası")

map_data = latest_df[
    [
        "latitude",
        "longitude",
        "temperature"
    ]
].copy()

st.map(
    map_data,
    latitude="latitude",
    longitude="longitude",
    size="temperature",
    zoom=5
)

# ==================================================
# ZAMAN SERİSİ
# ==================================================

st.divider()
st.subheader("📈 Şehir Sıcaklık Geçmişi")

selected_city = st.selectbox(
    "Bir il seç:",
    sorted(df["city"].unique())
)

city_history = (
    df[df["city"] == selected_city]
    .sort_values("datetime")
    .copy()
)

current_temperature = city_history.iloc[-1][
    "temperature"
]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"🌡️ {selected_city}",
        f"{current_temperature:.1f} °C"
    )

with col2:
    st.metric(
        "📊 Toplam Ölçüm",
        len(city_history)
    )

history_chart = (
    city_history[
        ["datetime", "temperature"]
    ]
    .set_index("datetime")
)

st.line_chart(history_chart)

# ==================================================
# GÜNCEL VERİ TABLOSU
# ==================================================

st.divider()
st.subheader("📋 Güncel 81 İl")

table = latest_df[
    [
        "city",
        "temperature",
        "datetime"
    ]
].sort_values(
    "temperature",
    ascending=False
)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

# ==================================================
# ALT BİLGİ
# ==================================================

st.divider()

st.caption(
    "DataPulse Türkiye | "
    "Python • SQL • SQLite • Pandas • "
    "Open-Meteo API • Streamlit"
)