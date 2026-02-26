# Email and Payment Action HITL - Quick Reference

## Three Approval Rules

1. **Payments > $50** → Requires approval
2. **New email contacts** → Requires approval  
3. **All social replies** → Requires approval

## Three-Folder Workflow

```
/Pending_Approval/  →  Human reviews  →  Move to /Approved/ or /Rejected/
     ↓
  [Approved] → AI executes action → Archives to /Approved/YYYY-MM/
     ↓
  [Rejected] → AI cancels action → Archives to /Rejected/YYYY-MM/
```

## How to Approve

1. **Review** request in `/Pending_Approval/[type]/`
2. **Decide**:
   - ✅ Approve: Move file to `/Approved/[type]/`
   - ❌ Reject: Move file to `/Rejected/[type]/` (add reason)
   - ✏️ Modify: Edit file, keep in `/Pending_Approval/[type]/`
3. **AI executes** approved actions automatically
4. **AI archives** to dated folders for audit trail

## Folder Structure

```
/Pending_Approval/
├── payments/     # Payments > $50
├── contacts/     # New email contacts
└── social/       # Social media replies

/Approved/
└── 2026-02/
    ├── payments/
    ├── contacts/
    └── social/

/Rejected/
└── 2026-02/
    ├── payments/
    ├── contacts/
    └── social/
```

## Request Types

### Payment Request
- Amount, recipient, purpose
- Budget impact analysis
- Invoice verification
- Risk assessment
- Supporting documents

### Email Request
- Draft email content
- Recipient verification
- Context and reasoning
- Risk assessment
- Expected outcome

### Social Reply Request
- Original message
- Draft reply
- Sentiment analysis
- Risk assessment
- Alternative responses

## MCP Servers

- **gmail-action**: Send/reply to emails
- **payment-processor**: Process payments
- **social-media**: Post social replies

## Audit Trail

All actions logged in:
- `/Logs/audit_YYYYMMDD.md` - Daily audit log
- `/Approved/YYYY-MM/` - Approved actions archive
- `/Rejected/YYYY-MM/` - Rejected actions archive

## Key Features

✅ Simple file-based approval (no complex UI)  
✅ Complete audit trail for compliance  
✅ Automatic execution after approval  
✅ Edit-before-approve capability  
✅ Organized by type and date  
✅ Full context for informed decisions  

---

**See full spec**: `Specs/MCP_Email_Action.md`
