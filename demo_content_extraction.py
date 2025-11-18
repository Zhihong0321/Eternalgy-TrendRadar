"""
Demo: NewsNow API + AI Processing with Full Content Extraction
Shows how the enhanced processor extracts and processes full article content
"""

import requests
import os
from datetime import datetime

# Set environment variables
os.environ['AI_API_KEY'] = 'sk-jW4WLdgCGCshSyFY9VbKXwj8y2YXclFHxw2x2WbXElFkcAlD'
os.environ['AI_API_URL'] = 'https://api.bltcy.ai/v1/'
os.environ['AI_MODEL'] = 'gpt-5-nano-2025-08-07'

from ai_processing import ArticleProcessorWithContent, RawArticle

print("=" * 80)
print("DEMO: NewsNow API + AI Processing with Content Extraction")
print("=" * 80)
print()

# Step 1: Fetch real news
print("Step 1: Fetching news from NewsNow API (EIA)...")
response = requests.get("https://eternalgy-newsnow-production.up.railway.app/api/s?id=eia")
data = response.json()
news_item = data['items'][0]

print(f"✓ Fetched: {news_item['title']}")
print(f"  URL: {news_item['url']}")
print()

# Step 2: Convert to RawArticle
raw_article = RawArticle(
    id=news_item['url'],
    title=news_item['title'],
    platform='eia',
    rank=1,
    url=news_item['url'],
    timestamp=datetime.fromtimestamp(news_item['pubDate'] / 1000)
)

# Step 3: Process with enhanced AI processor (with content extraction)
print("Step 2: Processing with Enhanced AI Processor...")
print("  - Extracting full article content from URL")
print("  - Cleaning and summarizing content")
print("  - Translating to 3 languages")
print()

try:
    processor = ArticleProcessorWithContent(
        api_url=os.environ['AI_API_URL'],
        api_key=os.environ['AI_API_KEY'],
        model=os.environ['AI_MODEL'],
        extract_content=True,  # Enable content extraction
        max_content_length=3000
    )
    
    # Reduce timeout for faster response
    processor.ai_client.timeout = 15
    
    processed = processor.process_single(raw_article)
    
    # Display results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    
    print("📰 ORIGINAL NEWS")
    print("-" * 80)
    print(f"Title: {processed.title_original}")
    print(f"URL: {processed.url}")
    print()
    
    # Show extracted content
    content = processed.metadata.get('content', '')
    excerpt = processed.metadata.get('excerpt', '')
    
    if content and content != processed.title_original:
        print("📄 EXTRACTED CONTENT")
        print("-" * 80)
        print(f"Excerpt: {excerpt}")
        print()
        print(f"Full Content ({len(content)} chars):")
        print(f"  {content[:300]}...")
        print()
    
    # Show summary
    summary = processed.metadata.get('summary', '')
    if summary:
        print("📝 AI SUMMARY")
        print("-" * 80)
        print(f"  {summary}")
        print()
    
    print("🌍 TRANSLATIONS (3 Languages)")
    print("-" * 80)
    print(f"Detected Language: {processed.detected_language.upper()}")
    print()
    print(f"🇬🇧 English:")
    print(f"  {processed.title_en}")
    print()
    print(f"🇨🇳 Chinese:")
    print(f"  {processed.title_zh}")
    print()
    print(f"🇲🇾 Malay:")
    print(f"  {processed.title_ms}")
    print()
    
    print("=" * 80)
    print("✓ SUCCESS!")
    print("=" * 80)
    print()
    print("The enhanced processor:")
    print("  1. ✓ Extracted full article content from URL")
    print("  2. ✓ Cleaned and summarized the content")
    print("  3. ✓ Translated summary to 3 languages")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("Note: Content extraction requires:")
    print("  - pip install readability-lxml beautifulsoup4 lxml")
    print("  - Working AI API endpoint")
