# 🚀 TrendRadar Deployment Guide - Custom NewsNow API

This guide will help you deploy TrendRadar on GitHub Actions with your own NewsNow API server.

## 📋 Prerequisites

1. **Your own NewsNow API server** running and accessible
   - Example: `https://your-newsnow-server.com`
   - Must support the same API format: `/api/s?id={platform_id}&latest`

2. **GitHub account** (free)

3. **Keywords list** - What news topics you want to filter

---

## 🔧 Step 1: Fork This Repository

1. Go to: https://github.com/sansan0/TrendRadar
2. Click the **Fork** button (top right)
3. Wait for the fork to complete

---

## ⚙️ Step 2: Configure Your Custom NewsNow API

### Add GitHub Secret for Your API URL

1. Go to your forked repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

   **Name:** `NEWSNOW_API_URL`
   
   **Value:** `https://your-newsnow-server.com` (without trailing slash)

   > ⚠️ **Important:** Do NOT include `/api/s` in the URL, just the base URL

### Example:
- ✅ Correct: `https://api.example.com`
- ✅ Correct: `http://192.168.1.100:3000`
- ❌ Wrong: `https://api.example.com/api/s`
- ❌ Wrong: `https://api.example.com/`

---

## 📝 Step 3: Configure Keywords Filter

Edit the file `config/frequency_words.txt` in your repository:

1. Go to your repository
2. Navigate to `config/frequency_words.txt`
3. Click the **pencil icon** (Edit)
4. Add your keywords (one per line):

```
AI
人工智能
Tesla
特斯拉
比亚迪
华为
```

**Syntax:**
- Normal keyword: `AI` - matches news containing "AI"
- Must include: `+keyword` - news MUST contain this
- Exclude: `!keyword` - filter out news with this word

**Example:**
```
AI
+人工智能
!广告
```
This will match news about AI and 人工智能, but exclude any with 广告.

4. Click **Commit changes**

---

## 🔔 Step 4: Configure Notifications (Optional)

If you want to receive push notifications, add these secrets:

### For Telegram:
- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID

### For WeWork (企业微信):
- `WEWORK_WEBHOOK_URL` - Your WeWork webhook URL

### For Feishu (飞书):
- `FEISHU_WEBHOOK_URL` - Your Feishu webhook URL

### For DingTalk (钉钉):
- `DINGTALK_WEBHOOK_URL` - Your DingTalk webhook URL

### For Email:
- `EMAIL_FROM` - Sender email
- `EMAIL_PASSWORD` - Email password or app password
- `EMAIL_TO` - Recipient email(s), comma-separated

---

## 🎯 Step 5: Configure Platforms

Edit `config/config.yaml` to select which platforms to monitor:

```yaml
platforms:
  - id: "zhihu"
    name: "知乎"
  - id: "weibo"
    name: "微博"
  - id: "douyin"
    name: "抖音"
  # Add more platforms supported by your NewsNow server
```

**Platform IDs** must match what your NewsNow API server supports.

---

## ⏰ Step 6: Configure Schedule

Edit `.github/workflows/crawler.yml` to change the schedule:

```yaml
on:
  schedule:
    - cron: "0 * * * *"  # Every hour
    # - cron: "*/30 * * * *"  # Every 30 minutes
    # - cron: "0 9,12,18 * * *"  # At 9am, 12pm, 6pm
```

**Cron examples:**
- `0 * * * *` - Every hour
- `*/30 * * * *` - Every 30 minutes
- `0 9-18 * * *` - Every hour from 9am to 6pm
- `0 9,12,15,18 * * *` - At 9am, 12pm, 3pm, 6pm

---

## 🚀 Step 7: Enable GitHub Actions

1. Go to your repository
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**
4. The workflow will run automatically based on your schedule

---

## 🧪 Step 8: Test Your Setup

### Manual Test:

1. Go to **Actions** tab
2. Click **Hot News Crawler** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for completion (usually 1-2 minutes)
5. Check the results:
   - Go to **Code** tab
   - Check `output/` folder for generated files
   - Check your notification channels

---

## 📊 Step 9: Enable GitHub Pages (Optional)

To view your news as a web page:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Select branch: **main** or **master**
4. Select folder: **/ (root)**
5. Click **Save**
6. Wait 1-2 minutes
7. Your page will be available at: `https://your-username.github.io/TrendRadar/`

---

## 🔍 Verification Checklist

- [ ] GitHub Actions is enabled
- [ ] `NEWSNOW_API_URL` secret is set (if using custom server)
- [ ] Keywords are configured in `frequency_words.txt`
- [ ] Platforms are configured in `config/config.yaml`
- [ ] Notification webhooks are set (optional)
- [ ] Schedule is configured in `crawler.yml`
- [ ] First manual run completed successfully
- [ ] Output files generated in `output/` folder
- [ ] GitHub Pages enabled (optional)

---

## 🐛 Troubleshooting

### Issue: No news data collected

**Check:**
1. Is your NewsNow API server accessible from GitHub Actions?
2. Does the API URL in secrets match your server?
3. Are the platform IDs correct?
4. Check the Actions logs for error messages

### Issue: No notifications received

**Check:**
1. Are the webhook secrets correctly set?
2. Is `enable_notification: true` in `config/config.yaml`?
3. Do your keywords match any news?

### Issue: GitHub Actions not running

**Check:**
1. Is GitHub Actions enabled in your repository?
2. Is the cron schedule correct?
3. Has the repository been active? (GitHub may disable Actions on inactive repos)

---

## 📁 Output Files

After each run, you'll find:

- `output/index.html` - Web view of filtered news
- `output/daily_news_YYYYMMDD.json` - Daily news data
- `output/current_news.json` - Latest news data
- `output/news_history.json` - Historical tracking data

---

## 🔄 Updating Your Deployment

To update TrendRadar with new features:

1. Check the original repository for updates
2. Manually copy changed files to your fork
3. Or use GitHub's "Sync fork" feature (may require manual conflict resolution)

---

## 💡 Tips

1. **Start with fewer platforms** to test your setup
2. **Use specific keywords** to reduce noise
3. **Test manually first** before relying on scheduled runs
4. **Monitor your GitHub Actions usage** (2000 minutes/month free)
5. **Keep your NewsNow API server stable** for reliable data collection

---

## 🆘 Need Help?

- Check the [original TrendRadar README](readme.md)
- Review GitHub Actions logs for errors
- Verify your NewsNow API server is working
- Test API endpoints manually with curl/Postman

---

## 🎉 You're All Set!

Your TrendRadar deployment will now:
1. Connect to YOUR NewsNow API server
2. Collect news from configured platforms
3. Filter by YOUR keywords
4. Send notifications to YOUR channels
5. Generate web pages with filtered results

Enjoy your personalized news filtering system! 🚀
