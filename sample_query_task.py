"""Sample script to create and run a query task"""
from news_search import NewsSearchModule, Database

def setup_database():
    """Initialize database tables"""
    print("Setting up database tables...")
    db = Database()
    db.init_tables()
    print("✓ Database tables created\n")

def create_sample_task():
    """Create a sample query task"""
    print("Creating sample query task...")
    db = Database()
    
    task_name = "malaysia_solar_pv_daily"
    prompt = "Search for Malaysia solar PV news from the last 24 hours. Return only news article URLs in JSON array format, maximum 20 links. No descriptions."
    schedule = "0 8 * * *"  # Daily at 8 AM
    
    # Check if task already exists
    existing = db.get_query_task(task_name)
    if existing:
        print(f"✓ Task '{task_name}' already exists\n")
        return task_name
    
    task_id = db.create_query_task(task_name, prompt, schedule)
    print(f"✓ Created task '{task_name}' (ID: {task_id})")
    print(f"  Prompt: {prompt}")
    print(f"  Schedule: {schedule}\n")
    
    return task_name

def run_sample_task(task_name: str):
    """Run the sample query task"""
    print(f"Running task: {task_name}")
    print("=" * 80)
    
    search_module = NewsSearchModule()
    result = search_module.run_task(task_name)
    
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    
    if result["success"]:
        print(f"✓ Task completed successfully")
        print(f"  Total URLs found: {result['total_found']}")
        print(f"  New links saved: {result['new_links']}")
        print(f"  Duplicates filtered: {result['duplicates']}")
        print(f"  Invalid URLs: {result['invalid']}")
        
        if result['urls']:
            print(f"\n  New URLs saved:")
            for item in result['urls']:
                print(f"    [{item['id']}] {item['url']}")
    else:
        print(f"✗ Task failed: {result.get('error')}")
    
    print("\n")

def list_pending_links():
    """List pending links for processing"""
    print("Pending links for processing:")
    print("=" * 80)
    
    db = Database()
    pending = db.get_pending_links(10)
    
    if pending:
        for link in pending:
            print(f"[{link['id']}] {link['url']}")
            print(f"    Source: {link['source_task']} | Discovered: {link['discovered_at']}")
    else:
        print("No pending links")
    
    print("\n")

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("NEWS SEARCH MODULE - SAMPLE QUERY TASK")
    print("=" * 80 + "\n")
    
    # Step 1: Setup database
    setup_database()
    
    # Step 2: Create sample task
    task_name = create_sample_task()
    
    # Step 3: Run the task
    run_sample_task(task_name)
    
    # Step 4: Show pending links
    list_pending_links()
    
    print("=" * 80)
    print("Sample task execution completed!")
    print("=" * 80)

if __name__ == "__main__":
    main()
