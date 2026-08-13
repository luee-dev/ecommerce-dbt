{{ config(materialized='table') }}

SELECT
    transaction_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    price,
    quantity * price as total_amount,
    order_status
FROM {{ ref('siver_ecommerce_sales') }}
