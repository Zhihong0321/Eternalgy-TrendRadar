"""Test deployment with Docker PostgreSQL"""
import time
import sys
import psycopg2
from news_search import NewsSearchModule, Database, ProcessorWorker

def wait_for_db(max_attempts=30):
    """Wait for PostgreSQL to be ready"""
    print("Waiting for PostgreSQL to be ready...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5433",
                database="news_db",
                user="postgres",
                password="postgres"
            )
            conn.close()
            print(f"✓ PostgreSQL is ready (attempt {attempt})")
            return True
        except psycopg2.OperationalError:
            print(f"  Attempt {attempt}/{max_attempts}: Waiting...")
            time.sleep(2)
    
    print("✗ PostgreSQL failed to start")
    return False

def test_database_connection():
    """Test database connection"""
    print("\n" + "=" * 80)
    print("TEST 1: Database Connection")
    print("=" * 80)
    
    try:
        db = Database()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ Connected to PostgreSQL")
            print(f"  Version: {version}")
            cursor.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_table_creation():
    """Test table creation"""
    print("\n" + "=" * 80)
    print("TEST 2: Table Creation")
    print("=" * 80)
    
    try:
        db = Database()
        db.init_tables()
        print("✓ Tables created successfully")
        
        # Verify tables exist
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            print(f"\n  Created tables:")
            for table in tables:
                print(f"    - {table[0]}")
            cursor.close()
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        return False

def test_query_task_creation():
    """Test creating a query task"""
    print("\n" + "=" * 80)
    print("TEST 3: Query Task Creation")
    print("=" * 80)
    
    try:
        db = Database()
        
        task_name = "malaysia_solar_pv_daily"
        prompt = "Search for Malaysia solar PV news from the last 24 hours. Return only news article URLs in JSON array format, maximum 20 links. No descriptions."
        schedule = "0 8 * * *"
        
        # Check if exists
        existing = db.get_query_task(task_name)
        if existing:
            print(f"✓ Task '{task_name}' already exists")
            print(f"  ID: {existing['id']}")
            print(f"  Active: {existing['is_active']}")
            return True
        
        # Create new task
        task_id = db.create_query_task(task_name, prompt, schedule)
        print(f"✓ Created task '{task_name}'")
        print(f"  ID: {task_id}")
        print(f"  Prompt: {prompt[:60]}...")
        print(f"  Schedule: {schedule}")
        return True
    except Exception as e:
        print(f"✗ Task creation failed: {e}")
        return False

def test_search_execution():
    """Test search execution"""
    print("\n" + "=" * 80)
    print("TEST 4: Search Execution")
    print("=" * 80)
    
    try:
        # Create processor (mock mode)
        processor = ProcessorWorker(ai_processor=None)
        
        # Create search module with processor
        search = NewsSearchModule(processor_worker=processor)
        
        # Run task
        print("Executing search query...")
        result = search.run_task("malaysia_solar_pv_daily")
        
        if result["success"]:
            print(f"✓ Search completed successfully")
            print(f"\n  📊 Search Results:")
            print(f"    Total URLs found: {result['total_found']}")
            print(f"    New links saved: {result['new_links']}")
            print(f"    Duplicates filtered: {result['duplicates']}")
            print(f"    Invalid URLs: {result['invalid']}")
            
            if result.get('processing'):
                proc = result['processing']
                print(f"\n  🔄 Processing Results:")
                print(f"    Total processed: {proc['total']}")
                print(f"    Success: {proc['success']}")
                print(f"    Failed: {proc['failed']}")
                
                if proc.get('by_domain'):
                    print(f"\n  📍 By Domain:")
                    for domain, stats in proc['by_domain'].items():
                        print(f"    {domain}: {stats['success']}/{stats['total']} success")
            
            if result['urls']:
                print(f"\n  🔗 Sample URLs (first 5):")
                for item in result['urls'][:5]:
                    print(f"    [{item['id']}] {item['url']}")
                if len(result['urls']) > 5:
                    print(f"    ... and {len(result['urls']) - 5} more")
            
            return True
        else:
            print(f"✗ Search failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"✗ Search execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_statistics():
    """Test statistics retrieval"""
    print("\n" + "=" * 80)
    print("TEST 5: Statistics")
    print("=" * 80)
    
    try:
        db = Database()
        stats = db.get_statistics()
        
        print(f"✓ Statistics retrieved")
        print(f"\n  📊 Links:")
        print(f"    Total: {stats['links']['total_links']}")
        print(f"    Pending: {stats['links']['pending']}")
        print(f"    Processing: {stats['links']['processing']}")
        print(f"    Completed: {stats['links']['completed']}")
        print(f"    Failed: {stats['links']['failed']}")
        
        print(f"\n  📋 Tasks:")
        print(f"    Total: {stats['tasks']['total_tasks']}")
        print(f"    Active: {stats['tasks']['active_tasks']}")
        
        return True
    except Exception as e:
        print(f"✗ Statistics retrieval failed: {e}")
        return False

def main():
    """Main test execution"""
    print("\n" + "=" * 80)
    print("DOCKER DEPLOYMENT TEST")
    print("=" * 80)
    
    # Wait for database
    if not wait_for_db():
        print("\n✗ Database not ready. Exiting.")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Database Connection", test_database_connection),
        ("Table Creation", test_table_creation),
        ("Query Task Creation", test_query_task_creation),
        ("Search Execution", test_search_execution),
        ("Statistics", test_statistics)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
