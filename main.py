import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Clean Data API")

def query(sql, params=()):
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/records")
def records(city: Optional[str] = None, limit: int = 50):
    sql, params = "SELECT * FROM customers", []
    if city:
        sql += " WHERE city = ?"
        params.append(city.title())
    sql += " LIMIT ?"
    params.append(limit)
    return query(sql, params)

@app.get("/records/{record_id}")
def one_record(record_id: int):
    rows = query("SELECT * FROM customers WHERE id = ?", (record_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="Record not found")
    return rows[0]