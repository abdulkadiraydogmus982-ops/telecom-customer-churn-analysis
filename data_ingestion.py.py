import pandas as pd
from sqlalchemy import create_engine
import urllib

# 1. IBM Telco Churn Verisini Doğrudan GitHub'dan Çekelim
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
print("Veri internetten indiriliyor...")
raw_df = pd.read_csv(url)

# 2. Veriyi Şirket Formatında 3 Parçaya Bölelim
dim_customers = raw_df[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents']]

fact_subscriptions = raw_df[['customerID', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 
                             'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 
                             'StreamingTV', 'StreamingMovies']]

fact_billing = raw_df[['customerID', 'Contract', 'PaperlessBilling', 'PaymentMethod', 
                       'MonthlyCharges', 'TotalCharges', 'Churn']]

# 3. MSSQL Bağlantı Ayarları (Windows Authentication - Windows Girişi İçin)
# NOT: Eğer SQL Server'a şifreyle giriyorsan UID ve PWD kısımlarını eklemeliyiz.
params = urllib.parse.quote_plus(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-3EL1LFFM\SQLEXPRESS01;'  # Eğer hata alırsan buraya kendi SQL Server adını yazmalısın
    r'DATABASE=GlobalTelco_DB;'
    r'Trusted_Connection=yes;'
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 4. Verileri Tablolara Basalım (Append moduyla)
print("Veriler MSSQL tablolara yükleniyor...")
try:
    dim_customers.to_sql('dim_customers', schema='dbo', con=engine, if_exists='append', index=False)
    fact_subscriptions.to_sql('fact_subscriptions', schema='dbo', con=engine, if_exists='append', index=False)
    fact_billing.to_sql('fact_billing', schema='dbo', con=engine, if_exists='append', index=False)
    print("🚀 Başarılı! Tüm veriler şirketin veri ambarına yüklendi.")
except Exception as e:
    print("❌ Bir hata oluştu:", e)