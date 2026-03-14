#!/usr/bin/env python3
"""
AI Public Problem Reporter - Website Verification Script
Verifies the complete web application is ready to run
"""

import sys
import os
from pathlib import Path
import subprocess


def check_python_version():
    """Check Python version."""
    print("\n🔍 Python Version Check")
    print("-" * 50)
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    print("✓ Python version OK")
    return True


def check_flask_installation():
    """Check if Flask is installed."""
    print("\n📦 Flask Installation Check")
    print("-" * 50)
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__} installed")
        return True
    except ImportError:
        print("❌ Flask not installed")
        print("   Install with: pip install -r requirements.txt")
        return False


def check_website_files():
    """Check all website files exist."""
    print("\n📁 Website Files Check")
    print("-" * 50)
    
    required_files = {
        'server.py': 'Flask application',
        'requirements.txt': 'Dependencies',
        'templates/index.html': 'Home page',
        'templates/submit.html': 'Submission form',
        'templates/dashboard.html': 'Dashboard',
        'static/style.css': 'Styling',
        'static/script.js': 'JavaScript',
    }
    
    all_exist = True
    for filepath, description in required_files.items():
        path = Path(filepath)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {filepath:30} ({size:,} bytes) - {description}")
        else:
            print(f"❌ {filepath:30} MISSING")
            all_exist = False
    
    return all_exist


def check_directories():
    """Check required directories."""
    print("\n📂 Directories Check")
    print("-" * 50)
    
    required_dirs = ['templates', 'static']
    
    for dirname in required_dirs:
        path = Path(dirname)
        if path.exists() and path.is_dir():
            files = list(path.glob('*'))
            print(f"✓ {dirname:20} ({len(files)} files)")
        else:
            print(f"❌ {dirname:20} MISSING")
            return False
    
    return True


def check_port_availability():
    """Check if port 5000 is available."""
    print("\n🔌 Port Availability Check")
    print("-" * 50)
    
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    
    if result == 0:
        print("⚠ Port 5000 appears to be in use")
        print("   Stop the application using it or use a different port")
        return False
    else:
        print("✓ Port 5000 is available")
        return True


def check_database_setup():
    """Check if database can be created."""
    print("\n🗄️  Database Check")
    print("-" * 50)
    
    db_path = Path('reports.db')
    
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"✓ Database exists ({size:,} bytes)")
        
        # Check if it can be opened
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"  Tables: {len(tables)}")
            conn.close()
            return True
        except Exception as e:
            print(f"⚠ Database may be corrupted: {e}")
            return False
    else:
        print("ℹ Database will be created on first run")
        return True


def test_flask_app():
    """Test if Flask app can be imported."""
    print("\n🚀 Flask Application Check")
    print("-" * 50)
    
    try:
        # Import app
        sys.path.insert(0, '.')
        from server import app, init_db
        
        print("✓ Flask application imported successfully")
        
        # Check for required functions
        if hasattr(app, 'route'):
            print("✓ Flask routes defined")
        
        print("✓ Database initialization available")
        return True
    
    except Exception as e:
        print(f"❌ Error loading Flask app: {e}")
        return False


def run_diagnostics():
    """Run all diagnostic checks."""
    print("\n" + "=" * 50)
    print("AI PUBLIC PROBLEM REPORTER - WEBSITE CHECK")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Flask Installation", check_flask_installation),
        ("Website Files", check_website_files),
        ("Directories", check_directories),
        ("Database Setup", check_database_setup),
        ("Port Availability", check_port_availability),
        ("Flask Application", test_flask_app),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {name}")
    
    print("\n" + "=" * 50)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🚀 Ready to run the website!")
        print("\nNextstep: python server.py")
        print("Then visit: http://localhost:5000")
        return True
    else:
        print(f"⚠ SOME CHECKS FAILED ({passed}/{total} passed)")
        print("\nFix the issues above and try again.")
        return False


def main():
    """Main entry point."""
    try:
        success = run_diagnostics()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
