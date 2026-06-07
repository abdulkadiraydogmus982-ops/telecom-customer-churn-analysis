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