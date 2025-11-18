"""
Quick demo: Fetch real news and process with AI
"""

import requests
import os
from datetime import datetime

# Set environment variables
os.environ['AI_API_KEY'] = 'sk-jW4WLdgCGCshSyFY9VbKXwj8y2YXclFHxw2x2WbXElFkcAlD'
os.environ['AI_API_URL'] = 'https://api.bltcy.ai/v1/'
os.environ['AI_MODEL'] = 'gpt-5-nano-2025-08-07'

from ai_processing import ArticleProcessor, RawArticle

print("=" * 80)
print("DEMO: NewsNow API + AI Processing")
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

# Step 3: Process with AI (with shorter timeout)
print("Step 2: Processing with AI (cleaning + translating)...")
print()

try:
    processor = ArticleProcessor(
        api_url=os.environ['AI_API_URL'],
        api_key=os.environ['AI_API_KEY'],
        model=os.environ['AI_MODEL']
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
    
    print("🧹 CLEANED TITLE")
    print("-" * 80)
    print(f"{processed.title_cleaned}")
    print()
    
    print("🌍 TRANSLATIONS")
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
    
except Exception as e:
    print(f"✗ Error: {e}")
    print()
    print("Note: The AI API might be slow or unavailable.")
    print("Showing original news only:")
    print()
    print(f"Title: {news_item['title']}")
    print(f"URL: {news_item['url']}")
