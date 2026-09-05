----------------------------------------** dev schema creation
CREATE SCHEMA IF NOT EXISTS dev.landing;
CREATE SCHEMA IF NOT EXISTS dev.bronze;
CREATE SCHEMA IF NOT EXISTS dev.silver;
CREATE SCHEMA IF NOT EXISTS dev.gold;
----------------------------------------** dev volume creation
CREATE VOLUME IF NOT EXISTS dev.landing.exchange_rates;
CREATE VOLUME IF NOT EXISTS dev.landing.loan_records;
CREATE VOLUME IF NOT EXISTS dev.landing.payment_records;



----------------------------------------** stg schema creation
CREATE SCHEMA IF NOT EXISTS stg.landing;
CREATE SCHEMA IF NOT EXISTS stg.bronze;
CREATE SCHEMA IF NOT EXISTS stg.silver;
CREATE SCHEMA IF NOT EXISTS stg.gold;
----------------------------------------** stg volume creation
CREATE VOLUME IF NOT EXISTS stg.landing.loan_records;
CREATE VOLUME IF NOT EXISTS stg.landing.exchange_rates;
CREATE VOLUME IF NOT EXISTS stg.landing.payment_records;



----------------------------------------** prod schema creation
CREATE SCHEMA IF NOT EXISTS prod.landing;
CREATE SCHEMA IF NOT EXISTS prod.bronze;
CREATE SCHEMA IF NOT EXISTS prod.silver;
CREATE SCHEMA IF NOT EXISTS prod.gold;
----------------------------------------** prod volume creation
CREATE VOLUME IF NOT EXISTS prod.landing.exchange_rates;
CREATE VOLUME IF NOT EXISTS prod.landing.loan_records;
CREATE VOLUME IF NOT EXISTS prod.landing.payment_records;
