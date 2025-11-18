"""Test with real AI processor integration"""
import sys
sys.path.insert(0, '.')

from news_search import NewsSearchModule, ProcessorWorker, Database
from ai_processing.processor_with_content import ArticleProcessorWithContent
from ai_processing.models.article import RawArticle
from datetime import datetime


class AIProcessorAdapter:
    """Adapter to integrate your existing AI processor"""
    
    def __init__(self):
        # Initialize your existing processor
        self.processor = ArticleProcessorWithContent(
            extract_content=True,
            max_content_length=3000
        )
    
    def process(self, url: str) -> dict:
        """
        Process a URL using your existing AI processor
        
        Returns:
            Dictionary with success, title, content, translated_content, metadata
        """
        try:
            print(f"  🔄 Scraping, cleaning, and translating...")
            
            # Create a RawArticle object
            raw_article = RawArticle(
                id=f"news_{datetime.now().timestamp()}",
                title="",  # Will be extracted from URL
                platform="web",
                rank=1,
                url=url,
                timestamp=datetime.now()
            )
            
            # Process with your existing pipeline
            processed = self.processor.process_single(raw_article)
            
            if processed:
                print(f"  ✓ Title: {processed.title_cleaned[:60]}...")
                print(f"  ✓ Language: {processed.detected_language}")
                print(f"  ✓ Translations: EN, ZH, MS")
                
                # Extract content from metadata
                content = processed.metadata.get('content', '')
                summary = processed.metadata.get('summary', '')
                tags = processed.metadata.get('tags', [])
                country = processed.metadata.get('country', 'XX')
                news_date = processed.metadata.get('news_date', None)
                
                # Format translated content as text
                translated_text = f"EN: {processed.title_en}\n\nZH: {processed.title_zh}\n\nMS: {processed.title_ms}"
                
                print(f"  ✓ Tags: {', '.join(tags) if tags else 'None'}")
                print(f"  ✓ Country: {country}")
                print(f"  ✓ News Date: {news_date or 'Not detected'}")
                
                return {
                    'success': True,
                    'title': processed.title_cleaned,
                    'content': content or summary,
                    'translated_content': translated_text,
                    'tags': tags,
                    'country': country,
                    'news_date': news_date,
                    'metadata': {
                        'original_title': processed.title_original,
                        'detected_language': processed.detected_language,
                        'summary': summary,
                        'excerpt': processed.metadata.get('excerpt', ''),
                        'word_count': len(content.split()) if content else 0,
                        'tags': tags,
                        'country': country,
                        'news_date': news_date,
                        'translations': {
                            'en': processed.title_en,
                            'zh': processed.title_zh,
                            'ms': processed.title_ms
                        }
                    }
                }
            else:
                print(f"  ✗ Processing returned no result")
                return {
                    'success': False,
                    'error': 'Processing returned no result'
                }
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }


def check_current_data():
    """Check what's currently in the database"""
    print("\n" + "=" * 80)
    print("CURRENT DATABASE STATUS")
    print("=" * 80)
    
    db = Database()
    
    # Check links
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM news_links")
        link_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM processed_content")
        content_count = cursor.fetchone()[0]
        
        print(f"\n📊 Database Status:")
        print(f"  news_links: {link_count} records")
        print(f"  processed_content: {content_count} records")
        
        if content_count == 0:
            print(f"\n⚠️  No processed content found!")
            print(f"  The previous test ran in MOCK mode.")
            print(f"  URLs were saved but not actually scraped/translated.")
        
        cursor.close()


def test_real_processing():
    """Test with real AI processor on a few URLs"""
    print("\n" + "=" * 80)
    print("TEST: Real AI Processing")
    print("=" * 80)
    
    db = Database()
    
    # Get a few pending or completed links to reprocess
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, url FROM news_links 
            WHERE id IN (1, 2, 3)
            LIMIT 3
        """)
        links = cursor.fetchall()
        cursor.close()
    
    if not links:
        print("No links found to process")
        return
    
    print(f"\nProcessing {len(links)} URLs with real AI processor...\n")
    
    # Create AI processor adapter
    ai_processor = AIProcessorAdapter()
    
    # Process each link
    for link_id, url in links:
        print(f"\n[{link_id}] {url}")
        
        # Reset status to pending
        db.update_link_status(link_id, 'pending')
        
        # Process
        result = ai_processor.process(url)
        
        if result['success']:
            # Save to database
            db.save_processed_content(
                link_id=link_id,
                title=result.get('title'),
                content=result.get('content'),
                translated_content=result.get('translated_content'),
                tags=result.get('tags', []),
                country=result.get('country', 'XX'),
                news_date=result.get('news_date', None),
                metadata=result.get('metadata')
            )
            db.update_link_status(link_id, 'completed')
            print(f"  ✓ Saved to database")
        else:
            db.update_link_status(link_id, 'failed', result.get('error'))
            print(f"  ✗ Failed: {result.get('error')}")


def show_processed_content():
    """Show processed content from database"""
    print("\n" + "=" * 80)
    print("PROCESSED CONTENT SAMPLE")
    print("=" * 80)
    
    db = Database()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                pc.link_id,
                nl.url,
                pc.title,
                pc.tags,
                pc.country,
                pc.news_date,
                LEFT(pc.content, 300) as content_preview,
                LEFT(pc.translated_content, 200) as translated_preview
            FROM processed_content pc
            JOIN news_links nl ON pc.link_id = nl.id
            LIMIT 3
        """)
        
        results = cursor.fetchall()
        cursor.close()
        
        if not results:
            print("\nNo processed content found yet.")
            return
        
        for link_id, url, title, tags, country, news_date, content, translated in results:
            print(f"\n[{link_id}] {title or 'No title'}")
            print(f"URL: {url}")
            print(f"Tags: {', '.join(tags) if tags else 'None'}")
            print(f"Country: {country}")
            print(f"News Date: {news_date or 'Not detected'}")
            print(f"Content:\n{content}...")
            print(f"Translated: {translated}...")


def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("REAL AI PROCESSOR TEST")
    print("=" * 80)
    
    # Step 1: Check current status
    check_current_data()
    
    # Step 2: Test real processing
    test_real_processing()
    
    # Step 3: Show results
    show_processed_content()
    
    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
