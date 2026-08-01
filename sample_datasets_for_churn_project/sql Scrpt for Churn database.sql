CREATE DATABASE CUSTOMER_CHURN_PROJECT;
USE CUSTOMER_CHURN_PROJECT;

CREATE TABLE Customers(
CustomerId VARCHAR(50),
Gender VARCHAR(10),
SeniorCitizen INT,
Partner VARCHAR(10),
Dependents VARCHAR(10),
Tenure INT,
PhoneService VARCHAR(10),
MultipleLines VARCHAR(50),
InternetService VARCHAR(20),
OnlineSecurity VARCHAR(20),
OnlineBackup VARCHAR(20),
DeviceProtection VARCHAR(20),
TechSupport VARCHAR(20),
StreamingTv VARCHAR(20),
StreamingMovies VARCHAR(20),
Contract VARCHAR(20),
PapelessBilling VARCHAR(20),
PaymentMethod VARCHAR(50),
MonthlyCharges FLOAT ,
TotalCharges FLOAT ,
Churn VARCHAR(10)
);
DESC CUSTOMERS;
