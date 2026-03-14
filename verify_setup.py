#!/usr/bin/env python3
"""
Verification and Health Check Script
Ensures the AI Public Problem Reporter is properly set up and ready to use.
Run this to verify everything is working correctly.
"""

import sys
from pathlib import Path


def check_environment():
    """Check Python environment."""
    print("🔍 Environment Check")
    print("-" * 50)
    
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Python Version: {python_version}")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required!")
        return False
    print("✓ Python version OK")
    return True


def check_files():
    """Check all required files exist."""
    print("\n📁 Files Check")
    print("-" * 50)
    
    required_files = {
        'problem_reporter.py': 'Main Application',
        'README.md': 'Documentation',
        'QUICKSTART.md': 'Quick Start Guide',
        'EXAMPLES.md': 'Example Reports',
        'CUSTOMIZATION.md': 'Customization Guide',
        'INDEX.md': 'Project Index'
    }
    
    all_exist = True
    for filename, description in required_files.items():
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {filename:30} ({size:,} bytes) - {description}")
        else:
            print(f"❌ {filename:30} MISSING - {description}")
            all_exist = False
    
    return all_exist


def check_reports_folder():
    """Check reports folder."""
    print("\n📂 Reports Folder Check")
    print("-" * 50)
    
    reports_dir = Path('reports')
    
    if reports_dir.exists():
        print(f"✓ Reports folder exists")
        
        txt_reports = list(reports_dir.glob('*.txt'))
        json_reports = list(reports_dir.glob('*.json'))
        
        total_reports = len(txt_reports) + len(json_reports)
        print(f"  - Text reports (.txt): {len(txt_reports)}")
        print(f"  - JSON reports (.json): {len(json_reports)}")
        print(f"  - Total reports: {total_reports}")
        
        if total_reports > 0:
            print(f"✓ Reports folder is working (has {total_reports} report(s))")
        else:
            print(f"✓ Reports folder is ready (empty, waiting for first report)")
        
        return True
    else:
        print(f"⚠ Reports folder doesn't exist yet (will be created on first run)")
        return True


def check_application():
    """Check if application runs without errors."""
    print("\n🚀 Application Check")
    print("-" * 50)
    
    try:
        app_file = Path('problem_reporter.py')
        
        if not app_file.exists():
            print("❌ Application file not found")
            return False
        
        # Try to import to check for syntax errors
        import importlib.util
        spec = importlib.util.spec_from_file_location("problem_reporter", app_file)
        module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(module)
            print("✓ Application loaded successfully (no syntax errors)")
            
            # Check for ProblemReporter class
            if hasattr(module, 'ProblemReporter'):
                print("✓ ProblemReporter class found")
                pr = module.ProblemReporter()
                print("✓ ProblemReporter instance created successfully")
                
                # Check for required methods
                required_methods = ['run', 'generate_report', 'suggest_department']
                for method in required_methods:
                    if hasattr(pr, method):
                        print(f"  ✓ Method '{method}' exists")
                    else:
                        print(f"  ❌ Method '{method}' missing")
                        return False
                
                return True
            else:
                print("❌ ProblemReporter class not found")
                return False
                
        except Exception as e:
            print(f"❌ Error loading application: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_documentation():
    """Check documentation files."""
    print("\n📖 Documentation Check")
    print("-" * 50)
    
    docs = {
        'README.md': 'Main Documentation',
        'QUICKSTART.md': 'Quick Start (2 min setup)',
        'EXAMPLES.md': 'Sample Reports',
        'CUSTOMIZATION.md': 'Advanced Customization'
    }
    
    all_exist = True
    for filename, description in docs.items():
        path = Path(filename)
        if path.exists():
            # Count lines
            with open(path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            print(f"✓ {filename:20} ({lines} lines) - {description}")
        else:
            print(f"❌ {filename:20} MISSING")
            all_exist = False
    
    return all_exist


def run_diagnostics():
    """Run all diagnostic checks."""
    print("\n" + "=" * 50)
    print("AI PUBLIC PROBLEM REPORTER - HEALTH CHECK")
    print("=" * 50)
    
    checks = [
        ("Environment", check_environment),
        ("Files", check_files),
        ("Reports Folder", check_reports_folder),
        ("Documentation", check_documentation),
        ("Application", check_application),
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
        print("\n🚀 System is ready to use!")
        print("\nNext step: Run the application")
        print("  python problem_reporter.py")
        return True
    else:
        print(f"⚠ SOME CHECKS FAILED ({passed}/{total} passed)")
        print("\nPlease fix the issues above before using the application.")
        return False


def main():
    """Main entry point."""
    try:
        success = run_diagnostics()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDiagnostics cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
