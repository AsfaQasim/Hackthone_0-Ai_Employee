/**
 * Core type definitions for the Weekly CEO Briefing system
 */

// ============================================================================
// Core Data Models
// ============================================================================

/**
 * Financial record representing revenue and expenses for a specific date
 */
export interface FinancialRecord {
  date: Date;
  category: string;
  revenue: number;
  expenses: number;
  description: string;
}

/**
 * Task representing completed work with duration and blocker information
 */
export interface Task {
  id: string;
  title: string;
  completedDate: Date;
  expectedDuration: number; // in hours
  actualDuration: number; // in hours
  blockers: string[];
  relatedGoals: string[];
}

/**
 * Business goal with target metrics and progress tracking
 */
export interface Goal {
  id: string;
  title: string;
  targetMetric: number;
  currentMetric: number;
  deadline: Date;
}

/**
 * Budget allocation for a specific category
 */
export interface Budget {
  category: string;
  amount: number;
  period: string; // e.g., "weekly", "monthly"
}

/**
 * Configurable thresholds for analysis
 */
export interface Thresholds {
  delayThreshold: number; // percentage, e.g., 50 means 50% over expected
  budgetOverrunThreshold: number; // percentage
  expenseIncreaseThreshold: number; // percentage
}

/**
 * Complete business goals configuration
 */
export interface BusinessGoals {
  goals: Goal[];
  budgets: Budget[];
  thresholds: Thresholds;
}

// ============================================================================
// Analysis Results
// ============================================================================

/**
 * Revenue breakdown by category
 */
export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
}

/**
 * Trend data for visualization
 */
export interface TrendData {
  weeks: Date[];
  values: number[];
}

/**
 * Complete revenue analysis summary
 */
export interface RevenueSummary {
  totalRevenue: number;
  previousWeekRevenue: number | null;
  percentageChange: number | null;
  categoryBreakdown: CategoryBreakdown[];
  trend: TrendData;
}

/**
 * Identified operational bottleneck
 */
export interface Bottleneck {
  type: 'delayed_task' | 'recurring_issue' | 'goal_progress';
  title: string;
  description: string;
  impactScore: number;
  affectedGoals: string[];
}

/**
 * Ranked bottleneck with priority
 */
export interface RankedBottleneck extends Bottleneck {
  rank: number;
}

/**
 * Complete bottleneck analysis report
 */
export interface BottleneckReport {
  bottlenecks: RankedBottleneck[];
  summary: string;
}

/**
 * Cost optimization opportunity
 */
export interface Opportunity {
  type: 'budget_overrun' | 'increasing_expense';
  category: string;
  currentAmount: number;
  targetAmount: number;
  potentialSavings: number;
  suggestion: string;
}

/**
 * Ranked opportunity with priority
 */
export interface RankedOpportunity extends Opportunity {
  rank: number;
}

/**
 * Cost-to-revenue ratio for a category
 */
export interface CostRatio {
  category: string;
  expenses: number;
  revenue: number;
  ratio: number;
}

/**
 * Complete cost optimization report
 */
export interface CostReport {
  opportunities: RankedOpportunity[];
  costRatios: CostRatio[];
  summary: string;
}

/**
 * Action item for next week
 */
export interface ActionItem {
  title: string;
  description: string;
  priority: number;
  source: 'bottleneck' | 'cost' | 'goal';
  estimatedImpact: string;
}

/**
 * Prioritized action item
 */
export interface PrioritizedActionItem extends ActionItem {
  rank: number;
}

/**
 * Goal progress tracking
 */
export interface GoalProgress {
  goalId: string;
  goalTitle: string;
  expectedProgress: number;
  actualProgress: number;
  progressPercentage: number;
}

// ============================================================================
// Report Structure
// ============================================================================

/**
 * Complete briefing report
 */
export interface BriefingReport {
  timestamp: Date;
  revenueSummary: RevenueSummary;
  bottlenecks: BottleneckReport;
  costOptimization: CostReport;
  nextWeekActions: PrioritizedActionItem[];
}

/**
 * All report sections for generation
 */
export interface ReportSections {
  revenueSummary: RevenueSummary;
  bottleneckReport: BottleneckReport;
  costReport: CostReport;
  actionItems: PrioritizedActionItem[];
}

// ============================================================================
// Raw Data Types (before parsing)
// ============================================================================

/**
 * Raw financial data before parsing
 */
export interface RawFinancialData {
  date: string;
  category: string;
  revenue: string | number;
  expenses: string | number;
  description: string;
}

/**
 * Raw task data before parsing
 */
export interface RawTask {
  id: string;
  title: string;
  completedDate: string;
  expectedDuration: string | number;
  actualDuration: string | number;
  blockers: string[];
  relatedGoals: string[];
}

// ============================================================================
// Validation and Error Handling
// ============================================================================

/**
 * Validation result for data records
 */
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Warning message for non-critical issues
 */
export interface Warning {
  type: 'FILE_READ_ERROR' | 'INVALID_DATA' | 'MISSING_THRESHOLD';
  message: string;
  context: Record<string, unknown>;
}

/**
 * Error response for critical failures
 */
export interface ErrorResponse {
  success: false;
  error: {
    type: 'MISSING_FOLDER' | 'INVALID_CONFIG' | 'WRITE_FAILURE';
    message: string;
    details: Record<string, unknown>;
  };
  warnings: Warning[];
}

/**
 * Success response with optional warnings
 */
export interface SuccessResponse<T> {
  success: true;
  data: T;
  warnings: Warning[];
}

/**
 * Combined response type
 */
export type Response<T> = SuccessResponse<T> | ErrorResponse;

// ============================================================================
// Percentage Change
// ============================================================================

/**
 * Percentage change calculation result
 */
export interface PercentageChange {
  current: number;
  previous: number;
  change: number;
  percentage: number;
}
