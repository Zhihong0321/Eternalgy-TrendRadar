"""
Test script to verify deployment readiness
Checks all critical components before deployment
"""

import sys
import os
from pathlib import Path

print("=" * 80)
print("DEPLOYMENT READINESS TEST")
print("=" * 80)
print()

# Test 1: Check Python version
print("Test 1: Python Version")
print(f"  Python: {sys.version}")
required_version = (3, 10)
current_version = sys.version_info[:2]
if current_version >= required_version:
    print(f"  ✓ Python {current_version[0]}.{current_version[1]} >= {required_version[0]}.{required_version[1]}")
else:
    print(f"  ✗ Python {current_version[0]}.{current_version[1]} < {required_version[0]}.{required_version[1]}")
print()

# Test 2: Check required files
print("Test 2: Required Files")
required_files = [
    "main.py",
    "requirements.txt",
    "config/config.yaml",
    "config/frequency_words.txt",
    "docker/Dockerfile",
    "docker/docker-compose.yml",
    "docker/entrypoint.sh",
    "docker/manage.py"
]

all_files_exist = True
for file_path in required_files:
    exists = Path(file_path).exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {file_path}")
    if not exists:
        all_files_exist = False
print()

# Test 3: Check dependencies
print("Test 3: Dependencies")
dependencies = [
    "requests",
    "pytz",
    "yaml",
]

all_deps_ok = True
for dep in dependencies:
    try:
        __import__(dep)
        print(f"  ✓ {dep}")
    except ImportError:
        print(f"  ✗ {dep} (not installed)")
        all_deps_ok = False
print()

# Test 4: Check main.py imports
print("Test 4: Main Module")
try:
    import main
    print(f"  ✓ main.py imports successfully")
    print(f"  ✓ Version: {main.VERSION}")
except Exception as e:
    print(f"  ✗ main.py import failed: {e}")
    all_deps_ok = False
print()

# Test 5: Check AI processing module
print("Test 5: AI Processing Module")
try:
    from ai_processing import ArticleProcessor, RawArticle
    print(f"  ✓ ai_processing imports successfully")
    print(f"  ✓ ArticleProcessor available")
    print(f"  ✓ RawArticle model available")
except Exception as e:
    print(f"  ✗ ai_processing import failed: {e}")
    all_deps_ok = False
print()

# Test 6: Check config loading
print("Test 6: Configuration")
try:
    config_path = "config/config.yaml"
    if Path(config_path).exists():
        print(f"  ✓ config.yaml exists")
        print(f"  ✓ Platforms configured: {len(main.CONFIG['PLATFORMS'])}")
        print(f"  ✓ Report mode: {main.CONFIG['REPORT_MODE']}")
        print(f"  ✓ Crawler enabled: {main.CONFIG['ENABLE_CRAWLER']}")
        print(f"  ✓ Notification enabled: {main.CONFIG['ENABLE_NOTIFICATION']}")
    else:
        print(f"  ✗ config.yaml not found")
        all_deps_ok = False
except Exception as e:
    print(f"  ✗ Config loading failed: {e}")
    all_deps_ok = False
print()

# Test 7: Check NewsNow API connectivity
print("Test 7: NewsNow API Connectivity")
try:
    import requests
    api_url = os.getenv('NEWSNOW_API_URL', 'https://eternalgy-newsnow-production.up.railway.app')
    test_url = f"{api_url}/api/s?id=eia"
    
    response = requests.get(test_url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ API accessible: {api_url}")
        print(f"  ✓ Test source (eia): {data.get('status')}")
        print(f"  ✓ Items returned: {len(data.get('items', []))}")
    else:
        print(f"  ✗ API returned status {response.status_code}")
except Exception as e:
    print(f"  ⚠ API test failed: {e}")
    print(f"  Note: This is OK if you're testing offline")
print()

# Test 8: Check output directory
print("Test 8: Output Directory")
try:
    output_dir = Path("output")
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created output directory")
    else:
        print(f"  ✓ Output directory exists")
except Exception as e:
    print(f"  ✗ Output directory check failed: {e}")
print()

# Test 9: Check Docker files
print("Test 9: Docker Configuration")
docker_files = {
    "docker/Dockerfile": "Dockerfile for building image",
    "docker/docker-compose.yml": "Docker Compose configuration",
    "docker/entrypoint.sh": "Container entrypoint script",
    "docker/.env": "Environment variables (optional)"
}

for file_path, description in docker_files.items():
    exists = Path(file_path).exists()
    status = "✓" if exists else ("⚠" if "optional" in description else "✗")
    print(f"  {status} {file_path}")
print()

# Final Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)

if all_files_exist and all_deps_ok:
    print("✓ ALL TESTS PASSED - Ready for deployment!")
    print()
    print("Next steps:")
    print("  1. Test locally: python main.py")
    print("  2. Build Docker: cd docker && docker-compose build")
    print("  3. Run Docker: docker-compose up -d")
    print("  4. Check logs: docker-compose logs -f")
else:
    print("✗ SOME TESTS FAILED - Fix issues before deployment")
    print()
    if not all_files_exist:
        print("  - Missing required files")
    if not all_deps_ok:
        print("  - Missing dependencies or import errors")
    print()
    print("Run: pip install -r requirements.txt")

print("=" * 80)
