"""Example: Integrate with your existing AI processor"""
import sys
sys.path.insert(0, '.')

from news_search import NewsSearchModule, ProcessorWorker
from ai_processing.processor_with_content import NewsProcessor


class AIProcessorAdapter:
    """Adapter to integrate your existing AI processor"""
    
    def __init__(self):
        # Initialize your existing AI processor
        self.news_processor = NewsProcessor()
    
    def process(self, url: str) -> dict:
        """
        Process a URL using your existing AI processor
        
        Args:
            url: URL to process
        
        Returns:
            Dictionary with success, title, content, translated_content, metadata
        """
        try:
            print(f"  Processing with AI: {url}")
            
            # Use your existing processor
            result = self.news_processor.process_url(url)
            
            if result and result.get('success'):
                return {
                    'success': True,
                    'title': result.get('title'),
                    'content': result.get('content'),
                    'translated_content': result.get('translated_content'),
                    'metadata': {
                        'source': result.get('source'),
                        'published_date': result.get('published_date'),
                        'author': result.get('author'),
                        'language': result.get('language'),
                        'word_count': result.get('word_count')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Processing failed')
                }
                
        except Exception as e:
            print(f"  Error in AI processing: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def run_with_ai_processor():
    """Run search and processing with your AI processor"""
    
    # Create AI processor adapter
    ai_processor = AIProcessorAdapter()
    
    # Create processor worker with your AI processor
    processor = ProcessorWorker(ai_processor=ai_processor)
    
    # Create search module with processor
    search_module = NewsSearchModule(processor_worker=processor)
    
    # Run task
    task_name = "malaysia_solar_pv_daily"
    result = search_module.run_task(task_name)
    
    print("\n" + "=" * 80)
    print("RESULTS WITH AI PROCESSING:")
    print("=" * 80)
    print(f"Search: {result['new_links']} new links")
    
    if result.get('processing'):
        proc = result['processing']
        print(f"Processing: {proc['success']}/{proc['total']} successful")
    
    return result


if __name__ == "__main__":
    run_with_ai_processor()
