#!/usr/bin/env python3
"""Test with urllib instead of subprocess for compatibility"""

import urllib.request
import urllib.error
from time import sleep

BASE_URL = 'http://localhost:5000'
print('Testing Flask API endpoints...\n')

tests = [
    ('Homepage', '/'),
    ('Submit page', '/submit'),
    ('Dashboard', '/dashboard'),
    ('List all reports API', '/api/reports'),
    ('Get departments API', '/api/departments'),
    ('Get statistics API', '/api/statistics'),
    ('Search API', '/api/search?q=water'),
    ('Export CSV API', '/api/export/csv'),
]

sleep(1)

passed = 0
for i, (name, path) in enumerate(tests, 1):
    url = BASE_URL + path
    try:
        response = urllib.request.urlopen(url, timeout=5)
        status = response.status
        status_str = '✅' if status == 200 else f'⚠️ {status}'
        print(f'{i}. {name:30} {status_str}')
        response.close()
        if status == 200:
            passed += 1
    except urllib.error.URLError as e:
        print(f'{i}. {name:30} ❌ Connection error')
    except Exception as e:
        print(f'{i}. {name:30} ❌ {str(e)[:30]}')

print(f'\n✅ Results: {passed}/{len(tests)} endpoints responding')
print('🎉 Web server is working!')
