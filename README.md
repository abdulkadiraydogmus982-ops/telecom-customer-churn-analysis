# Telecom Customer Churn Analytics & Prediction

## Project Overview

This project was developed to analyze customer churn behavior in a telecommunications company and predict which customers are likely to leave in the future using machine learning techniques.

The project covers the complete data analytics lifecycle, including:

* Data Ingestion
* Data Modeling
* Data Cleaning & Transformation
* Exploratory Data Analysis (EDA)
* Customer Segmentation
* Predictive Analytics

## Business Problem

Customer churn is one of the biggest challenges for telecom companies.

The goal of this project is to:

* Identify factors that influence customer churn.
* Discover high-risk customer groups.
* Segment customers based on their value.
* Predict future churn using machine learning.

---

## Technologies Used

### Database

* Microsoft SQL Server (MSSQL)

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* SQLAlchemy
* PyODBC

---

## Project Architecture

Raw Data

↓

SQL Server Database

↓

Data Cleaning & Transformation

↓

Exploratory Data Analysis (EDA)

↓

Customer Segmentation

↓

Machine Learning Model

↓

Customer Churn Prediction

---

## Phase 1: Data Engineering & Database Design

The raw telecom dataset was imported into Microsoft SQL Server.

The database was designed using a relational model with multiple tables:

* dim_customers
* fact_subscriptions
* fact_billing

A custom Python ingestion pipeline was developed to load the raw dataset into SQL Server.

---

## Phase 2: SQL Data Cleaning & Transformation

A master analytical view was created using SQL.

Key operations:

* Joining multiple tables using INNER JOIN
* Handling missing values
* Converting incorrect data types
* Creating calculated business metrics

Output:

v_churn_analytics_master

---

## Phase 3: Exploratory Data Analysis (EDA)

Business insights were generated through data visualization.

Key findings:

* Customers with monthly contracts have significantly higher churn rates.
* Customers with higher monthly charges are more likely to leave.
* Long-term contracts improve customer retention.

---

## Phase 4: Customer Segmentation

Customers were segmented according to their value using custom scoring methods.

Customer Groups:

* Champions
* Loyal Customers
* At Risk
* Lost Customers

This allows marketing teams to target customers more effectively.

---

## Phase 5: Churn Prediction

Machine learning techniques were used to predict customer churn.

Model:

* Random Forest Classifier

Preprocessing:

* One-Hot Encoding
* Train/Test Split (80/20)

Results:

| Metric    | Score         |
| --------- | ------------- |
| Accuracy  | 79.49%        |
| Recall    | 0.50          |
| Algorithm | Random Forest |

---

## Key Business Insights

* Contract type is one of the strongest predictors of churn.
* Monthly charges strongly influence customer retention.
* Customer segmentation helps optimize marketing spending.
* Predictive analytics enables proactive customer retention strategies.

---

## Future Improvements

* XGBoost implementation
* Hyperparameter optimization
* Interactive Power BI dashboard
* Real-time prediction API
* Automated ETL pipelines

---



## Data Visualizations

### Overall Churn Analysis

![Overall Churn Analysis](images/churn_overview.png)

This visualization presents the overall churn rate and the impact of contract type on customer retention.

---

### Monthly Charges vs Churn

![Monthly Charges vs Churn](images/monthly_charges_churn.png)

Customers with higher monthly charges show a significantly higher probability of churn.

---

### Customer Segmentation

![Customer Segmentation](images/customer_segmentation.png)

Customers were segmented into Champions, Loyal, At Risk and Lost groups to support targeted retention strategies.

---

### Feature Importance

![Feature Importance](images/feature_importance.png)

Feature importance analysis reveals which variables contribute most to churn prediction decisions.



## Author

Abdulkadir Aydogmus

Data Analytics | SQL | Python | Machine Learning
