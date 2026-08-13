import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Configuration
NUMBER_OF_RECORDS = 1000
ERROR_PERCENTAGE = 0.08 # 8% of records will contain errors

countries = ["KE", "UG", "TZ", "ET", "SO", "RW"]
categories = ["Electronics", "Clothing", "Sports", "Home", "Books"]
payment_methods = ["M-pesa", "Credit Card", "PayPal", "Airtel Money"]
order_status = ["Completed", "Cancelled", "Returned"]

def data_generation():
    data = []

    for i in range(NUMBER_OF_RECORDS):
        order_date = fake.date_between(start_date='-1y', end_date="today")
        quantity = random.randint(1, 5)
        price = round(ramdom.uniform(10, 500), 2)

        data.append({
            "transaction_id": f"T{i+1}",
            "order_date": order_date,
            "customer_id": f"C{random.randint(1, 300)}",
            "country": random.choice(countries),
            "product_id": f"P{random.randint(1, 200}}",
            "product_category": random.choice(categories),
            "quantity": quantity,
            "price": price,
            "payment_method": random.choice(payment_methods),
            "order_status": random.choice(order_status)
        })

    df = pd.DataFrame(data)

    inject_errors(df)

    df.to_csv("ecommerce_sales.csv", index=False)
    print("csv file successfully generated")

def inject_errors(df):
    num_errors = int(len(df) * ERROR_PERCENTAGE)

    for _ in range(num_errors):
        row = random.randint(0, len(df) - 1)
        error_type = random.choice([
            "null_customer",
            "negative_quantity",
            "invalid_price",
            "future_date",
            "invalid_country",
            "duplicate_transaction"
        ])

        if error_type == "null_customer":
            df.at[row, "customer_id"] = None
        elif error_type == "negative_quantity":
            df.at[row, "quantity"] = -random.randint(1, 5)
        elif error_type == "ivalid_price":
            df.at[row, "price"] = -random.randint(1, 100)
        elif error_type == "future_date":
            df.at[row, "order_date"] = datetime.now() + timedelta(days=30)
        elif error_type == "invalid_country":
            df.at[row, "country"] = "XYZ"
        elif error_type == "duplicate_transaction":
            df.at[row, "transaction_id"] = "T1"

if __name__ == "__main__":
    data_generation()
