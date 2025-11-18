"""Sample script with integrated processing workflow"""
from news_search import NewsSearchModule, Database, ProcessorWorker

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

def run_complete_workflow(task_name: str):
    """Run complete workflow: Search + Process"""
    print(f"Running complete workflow for task: {task_name}")
    print("=" * 80)
    
    # Initialize processor worker (with mock processing for demo)
    processor = ProcessorWorker(ai_processor=None)  # Pass your AI processor here
    
    # Initialize search module with processor
    search_module = NewsSearchModule(processor_worker=processor)
    
    # Run task (will auto-process if AUTO_PROCESS_AFTER_SEARCH=True)
    result = search_module.run_task(task_name)
    
    print("\n" + "=" * 80)
    print("WORKFLOW RESULTS:")
    print("=" * 80)
    
    if result["success"]:
        print(f"✓ Search completed successfully")
        print(f"\n📊 Search Statistics:")
        print(f"  Total URLs found: {result['total_found']}")
        print(f"  New links saved: {result['new_links']}")
        print(f"  Duplicates filtered: {result['duplicates']}")
        print(f"  Invalid URLs: {result['invalid']}")
        
        if result.get('processing'):
            proc = result['processing']
            print(f"\n🔄 Processing Statistics:")
            print(f"  Total processed: {proc['total']}")
            print(f"  Success: {proc['success']}")
            print(f"  Failed: {proc['failed']}")
            
            if proc.get('by_domain'):
                print(f"\n  By Domain:")
                for domain, stats in proc['by_domain'].items():
                    print(f"    {domain}: {stats['success']}/{stats['total']} success")
        
        if result['urls']:
            print(f"\n📝 New URLs:")
            for item in result['urls'][:5]:  # Show first 5
                print(f"  [{item['id']}] {item['url']}")
            if len(result['urls']) > 5:
                print(f"  ... and {len(result['urls']) - 5} more")
    else:
        print(f"✗ Workflow failed: {result.get('error')}")
    
    print("\n")

def show_statistics():
    """Show overall statistics"""
    print("=" * 80)
    print("OVERALL STATISTICS")
    print("=" * 80)
    
    db = Database()
    stats = db.get_statistics()
    
    print(f"\n📊 Links:")
    print(f"  Total: {stats['links']['total_links']}")
    print(f"  Pending: {stats['links']['pending']}")
    print(f"  Processing: {stats['links']['processing']}")
    print(f"  Completed: {stats['links']['completed']}")
    print(f"  Failed: {stats['links']['failed']}")
    
    print(f"\n📋 Tasks:")
    print(f"  Total: {stats['tasks']['total_tasks']}")
    print(f"  Active: {stats['tasks']['active_tasks']}")
    
    print("\n")

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("NEWS SEARCH MODULE - COMPLETE WORKFLOW DEMO")
    print("=" * 80 + "\n")
    
    # Step 1: Setup database
    setup_database()
    
    # Step 2: Create sample task
    task_name = create_sample_task()
    
    # Step 3: Run complete workflow (search + process)
    run_complete_workflow(task_name)
    
    # Step 4: Show statistics
    show_statistics()
    
    print("=" * 80)
    print("Demo completed!")
    print("=" * 80)

if __name__ == "__main__":
    main()
