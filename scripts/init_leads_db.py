#!/usr/bin/env python3
from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parent.parent
path = root / 'data' / 'leads.sqlite3'
path.parent.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(path) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            source TEXT,
            created_at TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    conn.commit()
print(path)
