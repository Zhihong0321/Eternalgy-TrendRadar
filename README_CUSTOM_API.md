# 🎯 TrendRadar with Custom NewsNow API

## What's New?

This fork adds support for connecting to **your own NewsNow API server**.

## Quick Setup

### 1. Set Your API URL

**GitHub Actions:**
```
Settings → Secrets → Actions → New secret
Name: NEWSNOW_API_URL
Value: https://your-newsnow-server.com
```

**Docker:**
```bash
# Edit docker/.env
NEWSNOW_API_URL=https://your-newsnow-server.com
```

**Local:**
```bash
export NEWSNOW_API_URL=https://your-newsnow-server.com
python main.py
```

### 2. Configure Keywords

Edit `config/frequency_words.txt` with your interests.

### 3. Deploy!

See [QUICK_START.md](QUICK_START.md) for step-by-step guide.

## Documentation

- 📖 [Quick Start Guide](QUICK_START.md) - 5 minutes setup
- 📚 [Full Deployment Guide](DEPLOYMENT_GUIDE.md) - Detailed instructions
- 📝 [Changes Summary](CHANGES_SUMMARY.md) - What was modified
- 🏗️ [Architecture](ARCHITECTURE.md) - System overview

## Default Behavior

Without configuration, uses public server: `https://newsnow.busiyi.world`

## Questions?

Check the documentation files above or the original [readme.md](readme.md)
