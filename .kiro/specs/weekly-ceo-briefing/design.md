# Design Document: Weekly CEO Briefing

## Overview

The Weekly CEO Briefing system is a data analysis and reporting tool that processes business data from multiple sources to generate actionable insights for executive decision-making. The system follows a pipeline architecture: data ingestion → analysis → insight generation → report formatting.

The system reads from three primary sources:
1. Accounting folder containing financial data (revenue, expenses)
2. Done folder containing completed tasks and their metadata
3. Business goals configuration defining strategic objectives and KPIs

The output is a structured briefing report with four key sections:
1. Revenue Summary - Financial performance analysis
2. Bottlenecks - Operational constraints identification
3. Cost Optimization - Expense reduction opportunities
4. Next Week Actions - Prioritized action items

## Architecture

The system follows a modular pipeline architecture with clear separation of concerns:

```
┌─────────────────┐
│  Data Ingestion │
│     Module      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Data Parser   │
│    & Validator  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Analysis     │
│     Engine      │
├─────────────────┤
│ • Revenue       │
│ • Bottlenecks   │
│ • Cost Opt      │
│ • Actions       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Report      │
│   Generator     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Briefing Report │
└─────────────────┘
```

### Key Design Decisions

1. **Pipeline Architecture**: Sequential processing ensures data flows through validation before analysis
2. **Modular Analyzers**: Each analysis type (revenue, bottlenecks, costs, actions) is independent
3. **Configuration-Driven**: Business goals and thresholds are externalized for flexibility
4. **Fail-Safe Processing**: Individual file failures don't halt the entire pipeline
5. **Structured Output**: Report uses consistent formatting for easy consumption

## Components and Interfaces

### 1. Data Ingestion Module

**Responsibility**: Load raw data from file system sources

**Interface**:
```
class DataIngestion:
    function ingestAccountingData(folderPath: string) -> RawFinancialData[]
    function ingestCompletedTasks(folderPath: string) -> RawTask[]
    function loadBusinessGoals(configPath: string) -> BusinessGoals
```

**Behavior**:
- Reads all files from specified folders
- Returns raw data structures without validation
- Logs errors for inaccessible files but continues processing
- Throws error only if required folders are completely missing

### 2. Data Parser and Validator

**Responsibility**: Parse raw data and validate integrity

**Interface**:
```
class DataParser:
    function parseFinancialData(raw: RawFinancialData[]) -> FinancialRecord[]
    function parseTaskData(raw: RawTask[]) -> Task[]
    function validateFinancialRecord(record: FinancialRecord) -> ValidationResult
    function validateTask(task: Task) -> ValidationResult
```

**Validation Rules**:
- Revenue values must be non-negative numbers
- Expense values must be non-negative numbers
- Dates must be parseable to ISO format
- Invalid records are logged and excluded from analysis

### 3. Revenue Analyzer

**Responsibility**: Analyze financial data to generate revenue insights

**Interface**:
```
class RevenueAnalyzer:
    function calculateWeeklyRevenue(records: FinancialRecord[]) -> number
    function calculateRevenueChange(current: number, previous: number) -> PercentageChange
    function breakdownByCategory(records: FinancialRecord[]) -> CategoryBreakdown[]
    function generateRevenueTrend(records: FinancialRecord[], weeks: number) -> TrendData
    function generateRevenueSummary(records: FinancialRecord[]) -> RevenueSummary
```

**Analysis Logic**:
- Aggregates revenue from all financial records for the current week
- Compares to previous week if historical data exists
- Calculates percentage change: `((current - previous) / previous) * 100`
- Groups revenue by category if category field exists
- Generates 4-week trend line for visualization

### 4. Bottleneck Detector

**Responsibility**: Identify operational constraints from task and goal data

**Interface**:
```
class BottleneckDetector:
    function detectDelayedTasks(tasks: Task[], threshold: Duration) -> Bottleneck[]
    function detectRecurringIssues(tasks: Task[]) -> Bottleneck[]
    function detectGoalProgress(tasks: Task[], goals: BusinessGoals) -> Bottleneck[]
    function rankBottlenecks(bottlenecks: Bottleneck[]) -> RankedBottleneck[]
    function generateBottleneckReport(tasks: Task[], goals: BusinessGoals) -> BottleneckReport
```

**Detection Logic**:
- **Delayed Tasks**: Tasks with actual duration > expected duration by threshold (default: 50%)
- **Recurring Issues**: Tasks with similar blocker descriptions appearing 3+ times
- **Goal Progress**: Goals with completion < 25% of expected progress for the week
- **Ranking**: Sort by impact score = (affected_goals_count * 10) + (delay_days * 2)

### 5. Cost Optimizer

**Responsibility**: Identify cost reduction opportunities

**Interface**:
```
class CostOptimizer:
    function detectBudgetOverruns(records: FinancialRecord[], budget: Budget) -> Opportunity[]
    function detectIncreasingExpenses(records: FinancialRecord[]) -> Opportunity[]
    function calculateCostRatios(records: FinancialRecord[]) -> CostRatio[]
    function rankOpportunities(opportunities: Opportunity[]) -> RankedOpportunity[]
    function generateCostReport(records: FinancialRecord[], budget: Budget) -> CostReport
```

**Analysis Logic**:
- **Budget Overruns**: Expense categories exceeding budget by 10%+
- **Increasing Expenses**: Categories with week-over-week increase > 15%
- **Cost Ratios**: Calculate expense/revenue ratio per category
- **Ranking**: Sort by potential_savings = overrun_amount or increase_amount
- **Suggestions**: Generate specific recommendations based on patterns

### 6. Action Item Generator

**Responsibility**: Create prioritized action items from analysis results

**Interface**:
```
class ActionItemGenerator:
    function generateFromBottlenecks(bottlenecks: RankedBottleneck[]) -> ActionItem[]
    function generateFromCostOpportunities(opportunities: RankedOpportunity[]) -> ActionItem[]
    function generateFromGoalProgress(goals: BusinessGoals, progress: GoalProgress[]) -> ActionItem[]
    function prioritizeActions(actions: ActionItem[]) -> PrioritizedActionItem[]
    function limitActions(actions: PrioritizedActionItem[], max: number) -> PrioritizedActionItem[]
```

**Generation Logic**:
- Each bottleneck generates 1 action item to address the constraint
- Each cost opportunity generates 1 action item to pursue savings
- Each lagging goal generates 1 action item to accelerate progress
- Priority score = (business_impact * 3) + (urgency * 2) + (effort_inverse * 1)
- Limit to top 10 actions to maintain focus

### 7. Report Generator

**Responsibility**: Format analysis results into readable briefing report

**Interface**:
```
class ReportGenerator:
    function formatRevenueSummary(summary: RevenueSummary) -> string
    function formatBottleneckReport(report: BottleneckReport) -> string
    function formatCostReport(report: CostReport) -> string
    function formatActionItems(actions: PrioritizedActionItem[]) -> string
    function generateBriefingReport(allSections: ReportSections) -> string
```

**Formatting Rules**:
- Use markdown formatting for structure
- Include section headers (##) for each major section
- Add timestamp at report header
- Use tables for numerical data
- Use bullet points for action items
- Include summary statistics at the top of each section

## Data Models

### FinancialRecord
```
{
    date: Date,
    category: string,
    revenue: number,
    expenses: number,
    description: string
}
```

### Task
```
{
    id: string,
    title: string,
    completedDate: Date,
    expectedDuration: Duration,
    actualDuration: Duration,
    blockers: string[],
    relatedGoals: string[]
}
```

### BusinessGoals
```
{
    goals: Goal[],
    budgets: Budget[],
    thresholds: Thresholds
}

Goal: {
    id: string,
    title: string,
    targetMetric: number,
    currentMetric: number,
    deadline: Date
}

Budget: {
    category: string,
    amount: number,
    period: string
}

Thresholds: {
    delayThreshold: number,
    budgetOverrunThreshold: number,
    expenseIncreaseThreshold: number
}
```

### RevenueSummary
```
{
    totalRevenue: number,
    previousWeekRevenue: number,
    percentageChange: number,
    categoryBreakdown: CategoryBreakdown[],
    trend: TrendData
}
```

### Bottleneck
```
{
    type: "delayed_task" | "recurring_issue" | "goal_progress",
    title: string,
    description: string,
    impactScore: number,
    affectedGoals: string[]
}
```

### Opportunity
```
{
    type: "budget_overrun" | "increasing_expense",
    category: string,
    currentAmount: number,
    targetAmount: number,
    potentialSavings: number,
    suggestion: string
}
```

### ActionItem
```
{
    title: string,
    description: string,
    priority: number,
    source: "bottleneck" | "cost" | "goal",
    estimatedImpact: string
}
```

### BriefingReport
```
{
    timestamp: Date,
    revenueSummary: RevenueSummary,
    bottlenecks: BottleneckReport,
    costOptimization: CostReport,
    nextWeekActions: PrioritizedActionItem[]
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Complete File Ingestion
*For any* folder containing files, when the system reads from that folder, all accessible files should be included in the returned data set.
**Validates: Requirements 1.1, 1.2**

### Property 2: Configuration Loading
*For any* valid Business Goals configuration file, the system should successfully load and parse all goals, budgets, and thresholds.
**Validates: Requirements 1.3, 8.1**

### Property 3: Missing Folder Error Reporting
*For any* required folder that does not exist, the system should return an error message that specifically identifies which folder is missing.
**Validates: Requirements 1.4**

### Property 4: Graceful File Failure Handling
*For any* set of files where some are unreadable, the system should process all readable files and log errors for unreadable ones without halting execution.
**Validates: Requirements 1.5**

### Property 5: Revenue Calculation Accuracy
*For any* set of financial records, the calculated total weekly revenue should equal the sum of all revenue values in those records.
**Validates: Requirements 2.1**

### Property 6: Revenue Comparison
*For any* two consecutive weeks with financial data, the system should calculate and report the difference between current and previous week revenue.
**Validates: Requirements 2.2**

### Property 7: Percentage Change Formula
*For any* two revenue values (current and previous), the calculated percentage change should equal `((current - previous) / previous) * 100`.
**Validates: Requirements 2.3**

### Property 8: Revenue Category Breakdown
*For any* set of financial records with category labels, the sum of all category breakdowns should equal the total revenue.
**Validates: Requirements 2.4**

### Property 9: Trend Data Inclusion
*For any* revenue summary generated with at least 4 weeks of historical data, the output should include trend data covering those 4 weeks.
**Validates: Requirements 2.5**

### Property 10: Delayed Task Detection
*For any* task where actual duration exceeds expected duration by the threshold percentage, that task should be identified as a bottleneck.
**Validates: Requirements 3.1**

### Property 11: Recurring Issue Detection
*For any* set of tasks where the same blocker description appears 3 or more times, those tasks should be identified as a recurring issue bottleneck.
**Validates: Requirements 3.2**

### Property 12: Goal Progress Detection
*For any* business goal where current progress is less than 25% of expected progress, that goal should be identified as a bottleneck.
**Validates: Requirements 3.3**

### Property 13: Bottleneck Ranking
*For any* set of bottlenecks, they should be ordered by impact score in descending order (highest impact first).
**Validates: Requirements 3.4**

### Property 14: Budget Overrun Detection
*For any* expense category where spending exceeds the budget by more than the threshold percentage, that category should be identified as a cost optimization opportunity.
**Validates: Requirements 4.1**

### Property 15: Expense Increase Detection
*For any* expense category where week-over-week spending increases by more than the threshold percentage, that category should be identified as a cost optimization opportunity.
**Validates: Requirements 4.2**

### Property 16: Cost-to-Revenue Ratio Calculation
*For any* expense category with associated revenue, the calculated ratio should equal `expenses / revenue` for that category.
**Validates: Requirements 4.3**

### Property 17: Cost Optimization Suggestions
*For any* detected cost optimization opportunity, the system should generate at least one specific suggestion for addressing it.
**Validates: Requirements 4.4**

### Property 18: Opportunity Prioritization
*For any* set of cost optimization opportunities, they should be ordered by potential savings in descending order (highest savings first).
**Validates: Requirements 4.5**

### Property 19: Action Generation from Bottlenecks
*For any* identified bottleneck, the system should generate at least one action item to address it.
**Validates: Requirements 5.1**

### Property 20: Action Generation from Cost Opportunities
*For any* identified cost optimization opportunity, the system should generate at least one action item to pursue it.
**Validates: Requirements 5.2**

### Property 21: Action Generation from Goal Progress
*For any* business goal with insufficient progress, the system should generate at least one action item to accelerate progress.
**Validates: Requirements 5.3**

### Property 22: Action Item Prioritization
*For any* set of action items, they should be ordered by priority score in descending order (highest priority first).
**Validates: Requirements 5.4**

### Property 23: Action Item Limiting
*For any* set of action items exceeding 10 items, the final output should contain exactly the top 10 highest-priority items.
**Validates: Requirements 5.5**

### Property 24: Report Structure Completeness
*For any* generated briefing report, it should contain all four required sections: Revenue Summary, Bottlenecks, Cost Optimization, and Next Week Actions.
**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

### Property 25: Report Timestamp
*For any* generated briefing report, it should include a timestamp indicating when the report was generated.
**Validates: Requirements 6.6**

### Property 26: Financial Value Validation
*For any* financial record, if it contains negative revenue or expense values, the validation should fail and the record should be excluded from analysis.
**Validates: Requirements 7.1, 7.2**

### Property 27: Date Format Validation
*For any* date string in a recognized format (ISO 8601, MM/DD/YYYY, etc.), the system should successfully parse it; for any unrecognized format, validation should fail.
**Validates: Requirements 7.3**

### Property 28: Invalid Data Logging
*For any* invalid data record detected during processing, the system should log a warning message containing details about the validation failure.
**Validates: Requirements 7.4**

### Property 29: Invalid Data Exclusion
*For any* invalid data record, it should not appear in the analysis results and the report should note the exclusion.
**Validates: Requirements 7.5**

### Property 30: Custom Threshold Application
*For any* custom threshold defined in the configuration, the system should use that threshold instead of the default value in all relevant analyses.
**Validates: Requirements 8.2, 8.3**

### Property 31: Default Threshold Fallback
*For any* threshold not specified in the configuration file, or when the configuration file is missing, the system should use the predefined default value.
**Validates: Requirements 8.4**

### Property 32: Configuration Validation
*For any* configuration file with invalid structure or values, the system should return an error message describing the specific validation failure.
**Validates: Requirements 8.5**

## Error Handling

The system implements a layered error handling strategy:

### Critical Errors (Halt Execution)
- Missing required folders (Accounting, Done)
- Invalid configuration file structure
- Unable to write output report

These errors prevent meaningful analysis and should fail fast with clear error messages.

### Non-Critical Errors (Log and Continue)
- Individual file read failures
- Invalid data records
- Missing optional configuration values

These errors are logged with details but don't prevent the system from generating a partial report.

### Error Response Format
```
{
    success: boolean,
    error?: {
        type: "MISSING_FOLDER" | "INVALID_CONFIG" | "WRITE_FAILURE",
        message: string,
        details: object
    },
    warnings: Warning[]
}

Warning: {
    type: "FILE_READ_ERROR" | "INVALID_DATA" | "MISSING_THRESHOLD",
    message: string,
    context: object
}
```

### Validation Error Handling
- Invalid financial records are excluded from analysis
- Exclusions are counted and reported in the briefing
- If >50% of records are invalid, generate a warning in the report
- If 100% of records are invalid, treat as critical error

## Testing Strategy

The Weekly CEO Briefing system will use a dual testing approach combining unit tests for specific scenarios and property-based tests for comprehensive validation.

### Unit Testing Approach

Unit tests will focus on:
- **Specific examples**: Verify correct behavior with known input/output pairs
- **Edge cases**: Empty folders, single record, missing historical data
- **Error conditions**: Invalid file formats, missing folders, malformed configuration
- **Integration points**: Data flow between components

Example unit tests:
- Revenue calculation with known financial records
- Bottleneck detection with specific delayed tasks
- Report generation with sample data
- Configuration loading with various file formats

### Property-Based Testing Approach

Property-based tests will verify universal correctness properties across randomized inputs. Each test will run a minimum of 100 iterations to ensure comprehensive coverage.

**Property Test Configuration**:
- Testing library: fast-check (JavaScript/TypeScript) or Hypothesis (Python)
- Minimum iterations: 100 per property
- Each test tagged with: `Feature: weekly-ceo-briefing, Property N: [property description]`

**Property Test Coverage**:
- All 32 correctness properties defined above
- Each property maps to specific requirements
- Properties cover: calculations, rankings, validations, data flow, error handling

**Generator Strategy**:
- Financial records: Random dates, categories, positive/negative values
- Tasks: Random durations, blockers, completion dates
- Business goals: Random targets, deadlines, progress values
- Configurations: Valid and invalid structures, missing fields

**Example Property Test Structure**:
```javascript
// Feature: weekly-ceo-briefing, Property 5: Revenue Calculation Accuracy
test('total revenue equals sum of all record revenues', () => {
  fc.assert(
    fc.property(
      fc.array(financialRecordGenerator()),
      (records) => {
        const calculated = calculateWeeklyRevenue(records);
        const expected = records.reduce((sum, r) => sum + r.revenue, 0);
        return Math.abs(calculated - expected) < 0.01; // floating point tolerance
      }
    ),
    { numRuns: 100 }
  );
});
```

### Test Organization

```
tests/
├── unit/
│   ├── data-ingestion.test.ts
│   ├── revenue-analyzer.test.ts
│   ├── bottleneck-detector.test.ts
│   ├── cost-optimizer.test.ts
│   ├── action-generator.test.ts
│   └── report-generator.test.ts
├── property/
│   ├── revenue-properties.test.ts
│   ├── bottleneck-properties.test.ts
│   ├── cost-properties.test.ts
│   ├── action-properties.test.ts
│   ├── validation-properties.test.ts
│   └── integration-properties.test.ts
└── generators/
    ├── financial-record.generator.ts
    ├── task.generator.ts
    ├── business-goals.generator.ts
    └── config.generator.ts
```

### Testing Priorities

1. **Critical Path**: Data ingestion → validation → revenue calculation → report generation
2. **Business Logic**: Bottleneck detection, cost optimization, action prioritization
3. **Error Handling**: Invalid data, missing files, configuration errors
4. **Edge Cases**: Empty data sets, single records, extreme values

### Continuous Validation

- All tests run on every code change
- Property tests catch regression across wide input space
- Unit tests provide fast feedback on specific scenarios
- Combined approach ensures both correctness and reliability
