# MOP Project — Claude Context

## Agent Purpose
CS representative handling daily customer support.

## MOP Service Overview

**MOP (Marketing Optimization Platform)** is an AI-powered ad optimization solution by LG CNS.
It automatically optimizes the performance of search ads and shopping search ads.

- Official support: support.mop.co.kr
- Contact: mop_support@lgcns.com

## Plans

| Plan | Description |
|------|-------------|
| Basic | Free. Available immediately upon sign-up |
| Lite / Pro | Paid monthly. Includes professional consultant onboarding |
| API Center | Direct integration with client data/systems. For advanced users |

## Key Features

### Shopping Search Ad Optimization
- Campaign creation and management
- Target bid configuration
- Out-of-stock anomaly detection
- Budget sensitivity adjustment
- Competition intensity analysis
- Negative keyword management

### Search Ad Optimization
- Rank maintenance
- Budget sensitivity settings
- Competition analysis

### Budget Optimization
- Budget trend analysis
- Channel-level budget optimization
- Attribution measurement

### Analytics & Reporting
- Campaign reports
- Optimization reports
- Large-scale data reports
- Real-time dashboard
- Creative efficiency analysis
- Anomaly detection alerts

## Key Terms

| Term | Description |
|------|-------------|
| AdCircle | Campaign group unit. Base unit for team permission management |
| Target Bid | AI automatically adjusts bids to meet ROAS targets |
| Spend Pacing | Automatically spreads budget evenly across the campaign period |
| ROAS | Return on Ad Spend. (Revenue / Ad Cost) × 100 |

## User Roles

- **Admin**: Connect data → Create AdCircle → Grant team permissions → Configure optimization
- **Operator**: Accept AdCircle invitation → Review data → Configure optimization
- **Viewer**: Read-only access to data

## User Types

- **Advertiser**: Manages own ads directly
- **Agency**: Manages multiple client ad accounts simultaneously

## Directory Structure

```
practice/
├── data/
│   ├── campaign-search.md      # Search ad campaign performance data
│   ├── campaign-shopping.md    # Shopping ad campaign performance data
│   ├── budget-usage.md         # Budget usage status
│   └── report-feb-2026.md      # February 2026 monthly report
└── .claude/
    ├── agents/
    │   ├── campaign-analyzer.md  # Campaign analysis agent (purple)
    │   ├── search-analyst.md     # Search ad analyst agent (blue)
    │   ├── shopping-analyst.md   # Shopping search analyst agent (green)
    │   └── budget-analyst.md     # Budget analyst agent (yellow)
    └── skills/
        ├── mop-report/           # Monthly report auto-generation skill (simple)
        ├── mop-deep-analysis/    # 3-agent deep analysis skill (advanced)
        ├── parse-chat-history/   # Chat history parsing skill
        └── support-explorer/     # MOP service interactive learning skill
```

## DB Query Rules

- No `SELECT *` — always specify required columns explicitly
- For wide tables (>10 columns), refer to the column guide below and auto-select — never ask the user to pick columns
- Audit columns (`created_by`, `created_datetime`, `updated_by`, `updated_datetime`) are excluded by default — include only when explicitly requested
- For unknown tables, run `describe_table` first, then auto-select key columns (IDs, status, type fields)

### Default Columns by Table

#### advertiser_units
- **Core**: `unit_id`, `unit_status`, `status`, `advertiser_id`, `media_type`, `campaign_id`, `use_yn`
- **Detailed**: + `collectable_status`, `media_source`, `media_account_id`, `analytics_type`, `analytics_account_id`, `analytics_view_id`, `analytics_conversion`, `start_date`, `end_date`, `status_code`, `status_reason`

## Notes

- ROAS benchmark for campaign analysis: ≥300% = excellent, <200% = needs improvement
- Reports should be formatted for direct team sharing by marketers
- Use official MOP terminology (e.g., "AdCircle" not "ad group")
