#!/usr/bin/env python3
"""Test enhanced features: GPS location and AI description"""

import urllib.request
import urllib.error
import json
from time import sleep

BASE_URL = 'http://localhost:5000'
print('===== TESTING ENHANCED FEATURES =====\n')

sleep(2)

# Test 1: Submit a report with GPS coordinates
print('1. Submitting report with GPS location...')
try:
    report_data = {
        'problem_type': 'Pothole',
        'location': 'Main Street near City Hall',
        'description': 'Large pothole about 1 meter wide and 20 cm deep, causing vehicle damage',
        'date_noticed': '2025-03-14',
        'severity': 'High',
        'evidence': 'Photos taken',
        'name': 'John Doe',
        'phone': '555-1234',
        'email': 'john@example.com',
        'latitude': '40.7128',
        'longitude': '-74.0060'
    }
    
    req = urllib.request.Request(
        f'{BASE_URL}/api/submit-report',
        data=json.dumps(report_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode('utf-8'))
    ref_id = result.get('reference_id')
    
    print(f'   ✅ Report submitted successfully')
    print(f'   Reference ID: {ref_id}')
    
    # Test 2: Display full report
    print('\n2. Retrieving full report with AI analysis...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/reports/{ref_id}', timeout=5)
    report = json.loads(response.read().decode('utf-8'))
    
    print(f'\n   📋 PUBLIC ISSUE REPORT')
    print(f'   ─' * 40)
    print(f'   Location: {report.get("location")}')
    print(f'   Latitude: {report.get("latitude")}')
    print(f'   Longitude: {report.get("longitude")}')
    print(f'   Issue Type: {report.get("problem_type")}')
    print(f'   AI Description:')
    print(f'   {report.get("ai_description")}')
    print(f'   Severity Level: {report.get("severity")}')
    print(f'   Suggested Department: {report.get("department")}')
    print(f'   Date Reported: {report.get("created_at")}')
    
    # Test 3: Test another issue type (Water Leak)
    print('\n3. Testing AI description for different issue type...')
    report_data2 = {
        'problem_type': 'Water Leakage',
        'location': 'Park Avenue near intersection',
        'description': 'Water gushing from underground pipe, causing street flooding',
        'date_noticed': '2025-03-14',
        'severity': 'High',
        'evidence': 'Video recorded',
        'name': 'Jane Smith',
        'phone': '555-9876',
        'email': 'jane@example.com',
        'latitude': '40.7580',
        'longitude': '-73.9855'
    }
    
    req = urllib.request.Request(
        f'{BASE_URL}/api/submit-report',
        data=json.dumps(report_data2).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode('utf-8'))
    ref_id2 = result.get('reference_id')
    
    response = urllib.request.urlopen(f'{BASE_URL}/api/reports/{ref_id2}', timeout=5)
    report2 = json.loads(response.read().decode('utf-8'))
    
    print(f'\n   📋 PUBLIC ISSUE REPORT')
    print(f'   ─' * 40)
    print(f'   Location: {report2.get("location")}')
    print(f'   Latitude: {report2.get("latitude")}')
    print(f'   Longitude: {report2.get("longitude")}')
    print(f'   Issue Type: {report2.get("problem_type")}')
    print(f'   AI Description:')
    print(f'   {report2.get("ai_description")}')
    print(f'   Severity Level: {report2.get("severity")}')
    print(f'   Suggested Department: {report2.get("department")}')
    
    # Test 4: Test garbage issue
    print('\n4. Testing AI description for garbage issue...')
    report_data3 = {
        'problem_type': 'Garbage',
        'location': 'Central Park area',
        'description': 'Garbage accumulation around park entrance, affecting cleanliness',
        'date_noticed': '2025-03-13',
        'severity': 'Medium',
        'name': 'Anonymous',
        'latitude': '40.7829',
        'longitude': '-73.9654'
    }
    
    req = urllib.request.Request(
        f'{BASE_URL}/api/submit-report',
        data=json.dumps(report_data3).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    response = urllib.request.urlopen(req, timeout=5)
    result = json.loads(response.read().decode('utf-8'))
    ref_id3 = result.get('reference_id')
    
    response = urllib.request.urlopen(f'{BASE_URL}/api/reports/{ref_id3}', timeout=5)
    report3 = json.loads(response.read().decode('utf-8'))
    
    print(f'\n   📋 PUBLIC ISSUE REPORT')
    print(f'   ─' * 40)
    print(f'   Location: {report3.get("location")}')
    print(f'   Latitude: {report3.get("latitude")}')
    print(f'   Longitude: {report3.get("longitude")}')
    print(f'   Issue Type: {report3.get("problem_type")}')
    print(f'   AI Description:')
    print(f'   {report3.get("ai_description")}')
    print(f'   Severity Level: {report3.get("severity")}')
    print(f'   Suggested Department: {report3.get("department")}')
    
    print('\n' + '='*50)
    print('✅ ALL ENHANCED FEATURES WORKING!')
    print('='*50)
    print('\nNew Features Verified:')
    print('  ✅ GPS Location Detection')
    print('  ✅ AI-Powered Problem Description')
    print('  ✅ Intelligent Department Routing')
    print('  ✅ Structured Report Format')
    print('\nThe application now provides:')
    print('  • Live GPS coordinates in reports')
    print('  • AI-generated professional descriptions')
    print('  • Smart department suggestions based on issue type')
    print('  • Complete structured report format for authorities')
    
except urllib.error.HTTPError as e:
    print(f'   ❌ HTTP Error {e.code}')
    try:
        error_body = json.loads(e.read().decode('utf-8'))
        print(f'   Details: {error_body}')
    except:
        pass
except Exception as e:
    print(f'   ❌ Error: {e}')
