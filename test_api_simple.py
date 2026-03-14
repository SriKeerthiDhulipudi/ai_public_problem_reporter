#!/usr/bin/env python3
"""Simplified API test with better error handling"""

import subprocess
import json
from time import sleep

BASE_URL = 'http://localhost:5000'
print('Testing Flask API endpoints...\n')

tests = [
    ('Homepage', 'GET', '/'),
    ('Submit page', 'GET', '/submit'),
    ('Dashboard', 'GET', '/dashboard'),
    ('List all reports', 'GET', '/api/reports'),
    ('Get departments', 'GET', '/api/departments'),
    ('Get statistics', 'GET', '/api/statistics'),
    ('Search reports', 'GET', '/api/search?q=water'),
]

sleep(1)  # Give server time

for i, (name, method, path) in enumerate(tests, 1):
    url = BASE_URL + path
    try:
        result = subprocess.run(
            ['curl', '-s', '-w', '%{http_code}', '-X', method, url],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Last 3 chars are status code
        output = result.stdout
        status_code = output[-3:] if len(output) >= 3 else '000'
        
        status_str = '✅ OK' if status_code.startswith('2') else f'⚠️  {status_code}'
        print(f'{i}️⃣  {name:25} {method} {status_str}')
        
    except subprocess.TimeoutExpired:
        print(f'{i}️⃣  {name:25} {method} ⏱️  TIMEOUT')
    except Exception as e:
        print(f'{i}️⃣  {name:25} {method} ❌ {str(e)[:30]}')

print('\n✅ API endpoint testing complete!')
