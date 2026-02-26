import { describe, it, expect } from 'vitest';
import { DataParser } from '../../src/weekly-ceo-briefing/components/DataParser';
import { RawFinancialData, RawTask } from '../../src/weekly-ceo-briefing/types';

describe('DataParser', () => {
  const parser = new DataParser();

  describe('parseFinancialData', () => {
    it('should parse valid financial data with ISO dates', () => {
      const rawData: RawFinancialData[] = [
        {
          date: '2024-01-15',
          category: 'Sales',
          revenue: '1000.50',
          expenses: '200.25',
          description: 'Product sales',
        },
      ];

      const result = parser.parseFinancialData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].date).toBeInstanceOf(Date);
      expect(result[0].category).toBe('Sales');
      expect(result[0].revenue).toBe(1000.50);
      expect(result[0].expenses).toBe(200.25);
      expect(result[0].description).toBe('Product sales');
    });

    it('should parse financial data with numeric values', () => {
      const rawData: RawFinancialData[] = [
        {
          date: '2024-01-15',
          category: 'Sales',
          revenue: 1000.50,
          expenses: 200.25,
          description: 'Product sales',
        },
      ];

      const result = parser.parseFinancialData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].revenue).toBe(1000.50);
      expect(result[0].expenses).toBe(200.25);
    });

    it('should skip records with invalid dates', () => {
      const rawData: RawFinancialData[] = [
        {
          date: 'invalid-date',
          category: 'Sales',
          revenue: '1000',
          expenses: '200',
          description: 'Product sales',
        },
        {
          date: '2024-01-15',
          category: 'Services',
          revenue: '500',
          expenses: '100',
          description: 'Consulting',
        },
      ];

      const result = parser.parseFinancialData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].category).toBe('Services');
    });

    it('should handle empty array', () => {
      const result = parser.parseFinancialData([]);
      expect(result).toHaveLength(0);
    });
  });

  describe('parseTaskData', () => {
    it('should parse valid task data with ISO dates', () => {
      const rawData: RawTask[] = [
        {
          id: 'task-1',
          title: 'Complete feature',
          completedDate: '2024-01-15',
          expectedDuration: '8',
          actualDuration: '10',
          blockers: ['API delay'],
          relatedGoals: ['goal-1'],
        },
      ];

      const result = parser.parseTaskData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].id).toBe('task-1');
      expect(result[0].title).toBe('Complete feature');
      expect(result[0].completedDate).toBeInstanceOf(Date);
      expect(result[0].expectedDuration).toBe(8);
      expect(result[0].actualDuration).toBe(10);
      expect(result[0].blockers).toEqual(['API delay']);
      expect(result[0].relatedGoals).toEqual(['goal-1']);
    });

    it('should parse task data with numeric durations', () => {
      const rawData: RawTask[] = [
        {
          id: 'task-1',
          title: 'Complete feature',
          completedDate: '2024-01-15',
          expectedDuration: 8,
          actualDuration: 10,
          blockers: [],
          relatedGoals: [],
        },
      ];

      const result = parser.parseTaskData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].expectedDuration).toBe(8);
      expect(result[0].actualDuration).toBe(10);
    });

    it('should skip tasks with invalid dates', () => {
      const rawData: RawTask[] = [
        {
          id: 'task-1',
          title: 'Invalid task',
          completedDate: 'not-a-date',
          expectedDuration: '8',
          actualDuration: '10',
          blockers: [],
          relatedGoals: [],
        },
        {
          id: 'task-2',
          title: 'Valid task',
          completedDate: '2024-01-15',
          expectedDuration: '5',
          actualDuration: '6',
          blockers: [],
          relatedGoals: [],
        },
      ];

      const result = parser.parseTaskData(rawData);

      expect(result).toHaveLength(1);
      expect(result[0].id).toBe('task-2');
    });

    it('should handle empty array', () => {
      const result = parser.parseTaskData([]);
      expect(result).toHaveLength(0);
    });
  });

  describe('parseDate', () => {
    it('should parse ISO 8601 date format', () => {
      const date = parser.parseDate('2024-01-15');
      expect(date).toBeInstanceOf(Date);
      expect(date.getFullYear()).toBe(2024);
      expect(date.getMonth()).toBe(0); // January is 0
      expect(date.getDate()).toBe(15);
    });

    it('should parse ISO 8601 datetime format', () => {
      const date = parser.parseDate('2024-01-15T10:30:00.000Z');
      expect(date).toBeInstanceOf(Date);
      expect(date.getFullYear()).toBe(2024);
    });

    it('should parse MM/DD/YYYY format', () => {
      const date = parser.parseDate('01/15/2024');
      expect(date).toBeInstanceOf(Date);
      expect(date.getFullYear()).toBe(2024);
      expect(date.getMonth()).toBe(0);
      expect(date.getDate()).toBe(15);
    });

    it('should parse DD-MM-YYYY format', () => {
      const date = parser.parseDate('15-01-2024');
      expect(date).toBeInstanceOf(Date);
      expect(date.getFullYear()).toBe(2024);
      expect(date.getMonth()).toBe(0);
      expect(date.getDate()).toBe(15);
    });

    it('should parse YYYY/MM/DD format', () => {
      const date = parser.parseDate('2024/01/15');
      expect(date).toBeInstanceOf(Date);
      expect(date.getFullYear()).toBe(2024);
      expect(date.getMonth()).toBe(0);
      expect(date.getDate()).toBe(15);
    });

    it('should throw error for invalid date format', () => {
      expect(() => parser.parseDate('invalid-date')).toThrow('Unable to parse date: invalid-date');
    });

    it('should throw error for empty string', () => {
      expect(() => parser.parseDate('')).toThrow('Unable to parse date: ');
    });

    it('should throw error for nonsensical date', () => {
      expect(() => parser.parseDate('not-a-date-at-all')).toThrow();
    });
  });
});
