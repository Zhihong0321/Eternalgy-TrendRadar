# Enhanced News Cleaning System

## ✅ Implemented Features

### 1. **Function Calling with Strict JSON Output**
- Uses OpenAI function calling API for structured output
- Guarantees consistent JSON format
- Schema-validated responses

### 2. **Tags System**
- AI selects up to 3 most relevant tags from predefined list:
  - Solar
  - Wind
  - EV
  - Big Project
  - Tech
  - Policy
  - Finance
  - Storage
- Stored as PostgreSQL array for efficient querying

### 3. **Country Detection**
- AI identifies news origin country
- Uses standard 2-letter ISO codes (MY, SG, CN, US, TH, ID, PH, etc.)
- Indexed for fast filtering

### 4. **News Date Extraction**
- AI extracts publication date from article content
- Format: YYYY-MM-DD
- Stored as PostgreSQL DATE type
- Indexed for chronological queries

### 5. **Bullet-Point Formatting**
- Content restructured into 3-5 clean bullet points
- Each bullet = ONE clear factual statement
- No ads, filler, clickbait, or promotional content
- Maintains original language

## 📊 Database Schema

```sql
CREATE TABLE processed_content (
    id SERIAL PRIMARY KEY,
    link_id INTEGER UNIQUE REFERENCES news_links(id),
    title TEXT,
    content TEXT,
    translated_content TEXT,
    tags TEXT[],                    -- Array of tags
    country VARCHAR(2),             -- 2-letter country code
    news_date DATE,                 -- Publication date
    metadata JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX idx_processed_content_tags ON processed_content USING GIN(tags);
CREATE INDEX idx_processed_content_country ON processed_content(country);
CREATE INDEX idx_processed_content_news_date ON processed_content(news_date);
```

## 🔧 Function Calling Schema

```json
{
  "name": "clean_news_article",
  "parameters": {
    "type": "object",
    "properties": {
      "tags": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["Solar", "Wind", "EV", "Big Project", "Tech", "Policy", "Finance", "Storage"]
        },
        "maxItems": 3
      },
      "country": {
        "type": "string",
        "pattern": "^[A-Z]{2}$"
      },
      "news_date": {
        "type": "string",
        "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
      },
      "bullets": {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 3,
        "maxItems": 5
      }
    },
    "required": ["tags", "country", "news_date", "bullets"]
  }
}
```

## 📝 Example Output

### Input Article:
```
Title: Samaiden secures 99.99 MW LSS PV plant project in Kelantan
Content: Samaiden Group Berhad announce that its wholly-owned subsidiary 
has been shortlisted by the Energy Commission for the development of a 
99.99 Megawatts Large Scale Solar Photovoltaic Plant in Pasir Mas, Kelantan...
[Full article with ads, filler, promotional content]
```

### AI-Processed Output:
```json
{
  "tags": ["Solar", "Big Project", "Finance"],
  "country": "MY",
  "news_date": "2024-12-23",
  "bullets": [
    "Samaiden Group Berhad's wholly-owned subsidiary has been shortlisted by Malaysia's Energy Commission for the development of a 99.99 MW Large Scale Solar PV plant in Pasir Mas, Kelantan.",
    "A notification letter was issued on 23 December 2024, formally acknowledging the selection.",
    "The project represents a significant investment in Malaysia's renewable energy infrastructure."
  ]
}
```

## 🎯 Benefits

### For Readers:
- **Fast Reading**: Bullet points instead of long paragraphs
- **Ad-Free**: No promotional content or filler
- **Clear Facts**: Each bullet = one clear statement
- **No Clickbait**: Straight to the facts

### For Platform:
- **Searchable**: Query by tags, country, date
- **Structured**: Consistent JSON format
- **Multilingual**: Translated to EN, ZH, MS
- **Indexed**: Fast database queries

## 🔍 Query Examples

### Find all Solar news from Malaysia:
```sql
SELECT * FROM processed_content 
WHERE 'Solar' = ANY(tags) 
AND country = 'MY'
ORDER BY news_date DESC;
```

### Find Big Projects in last 30 days:
```sql
SELECT * FROM processed_content 
WHERE 'Big Project' = ANY(tags)
AND news_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY news_date DESC;
```

### Find all EV + Policy news:
```sql
SELECT * FROM processed_content 
WHERE tags @> ARRAY['EV', 'Policy']
ORDER BY news_date DESC;
```

### Get news by country and tag:
```sql
SELECT country, COUNT(*) as count
FROM processed_content
WHERE 'Solar' = ANY(tags)
GROUP BY country
ORDER BY count DESC;
```

## 🚀 API Integration

The system automatically:
1. Searches for news URLs (GPT-4o-mini-search-preview)
2. Scrapes HTML content
3. Cleans with AI (function calling)
4. Extracts tags, country, date
5. Formats as bullet points
6. Translates to 3 languages
7. Stores in PostgreSQL

All in one automated workflow!

## 📈 Performance

- **Search**: ~$0.00016 per query (376 tokens)
- **Processing**: ~$0.0001 per article (depends on length)
- **Speed**: ~2-3 seconds per article
- **Rate Limiting**: 3s delay between same-domain requests
- **Concurrent**: 3 domains processed simultaneously

## 🎨 Content Quality

**Before (typical news site):**
```
Samaiden Group Berhad (Samaiden), a leading renewable energy solutions 
provider in Malaysia, is pleased to announce that its wholly-owned 
subsidiary, Samaiden Engineering Sdn Bhd, has been shortlisted by the 
Energy Commission of Malaysia for the development of a 99.99 Megawatts 
(MW) Large Scale Solar Photovoltaic (LSS PV) Plant in Pasir Mas, Kelantan.

This exciting development marks another significant milestone for Samaiden 
as it continues to expand its footprint in Malaysia's renewable energy 
sector. The company has been at the forefront of solar energy solutions...
[continues with promotional content, company history, etc.]
```

**After (your portal):**
```
• Samaiden Group Berhad's subsidiary shortlisted for 99.99 MW solar plant 
  in Pasir Mas, Kelantan
• Energy Commission issued notification on 23 December 2024
• Project represents major investment in Malaysia's renewable infrastructure

Tags: Solar, Big Project, Finance
Country: MY
Date: 2024-12-23
```

**Result**: 90% shorter, 100% clearer, 0% fluff! 🎯
