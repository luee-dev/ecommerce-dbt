# 🛒 E-Commerce Data Engineering Pipeline with dbt

An end-to-end data engineering project that simulates an e-commerce sales platform using **Python Faker**, loads data into **PostgreSQL**, and transforms it through a **Medallion Architecture (Bronze → Silver → Gold)** using **dbt**.

The project demonstrates modern ELT practices including synthetic data generation, data quality validation, layered data modeling, dimensional modeling, and containerized development using Docker.

---

# 📖 Project Overview

Organizations rarely perform analytics directly on transactional data. Instead, raw data is ingested into a data warehouse, cleaned, standardized, and transformed into business-ready models.

This project follows that approach by:

* Generating realistic e-commerce transaction data with Python Faker
* Injecting intentional data quality issues to simulate real-world datasets
* Loading raw data into PostgreSQL
* Transforming data with dbt using the Medallion Architecture
* Creating dimensional models for analytical reporting

---

# 🏗️ Architecture

```text
                        Python Faker
                              │
                              ▼
                Synthetic E-Commerce Dataset
                              │
                              ▼
                     PostgreSQL Warehouse
                              │
                              ▼
                   Bronze Layer (Raw View)
                              │
                              ▼
             Silver Layer (Clean & Standardized)
                              │
                              ▼
          Gold Layer (Star Schema Dimensions & Facts)
                              │
                              ▼
                 BI Reporting / SQL Analytics
```

---

# 🎯 Business Scenario

Imagine working as a Data Engineer for an online retailer.

Thousands of transactions are generated daily, but the raw data contains common quality issues such as:

* Missing customer IDs
* Duplicate transactions
* Negative prices
* Invalid quantities
* Future order dates
* Invalid country codes

Before analysts can build dashboards, the data must be cleaned and transformed into reliable business models.

This project demonstrates that complete ELT workflow.

---

# 🛠️ Technology Stack

| Category            | Technology              |
| ------------------- | ----------------------- |
| Programming         | Python 3.11             |
| Data Generation     | Faker                   |
| Data Processing     | Pandas                  |
| Database            | PostgreSQL 15           |
| Data Transformation | dbt Core                |
| dbt Adapter         | dbt-postgres            |
| Containerization    | Docker & Docker Compose |
| SQL                 | PostgreSQL SQL          |
| Version Control     | Git & GitHub            |

---

# 📁 Project Structure

```text
.
├── data-source/
│   └── sales-generation.py
│
├── bronze/
│   └── bronze_ecommerce_sales.sql
│
├── silver/
│   └── silver_ecommerce_sales.sql
│
├── gold/
│   ├── dim_customer.sql
│   ├── dim_product.sql
│   └── fct_order.sql
│
├── tests/
├── dbt_project.yml
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# 📊 Synthetic Data Generation

The dataset is generated using **Python Faker**.

Each execution creates **1,000 synthetic e-commerce transactions** containing realistic customer and order information.

## Generated Fields

| Column           | Description                       |
| ---------------- | --------------------------------- |
| transaction_id   | Unique transaction identifier     |
| order_date       | Order date                        |
| customer_id      | Customer identifier               |
| customer_name    | Customer name                     |
| country          | Customer country                  |
| product_id       | Product identifier                |
| product_category | Product category                  |
| quantity         | Quantity purchased                |
| price            | Unit price                        |
| payment_method   | Payment type                      |
| order_status     | Completed, Cancelled, or Returned |

---

# ⚠️ Simulated Data Quality Issues

To better represent production datasets, approximately **8% of records** are intentionally corrupted.

Injected errors include:

* Missing customer IDs
* Negative quantities
* Negative prices
* Future order dates
* Invalid country codes
* Duplicate transaction IDs

These issues are resolved during the Silver transformation layer.

---

# 🥉 Bronze Layer

**Model:** `bronze.sql`

Purpose:

Store raw transactional data exactly as received.

No transformations are applied.

```sql
SELECT *
FROM ecommerce_sales
```

The Bronze layer serves as the immutable source for downstream transformations.

---

# 🥈 Silver Layer

**Model:** `silver.sql`

The Silver layer improves data quality by applying business rules and standardization.

## Transformations Performed

### Date Validation

Removes transactions with future dates.

```sql
order_date <= current_date
```

### Customer Validation

Removes records with missing customer IDs.

### Country Standardization

Unknown country codes are replaced with:

```text
Unknown
```

### Quantity Validation

Negative quantities become:

```text
1
```

### Price Validation

Negative prices become:

```text
0
```

### Deduplication

Duplicate transaction IDs are removed using:

```sql
ROW_NUMBER()
OVER (
    PARTITION BY transaction_id
    ORDER BY order_date DESC
)
```

Only the most recent transaction is retained.

---

# 🥇 Gold Layer

The Gold layer transforms cleaned transactional data into a simple dimensional model for analytics.

## Customer Dimension

**Model:** `dim_customer.sql`

Attributes:

* Customer ID
* Customer Name
* Country

---

## Product Dimension

**Model:** `dim_product.sql`

Attributes:

* Product ID
* Product Category

---

## Order Fact Table

**Model:** `fct_order.sql`

Measures:

* Quantity
* Price
* Total Amount

Calculated metric:

```text
Total Amount = Quantity × Price
```

The fact table links customers, products, and sales transactions, making it suitable for reporting and dashboarding.

---

# 📈 Data Flow

```text
Python Faker
      │
      ▼
Generate CSV
      │
      ▼
PostgreSQL
      │
      ▼
Bronze View
      │
      ▼
Silver Table
      │
      ▼
Gold Star Schema
      │
      ▼
Analytics & Reporting
```

---

# 🐳 Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-dbt.git

cd ecommerce-dbt
```

---

## 2. Start Docker

```bash
docker compose up --build
```

This starts:

* PostgreSQL 15
* dbt Core

---

## 3. Generate Synthetic Data

```bash
python data-source/sales-generator.py
```

This creates:

```text
ecommerce_sales.csv
```

---

## 4. Load Data into PostgreSQL

Import the generated CSV into the `ecommerce_sales` table using your preferred method (for example, `COPY`, pgAdmin, or another PostgreSQL client).

---

## 5. Execute dbt Models

Run all models:

```bash
docker exec -it dbt_core dbt run
```

Run tests:

```bash
docker exec -it dbt_core dbt test
```

---

# 📊 Final Data Model

```text
                     fct_order
                   ┌─────────────┐
                   │transaction_id│
                   │customer_id   │
                   │product_id    │
                   │order_date    │
                   │quantity      │
                   │price         │
                   │total_amount  │
                   └──────┬───────┘
                          │
           ┌──────────────┴──────────────┐
           │                             │
           ▼                             ▼

    dim_customer                 dim_product
    ─────────────                ─────────────
    customer_id                  product_id
    country                      product_category
    ```

---

# 💡 Skills Demonstrated

* Python
* Faker
* Pandas
* PostgreSQL
* SQL
* dbt
* ELT Pipeline Design
* Medallion Architecture
* Data Cleaning
* Data Validation
* Data Quality Rules
* Deduplication with Window Functions
* Star Schema Modeling
* Docker
* Docker Compose
* Git

---

# 🚀 Future Enhancements

Planned improvements include:

* Incremental dbt models
* dbt source freshness checks
* Generic and custom dbt tests
* dbt documentation (`dbt docs`)
* Snapshot models (Slowly Changing Dimensions)
* Airflow orchestration
* Power BI dashboards
* GitHub Actions CI/CD
* Cloud deployment (AWS, Azure, or GCP)
* Partitioned fact tables
* Additional dimensions (Date, Payment, Geography)

---

# 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 About This Project

This repository was built as a portfolio project to demonstrate practical data engineering skills using open-source technologies. It showcases how synthetic transactional data can be transformed into analytics-ready datasets using a layered Medallion Architecture and dimensional modeling with dbt, following patterns commonly used in modern data platforms.
