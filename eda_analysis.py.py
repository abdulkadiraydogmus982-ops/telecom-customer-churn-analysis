import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib
from sqlalchemy import create_engine

# 1. MSSQL Bağlantısını Kur ve Veriyi Çek
params = urllib.parse.quote_plus(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-3EL1LFFM\SQLEXPRESS01;'  # Hata alırsan kendi SQL Server adını yaz
    r'DATABASE=GlobalTelco_DB;'
    r'Trusted_Connection=yes;'
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

query = "SELECT * FROM v_churn_analytics_master"
df = pd.read_sql(query, engine)

print(f"Veri başarıyla Python'a aktarıldı. Toplam Gözlem: {df.shape[0]} satır, {df.shape[1]} sütun.\n")

# --- KURUMSAL ANALİZ VE GÖRSELLEŞTİRME ---

# Grafiklerin genel tarzını belirleyelim (Şirket sunumlarına uygun temiz bir tarz)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 5))

# İÇGÖRÜ 1: Şirketin Genel Churn Oranı Nedir?
plt.subplot(1, 2, 1)
churn_counts = df['is_churn'].value_counts(normalize=True) * 100
sns.barplot(x=churn_counts.index, y=churn_counts.values, palette="muted")
plt.title("Şirket Genel Müşteri Terk (Churn) Oranı (%)", fontsize=12, fontweight='bold')
plt.xlabel("Kayıp Durumu (0: Kalan, 1: Kaçan)")
plt.ylabel("Oran (%)")
for i, v in enumerate(churn_counts.values):
    plt.text(i, v + 1, f"%{v:.1f}", ha='center', fontweight='bold')

# İÇGÖRÜ 2: Sözleşme Tipi Churn Durumunu Nasıl Etkiliyor?
# (Şirket yöneticilerinin en çok merak ettiği analizlerden biri)
plt.subplot(1, 2, 2)
sns.countplot(data=df, x='contract_type', hue='is_churn', palette="Set2")
plt.title("Sözleşme Tipine Göre Müşteri Dağılımı", fontsize=12, fontweight='bold')
plt.xlabel("Sözleşme Türü")
plt.ylabel("Müşteri Sayısı")
plt.legend(title='Durum', labels=['Kalan', 'Kaçan'])

plt.tight_layout()
plt.show()

# İÇGÖRÜ 3: Sayısal Analiz (Aylık Ücretlerin Churn Üzerindeki Etkisi)
plt.figure(figsize=(8, 5))
sns.kdeplot(data=df, x='MonthlyCharges', hue='is_churn', fill=True, common_norm=False, palette="crest", alpha=0.5)
plt.title("Aylık Ücret Dağılımının Churn Durumuna Göre Analizi", fontsize=12, fontweight='bold')
plt.xlabel("Aylık Ödenen Ücret ($)")
plt.ylabel("Yoğunluk")
plt.show()



# --- MÜŞTERİ SEGMENTASYONU VE SKORLAMA ---

# 1. Özelliklerin Hazırlanması (Normalizasyon)
# Müşterileri adil karşılaştırmak için 0-1 arası bir puanlama yapalım
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# Skorlama için kullanacağımız sütunlar: Tenure, MonthlyCharges, TotalCharges
df['tenure_score'] = scaler.fit_transform(df[['customer_tenure_months']])
df['monthly_score'] = scaler.fit_transform(df[['MonthlyCharges']])
df['total_score'] = scaler.fit_transform(df[['TotalCharges']])

# 2. Toplam Değer Skoru (Customer Value Score) Hesaplama
# Şirket mantığı: Uzun süredir bizimle olan (tenure) ve çok para bırakan (total) değerlidir.
df['customer_value_score'] = (df['tenure_score'] * 0.4) + (df['total_score'] * 0.4) + (df['monthly_score'] * 0.2)

# 3. Segmentlere Ayırma (Kural Tabanlı Segmentasyon)
def segment_customers(score):
    if score > 0.7:
        return 'Champions (En Değerli)'
    elif score > 0.4:
        return 'Loyal Customers (Sadık)'
    elif score > 0.2:
        return 'At Risk (Riskli)'
    else:
        return 'Lost/Low Value (Düşük Değer/Kayıp)'

df['customer_segment'] = df['customer_value_score'].apply(segment_customers)

# 4. Segmentlerin Görselleştirilmesi
plt.figure(figsize=(10, 6))
segment_counts = df['customer_segment'].value_counts().sort_values(ascending=False)
sns.barplot(x=segment_counts.values, y=segment_counts.index, palette="viridis")
plt.title("Müşteri Segmentasyonu Dağılımı", fontsize=14, fontweight='bold')
plt.xlabel("Müşteri Sayısı")
plt.ylabel("Segmentler")
plt.show()

# 5. Segmentlere Göre Churn Oranı (Şirket için en kritik tablo)
segment_churn = df.groupby('customer_segment')['is_churn'].mean().sort_values(ascending=False) * 100
print("\n--- Segment Bazlı Churn Oranları (%) ---")
print(segment_churn)


# --- MAKİNE ÖĞRENMESİ İLE CHURN TAHMİNİ ---

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. Model İçin Özellik Seçimi (Feature Selection)
# Kimlik belirten ve hedef değişken olan sütunları çıkarıyoruz, kalanları X yapıyoruz
features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'customer_tenure_months', 
            'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
            'TechSupport', 'StreamingTV', 'StreamingMovies', 'contract_type', 
            'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']

X = df[features]
y = df['is_churn'] # Hedef Değişken (0: Kalır, 1: Gider)

# 2. Kategorik Değişkenleri Sayısallaştırma (One-Hot Encoding)
# Bilgisayarın 'DSL' veya 'Male' kelimelerini anlaması için 0 ve 1'lere bölüyoruz
X_encoded = pd.get_dummies(X, drop_first=True)

# 3. Veriyi Eğitim ve Test Olarak Bölme (Train-Test Split)
# Verinin %80'i ile modeli eğiteceğiz, %20'si ile modeli test edeceğiz
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.20, random_state=42, stratify=y)

print(f"Eğitim Seti Boyutu: {X_train.shape[0]} satır")
print(f"Test Seti Boyutu: {X_test.shape[0]} satır\n")

# 4. Modelin Kurulması ve Eğitilmesi (Random Forest)
print("Random Forest Modeli eğitiliyor...")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# 5. Model Tahminleri ve Başarı Analizi
y_pred = model.predict(X_test)

print("\n================ KURUMSAL MODEL RAPORU ================")
print(f"Genel Doğruluk (Accuracy) Skoru: %{accuracy_score(y_test, y_pred)*100:.2f}")
print("\nSınıflandırma Raporu (Classification Report):")
print(classification_report(y_test, y_pred))
print("=======================================================")

# 6. Özellik Önem Düzeyleri (Feature Importance)
# Şirket yöneticisine "Modelimiz en çok hangi değişkene bakarak karar veriyor?" sorusunun cevabı
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices][:10], y=X_encoded.columns[indices][:10], palette="mako")
plt.title("Modelin Karar Verirken En Çok Önem Verdiği İlk 10 Özellik", fontsize=12, fontweight='bold')
plt.xlabel("Önem Skoru")
plt.ylabel("Özellikler")
plt.tight_layout()
plt.show()