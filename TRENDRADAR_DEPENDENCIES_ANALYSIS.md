# TrendRadar Dependencies Analysis (UPDATED)

## Executive Summary

**IMPORTANT UPDATE**: You've confirmed that NewsNow API has been **completely abandoned**. All data now comes from GPT-4o-mini-web-search.

Based on code investigation, here's what you **still depend on** from the original TrendRadar repo:

---

## ✅ What You've Built (Fully Independent)

### 1. **GPT-4o-mini Web Search Module** (`news_search/`)
- **Purpose**: Grab news link URLs using AI search
- **API**: `https://api.bltcy.ai/v1/chat/completions`
- **Model**: `gpt-4o-mini-search-preview`
- **Status**: ✅ Fully independent, replaces NewsNow API

### 2. **AI Content Processor** (`ai_processing/`)
- **Purpose**: Web scrape content, clean, and translate news
- **API**: `https://api.bltcy.ai/v1/`
- **Model**: `gpt-5-nano-2025-08-07`
- **Features**:
  - Content extraction from URLs
  - Title cleaning
  - Translation to 3 languages (EN, ZH, MS)
  - Language detection
- **Status**: ✅ Fully independent

### 3. **PostgreSQL Database** (via Docker Compose)
- **Purpose**: Store news links and processed content
- **Tables**:
  - `news_links` - Discovered URLs with deduplication
  - `processed_content` - Cleaned and translated articles
  - `query_tasks` - Reusable search queries
- **Status**: ✅ Fully independent, self-hosted

---

## ⚠️ What You STILL Depend On (Original TrendRadar Code)

### 1. **main.py** - Core TrendRadar Application

**File**: `main.py` (4,557 lines)

**What it contains**:
- ❌ **NewsNow API integration** (lines 455, 161) - **NO LONGER USED** but code still exists
- ✅ **Configuration management** (`load_config()`)
- ✅ **Notification system** (Feishu, DingTalk, WeWork, Telegram, Email, ntfy)
- ✅ **Keyword filtering** (`frequency_words.txt` parsing)
- ✅ **Trending algorithm** (rank/frequency/hotness weights)
- ✅ **HTML report generation**
- ✅ **Push time window control**
- ✅ **Multi-platform notification batching**

**Classes/Functions you depend on**:
```python
# Configuration
load_config()
CONFIG = load_config()

# Data structures (even if not using NewsNow anymore)
class DataFetcher
class PushRecordManager

# Notification functions
send_to_feishu()
send_to_dingtalk()
send_to_wework()
send_to_telegram()
send_to_email()
send_to_ntfy()

# Report generation
generate_html_report()
save_titles_to_file()

# Keyword filtering
load_frequency_words()
parse_file_titles()

# Trending algorithm
calculate_weighted_score()
```

**Status**: ⚠️ **HEAVILY DEPENDENT** - This is the core TrendRadar codebase

---

### 2. **config/config.yaml** - Configuration File

**What it configures**:
- ✅ Crawler settings (request intervals, proxy)
- ✅ Report modes (daily/current/incremental)
- ✅ Notification settings (webhooks, batch sizes)
- ✅ Push time window control
- ✅ Trending algorithm weights
- ❌ **Platform list** (Zhihu, Weibo, etc.) - **NO LONGER RELEVANT** if not using NewsNow

**Status**: ⚠️ **PARTIALLY DEPENDENT** - Configuration structure from TrendRadar

---

### 3. **config/frequency_words.txt** - Keyword Filtering

**What it does**:
- Defines keywords to monitor (e.g., "AI", "比亚迪", "教育政策")
- Supports normal words, required words (+), filter words (!)
- Group-based management

**Status**: ⚠️ **DEPENDENT** - TrendRadar's keyword filtering system

---

### 4. **GitHub Actions Workflow** (`.github/workflows/crawler.yml`)

**What it does**:
- Scheduled execution (hourly via cron)
- Runs `python main.py`
- Commits and pushes output to GitHub Pages
- Manages environment variables for webhooks

**Status**: ⚠️ **DEPENDENT** - TrendRadar's deployment automation

---

### 5. **Notification System** (Multiple Platforms)

**Platforms supported** (all from TrendRadar):
- Feishu (飞书)
- DingTalk (钉钉)
- WeWork (企业微信)
- Telegram
- Email (with SMTP auto-detection)
- ntfy

**Features**:
- Message batching for size limits
- Markdown/HTML formatting
- Push time window control
- Multi-channel simultaneous push

**Status**: ⚠️ **FULLY DEPENDENT** - All notification code from TrendRadar

---

### 6. **HTML Report Generation**

**What it generates**:
- `output/index.html` - Web-based news report
- Mobile-responsive design
- GitHub Pages compatible
- Save-as-image functionality

**Status**: ⚠️ **DEPENDENT** - TrendRadar's reporting system

---

### 7. **Trending Algorithm**

**Algorithm components**:
```yaml
weight:
  rank_weight: 0.6      # Prioritize high-ranking news
  frequency_weight: 0.3  # Consider repeated appearances
  hotness_weight: 0.1    # Factor in ranking quality
```

**Status**: ⚠️ **DEPENDENT** - TrendRadar's custom trending algorithm

---

## 📊 Updated Dependency Breakdown

| Component | Source | Status | Notes |
|-----------|--------|--------|-------|
| **News Discovery** | ✅ Your GPT-4o-mini | Independent | Replaces NewsNow API |
| **Content Processing** | ✅ Your AI processor | Independent | Custom built |
| **Database** | ✅ Your PostgreSQL | Independent | Self-hosted |
| **Core Application** | ⚠️ TrendRadar `main.py` | **DEPENDENT** | 4,557 lines of code |
| **Configuration** | ⚠️ TrendRadar `config.yaml` | **DEPENDENT** | Config structure |
| **Keyword Filtering** | ⚠️ TrendRadar | **DEPENDENT** | `frequency_words.txt` |
| **Notifications** | ⚠️ TrendRadar | **DEPENDENT** | 6 platforms |
| **HTML Reports** | ⚠️ TrendRadar | **DEPENDENT** | Report generation |
| **Trending Algorithm** | ⚠️ TrendRadar | **DEPENDENT** | Weighted scoring |
| **GitHub Actions** | ⚠️ TrendRadar | **DEPENDENT** | Deployment workflow |

---

## 🔍 Critical Findings

### What You NO LONGER Depend On:
1. ✅ **NewsNow API** - Replaced with GPT-4o-mini-web-search
2. ✅ **External trending data** - Now self-sourced

### What You STILL Depend On:
1. ⚠️ **main.py** (4,557 lines) - Core application logic
2. ⚠️ **Notification system** - All 6 platform integrations
3. ⚠️ **Configuration management** - YAML parsing and structure
4. ⚠️ **Keyword filtering** - frequency_words.txt parsing
5. ⚠️ **HTML report generation** - Web output
6. ⚠️ **Trending algorithm** - Weighted scoring system
7. ⚠️ **GitHub Actions workflow** - Deployment automation
8. ⚠️ **Push time window control** - Notification scheduling

---

## 🎯 Current Architecture

```
GPT-4o-mini Web Search (api.bltcy.ai)
    ↓ [Discover news URLs]
Your PostgreSQL Database
    ↓ [Store links]
Your AI Processor (api.bltcy.ai)
    ↓ [Extract & translate content]
PostgreSQL (processed_content)
    ↓
┌─────────────────────────────────────┐
│  TrendRadar main.py (STILL USED)    │
│  ├─ Load config.yaml                │
│  ├─ Parse frequency_words.txt       │
│  ├─ Apply trending algorithm        │
│  ├─ Generate HTML reports           │
│  ├─ Send notifications (6 platforms)│
│  └─ Push time window control        │
└─────────────────────────────────────┘
    ↓
Output: HTML + Notifications
```

---

## 💡 To Become FULLY Independent

You would need to **rewrite or replace**:

### High Priority (Core Functionality):
1. **main.py** - Rewrite core application logic
   - Configuration management
   - Keyword filtering engine
   - Trending algorithm
   - Report generation

2. **Notification System** - Rebuild or keep
   - 6 platform integrations (3,000+ lines of code)
   - Message batching logic
   - Format conversion (Markdown/HTML)

### Medium Priority:
3. **HTML Report Generator** - Rebuild web output
4. **GitHub Actions Workflow** - Adapt for new structure
5. **Configuration System** - New YAML structure

### Low Priority:
6. **Push Time Window** - Notification scheduling
7. **Version Check** - Update notification

**Estimated Effort**: 
- **High** - Rewriting main.py alone is 4,500+ lines
- **Medium** - Notification system is complex (6 platforms)
- **Low** - Configuration and workflows are straightforward

---

## 📝 Summary

### What You've Achieved:
✅ **Data Independence**: No longer depend on NewsNow API
✅ **Custom Pipeline**: GPT-4o-mini search → AI processing → PostgreSQL

### What You Still Use from TrendRadar:
⚠️ **Core Application** (`main.py` - 4,557 lines)
⚠️ **Notification System** (6 platforms)
⚠️ **Configuration Management** (`config.yaml`)
⚠️ **Keyword Filtering** (`frequency_words.txt`)
⚠️ **HTML Report Generation**
⚠️ **Trending Algorithm**
⚠️ **GitHub Actions Workflow**

### Bottom Line:
You've replaced the **data source** (NewsNow → GPT-4o-mini) but still heavily depend on TrendRadar's **application logic, notification system, and reporting infrastructure**. The core `main.py` file is essentially the entire TrendRadar application.

---

## 🔗 Related Files

- `main.py` - Uses NewsNow API (line 455)
- `mcp_server/tools/system.py` - Uses NewsNow API (line 161)
- `news_search/` - Your independent search module
- `ai_processing/` - Your independent AI processor
- `docker-compose.yml` - Your PostgreSQL setup
- `ARCHITECTURE.md` - System architecture overview
- `README_CUSTOM_API.md` - How to configure custom NewsNow server

---

**Generated**: 2025-11-18
**Analysis Type**: Code Investigation (No Modifications)
