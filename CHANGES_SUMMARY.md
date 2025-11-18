# 📝 Changes Summary - Custom NewsNow API Support

## What Was Changed

This repository has been modified to support connecting to **your own NewsNow API server** instead of the default public server.

---

## 🔧 Modified Files

### 1. `main.py`
**Line ~455:** Added support for custom API URL via environment variable

```python
# Before:
url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"

# After:
api_base_url = os.getenv('NEWSNOW_API_URL', 'https://newsnow.busiyi.world')
url = f"{api_base_url}/api/s?id={id_value}&latest"
```

### 2. `mcp_server/tools/system.py`
**Line ~160:** Added same support for MCP server

```python
# Added import
import os

# Modified URL construction
api_base_url = os.getenv('NEWSNOW_API_URL', 'https://newsnow.busiyi.world')
url = f"{api_base_url}/api/s?id={id_value}&latest"
```

### 3. `.github/workflows/crawler.yml`
**Line ~50:** Added environment variable for GitHub Actions

```yaml
env:
  # Custom NewsNow API Server URL (optional)
  NEWSNOW_API_URL: ${{ secrets.NEWSNOW_API_URL }}
  # ... other env vars
```

### 4. `docker/docker-compose.yml`
**Line ~12:** Added environment variable for Docker deployment

```yaml
environment:
  - TZ=Asia/Shanghai
  # NewsNow API配置
  - NEWSNOW_API_URL=${NEWSNOW_API_URL:-https://newsnow.busiyi.world}
  # ... other env vars
```

---

## 🎯 How It Works

### Default Behavior (No Configuration)
If you don't set `NEWSNOW_API_URL`, it will use the public server:
- `https://newsnow.busiyi.world`

### Custom Server (With Configuration)
Set the `NEWSNOW_API_URL` environment variable to your server:
- GitHub Actions: Add as a **Secret**
- Docker: Set in `.env` file or docker-compose
- Local: Set as system environment variable

---

## 🚀 Deployment Options

### Option 1: GitHub Actions (Recommended)
1. Fork this repository
2. Add `NEWSNOW_API_URL` as a GitHub Secret
3. Configure keywords in `config/frequency_words.txt`
4. Enable GitHub Actions
5. Done! It runs automatically

### Option 2: Docker
1. Clone this repository
2. Create `.env` file with `NEWSNOW_API_URL=https://your-server.com`
3. Run `docker-compose up -d`
4. Done! It runs on schedule

### Option 3: Local Python
1. Clone this repository
2. Set environment variable: `export NEWSNOW_API_URL=https://your-server.com`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

---

## ✅ Benefits

1. **Flexibility:** Use your own NewsNow server or the public one
2. **Privacy:** Keep your data on your own infrastructure
3. **Customization:** Add custom platforms to your NewsNow server
4. **Reliability:** Don't depend on public server availability
5. **Backward Compatible:** Works without any configuration (uses public server)

---

## 🔍 Testing Your Setup

### Test if your API is accessible:
```bash
curl https://your-newsnow-server.com/api/s?id=zhihu&latest
```

Should return JSON with news data.

### Test TrendRadar locally:
```bash
export NEWSNOW_API_URL=https://your-newsnow-server.com
python main.py
```

Check `output/` folder for results.

---

## 📚 Documentation

- **Quick Start:** See [QUICK_START.md](QUICK_START.md)
- **Full Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Original README:** See [readme.md](readme.md)

---

## 🆘 Troubleshooting

### Issue: Still using public server
- Check if environment variable is set correctly
- Verify secret name is exactly `NEWSNOW_API_URL`
- Check GitHub Actions logs for the actual URL being used

### Issue: Connection failed
- Verify your NewsNow server is accessible
- Check if URL format is correct (no trailing slash)
- Test API endpoint manually with curl

### Issue: No data returned
- Verify platform IDs match your NewsNow server
- Check if your server has data for those platforms
- Review error logs in GitHub Actions or Docker logs

---

## 🎉 Ready to Deploy!

Follow the [QUICK_START.md](QUICK_START.md) guide to get started in 5 minutes!
