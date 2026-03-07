# Facebook Integration Architecture

## How Facebook Auto-Posting Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Employee Gold Tier                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Trigger Events (When to Post)                                  │
├─────────────────────────────────────────────────────────────────┤
│  • New invoice created in Odoo                                  │
│  • Weekly business summary (Monday 9 AM)                        │
│  • New customer onboarded                                       │
│  • Milestone achieved (revenue target, etc.)                    │
│  • Scheduled posts (daily motivation, etc.)                     │
│  • AI decides to post update                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  AI Employee Decision Layer                                     │
├─────────────────────────────────────────────────────────────────┤
│  1. Analyze event                                               │
│  2. Determine message content                                   │
│  3. Select platform (Facebook, Instagram, or both)              │
│  4. Check approval workflow (if required)                       │
│  5. Format message for platform                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  MCP Server: Facebook/Instagram                                 │
│  (Skills/mcp_servers/facebook_instagram_mcp_server.py)          │
├─────────────────────────────────────────────────────────────────┤
│  Tools Available:                                               │
│  • post_to_facebook                                             │
│  • post_to_instagram                                            │
│  • get_facebook_insights                                        │
│  • get_instagram_insights                                       │
│  • get_facebook_posts                                           │
│  • get_instagram_posts                                          │
│  • generate_social_media_summary                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Facebook Graph API v18.0                                       │
│  (https://graph.facebook.com/v18.0)                             │
├─────────────────────────────────────────────────────────────────┤
│  Authentication: Page Access Token                              │
│  Endpoint: /me/feed (POST)                                      │
│  Parameters: message, link, photo_url, scheduled_time           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Facebook Platform                                              │
├─────────────────────────────────────────────────────────────────┤
│  • Facebook Page                                                │
│  • Instagram Business Account                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Your Audience                                                  │
│  • Page Followers                                               │
│  • Instagram Followers                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Posting to Facebook

```
1. EVENT TRIGGER
   └─> Odoo creates invoice #123 for $5,000

2. AI DECISION
   └─> "This is worth posting about!"
   └─> Generate message: "🎉 New Invoice! Customer: Acme Corp, Amount: $5,000"

3. MCP SERVER CALL
   └─> execute_tool("post_to_facebook", {
         "message": "🎉 New Invoice!...",
         "photo_url": "https://..."
       })

4. API REQUEST
   POST https://graph.facebook.com/v18.0/me/feed
   Params:
     - access_token: EAA...
     - message: "🎉 New Invoice!..."
     - photo_url: "https://..."

5. FACEBOOK RESPONSE
   {
     "id": "123456789_987654321"
   }

6. TRACKING
   └─> Save to vault: Social_Media_Tracking/facebook_TIMESTAMP_987654321.md
   └─> Log action: Audit Logger

7. COMPLETE
   └─> Post is live on Facebook!
```

---

## Authentication Flow

```
┌──────────────────────────────────────────────────────────────┐
│  1. Facebook Developer                                       │
│     • Create App                                              │
│     • Get App ID & Secret                                    │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  2. Graph API Explorer                                       │
│     • Get User Token (short-lived)                           │
│     • Request permissions:                                   │
│       - pages_manage_posts                                   │
│       - pages_read_engagement                                │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  3. Exchange for Long-Lived Token                            │
│     • POST /oauth/access_token                               │
│     • Valid for 60 days                                      │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  4. Get Page Access Token                                    │
│     • GET /me/accounts                                       │
│     • Extract page token from response                       │
│     • Page tokens don't expire!                              │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  5. Get Instagram Business Account ID                        │
│     • GET /me?fields=instagram_business_account              │
│     • Save account ID                                        │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  6. Store in .env                                            │
│     FACEBOOK_PAGE_ACCESS_TOKEN=EAA...                        │
│     INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000          │
└──────────────────────────────────────────────────────────────┘
```

---

## Auto-Posting Workflow Example

### Scenario: Weekly Business Summary

```
Monday 9:00 AM
    │
    ▼
┌─────────────────────────┐
│  Scheduler Trigger      │
│  (Every Monday 9 AM)    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Get Data from Odoo     │
│  • Revenue this week    │
│  • Expenses             │
│  • New customers        │
│  • Invoices created     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  AI Generates Message   │
│  "📊 Weekly Summary     │
│   Revenue: $5,000       │
│   Profit: $3,000        │
│   New Clients: 2        │
│   #BusinessGrowth"      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Post to Facebook       │
│  • Message + Image      │
│  • Auto-generated chart │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Post to Instagram      │
│  • Caption + Image      │
│  • Hashtags             │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Track in Vault         │
│  • Save post IDs        │
│  • Log engagement       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Monitor Engagement     │
│  • Likes                │
│  • Comments             │
│  • Shares               │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Auto-Respond to        │
│  Comments (Optional)    │
│  • Thank for likes      │
│  • Answer questions     │
└─────────────────────────┘
```

---

## Integration Points

### With Odoo (Accounting)
```
Odoo Invoice Created
    │
    ▼
AI Employee Detects
    │
    ▼
Generate Celebration Post
    │
    ▼
Post to Facebook + Instagram
```

### With CEO Briefing
```
Generate Weekly Briefing
    │
    ▼
Extract Key Metrics
    │
    ▼
Create Social Media Summary
    │
    ▼
Schedule Post for Monday 9 AM
```

### With WhatsApp
```
Customer Messages "Pricing"
    │
    ▼
AI Responds via WhatsApp
    │
    ▼
Log as New Lead
    │
    ▼
(Optional) Post "Welcome New Client"
```

---

## File Structure

```
hackthone_0/
├── Skills/
│   └── mcp_servers/
│       ├── facebook_instagram_mcp_server.py    ← Main integration
│       ├── odoo_mcp_server.py                   ← Accounting data
│       └── base_mcp_server.py                   ← Base class
├── .env                                          ← Tokens & config
├── test_facebook_autopost.py                     ← Test script
├── test_facebook_autopost.bat                    ← Windows test
├── FACEBOOK_INSTAGRAM_AUTOPOST_GUIDE.md          ← Full guide
├── FACEBOOK_QUICK_START.md                       ← Quick start
└── FACEBOOK_INTEGRATION_ARCHITECTURE.md          ← This file
```

---

## Security Considerations

```
┌────────────────────────────────────────────────────────────┐
│  ✅ DO:                                                     │
│     • Store tokens in .env file                            │
│     • Add .env to .gitignore                               │
│     • Use long-lived tokens                                │
│     • Rotate tokens every 60 days                          │
│     • Limit app permissions                                │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  ❌ DON'T:                                                  │
│     • Commit .env to Git                                   │
│     • Share tokens publicly                                │
│     • Use personal account token                           │
│     • Grant unnecessary permissions                        │
│     • Hardcode tokens in code                              │
└────────────────────────────────────────────────────────────┘
```

---

## Monitoring & Analytics

```
Facebook Graph API
    │
    ▼
Get Insights (Daily/Weekly)
    │
    ├──> Page Impressions
    ├──> Post Engagements
    ├──> Page Likes
    ├──> Reach
    └──> Follower Growth
            │
            ▼
    Store in Vault (Social_Media_Tracking/)
            │
            ▼
    Include in CEO Briefing
            │
            ▼
    AI Analyzes Trends
            │
            ▼
    Optimize Posting Strategy
```

---

**Your AI Employee now has complete Facebook/Instagram automation!** 🚀
