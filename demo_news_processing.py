"""
Demo: Fetch news from NewsNow API and process with AI
"""

import requests
import os
import sys
from datetime import datetime

# Add ai_processing to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_processing.models.article import RawArticle
from ai_processing.processor import ArticleProcessor
from ai_processing.config import AIConfig

def fetch_news_from_api():
    """Fetch one news item from EIA source"""
    print("Fetching news from NewsNow API (EIA source)...")
    
    response = requests.get(
        "https://eternalgy-newsnow-production.up.railway.app/api/s?id=eia",
        timeout=10
    )
    
    if response.status_code != 200:
        raise Exception(f"API returned status {response.status_code}")
    
    data = response.json()
    
    if not data.get('items') or len(data['items']) == 0:
        raise Exception("No news items available")
    
    # Get the first news item
    news_item = data['items'][0]
    
    print(f"✓ Fetched news from {data['id']}")
    print(f"  Title: {news_item['title']}")
    print(f"  URL: {news_item['url']}")
    print()
    
    return news_item, data['id']

def create_raw_article(news_item, platform):
    """Convert API response to RawArticle"""
    return RawArticle(
        id=str(news_item.get('id', news_item['url'])),
        title=news_item['title'],
        platform=platform,
        rank=1,
        url=news_item['url'],
        timestamp=datetime.fromtimestamp(news_item['pubDate'] / 1000) if news_item.get('pubDate') else datetime.now(),
        metadata={
            'pubDate': news_item.get('pubDate'),
            'extra': news_item.get('extra', {})
        }
    )

def main():
    print("=" * 80)
    print("NewsNow API + AI Processing Demo")
    print("=" * 80)
    print()
    
    # Step 1: Fetch news from API
    try:
        news_item, platform = fetch_news_from_api()
    except Exception as e:
        print(f"✗ Failed to fetch news: {e}")
        return
    
    # Step 2: Convert to RawArticle
    raw_article = create_raw_article(news_item, platform)
    
    # Step 3: Initialize AI Processor
    print("Initializing AI Processor...")
    
    # Check for API key
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        print("⚠ Warning: AI_API_KEY not set in environment")
        print("  Set it with: set AI_API_KEY=your_key_here")
        print()
        print("Using default configuration (may fail without valid API key)")
        print()
    
    config = AIConfig(
        api_url=os.getenv("AI_API_URL", "https://api.bltcy.ai/v1/"),
        api_key=api_key or "",
        model=os.getenv("AI_MODEL", "gpt-5-nano-2025-08-07"),
        enable_cleaning=True,
        enable_translation=True
    )
    
    processor = ArticleProcessor(config=config)
    print("✓ AI Processor initialized")
    print()
    
    # Step 4: Process the article
    print("-" * 80)
    print("Processing article through AI pipeline...")
    print("-" * 80)
    print()
    
    try:
        processed = processor.process_single(raw_article)
        
        # Step 5: Display results
        print("=" * 80)
        print("RESULTS")
        print("=" * 80)
        print()
        
        print("📰 ORIGINAL NEWS")
        print("-" * 80)
        print(f"Platform: {processed.platform}")
        print(f"URL: {processed.url}")
        print(f"Published: {processed.collected_at}")
        print()
        print(f"Original Title:")
        print(f"  {processed.title_original}")
        print()
        
        print("🧹 CLEANED TITLE")
        print("-" * 80)
        print(f"  {processed.title_cleaned}")
        print()
        
        print("🌍 TRANSLATIONS (3 Languages)")
        print("-" * 80)
        print(f"Detected Language: {processed.detected_language.upper()}")
        print()
        
        print("🇬🇧 English:")
        print(f"  {processed.title_en}")
        print()
        
        print("🇨🇳 Chinese (Simplified):")
        print(f"  {processed.title_zh}")
        print()
        
        print("🇲🇾 Malay:")
        print(f"  {processed.title_ms}")
        print()
        
        print("=" * 80)
        print("✓ Processing completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"✗ Processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
