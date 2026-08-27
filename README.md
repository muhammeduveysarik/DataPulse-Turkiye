# 🌡️ DataPulse Türkiye

DataPulse Türkiye, Türkiye'nin 81 ilinden gerçek zamanlı hava durumu verilerini toplayan, işleyen, SQL veritabanında saklayan ve interaktif bir dashboard üzerinden analiz eden uçtan uca bir veri projesidir.

Proje; veri toplama, ETL pipeline, SQL, veri kalitesi, zaman serisi analizi, görselleştirme ve otomatik veri toplama süreçlerini uygulamalı olarak göstermek amacıyla geliştirilmiştir.

## 🚀 Proje Mimarisi

```text
Open-Meteo API
      ↓
Python ETL Pipeline
      ↓
Retry Mechanism
      ↓
SQLite Database
      ↓
Data Quality Checks
      ↓
Pandas Analysis
      ↓
Streamlit Dashboard
      ↓
Historical / Time-Series Analysis
```

Veri toplama işlemi Windows Task Scheduler ile saatlik olarak otomatik çalıştırılabilir.

## ✨ Özellikler

- Türkiye'nin 81 ilinden hava durumu verisi toplama
- Open-Meteo API entegrasyonu
- Python tabanlı ETL pipeline
- API hatalarında otomatik retry mekanizması
- SQLite üzerinde historical data saklama
- SQL sorguları ile veri analizi
- Pandas ile veri işleme
- Eksik ve hatalı veri kontrolleri
- Duplicate kayıt kontrolü
- En sıcak ve en soğuk şehir analizi
- Türkiye sıcaklık ortalaması
- En sıcak / en soğuk 10 şehir
- 81 ilin harita üzerinde görüntülenmesi
- Şehir bazlı sıcaklık geçmişi
- Time-series grafikler
- Streamlit tabanlı interaktif dashboard
- Saatlik otomatik veri toplama

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Kullanım |
|---|---|
| Python | Ana programlama dili |
| Requests | API üzerinden veri toplama |
| Open-Meteo API | Hava durumu veri kaynağı |
| SQLite | Veritabanı |
| SQL | Veri sorgulama |
| Pandas | Veri analizi ve işleme |
| Matplotlib | Veri görselleştirme |
| Streamlit | Dashboard |
| Windows Task Scheduler | Pipeline otomasyonu |

## 🔄 ETL Pipeline

### Extract

Open-Meteo API üzerinden 81 ilin güncel sıcaklık verileri alınır.

### Transform

API'den gelen veriler işlenir ve şehir, koordinat, zaman ve sıcaklık bilgileri standart bir yapıya dönüştürülür.

### Load

İşlenen veriler SQLite veritabanındaki `weather` tablosuna kaydedilir.

Her çalıştırmada yeni ölçümler eklenerek geçmiş hava durumu verileri korunur.

## 🔁 Retry Mekanizması

API isteğinin geçici olarak başarısız olması durumunda pipeline isteği otomatik olarak tekrar dener.

Bu sayede tek bir şehirde oluşan geçici bağlantı problemi tüm pipeline'ın başarısız olmasına neden olmaz.

## 🗄️ Veritabanı

Ana veritabanı:

```text
weather.db
```

Ana tablo:

```text
weather
```

Örnek SQL sorgusu:

```sql
SELECT city, temperature
FROM weather
ORDER BY temperature DESC
LIMIT 10;
```

## ✅ Data Quality

Pipeline içerisindeki veriler için çeşitli kalite kontrolleri uygulanır:

- Eksik değer kontrolü
- Anormal sıcaklık kontrolü
- 81 ilin mevcut olup olmadığının kontrolü
- Duplicate kayıt kontrolü

Kontroller başarılı olduğunda:

```text
DATA QUALITY CHECK PASSED
```

sonucu alınır.

## 📊 Dashboard

Streamlit dashboard üzerinden:

- Güncel sıcaklıklar
- En sıcak şehir
- En soğuk şehir
- Türkiye sıcaklık ortalaması
- En sıcak 10 şehir
- En soğuk 10 şehir
- Türkiye haritası
- Şehir bazlı sıcaklık geçmişi
- Historical data
- Time-series grafikler

incelenebilir.

Dashboard'u çalıştırmak için:

```bash
streamlit run dashboard.py
```

## ▶️ ETL Pipeline'ı Çalıştırma

```bash
python main.py
```

## 🔍 Data Quality Kontrolü

```bash
python data_quality.py
```

## 📂 Proje Yapısı

```text
DataPulseV2/
│
├── main.py
├── dashboard.py
├── analysis.py
├── queries.py
├── database.py
├── data_quality.py
├── cities.csv
├── weather.db
└── README.md
```

## 🎯 Projenin Amacı

DataPulse Türkiye ile uçtan uca bir veri pipeline'ının temel bileşenleri uygulamalı olarak oluşturulmuştur:

**Data Collection → ETL → Database → SQL → Data Quality → Analysis → Visualization → Automation**

Proje, ilerleyen aşamalarda PostgreSQL, Docker, cloud deployment ve daha gelişmiş veri orkestrasyon araçlarıyla genişletilebilir.