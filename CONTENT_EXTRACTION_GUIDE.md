# Content Extraction Feature Guide

**Version**: 1.1.0  
**Date**: November 18, 2025

---

## Overview

The AI Processing module now includes **full article content extraction** using Mozilla's Readability algorithm. Instead of processing only titles, it can now:

1. **Extract full article content** from URLs
2. **Clean and summarize** the content with AI
3. **Translate summaries** to 3 languages (EN, ZH, MS)

---

## What's New

### Before (v1.0.0)
- ❌ Only processed article titles
- ❌ No content extraction
- ✅ Title cleaning and translation

### After (v1.1.0)
- ✅ **Full article content extraction** from URLs
- ✅ **AI-powered summarization** of content
- ✅ **Content cleaning** (removes ads, formatting)
- ✅ **Multi-language translation** of summaries
- ✅ Backward compatible with title-only processing

---

## Architecture

```
NewsNow API → Content Extractor → AI Cleaner → Translator → 3 Languages
     ↓              ↓                  ↓            ↓
   Title         Full Text         Summary      EN/ZH/MS
```

### New Components

1. **ContentExtractor** (`services/content_extractor.py`)
   - Uses `readability-lxml` (Python port of Mozilla Readability)
   - Extracts clean article text from HTML
   - Removes ads, navigation, footers
   - Returns title, content, excerpt

2. **ContentCleaner** (`services/content_cleaner.py`)
   - AI-powered content summarization
   - Removes promotional content
   - Creates 2-3 sentence summaries
   - Batch processing support

3. **ArticleProcessorWithContent** (`processor_with_content.py`)
   - Enhanced processor with content extraction
   - Orchestrates full pipeline
   - Backward compatible

---

## Installation

### Required Dependencies

```bash
pip install readability-lxml beautifulsoup4 lxml
```

Or update from `requirements.txt`:

```txt
readability-lxml>=0.8.1,<1.0.0
beautifulsoup4>=4.12.0,<5.0.0
lxml>=5.0.0,<6.0.0
```

---

## Usage

### Basic Usage (Title Only - Backward Compatible)

```python
from ai_processing import ArticleProcessor, RawArticle

# Original processor still works
processor = ArticleProcessor(
    api_url="https://api.bltcy.ai/v1/",
    api_key="your-key",
    model="gpt-5-nano-2025-08-07"
)

raw_article = RawArticle(
    id="news_001",
    title="Breaking News Title",
    platform="eia",
    rank=1,
    url="https://example.com/article"
)

processed = processor.process_single(raw_article)
```

### Enhanced Usage (With Content Extraction)

```python
from ai_processing import ArticleProcessorWithContent, RawArticle

# New enhanced processor
processor = ArticleProcessorWithContent(
    api_url="https://api.bltcy.ai/v1/",
    api_key="your-key",
    model="gpt-5-nano-2025-08-07",
    extract_content=True,  # Enable content extraction
    max_content_length=3000  # Max chars to extract
)

raw_article = RawArticle(
    id="news_001",
    title="Breaking News Title",
    platform="eia",
    rank=1,
    url="https://example.com/article"  # URL is required
)

processed = processor.process_single(raw_article)

# Access extracted content
print(f"Original Title: {processed.title_original}")
print(f"Summary: {processed.metadata['summary']}")
print(f"Full Content: {processed.metadata['content']}")
print(f"Excerpt: {processed.metadata['excerpt']}")

# Access translations
print(f"English: {processed.title_en}")
print(f"Chinese: {processed.title_zh}")
print(f"Malay: {processed.title_ms}")
```

---

## Real Example

### Input (from NewsNow API)

```json
{
  "id": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
  "title": "U.S. rig counts remain low as production efficiencies improve",
  "url": "https://www.eia.gov/todayinenergy/detail.php?id=66645",
  "pubDate": 1763388000000
}
```

### Processing Pipeline

```
1. Fetch URL → Extract Content (2778 chars)
2. AI Summarization → Clean Summary (3 sentences)
3. Translation → EN/ZH/MS versions
```

### Output

**Extracted Content** (2778 characters):
```
In-brief analysis November 17, 2025... The average number of active rigs 
per month that are drilling for oil and natural gas in the U.S. Lower 48 
states has declined steadily over the past few years from a recent peak 
of 750 rigs in December 2022 to 517 rigs in October 2025...
```

**AI Summary** (3 sentences):
```
U.S. Lower 48 active rigs remained at low levels in October 2025, with 
517 rigs drilling, down from 750 in December 2022, as operators pursue 
efficiency gains. Oil-directed rigs fell 33% to 397 and natural 
gas-directed rigs declined 23% to 120 since 2022, yet crude and natural 
gas production reached record highs in mid-2025 due to longer laterals 
and more efficient completions. The Permian remains the largest 
crude-producing region...
```

**Translations**:
- 🇬🇧 EN: U.S. rig counts remain low as production efficiencies improve
- 🇨🇳 ZH: 美国钻井数量保持低位，生产效率提高
- 🇲🇾 MS: Kiraan pelantar AS kekal rendah ketika kecekapan pengeluaran bertambah baik

---

## Configuration

### Environment Variables

```bash
# AI API Configuration
AI_API_URL=https://api.bltcy.ai/v1/
AI_API_KEY=your-api-key
AI_MODEL=gpt-5-nano-2025-08-07

# Content Extraction Settings
AI_EXTRACT_CONTENT=true
AI_MAX_CONTENT_LENGTH=3000
AI_CONTENT_TIMEOUT=10
```

### Python Configuration

```python
from ai_processing import ArticleProcessorWithContent
from ai_processing.config import AIConfig

config = AIConfig(
    api_url="https://api.bltcy.ai/v1/",
    api_key="your-key",
    model="gpt-5-nano-2025-08-07",
    enable_cleaning=True,
    enable_translation=True,
    batch_size=5,
    timeout=15
)

processor = ArticleProcessorWithContent(
    config=config,
    extract_content=True,
    max_content_length=3000
)
```

---

## API Reference

### ContentExtractor

```python
from ai_processing.services.content_extractor import ContentExtractor

extractor = ContentExtractor(
    timeout=10,
    max_content_length=5000,
    user_agent="Custom User Agent"
)

# Extract single URL
result = extractor.extract_content("https://example.com/article")
# Returns: {'title': '...', 'content': '...', 'excerpt': '...', 'url': '...'}

# Extract multiple URLs
results = extractor.extract_batch([url1, url2, url3])
# Returns: {url: result_dict}

# Extract with fallback
result = extractor.extract_with_fallback(url, fallback_title="Title")
```

### ContentCleaner

```python
from ai_processing.services.content_cleaner import ContentCleaner

cleaner = ContentCleaner(
    ai_client=ai_client,
    batch_size=5,
    max_content_length=3000
)

# Clean single article
result = cleaner.clean_single(
    title="Article Title",
    content="Full article content...",
    url="https://example.com"
)
# Returns: {'title': '...', 'summary': '...', 'original_content': '...'}

# Clean batch
articles = [
    {'title': 'Title 1', 'content': 'Content 1'},
    {'title': 'Title 2', 'content': 'Content 2'}
]
cleaned = cleaner.clean_batch(articles)
```

### ArticleProcessorWithContent

```python
from ai_processing import ArticleProcessorWithContent

processor = ArticleProcessorWithContent(
    api_url="https://api.bltcy.ai/v1/",
    api_key="your-key",
    model="gpt-5-nano-2025-08-07",
    extract_content=True,
    max_content_length=3000
)

# Process single article
processed = processor.process_single(raw_article)

# Process batch
processed_list = processor.process_articles(raw_articles)

# Create from environment
processor = ArticleProcessorWithContent.from_env()
```

---

## Performance

### Processing Time

| Operation | Time | Notes |
|-----------|------|-------|
| Content Extraction | 1-3s | Per URL |
| AI Summarization | 2-5s | Per article |
| Translation | 2-5s | Per article |
| **Total** | **5-13s** | Per article |

### Batch Processing

- Batch size: 5 articles (configurable)
- Parallel extraction: No (sequential)
- AI batch calls: Yes (reduces API calls)

### Optimization Tips

1. **Adjust batch size** based on API limits
2. **Cache extracted content** to avoid re-fetching
3. **Use shorter max_content_length** for faster processing
4. **Implement async extraction** for better performance

---

## Error Handling

### Graceful Fallbacks

1. **Content Extraction Fails**
   - Falls back to title only
   - Continues processing

2. **AI Summarization Fails**
   - Returns original title
   - Logs error

3. **Translation Fails**
   - Returns summary in all languages
   - Continues processing

### Example

```python
try:
    processed = processor.process_single(raw_article)
except Exception as e:
    print(f"Processing failed: {e}")
    # Processor has built-in fallbacks
    # Will return partial results
```

---

## Testing

### Run Demo

```bash
python demo_content_extraction.py
```

### Expected Output

```
✓ Fetched news from NewsNow API
✓ Extracted full article content (2778 chars)
✓ AI summary generated (3 sentences)
✓ Translated to 3 languages
```

### Unit Tests

```bash
python -m pytest ai_processing/tests/
```

---

## Migration Guide

### From v1.0.0 to v1.1.0

**No breaking changes!** Your existing code continues to work.

#### Option 1: Keep Using Title-Only Processing

```python
# No changes needed
from ai_processing import ArticleProcessor
processor = ArticleProcessor(...)
```

#### Option 2: Upgrade to Content Extraction

```python
# Change import
from ai_processing import ArticleProcessorWithContent

# Change class name
processor = ArticleProcessorWithContent(
    ...,
    extract_content=True  # Add this
)
```

---

## Troubleshooting

### Issue: "Module 'readability' not found"

**Solution**:
```bash
pip install readability-lxml beautifulsoup4 lxml
```

### Issue: "Content extraction failed"

**Possible causes**:
1. URL is not accessible
2. Website blocks scrapers
3. Content is behind paywall

**Solution**: Processor falls back to title automatically

### Issue: "AI API timeout"

**Solution**:
```python
processor.ai_client.timeout = 30  # Increase timeout
```

---

## Roadmap

### v1.2.0 (Planned)
- [ ] Async content extraction
- [ ] Content caching
- [ ] Image extraction
- [ ] PDF support

### v1.3.0 (Planned)
- [ ] Multi-source aggregation
- [ ] Duplicate detection
- [ ] Sentiment analysis

---

## Summary

✅ **Content extraction** using Mozilla Readability  
✅ **AI summarization** of full articles  
✅ **Multi-language translation** of summaries  
✅ **Backward compatible** with v1.0.0  
✅ **Production ready** with error handling  

The enhanced processor transforms your news pipeline from title-only to full-content processing with AI-powered summarization and translation!

---

## Demo Files

- `demo_content_extraction.py` - Full demo with real news
- `ai_processing/services/content_extractor.py` - Content extraction service
- `ai_processing/services/content_cleaner.py` - Content cleaning service
- `ai_processing/processor_with_content.py` - Enhanced processor

Run `python demo_content_extraction.py` to see it in action!
