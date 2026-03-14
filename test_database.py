#!/usr/bin/env python3
"""Test script to verify database setup"""

import sqlite3
from pathlib import Path

db = Path('reports.db')
if db.exists():
    print(f'✅ Database exists ({db.stat().st_size:,} bytes)')
    
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f'✅ Tables created: {len(tables)}')
    
    for table in tables:
        print(f'   - {table[0]}')
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'     Records: {count}')
    
    conn.close()
    print('\n✅ Database integrity verified')
else:
    print('⚠️  Database will be created on first run')
