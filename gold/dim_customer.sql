{{ config(materialized='table') }}

SELECT DISTINCT
    customer_id,
    customer_name,
    country
FROM {{ ref('silver_ecommerce_sales') }}
