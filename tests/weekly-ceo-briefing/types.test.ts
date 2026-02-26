/**
 * Basic tests to verify type definitions and test setup
 */

import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';
import {
  financialRecordGenerator,
  taskGenerator,
  businessGoalsGenerator,
} from './generators/index.js';

describe('Weekly CEO Briefing - Type System', () => {
  it('should generate valid financial records', () => {
    fc.assert(
      fc.property(financialRecordGenerator(), (record) => {
        expect(record).toBeDefined();
        expect(record.date).toBeInstanceOf(Date);
        expect(typeof record.category).toBe('string');
        expect(typeof record.revenue).toBe('number');
        expect(typeof record.expenses).toBe('number');
        expect(typeof record.description).toBe('string');
        expect(record.revenue).toBeGreaterThanOrEqual(0);
        expect(record.expenses).toBeGreaterThanOrEqual(0);
        return true;
      }),
      { numRuns: 10 }
    );
  });

  it('should generate valid tasks', () => {
    fc.assert(
      fc.property(taskGenerator(), (task) => {
        expect(task).toBeDefined();
        expect(typeof task.id).toBe('string');
        expect(typeof task.title).toBe('string');
        expect(task.completedDate).toBeInstanceOf(Date);
        expect(typeof task.expectedDuration).toBe('number');
        expect(typeof task.actualDuration).toBe('number');
        expect(Array.isArray(task.blockers)).toBe(true);
        expect(Array.isArray(task.relatedGoals)).toBe(true);
        return true;
      }),
      { numRuns: 10 }
    );
  });

  it('should generate valid business goals', () => {
    fc.assert(
      fc.property(businessGoalsGenerator(), (config) => {
        expect(config).toBeDefined();
        expect(Array.isArray(config.goals)).toBe(true);
        expect(Array.isArray(config.budgets)).toBe(true);
        expect(config.thresholds).toBeDefined();
        expect(typeof config.thresholds.delayThreshold).toBe('number');
        expect(typeof config.thresholds.budgetOverrunThreshold).toBe('number');
        expect(typeof config.thresholds.expenseIncreaseThreshold).toBe('number');
        return true;
      }),
      { numRuns: 10 }
    );
  });
});
