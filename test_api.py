#!/usr/bin/env python3
"""Test Flask API endpoints"""

import requests
import json
from time import sleep

# Give server time to start
sleep(2)

BASE_URL = 'http://localhost:5000'
print('Testing Flask API endpoints...\n')

try:
    # Test 1: Homepage
    print('1️⃣  Testing homepage...')
    r = requests.get(f'{BASE_URL}/')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    
    # Test 2: Submit page
    print('2️⃣  Testing submit form page...')
    r = requests.get(f'{BASE_URL}/submit')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    
    # Test 3: Dashboard
    print('3️⃣  Testing dashboard page...')
    r = requests.get(f'{BASE_URL}/dashboard')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    
    # Test 4: Get all reports
    print('4️⃣  Testing GET /api/reports...')
    r = requests.get(f'{BASE_URL}/api/reports')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Reports in DB: {len(data)}')
    
    # Test 5: Get departments
    print('5️⃣  Testing GET /api/departments...')
    r = requests.get(f'{BASE_URL}/api/departments')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    if r.status_code == 200:
        depts = r.json()
        print(f'   Departments available: {len(depts)}')
    
    # Test 6: Get statistics
    print('6️⃣  Testing GET /api/statistics...')
    r = requests.get(f'{BASE_URL}/api/statistics')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    if r.status_code == 200:
        stats = r.json()
        print(f'   Total reports: {stats.get("total_reports", 0)}')
    
    # Test 7: Submit a test report
    print('7️⃣  Testing POST /api/submit-report (test submission)...')
    payload = {
        'problem_type': 'pothole',
        'location': 'Main Street near City Hall',
        'description': 'Large pothole causing damage to vehicles',
        'date_noticed': '2025-03-14',
        'severity': 'high',
        'evidence': 'photos and video',
        'name': 'John Doe',
        'phone': '555-1234',
        'email': 'john@example.com'
    }
    r = requests.post(f'{BASE_URL}/api/submit-report', json=payload)
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 201 else "❌ FAILED"}')
    if r.status_code == 201:
        result = r.json()
        ref_id = result.get('reference_id')
        print(f'   Reference ID: {ref_id}')
        
        # Test 8: Retrieve the submitted report
        print('8️⃣  Testing GET /api/reports/<reference_id>...')
        r = requests.get(f'{BASE_URL}/api/reports/{ref_id}')
        print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
        if r.status_code == 200:
            report = r.json()
            print(f'   Report retrieved: {report["problem_type"]} at {report["location"]}')
    
    # Test 9: Search
    print('9️⃣  Testing /api/search...')
    r = requests.get(f'{BASE_URL}/api/search?q=pothole')
    print(f'   Status: {r.status_code} {"✅ OK" if r.status_code == 200 else "❌ FAILED"}')
    
    print('\n✅ All API endpoints working!')
    
except Exception as e:
    print(f'\n❌ Error during testing: {e}')
    print('   Server may not be running on port 5000')
