# 🚀 Facebook Auto Post Guide

## Quick Start

You now have 3 ways to auto-post to Facebook:

### Method 1: Simple One-Time Post

**Command Line**:
```bash
python facebook_auto_post.py "Your message here"
```

**Batch File** (Windows):
```bash
facebook_auto_post.bat
```

**Example**:
```bash
python facebook_auto_post.py "🚀 Excited to share my new project! #AI #Innovation"
```

### Method 2: Scheduled Posts (Daily)

**Run the scheduler**:
```bash
python facebook_scheduled_posts.py
```

This will post automatically at:
- 9:00 AM - Morning motivation
- 12:00 PM - Midday check-in
- 6:00 PM - Evening thoughts

**Customize the schedule**:
Edit `facebook_scheduled_posts.py` and modify the `SCHEDULED_POSTS` list:

```python
SCHEDULED_POSTS = [
    {
        'time': '09:00',
        'message': 'Your custom morning message'
    },
    {
        'time': '15:00',
        'message': 'Your custom afternoon message'
    }
]
```

### Method 3: Business Auto Poster

**Post daily update**:
```bash
python Skills/facebook_auto_poster.py
```

**Post custom message**:
```bash
python Skills/facebook_auto_poster.py "Your custom message"
```

**Post achievement**:
```python
from Skills.facebook_auto_poster import FacebookAutoPoster

poster = FacebookAutoPoster()
poster.post_achievement("Completed Gold Tier AI Employee!")
```

## Test Your Setup

Run the test script:
```bash
test_facebook_post.bat
```

This will post a test message to verify everything works.

## Features

### ✅ What You Can Do

1. **One-time posts**: Post immediately with a single command
2. **Scheduled posts**: Set up daily/weekly posting schedule
3. **Business updates**: Auto-post based on business activity
4. **Track posts**: All posts are tracked in `Social_Media_Tracking/` folder
5. **Error handling**: Automatic retry and error logging

### 📁 Post Tracking

All posts are saved in `Social_Media_Tracking/` with:
- Timestamp
- Post ID
- Post URL
- Message content
- Success/failure status

Example: `Social_Media_Tracking/facebook_20260304_143000_post.md`

## Customization

### Change Post Frequency

Edit `facebook_scheduled_posts.py`:

```python
# Post every hour
schedule.every().hour.do(post_scheduled, message)

# Post every Monday at 9 AM
schedule.every().monday.at("09:00").do(post_scheduled, message)

# Post every 30 minutes
schedule.every(30).minutes.do(post_scheduled, message)
```

### Add Images to Posts

Modify `facebook_auto_post.py`:

```python
result = post_to_facebook(
    message="Check out this image!",
    image_url="https://example.com/image.jpg"
)
```

### Post with Links

```python
result = post_to_facebook(
    message="Read my latest blog post!",
    link="https://yourblog.com/post"
)
```

## Integration with AI Employee

### Auto-post CEO Briefings

Add to `Skills/ceo_briefing_generator.py`:

```python
from facebook_auto_poster import FacebookAutoPoster

# After generating briefing
poster = FacebookAutoPoster()
poster.post_custom(f"📊 Weekly Business Update: {summary}")
```

### Auto-post Achievements

Add to your task completion logic:

```python
from facebook_auto_poster import FacebookAutoPoster

# When task completed
poster = FacebookAutoPoster()
poster.post_achievement(f"Completed: {task_name}")
```

### Auto-post from Watchers

Add to `Skills/gmail_watcher.py`:

```python
from facebook_auto_poster import FacebookAutoPoster

# When important email received
poster = FacebookAutoPoster()
poster.post_custom("📧 Important update received!")
```

## Scheduling with Windows Task Scheduler

To run posts automatically even when you're not at the computer:

1. Open Task Scheduler (search in Windows)
2. Click "Create Basic Task"
3. Name: "Facebook Auto Post"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
6. Program: `python`
7. Arguments: `C:\path\to\facebook_auto_post.py "Your message"`
8. Click Finish

## Troubleshooting

### Issue: "Token expired"

**Solution**:
1. Go to Graph API Explorer
2. Generate new token
3. Get page token from `/me/accounts`
4. Update `FACEBOOK_PAGE_ACCESS_TOKEN` in `.env`

### Issue: "Permission denied"

**Solution**:
Make sure your token has `pages_manage_posts` permission.

### Issue: "Page not found"

**Solution**:
Verify `FACEBOOK_PAGE_ID` in `.env` is correct.

### Issue: Posts not appearing

**Solution**:
- Check if post was successful (look in `Social_Media_Tracking/`)
- Verify you're looking at the correct Facebook page
- Check Facebook page settings (posts might be pending review)

## Best Practices

1. **Don't spam**: Post 2-3 times per day maximum
2. **Add value**: Make posts interesting and engaging
3. **Use hashtags**: Include relevant hashtags
4. **Track performance**: Review which posts get engagement
5. **Rotate content**: Don't post the same message repeatedly
6. **Check token**: Refresh token before it expires

## Example Posts

### Business Update
```python
python facebook_auto_post.py "🚀 Exciting progress on our AI project! Just completed the Gold Tier implementation. #AI #Innovation #Tech"
```

### Achievement
```python
python facebook_auto_post.py "🎉 Milestone achieved! Our AI Employee system is now fully autonomous. #Success #Automation"
```

### Daily Motivation
```python
python facebook_auto_post.py "☀️ Good morning! Remember: Progress over perfection. #MondayMotivation #Productivity"
```

### Behind the Scenes
```python
python facebook_auto_post.py "👨‍💻 Working on some exciting features today. Stay tuned! #Development #BehindTheScenes"
```

## Advanced: Bulk Posting

Create a file `posts.txt` with one message per line:

```
🚀 First post about AI
🤖 Second post about automation
💡 Third post about innovation
```

Then run:

```python
with open('posts.txt', 'r') as f:
    for line in f:
        if line.strip():
            os.system(f'python facebook_auto_post.py "{line.strip()}"')
            time.sleep(3600)  # Wait 1 hour between posts
```

## Next Steps

1. ✅ Test with `test_facebook_post.bat`
2. ✅ Customize scheduled posts
3. ✅ Set up Windows Task Scheduler
4. ✅ Integrate with your AI Employee workflows
5. ✅ Monitor post performance

---

**Your Facebook auto-posting system is ready!** 🎉

Start with the test script, then customize to fit your needs.
