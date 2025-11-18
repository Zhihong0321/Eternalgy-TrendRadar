# ⚡ Quick Start - 5 Minutes Setup

## 1️⃣ Fork Repository
Fork https://github.com/sansan0/TrendRadar to your GitHub account

## 2️⃣ Add Your NewsNow API URL
**Settings** → **Secrets** → **Actions** → **New secret**

- Name: `NEWSNOW_API_URL`
- Value: `https://your-newsnow-server.com`

## 3️⃣ Configure Keywords
Edit `config/frequency_words.txt`:
```
AI
Tesla
华为
比亚迪
```

## 4️⃣ Enable GitHub Actions
**Actions** tab → **Enable workflows**

## 5️⃣ Test Run
**Actions** → **Hot News Crawler** → **Run workflow**

## ✅ Done!
Check `output/` folder for results after 1-2 minutes.

---

## 📌 Optional: Add Notifications

Add these secrets for push notifications:
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
- `WEWORK_WEBHOOK_URL`
- `FEISHU_WEBHOOK_URL`
- `DINGTALK_WEBHOOK_URL`

---

## 🌐 Optional: Enable Web View

**Settings** → **Pages** → **Deploy from branch: main**

Your page: `https://your-username.github.io/TrendRadar/`

---

## 🔧 Default Behavior

- **API Server:** Your custom NewsNow server (or public if not set)
- **Schedule:** Every hour
- **Filter:** Keywords in `frequency_words.txt`
- **Output:** `output/` folder + notifications

---

## 📖 Full Guide
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
