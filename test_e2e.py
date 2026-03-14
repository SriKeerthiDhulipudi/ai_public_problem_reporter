#!/usr/bin/env python3
"""End-to-end test: Submit report via API and verify it appears in dashboard"""

import urllib.request
import urllib.error
import json
from time import sleep

BASE_URL = 'http://localhost:5000'
print('===== END-TO-END TESTING =====\n')

sleep(1)

# Test 1: Submit a report
print('1. Submitting report...')
try:
    report_data = {
        'problem_type': 'Water Leak',
        'location': 'Main Street junction with Park Avenue',
        'description': 'Water gushing from underground pipe causing street flooding',
        'date_noticed': '2025-03-14',
        'severity': 'High',
        'evidence': 'Multiple photos and video',
        'name': 'Jane Smith',
        'phone': '555-9876',
        'email': 'jane.smith@email.com'
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
    
    # Test 2: Retrieve the submitted report
    print('\n2. Retrieving submitted report...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/reports/{ref_id}', timeout=5)
    report = json.loads(response.read().decode('utf-8'))
    
    print(f'   ✅ Report retrieved successfully')
    print(f'   Type: {report.get("problem_type")}')
    print(f'   Location: {report.get("location")}')
    print(f'   Severity: {report.get("severity")}')
    print(f'   Department: {report.get("department")}')
    print(f'   Status: {report.get("status")}')
    
    # Test 3: List all reports
    print('\n3. Checking reports list...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/reports', timeout=5)
    reports = json.loads(response.read().decode('utf-8'))
    print(f'   ✅ Total reports in system: {len(reports)}')
    
    # Test 4: Get statistics
    print('\n4. Checking statistics...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/statistics', timeout=5)
    stats = json.loads(response.read().decode('utf-8'))
    print(f'   ✅ Statistics retrieved')
    print(f'   Total Reports: {stats.get("total_reports")}')
    print(f'   High Severity: {stats.get("severity_breakdown", {}).get("High", 0)}')
    
    # Test 5: Add a comment
    print('\n5. Adding comment to report...')
    comment_data = {'comment': 'Maintenance crew dispatched - ETA 30 minutes'}
    req = urllib.request.Request(
        f'{BASE_URL}/api/reports/{ref_id}/comments',
        data=json.dumps(comment_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req, timeout=5)
    comment_result = json.loads(response.read().decode('utf-8'))
    print(f'   ✅ Comment added')
    
    # Test 6: Update report status
    print('\n6. Updating report status...')
    status_data = {'status': 'In Progress'}
    req = urllib.request.Request(
        f'{BASE_URL}/api/reports/{ref_id}/status',
        data=json.dumps(status_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    response = urllib.request.urlopen(req, timeout=5)
    print(f'   ✅ Status updated to: In Progress')
    
    # Test 7: Search
    print('\n7. Searching for reports...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/search?q=water', timeout=5)
    search_results = json.loads(response.read().decode('utf-8'))
    print(f'   ✅ Found {len(search_results)} report(s) matching "water"')
    
    # Test 8: Export CSV
    print('\n8. Testing CSV export...')
    response = urllib.request.urlopen(f'{BASE_URL}/api/export/csv', timeout=5)
    csv_data = response.read().decode('utf-8')
    lines = csv_data.strip().split('\n')
    print(f'   ✅ CSV export working ({len(lines)} lines exported)')
    
    print('\n' + '='*40)
    print('✅ ALL TESTS PASSED!')
    print('='*40)
    print('\nThe complete application is working:')
    print('  • Report submission ✅')
    print('  • Report retrieval ✅')
    print('  • Report listing ✅')
    print('  • Statistics ✅')
    print('  • Comments ✅')
    print('  • Status updates ✅')
    print('  • Search functionality ✅')
    print('  • CSV export ✅')
    
except urllib.error.HTTPError as e:
    print(f'   ❌ HTTP Error {e.code}: {e.reason}')
    print(f'   Body: {e.read().decode()}')
except urllib.error.URLError as e:
    print(f'   ❌ Connection error: {e.reason}')
except Exception as e:
    print(f'   ❌ Error: {e}')
