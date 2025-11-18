# 🚀 Quick Reference - AI Processing Module

## Installation

```bash
# No installation needed - module is ready to use
# Only dependency: requests (already in TrendRadar)
```

## Basic Usage

```python
from ai_processing import ArticleProcessor, RawArticle

# Initialize
processor = ArticleProcessor(
    api_url="https://api.bltcy.ai/v1/",
    api_key="sk-jW4WLdgCGCshSyFY9VbKXwj8y2YXclFHxw2x2WbXElFkcAlD",
    model="gpt-5-nano-2025-08-07"
)

# Process
article = RawArticle(id="1", title="华为新手机", platform="zhihu", rank=1)
result = processor.process_single(article)

# Access
print(result.title_en)  # English
print(result.title_zh)  # Chinese
print(result.title_ms)  # Malay
```

## Environment Variables

```bash
AI_API_URL=https://api.bltcy.ai/v1/
AI_API_KEY=your-key
AI_MODEL=gpt-5-nano-2025-08-07
```

## Test

```bash
python -m ai_processing.test_module
```

## Cost

~$0.72/month for 50 articles/hour

## Documentation

- `ai_processing/README.md` - Full docs
- `ai_processing/INTEGRATION_GUIDE.md` - Integration steps
- `AI_PROCESSING_SUMMARY.md` - Complete summary

## Support

All tests passed ✅  
Module is production-ready 🚀
