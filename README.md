# Clean Data API

## Problem
Customer data arrived as a messy CSV: inconsistent city casing, mixed date formats,
currency symbols in amounts, invalid emails, and duplicate rows. It was unusable for
reporting or integration.

## Approach
1. Cleaned the data with pandas (deduplication, normalization, validation)
2. Stored it in SQLite
3. Exposed it through a FastAPI REST API with filtering

## Before / After

Raw CSV:
```
id,name,email,city,signup_date,amount
1,,user1@example.com,Amsterdam,31-12-2023,"1,200.00"
2,jan JANSEN,USER2@Example.com ,AMSTERDAM,31-12-2023,100
```

API response:
```json
{
  "id": 81,
  "name": "Anna De Vries",
  "email": null,
  "city": "Amsterdam",
  "signup_date": "2024-04-20",
  "amount": 250.5
}
```

## Run it
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn pandas
    python make_messy_data.py
    python clean.py
    uvicorn main:app --reload
Then open http://127.0.0.1:8000/docs

## Tradeoffs
- SQLite is simple and needs no setup, but wouldn't suit many concurrent writers
- Invalid emails are set to null rather than dropped, so no records are lost

## Results
- 215 raw rows reduced to 200 unique clean rows
- Every date in ISO format, every amount numeric

## Next steps
Dockerize, add tests, deploy to the cloud