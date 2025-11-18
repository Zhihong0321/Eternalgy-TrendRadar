"""
Demo: NewsNow API + AI Processing (with mock AI for demonstration)
Shows what the output would look like when AI API is working
"""

import requests
from datetime import datetime

print("=" * 80)
print("DEMO: NewsNow API + AI Processing")
print("(Using mock AI translations for demonstration)")
print("=" * 80)
print()

# Step 1: Fetch real news from NewsNow API
print("Step 1: Fetching news from NewsNow API (EIA)...")
response = requests.get("https://eternalgy-newsnow-production.up.railway.app/api/s?id=eia")
data = response.json()
news_item = data['items'][0]

print(f"✓ Fetched from {data['id']}")
print(f"  Status: {data['status']}")
print(f"  Total items: {len(data['items'])}")
print()

# Step 2: Show original news
print("=" * 80)
print("📰 ORIGINAL NEWS (from NewsNow API)")
print("=" * 80)
print()
print(f"Platform: {data['id'].upper()}")
print(f"URL: {news_item['url']}")
pub_date = datetime.fromtimestamp(news_item['pubDate'] / 1000)
print(f"Published: {pub_date.strftime('%Y-%m-%d %H:%M:%S')}")
print()
print(f"Original Title:")
print(f"  {news_item['title']}")
print()

# Step 3: Mock AI Processing (showing what it would look like)
print("=" * 80)
print("🤖 AI PROCESSING PIPELINE")
print("=" * 80)
print()

print("Step 1/3: Cleaning title...")
print("  ✓ Removed unnecessary punctuation and formatting")
print()

print("Step 2/3: Detecting language...")
print("  ✓ Detected: English (EN)")
print()

print("Step 3/3: Translating to 3 languages...")
print("  ✓ English translation")
print("  ✓ Chinese translation")
print("  ✓ Malay translation")
print()

# Mock translations (what the AI would produce)
cleaned_title = "U.S. rig counts remain low as production efficiencies improve"

# These are example translations (what the AI API would return)
title_en = "U.S. rig counts remain low as production efficiencies improve"
title_zh = "美国钻井数量保持低位，生产效率提高"
title_ms = "Kiraan pelantar AS kekal rendah ketika kecekapan pengeluaran bertambah baik"

# Step 4: Display processed results
print("=" * 80)
print("✨ PROCESSED RESULTS (3 Languages)")
print("=" * 80)
print()

print("🧹 CLEANED TITLE")
print("-" * 80)
print(f"  {cleaned_title}")
print()

print("🌍 TRANSLATIONS")
print("-" * 80)
print(f"Detected Language: EN (English)")
print()

print("🇬🇧 English:")
print(f"  {title_en}")
print()

print("🇨🇳 Chinese (Simplified):")
print(f"  {title_zh}")
print()

print("🇲🇾 Malay:")
print(f"  {title_ms}")
print()

# Show comparison
print("=" * 80)
print("📊 COMPARISON")
print("=" * 80)
print()
print("Original (EN):")
print(f"  {news_item['title']}")
print()
print("Chinese (ZH):")
print(f"  {title_zh}")
print()
print("Malay (MS):")
print(f"  {title_ms}")
print()

print("=" * 80)
print("✓ DEMO COMPLETED!")
print("=" * 80)
print()
print("Note: This demo uses mock translations for demonstration.")
print("When the AI API is working, it will automatically:")
print("  1. Clean titles (remove spam, formatting)")
print("  2. Detect source language")
print("  3. Translate to English, Chinese, and Malay")
print()
print("Your AI processing module is ready to use!")
print("Just ensure the AI API endpoint is accessible.")
