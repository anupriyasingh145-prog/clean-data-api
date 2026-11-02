import sqlite3
import pandas as pd

df = pd.read_csv("data/raw_customers.csv", dtype=str)
print("Raw rows:", len(df))

df = df.drop_duplicates()
df["id"] = df["id"].astype(int)

df["name"] = (df["name"].fillna("").str.strip()
              .str.replace(r"\s+", " ", regex=True).str.title())
df["name"] = df["name"].where(df["name"] != "", None)

df["email"] = df["email"].fillna("").str.strip().str.lower()
valid = df["email"].str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
df["email"] = df["email"].where(valid, None)

df["city"] = df["city"].fillna("").str.strip().str.title()

df["signup_date"] = pd.to_datetime(
    df["signup_date"], format="mixed", dayfirst=True, errors="coerce"
).dt.strftime("%Y-%m-%d")

df["amount"] = pd.to_numeric(
    df["amount"].fillna("").str.replace(r"[€,]", "", regex=True), errors="coerce"
)

print("Clean rows:", len(df))
print(df.isna().sum())

with sqlite3.connect("customers.db") as conn:
    df.to_sql("customers", conn, if_exists="replace", index=False)
print("Saved to customers.db")