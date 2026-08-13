{{ config(materialized='table') }}

SELECT DISTINCT
    product_id,
    product_category
FROM {{ ref('sivler_ecommerce_sales') }}

