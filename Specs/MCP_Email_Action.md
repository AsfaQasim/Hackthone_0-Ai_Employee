---
type: feature_spec
status: draft
category: action
risk_level: high
created: 2026-02-15
requires_approval: true
mcp_servers: [gmail-action, payment-processor, social-media]
---

# Email and Payment Action Specification with HITL

## Overview

An action layer component that handles email responses, payment processing, and social media interactions with mandatory human-in-the-loop approval for sensitive operations.

## Purpose

Enable the Personal AI Employee to:
- Draft and send email responses
- Process payments and financial transactions
- Respond to social media messages
- Enforce approval rules for sensitive actions
- Track approval decisions and outcomes
- Learn from human feedback

## Approval Rules

### Rule 1: Payment Approval
**Trigger**: Any payment or financial transaction > $50  
**Requires**: Human approval before execution  
**Folder**: /Pending_Approval/payments/

### Rule 2: New Contact Approval
**Trigger**: Email to/from contact not in address book  
**Requires**: Human approval before sending  
**Folder**: /Pending_Approval/contacts/

### Rule 3: Social Reply Approval
**Trigger**: Any reply to social media (Twitter, LinkedIn, etc.)  
**Requires**: Human approval before posting  
**Folder**: /Pending_Approval/social/

## User Stories

### US-1: Payment Approval
**As a** user  
**I want** to approve all payments over $50  
**So that** I maintain control over my finances

**Acceptance Criteria**:
- Payments > $50 create approval request in /Pending_Approval/payments/
- Request includes amount, recipient, purpose, invoice
- I can approve (move to /Approved/), reject (move to /Rejected/), or modify
- Approved payments execute automatically
- Rejected payments are logged with reason

### US-2: New Contact Approval
**As a** user  
**I want** to approve emails to new contacts  
**So that** I control who I communicate with

**Acceptance Criteria**:
- Emails to unknown contacts create approval request
- Request includes draft email, recipient info, context
- I can approve, reject, or edit the email
- Approved emails send automatically
- Contact is added to approved list


### US-3: Social Reply Approval
**As a** user  
**I want** to approve all social media replies  
**So that** I maintain my public reputation

**Acceptance Criteria**:
- Social replies create approval request in /Pending_Approval/social/
- Request includes draft reply, original message, platform
- I can approve, reject, or edit the reply
- Approved replies post automatically
- Rejected replies are logged with feedback

### US-4: Approval Workflow
**As a** user  
**I want** a simple approval workflow  
**So that** I can quickly review and decide

**Acceptance Criteria**:
- All requests in /Pending_Approval/ organized by type
- Move to /Approved/ to approve
- Move to /Rejected/ to reject
- Edit file to modify before approving
- System detects moves and executes accordingly

### US-5: Audit Trail
**As a** user  
**I want** complete history of approvals  
**So that** I can review past decisions

**Acceptance Criteria**:
- All approved actions archived in /Approved/
- All rejected actions archived in /Rejected/
- Each includes timestamp, decision, outcome
- Searchable and queryable
- Exportable for accounting/compliance

## Architecture

### Approval Workflow

```
┌─────────────────────────────────────────────────────────┐
│                  ACTION TRIGGER                          │
├─────────────────────────────────────────────────────────┤
│  Payment Request  │  Email Draft  │  Social Reply       │
└─────────────────────────────────────────────────────────┘
                          ↓
                   Check Approval Rules
                          ↓
        ┌─────────────────┴─────────────────┐
        │                                   │
    [Requires Approval]              [Auto-Execute]
        │                                   │
        ↓                                   ↓
Create Approval Request              Execute Action
        │                                   │
        ↓                                   ↓
Save to /Pending_Approval/           Log to /Logs/
        │
        ↓
    Notify Human
        │
        ↓
    Wait for Decision
        │
        ├─ [Moved to /Approved/] ──→ Execute Action
        │                                   ↓
        │                              Log Success
        │                                   ↓
        │                         Archive to /Approved/
        │
        ├─ [Moved to /Rejected/] ──→ Cancel Action
        │                                   ↓
        │                              Log Rejection
        │                                   ↓
        │                         Archive to /Rejected/
        │
        └─ [Modified in place] ──→ Re-validate
                                          ↓
                                   Update Request
                                          ↓
                                   Wait for Decision
```

### Folder Structure

```
/Pending_Approval/
├── payments/
│   ├── payment_20260215_103000_vendor_invoice.md
│   ├── payment_20260215_110000_contractor_fee.md
│   └── payment_20260215_143000_software_license.md
├── contacts/
│   ├── email_20260215_104500_new_client_intro.md
│   ├── email_20260215_120000_partnership_inquiry.md
│   └── email_20260215_153000_job_applicant.md
└── social/
    ├── twitter_20260215_105000_customer_question.md
    ├── linkedin_20260215_130000_connection_request.md
    └── twitter_20260215_160000_product_feedback.md

/Approved/
├── 2026-02/
│   ├── payments/
│   ├── contacts/
│   └── social/
└── 2026-01/
    ├── payments/
    ├── contacts/
    └── social/

/Rejected/
├── 2026-02/
│   ├── payments/
│   ├── contacts/
│   └── social/
└── 2026-01/
    ├── payments/
    ├── contacts/
    └── social/
```

## Approval Request Formats

### Payment Approval Request

```markdown
---
type: payment_approval
request_id: pay_20260215_103000
amount: 1250.00
currency: USD
recipient: Acme Software Inc
category: software_license
created: 2026-02-15T10:30:00Z
due_date: 2026-02-20
risk_level: medium
---

# Payment Approval: Acme Software License - $1,250

## Payment Details

**Amount**: $1,250.00 USD  
**Recipient**: Acme Software Inc  
**Purpose**: Annual software license renewal  
**Invoice**: INV-2026-0215  
**Due Date**: February 20, 2026

## Why This Payment

- Annual renewal for project management software
- Used by entire team (12 users)
- Current license expires February 28
- Price unchanged from last year

## Budget Impact

**Budget Category**: Software & Tools  
**Monthly Budget**: $5,000  
**Spent This Month**: $2,340  
**After This Payment**: $3,590 (72% of budget)  
**Remaining**: $1,410

## Verification

✅ **Invoice Verified**: Matches last year's invoice  
✅ **Vendor Verified**: Existing vendor in system  
✅ **Budget Available**: Within monthly allocation  
✅ **Due Date**: 5 days until due

## Payment Method

**Method**: Bank Transfer  
**Account**: Business Checking (...4532)  
**Processing Time**: 2-3 business days  
**Fees**: $0 (free transfer)

## Alternatives Considered

1. **Pay Now** (Recommended)
   - Avoid late fees
   - Maintain service continuity
   - Take advantage of early payment discount (2%)

2. **Delay Payment**
   - Risk late fee ($50)
   - Risk service interruption
   - No benefit to delaying

3. **Cancel Service**
   - Save $1,250
   - Lose project management capability
   - Team productivity impact
   - Not recommended

## Risk Assessment

**Risk Level**: MEDIUM

**Risks**:
- Budget impact (25% of monthly software budget)
- Vendor dependency (locked in for 1 year)

**Mitigation**:
- Essential tool for team productivity
- Proven value over past 2 years
- No better alternatives at this price

## Supporting Documents

- [[Invoices/INV-2026-0215.pdf]] - Original invoice
- [[Contracts/Acme_Software_Agreement.pdf]] - Service agreement
- [[Accounting/software_budget_2026.md]] - Budget tracking

## How to Approve

### ✅ Approve Payment
**Move this file to**: `/Approved/payments/`

I will:
1. Process payment via bank transfer
2. Send payment confirmation to vendor
3. Update accounting records
4. Schedule next year's renewal reminder
5. Archive to /Approved/2026-02/payments/

### ❌ Reject Payment
**Move this file to**: `/Rejected/payments/`

Please add your reason:
```
## Rejection Reason

[Why you're rejecting this payment]
```

I will:
1. Cancel payment processing
2. Notify vendor of non-payment
3. Log rejection reason
4. Archive to /Rejected/2026-02/payments/

### ✏️ Modify Payment
**Edit this file** and keep in `/Pending_Approval/payments/`

You can change:
- Amount (e.g., negotiate discount)
- Payment date (e.g., delay until next month)
- Payment method (e.g., use credit card instead)
- Add conditions (e.g., "only if vendor provides X")

---

**Status**: PENDING YOUR APPROVAL  
**Created**: 2026-02-15 10:30 AM  
**Expires**: 2026-02-20 (5 days)  
**Priority**: MEDIUM

*If not approved by due date, I will move to /Rejected/ to avoid late payment.*
```

### Email Contact Approval Request

```markdown
---
type: email_approval
request_id: email_20260215_104500
recipient: sarah.johnson@newclient.com
recipient_name: Sarah Johnson
contact_status: new
email_type: business_introduction
created: 2026-02-15T10:45:00Z
risk_level: low
---

# Email Approval: Introduction to Sarah Johnson (New Contact)

## Recipient Information

**Name**: Sarah Johnson  
**Email**: sarah.johnson@newclient.com  
**Company**: NewClient Corp  
**Title**: VP of Engineering  
**Status**: ⚠️ NEW CONTACT (not in address book)

## Context

**Why I'm Emailing**:
- Sarah requested demo via website contact form
- Matches ideal customer profile (enterprise, engineering)
- Potential $50K opportunity

**Previous Interaction**:
- Submitted contact form 2 hours ago
- Requested demo for team of 25 engineers
- Mentioned competitor comparison

## Draft Email

```
Subject: Re: Demo Request - Project Management for Engineering Teams

Hi Sarah,

Thank you for your interest in our project management platform!

I'd be happy to schedule a demo for your engineering team. Based on your 
note about managing 25 engineers, I think our Enterprise plan would be 
a great fit.

I have availability this week:
- Thursday, Feb 17 at 2:00 PM PT
- Friday, Feb 18 at 10:00 AM PT

Would either of these times work for you? The demo typically takes 30 
minutes, and I'll show you features specifically relevant to engineering 
teams.

Looking forward to connecting!

Best regards,
[Your Name]
```

## Why This Email is Appropriate

✅ **Professional Tone**: Business-appropriate language  
✅ **Relevant Content**: Addresses her specific needs  
✅ **Clear CTA**: Proposes specific meeting times  
✅ **Value Focus**: Mentions relevant features  
✅ **No Spam**: Direct response to her inquiry

## Risk Assessment

**Risk Level**: LOW

**Why Low Risk**:
- Responding to inbound inquiry (not cold outreach)
- Professional business context
- Standard sales response
- No sensitive information shared

## Contact Verification

**Email Domain**: newclient.com ✅ Valid  
**Company**: NewClient Corp ✅ Real company (verified via LinkedIn)  
**Title**: VP of Engineering ✅ Confirmed on LinkedIn  
**Spam Check**: ❌ Not spam (legitimate inquiry)

## Expected Outcome

**If Approved**:
- Email sent within 1 hour
- Sarah added to CRM
- Demo scheduled if she responds
- Potential $50K opportunity

**If Rejected**:
- No email sent
- Inquiry marked as declined
- Opportunity lost

## How to Approve

### ✅ Approve Email
**Move this file to**: `/Approved/contacts/`

I will:
1. Send email immediately
2. Add Sarah to approved contacts
3. Add to CRM with "demo requested" status
4. Track response and follow up if needed
5. Archive to /Approved/2026-02/contacts/

### ❌ Reject Email
**Move this file to**: `/Rejected/contacts/`

Please add your reason:
```
## Rejection Reason

[Why you're rejecting this email]
```

I will:
1. Not send email
2. Mark inquiry as declined
3. Log rejection reason
4. Archive to /Rejected/2026-02/contacts/

### ✏️ Edit Email
**Edit the draft above** and keep in `/Pending_Approval/contacts/`

You can change:
- Email content (tone, details, offer)
- Subject line
- Meeting times
- Add/remove information

---

**Status**: PENDING YOUR APPROVAL  
**Created**: 2026-02-15 10:45 AM  
**Priority**: MEDIUM (inbound inquiry)  
**Response Time**: Should respond within 4 hours

*Quick response improves conversion rate by 40%*
```


### Social Reply Approval Request

```markdown
---
type: social_approval
request_id: social_20260215_105000
platform: twitter
original_author: @customer_john
original_message_id: "1234567890"
reply_type: customer_support
created: 2026-02-15T10:50:00Z
risk_level: medium
---

# Social Reply Approval: Twitter Response to @customer_john

## Original Message

**Platform**: Twitter (X)  
**From**: @customer_john  
**Posted**: 2026-02-15 10:30 AM  
**Visibility**: Public  
**Engagement**: 12 likes, 3 retweets

> "@YourCompany The new update broke my workflow! Can't export reports 
> anymore. This is frustrating. #bug #disappointed"

## Sentiment Analysis

**Sentiment**: 😠 Negative (frustrated customer)  
**Tone**: Upset but not hostile  
**Issue**: Product bug (export feature)  
**Urgency**: High (affecting their work)  
**Public Impact**: Medium (12 likes = others experiencing same issue)

## Draft Reply

```
@customer_john We're sorry to hear about the export issue! Our team 
is investigating this bug right now. 

As a workaround, you can export via Settings > Data > Export (legacy). 
We'll have a fix deployed by end of day.

DM us if you need immediate help! 🙏
```

**Character Count**: 237/280 ✅  
**Tone**: Apologetic, helpful, professional  
**Includes**: Acknowledgment, workaround, timeline, CTA

## Why This Reply is Appropriate

✅ **Acknowledges Issue**: Shows we heard them  
✅ **Provides Solution**: Offers immediate workaround  
✅ **Sets Expectation**: Timeline for fix  
✅ **Offers Help**: Invites DM for support  
✅ **Professional Tone**: Appropriate for public response  
✅ **No Blame**: Doesn't make excuses

## Risk Assessment

**Risk Level**: MEDIUM

**Why Medium Risk**:
- Public response (visible to all followers)
- Admits bug exists (transparency vs reputation)
- Sets timeline expectation (must deliver)
- Customer is frustrated (could escalate)

**Mitigation**:
- Honest and transparent
- Provides immediate workaround
- Realistic timeline (end of day)
- Offers private support channel

## Context

**Customer**: @customer_john  
**Relationship**: Paying customer (verified)  
**Account Age**: 2 years  
**Previous Issues**: 1 (resolved positively)  
**Sentiment History**: Generally positive

**Bug Status**:
- Confirmed bug in v2.3.1
- Affects export feature
- Fix in progress (ETA: 4 hours)
- Workaround available (legacy export)

## Alternative Responses

### Option 1: Detailed Technical (Not Recommended)
```
@customer_john The export bug is due to a regression in the new 
data pipeline. We're rolling back the change and will redeploy...
```
❌ Too technical for public tweet  
❌ Too long (over character limit)

### Option 2: Minimal Response (Not Recommended)
```
@customer_john Thanks for reporting! We're looking into it.
```
❌ Too vague  
❌ No workaround provided  
❌ No timeline

### Option 3: Defensive (Not Recommended)
```
@customer_john The export feature works fine for most users. 
Have you tried clearing your cache?
```
❌ Dismissive tone  
❌ Blames user  
❌ Not helpful

## Expected Outcome

**If Approved**:
- Reply posted publicly
- Customer receives workaround
- Others see we're responsive
- Reputation maintained
- Issue tracked for follow-up

**If Rejected**:
- No public reply
- Customer remains frustrated
- Others see no response
- Reputation risk

## How to Approve

### ✅ Approve Reply
**Move this file to**: `/Approved/social/`

I will:
1. Post reply immediately
2. Monitor for customer response
3. Follow up when bug is fixed
4. Track sentiment change
5. Archive to /Approved/2026-02/social/

### ❌ Reject Reply
**Move this file to**: `/Rejected/social/`

Please add your reason:
```
## Rejection Reason

[Why you're rejecting this reply]
[What should we do instead?]
```

I will:
1. Not post reply
2. Log rejection reason
3. Wait for alternative guidance
4. Archive to /Rejected/2026-02/social/

### ✏️ Edit Reply
**Edit the draft above** and keep in `/Pending_Approval/social/`

You can change:
- Tone (more/less formal)
- Content (add/remove details)
- Workaround instructions
- Timeline commitment
- Call to action

---

**Status**: PENDING YOUR APPROVAL  
**Created**: 2026-02-15 10:50 AM  
**Priority**: HIGH (public complaint)  
**Response Time**: Should respond within 1 hour

*Fast response to public complaints improves customer satisfaction by 60%*
```

## MCP Server Integration

### Gmail Action Server

**Configuration**:
```json
{
  "mcpServers": {
    "gmail-action": {
      "command": "node",
      "args": ["./mcp-servers/gmail-action-server.js"],
      "env": {
        "GMAIL_CREDENTIALS_PATH": "./config/gmail-credentials.json",
        "GMAIL_TOKEN_PATH": "./config/gmail-token.json"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**MCP Tools**:

#### gmail.send(to, subject, body)
- **Purpose**: Send email
- **Inputs**: Recipient, subject, body
- **Outputs**: Message ID, success status
- **Risk**: HIGH (requires approval for new contacts)

#### gmail.reply(messageId, body)
- **Purpose**: Reply to email
- **Inputs**: Original message ID, reply body
- **Outputs**: Reply message ID, success status
- **Risk**: MEDIUM (requires approval for new contacts)

#### gmail.draft(to, subject, body)
- **Purpose**: Create draft email
- **Inputs**: Recipient, subject, body
- **Outputs**: Draft ID
- **Risk**: LOW (no sending)

### Payment Processor Server

**Configuration**:
```json
{
  "mcpServers": {
    "payment-processor": {
      "command": "node",
      "args": ["./mcp-servers/payment-server.js"],
      "env": {
        "BANK_API_KEY": "...",
        "BANK_API_SECRET": "..."
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**MCP Tools**:

#### payment.create(amount, recipient, purpose)
- **Purpose**: Create payment
- **Inputs**: Amount, recipient, purpose
- **Outputs**: Payment ID, status
- **Risk**: HIGH (requires approval if > $50)

#### payment.verify(invoiceId)
- **Purpose**: Verify invoice
- **Inputs**: Invoice ID
- **Outputs**: Verification status, details
- **Risk**: LOW (read-only)

#### payment.schedule(paymentId, date)
- **Purpose**: Schedule payment
- **Inputs**: Payment ID, execution date
- **Outputs**: Schedule confirmation
- **Risk**: MEDIUM (commits to future payment)

### Social Media Server

**Configuration**:
```json
{
  "mcpServers": {
    "social-media": {
      "command": "node",
      "args": ["./mcp-servers/social-server.js"],
      "env": {
        "TWITTER_API_KEY": "...",
        "LINKEDIN_API_KEY": "..."
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**MCP Tools**:

#### social.reply(platform, messageId, content)
- **Purpose**: Reply to social message
- **Inputs**: Platform, message ID, reply content
- **Outputs**: Reply ID, status
- **Risk**: HIGH (public, requires approval)

#### social.post(platform, content)
- **Purpose**: Create new post
- **Inputs**: Platform, content
- **Outputs**: Post ID, status
- **Risk**: HIGH (public, requires approval)

#### social.analyze(messageId)
- **Purpose**: Analyze message sentiment
- **Inputs**: Message ID
- **Outputs**: Sentiment, tone, urgency
- **Risk**: LOW (read-only)

## Approval Detection

### File Watcher

**Watches**:
- `/Pending_Approval/**/*.md` - New approval requests
- `/Approved/**/*.md` - Approved actions
- `/Rejected/**/*.md` - Rejected actions

**Detection Logic**:
```python
def detect_approval_decision(event):
    if event.type == "FILE_MOVED":
        source_folder = get_folder(event.source_path)
        dest_folder = get_folder(event.dest_path)
        
        if source_folder == "Pending_Approval":
            if dest_folder == "Approved":
                return "APPROVED"
            elif dest_folder == "Rejected":
                return "REJECTED"
    
    elif event.type == "FILE_MODIFIED":
        if get_folder(event.path) == "Pending_Approval":
            return "MODIFIED"
    
    return None

def handle_approval(request_file, decision):
    request = parse_request(request_file)
    
    if decision == "APPROVED":
        execute_action(request)
        log_success(request)
        archive_to_approved(request)
    
    elif decision == "REJECTED":
        cancel_action(request)
        log_rejection(request)
        archive_to_rejected(request)
    
    elif decision == "MODIFIED":
        re_validate_request(request)
        # Keep in Pending_Approval for re-review
```


## Approval Rule Engine

### Rule Definitions

```yaml
# /Control/approval_rules.yaml

approval_rules:
  # Payment Rules
  payments:
    - name: "Large Payment Approval"
      condition: "amount > 50"
      action: "require_approval"
      folder: "Pending_Approval/payments"
      priority: "high"
      
    - name: "Recurring Payment Auto-Approve"
      condition: "amount <= 50 AND recurring == true"
      action: "auto_approve"
      log: true
      
    - name: "Emergency Payment"
      condition: "amount > 50 AND priority == 'critical'"
      action: "require_approval"
      notify: "immediate"
      expiry_hours: 4
  
  # Email Rules
  emails:
    - name: "New Contact Approval"
      condition: "recipient NOT IN approved_contacts"
      action: "require_approval"
      folder: "Pending_Approval/contacts"
      priority: "medium"
      
    - name: "Known Contact Auto-Send"
      condition: "recipient IN approved_contacts"
      action: "auto_approve"
      log: true
      
    - name: "Reply to Existing Thread"
      condition: "is_reply == true AND original_sender IN approved_contacts"
      action: "auto_approve"
      log: true
  
  # Social Media Rules
  social:
    - name: "All Social Replies Require Approval"
      condition: "platform IN ['twitter', 'linkedin', 'facebook']"
      action: "require_approval"
      folder: "Pending_Approval/social"
      priority: "high"
      
    - name: "Negative Sentiment Priority"
      condition: "sentiment == 'negative'"
      action: "require_approval"
      priority: "critical"
      notify: "immediate"
      
    - name: "High Engagement Priority"
      condition: "engagement_score > 100"
      action: "require_approval"
      priority: "high"
      notify: "immediate"

# Approval Thresholds
thresholds:
  payment_amount: 50.00
  payment_currency: "USD"
  social_engagement_high: 100
  email_response_time_hours: 4
  
# Notification Settings
notifications:
  critical_approval:
    enabled: true
    methods: ["file", "desktop", "email"]
  
  high_priority:
    enabled: true
    methods: ["file", "desktop"]
  
  medium_priority:
    enabled: true
    methods: ["file"**: 2 (17%)  
**Average Response Time**: 1.2 hours  
**Fastest Response**: 5 minutes  
**Slowest Response**: 3.5 hours

**By Category**:
- Payments: 3 approved, 1 rejected
- Emails: 5 approved, 1 rejected
- Social: 2 approved, 0 rejected

**Financial Impact**:
- Total Approved: $2,100
- Total Rejected: $299
- Net Spend: $2,100
```

### 1. Twitter - Customer Support
- **Request ID**: social_20260215_105000
- **Platform**: Twitter
- **Original**: @customer_john complaint about bug
- **Reply**: Apologized, provided workaround
- **Requested**: 2026-02-15 10:50 AM
- **Approved**: 2026-02-15 11:05 AM (15 min)
- **Posted**: 2026-02-15 11:06 AM
- **Reply ID**: TWEET-2026-0215-001
- **Status**: ✅ Posted
- **Outcome**: Customer thanked us, issue resolved

### Rejected (0)

---

## Summary

**Total Requests**: 12  
**Approved**: 10 (83%)  
**Rejected1:00 AM (15 min)
- **Sent**: 2026-02-15 11:01 AM
- **Message ID**: MSG-2026-0215-001
- **Status**: ✅ Sent
- **Response**: Received reply, demo scheduled

### Rejected (1)

#### 1. Spam Inquiry
- **Request ID**: email_20260215_153000
- **Recipient**: suspicious@example.com (NEW)
- **Subject**: Re: Partnership Opportunity
- **Requested**: 2026-02-15 15:30 PM
- **Rejected**: 2026-02-15 15:35 PM (5 min)
- **Reason**: "Looks like spam, don't respond"
- **Status**: ❌ Not sent

## Social Media

### Approved (2)

#: $299.00 USD
- **Recipient**: MarketingTool.com
- **Purpose**: Monthly subscription
- **Requested**: 2026-02-15 14:30 PM
- **Rejected**: 2026-02-15 15:00 PM (30 min)
- **Reason**: "Not using this tool anymore, cancel subscription"
- **Status**: ❌ Cancelled

## Emails

### Approved (5)

#### 1. Sarah Johnson - Demo Request
- **Request ID**: email_20260215_104500
- **Recipient**: sarah.johnson@newclient.com (NEW)
- **Subject**: Re: Demo Request
- **Requested**: 2026-02-15 10:45 AM
- **Approved**: 2026-02-15 1 ID**: PAY-2026-0215-001
- **Status**: ✅ Completed

#### 2. Contractor Fee - $850
- **Request ID**: pay_20260215_110000
- **Amount**: $850.00 USD
- **Recipient**: John Smith (Contractor)
- **Purpose**: February consulting services
- **Requested**: 2026-02-15 11:00 AM
- **Approved**: 2026-02-15 14:30 PM (3.5 hours)
- **Executed**: 2026-02-15 14:31 PM
- **Payment ID**: PAY-2026-0215-002
- **Status**: ✅ Completed

### Rejected (1)

#### 1. Marketing Tool - $299
- **Request ID**: pay_20260215_143000
- **Amount**tetime.now().isoformat()
        }
```

## Audit and Compliance

### Audit Log Format

```markdown
---
type: audit_log
date: 2026-02-15
---

# Audit Log - February 15, 2026

## Payments

### Approved (3)

#### 1. Acme Software License - $1,250
- **Request ID**: pay_20260215_103000
- **Amount**: $1,250.00 USD
- **Recipient**: Acme Software Inc
- **Purpose**: Annual software license
- **Requested**: 2026-02-15 10:30 AM
- **Approved**: 2026-02-15 11:15 AM (45 min)
- **Executed**: 2026-02-15 11:16 AM
- **Paymentest.data["original_message_id"]
        content = request.data["reply_content"]
        
        # Post reply
        reply_id = self.mcp.call(
            "social-media",
            "social.reply",
            {
                "platform": platform,
                "message_id": message_id,
                "content": content,
                "reference": request.id
            }
        )
        
        return {
            "reply_id": reply_id,
            "platform": platform,
            "posted_at": da "subject": subject,
                "body": body,
                "reference": request.id
            }
        )
        
        # Add to approved contacts
        self.add_approved_contact(to)
        
        return {
            "message_id": message_id,
            "sent_at": datetime.now().isoformat(),
            "recipient": to
        }
    
    def execute_social(self, request):
        """Post social reply via MCP"""
        
        platform = request.data["platform"]
        message_id = requ     return {
            "payment_id": payment_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    
    def execute_email(self, request):
        """Send email via MCP"""
        
        to = request.data["recipient"]
        subject = request.data["subject"]
        body = request.data["body"]
        
        # Send email
        message_id = self.mcp.call(
            "gmail-action",
            "gmail.send",
            {
                "to": to,
                 
        # Create payment
        payment_id = self.mcp.call(
            "payment-processor",
            "payment.create",
            {
                "amount": amount,
                "recipient": recipient,
                "purpose": purpose,
                "reference": request.id
            }
        )
        
        # Verify payment created
        status = self.mcp.call(
            "payment-processor",
            "payment.status",
            {"payment_id": payment_id}
        )
        
   
            return result
            
        except Exception as e:
            # Log failure
            self.logger.log_error(request, e)
            
            # Move to Needs_Action for review
            self.move_to_needs_action(request, str(e))
            
            raise
    
    def execute_payment(self, request):
        """Execute payment via MCP"""
        
        amount = request.data["amount"]
        recipient = request.data["recipient"]
        purpose = request.data["purpose"]
      elif action_type == "email_approval":
                result = self.execute_email(request)
            
            elif action_type == "social_approval":
                result = self.execute_social(request)
            
            else:
                raise ValueError(f"Unknown action type: {action_type}")
            
            # Log success
            self.logger.log_success(request, result)
            
            # Archive to Approved
            self.archive_approved(request, result)
            ecutor

```python
class ActionExecutor:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.logger = Logger()
    
    def execute_approved_action(self, request):
        """Execute action after approval"""
        
        try:
            # Parse request
            action_type = request.metadata["type"]
            
            # Execute based on type
            if action_type == "payment_approval":
                result = self.execute_payment(request)
            
            ient"),
            "platform": action.get("platform"),
            "sentiment": action.get("sentiment"),
            "engagement_score": action.get("engagement_score", 0),
            "is_reply": action.get("is_reply", False),
            "recurring": action.get("recurring", False),
            "priority": action.get("priority", "medium"),
            "approved_contacts": self.get_approved_contacts()
        }
        
        return eval_condition(condition, context)
```

## Execution Engine

### Action Ex     return ApprovalDecision(
            required=True,
            folder="Pending_Approval/other",
            priority="medium"
        )
    
    def evaluate_condition(self, condition, action):
        """Evaluate rule condition against action"""
        
        # Parse condition (e.g., "amount > 50")
        # Evaluate against action properties
        # Return True if condition matches
        
        context = {
            "amount": action.get("amount", 0),
            "recipient": action.get("recippe(action.type)
        
        for rule in rules:
            if self.evaluate_condition(rule.condition, action):
                return ApprovalDecision(
                    required=rule.action == "require_approval",
                    folder=rule.folder,
                    priority=rule.priority,
                    notify=rule.get("notify", "standard"),
                    expiry_hours=rule.get("expiry_hours", 72)
                )
        
        # Default: require approval for unknown actions
   ]

# Auto-Approval Settings
auto_approval:
  enabled: true
  max_per_day: 50
  require_log: true
  
# Expiry Settings
expiry:
  default_hours: 72
  critical_hours: 4
  payment_hours: 48
```

### Rule Evaluation

```python
class ApprovalRuleEngine:
    def __init__(self, rules_config):
        self.rules = load_rules(rules_config)
    
    def evaluate(self, action):
        """Evaluate if action requires approval"""
        
        # Get applicable rules for action type
        rules = self.get_rules_for_ty