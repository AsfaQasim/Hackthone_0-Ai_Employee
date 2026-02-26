/**
 * Property-based test generators for Weekly CEO Briefing
 * 
 * These generators create random test data for property-based testing
 * using fast-check library.
 */

import * as fc from 'fast-check';
import type {
  FinancialRecord,
  Task,
  Goal,
  Budget,
  Thresholds,
  BusinessGoals,
  RawFinancialData,
  RawTask,
} from '../../../src/weekly-ceo-briefing/types.js';

// ============================================================================
// Date Generators
// ============================================================================

/**
 * Generate a random date within a reasonable range
 */
export const dateGenerator = (): fc.Arbitrary<Date> =>
  fc.date({
    min: new Date('2020-01-01'),
    max: new Date('2030-12-31'),
  });

/**
 * Generate a date string in ISO format
 */
export const dateStringGenerator = (): fc.Arbitrary<string> =>
  dateGenerator().map(d => d.toISOString());

// ============================================================================
// Financial Data Generators
// ============================================================================

/**
 * Generate a valid financial record
 */
export const financialRecordGenerator = (): fc.Arbitrary<FinancialRecord> =>
  fc.record({
    date: dateGenerator(),
    category: fc.oneof(
      fc.constant('Sales'),
      fc.constant('Services'),
      fc.constant('Products'),
      fc.constant('Consulting'),
      fc.constant('Other')
    ),
    revenue: fc.double({ min: 0, max: 1000000, noNaN: true }),
    expenses: fc.double({ min: 0, max: 1000000, noNaN: true }),
    description: fc.string({ minLength: 5, maxLength: 100 }),
  });

/**
 * Generate raw financial data (before parsing)
 */
export const rawFinancialDataGenerator = (): fc.Arbitrary<RawFinancialData> =>
  fc.record({
    date: dateStringGenerator(),
    category: fc.string({ minLength: 1, maxLength: 50 }),
    revenue: fc.oneof(
      fc.double({ min: 0, max: 1000000, noNaN: true }),
      fc.double({ min: 0, max: 1000000, noNaN: true }).map(String)
    ),
    expenses: fc.oneof(
      fc.double({ min: 0, max: 1000000, noNaN: true }),
      fc.double({ min: 0, max: 1000000, noNaN: true }).map(String)
    ),
    description: fc.string({ minLength: 0, maxLength: 200 }),
  });

/**
 * Generate financial record with potential invalid data
 */
export const invalidFinancialRecordGenerator = (): fc.Arbitrary<Partial<FinancialRecord>> =>
  fc.record({
    date: fc.option(dateGenerator(), { nil: undefined }),
    category: fc.option(fc.string(), { nil: undefined }),
    revenue: fc.option(fc.double({ noNaN: true }), { nil: undefined }), // may be negative
    expenses: fc.option(fc.double({ noNaN: true }), { nil: undefined }), // may be negative
    description: fc.option(fc.string(), { nil: undefined }),
  });

// ============================================================================
// Task Generators
// ============================================================================

/**
 * Generate a valid task
 */
export const taskGenerator = (): fc.Arbitrary<Task> =>
  fc.record({
    id: fc.uuid(),
    title: fc.string({ minLength: 5, maxLength: 100 }),
    completedDate: dateGenerator(),
    expectedDuration: fc.double({ min: 0.5, max: 160, noNaN: true }), // 0.5 to 160 hours
    actualDuration: fc.double({ min: 0.5, max: 320, noNaN: true }), // may exceed expected
    blockers: fc.array(fc.string({ minLength: 5, maxLength: 50 }), { maxLength: 5 }),
    relatedGoals: fc.array(fc.uuid(), { maxLength: 3 }),
  });

/**
 * Generate raw task data (before parsing)
 */
export const rawTaskGenerator = (): fc.Arbitrary<RawTask> =>
  fc.record({
    id: fc.uuid(),
    title: fc.string({ minLength: 5, maxLength: 100 }),
    completedDate: dateStringGenerator(),
    expectedDuration: fc.oneof(
      fc.double({ min: 0.5, max: 160, noNaN: true }),
      fc.double({ min: 0.5, max: 160, noNaN: true }).map(String)
    ),
    actualDuration: fc.oneof(
      fc.double({ min: 0.5, max: 320, noNaN: true }),
      fc.double({ min: 0.5, max: 320, noNaN: true }).map(String)
    ),
    blockers: fc.array(fc.string({ minLength: 5, maxLength: 50 }), { maxLength: 5 }),
    relatedGoals: fc.array(fc.uuid(), { maxLength: 3 }),
  });

// ============================================================================
// Business Goals Generators
// ============================================================================

/**
 * Generate a valid goal
 */
export const goalGenerator = (): fc.Arbitrary<Goal> =>
  fc.record({
    id: fc.uuid(),
    title: fc.string({ minLength: 10, maxLength: 100 }),
    targetMetric: fc.double({ min: 1, max: 1000000, noNaN: true }),
    currentMetric: fc.double({ min: 0, max: 1000000, noNaN: true }),
    deadline: dateGenerator(),
  });

/**
 * Generate a valid budget
 */
export const budgetGenerator = (): fc.Arbitrary<Budget> =>
  fc.record({
    category: fc.oneof(
      fc.constant('Marketing'),
      fc.constant('Operations'),
      fc.constant('Development'),
      fc.constant('Sales'),
      fc.constant('Other')
    ),
    amount: fc.double({ min: 1000, max: 1000000, noNaN: true }),
    period: fc.oneof(fc.constant('weekly'), fc.constant('monthly')),
  });

/**
 * Generate valid thresholds
 */
export const thresholdsGenerator = (): fc.Arbitrary<Thresholds> =>
  fc.record({
    delayThreshold: fc.double({ min: 10, max: 100, noNaN: true }),
    budgetOverrunThreshold: fc.double({ min: 5, max: 50, noNaN: true }),
    expenseIncreaseThreshold: fc.double({ min: 5, max: 50, noNaN: true }),
  });

/**
 * Generate complete business goals configuration
 */
export const businessGoalsGenerator = (): fc.Arbitrary<BusinessGoals> =>
  fc.record({
    goals: fc.array(goalGenerator(), { minLength: 1, maxLength: 10 }),
    budgets: fc.array(budgetGenerator(), { minLength: 1, maxLength: 10 }),
    thresholds: thresholdsGenerator(),
  });

// ============================================================================
// Array Generators
// ============================================================================

/**
 * Generate an array of financial records
 */
export const financialRecordsArrayGenerator = (
  minLength = 0,
  maxLength = 50
): fc.Arbitrary<FinancialRecord[]> =>
  fc.array(financialRecordGenerator(), { minLength, maxLength });

/**
 * Generate an array of tasks
 */
export const tasksArrayGenerator = (
  minLength = 0,
  maxLength = 50
): fc.Arbitrary<Task[]> =>
  fc.array(taskGenerator(), { minLength, maxLength });

/**
 * Generate an array of goals
 */
export const goalsArrayGenerator = (
  minLength = 0,
  maxLength = 10
): fc.Arbitrary<Goal[]> =>
  fc.array(goalGenerator(), { minLength, maxLength });
