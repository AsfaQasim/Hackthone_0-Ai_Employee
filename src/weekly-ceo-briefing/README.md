# Weekly CEO Briefing System

A data analysis and reporting tool that processes business data from multiple sources to generate actionable insights for executive decision-making.

## Architecture

The system follows a modular pipeline architecture:

```
Data Ingestion → Parsing/Validation → Analysis → Report Generation
```

### Components

1. **Data Ingestion Module** - Loads raw data from file system sources
2. **Data Parser and Validator** - Parses and validates data integrity
3. **Revenue Analyzer** - Analyzes financial data for revenue insights
4. **Bottleneck Detector** - Identifies operational constraints
5. **Cost Optimizer** - Identifies cost reduction opportunities
6. **Action Item Generator** - Creates prioritized action items
7. **Report Generator** - Formats analysis into readable briefing report

## Data Models

All type definitions are in `types.ts`:

- **FinancialRecord** - Revenue and expense data
- **Task** - Completed work with duration tracking
- **BusinessGoals** - Strategic objectives and KPIs
- **RevenueSummary** - Financial performance analysis
- **Bottleneck** - Operational constraints
- **Opportunity** - Cost optimization opportunities
- **ActionItem** - Prioritized tasks for next week
- **BriefingReport** - Complete output document

## Testing

The system uses a dual testing approach:

- **Unit Tests** - Specific examples and edge cases
- **Property-Based Tests** - Universal correctness properties

Test generators are available in `tests/weekly-ceo-briefing/generators/` for creating random test data.

## Development

```bash
# Run all tests
npm test

# Run only unit tests
npm run test:unit

# Run only property tests
npm run test:property

# Build
npm run build
```
