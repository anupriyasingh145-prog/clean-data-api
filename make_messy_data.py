import csv
import random
from pathlib import Path

random.seed(42)
cities = ["Amsterdam", "amsterdam ", "AMSTERDAM", "Utrecht", "utrecht", "Rotterdam", "Almere", "almere "]
names = ["  Anna de Vries", "jan JANSEN", "Piet Bakker ", "SOFIE smit", "Lars  Visser", ""]
dates = ["2024-01-15", "15/02/2024", "March 3, 2024", "2024-04-20", "", "31-12-2023"]
amounts = ["100", "€250.50", "1,200.00", "abc", "", "75.5"]

rows = []
for i in range(1, 201):
    rows.append({
        "id": i,
        "name": random.choice(names),
        "email": random.choice([f"user{i}@example.com", f"USER{i}@Example.com ", "not-an-email", ""]),
        "city": random.choice(cities),
        "signup_date": random.choice(dates),
        "amount": random.choice(amounts),
    })
rows += random.sample(rows, 15)  # add duplicates

Path("data").mkdir(exist_ok=True)
with open("data/raw_customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("Created data/raw_customers.csv with", len(rows), "rows")