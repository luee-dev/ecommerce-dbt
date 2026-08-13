{{ config(materialized='table') }}

with cleaned as (
    SELECT
        transaction_id,
	cast(order_date as date) as order_date,
	customer_id,
	customer_name,
	case
	    when country in ('KE', 'UG', 'TZ', 'SO', 'ET', 'RW') then country
	    else 'Unknown'
	end as country,
	product_id,
	product_category,
	case
	    when quantity > 0 then quantity
	    else 1
	end as quantity,
	case
	    when price > 0 then price
	    else 0
	end as price,
	order_status
    FROM {{ ref('bronze_ecommerce_sales') }}
    WHERE customer_id IS NOT NULL
        AND CAST(order_date as date) <= current_date
),

deduplicated as (
    SELECT *,
	row_number() OVER(PARTITION BY transaction_id ORDER BY order_date DESC) as rn
    from cleaned
)

SELECT *
FROM deduplicated
WHERE rn = 1
