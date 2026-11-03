import sqlite3

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_records_respects_limit():
    r = client.get("/records?limit=5")
    assert r.status_code == 200
    assert len(r.json()) <= 5


def test_city_filter_returns_clean_city():
    r = client.get("/records?city=Amsterdam")
    assert r.status_code == 200
    assert all(rec["city"] == "Amsterdam" for rec in r.json())


def test_missing_record_returns_404():
    assert client.get("/records/999999").status_code == 404


def test_no_duplicate_ids():
    conn = sqlite3.connect("customers.db")
    total, unique = conn.execute(
        "SELECT COUNT(*), COUNT(DISTINCT id) FROM customers"
    ).fetchone()
    assert total == unique