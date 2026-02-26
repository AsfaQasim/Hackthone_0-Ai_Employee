import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import { DataIngestion } from '../../src/weekly-ceo-briefing/components/DataIngestion';
import type { RawFinancialData, RawTask, BusinessGoals } from '../../src/weekly-ceo-briefing/types';

describe('DataIngestion', () => {
  let dataIngestion: DataIngestion;
  const testDir = path.join(__dirname, 'test-data');
  const accountingDir = path.join(testDir, 'accounting');
  const doneDir = path.join(testDir, 'done');
  const configPath = path.join(testDir, 'config.json');

  beforeEach(() => {
    dataIngestion = new DataIngestion();
    
    // Create test directories
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
    if (!fs.existsSync(accountingDir)) {
      fs.mkdirSync(accountingDir, { recursive: true });
    }
    if (!fs.existsSync(doneDir)) {
      fs.mkdirSync(doneDir, { recursive: true });
    }
  });

  afterEach(() => {
    // Clean up test directories
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
    }
  });

  describe('ingestAccountingData', () => {
    it('should return error when folder does not exist', () => {
      const nonExistentPath = path.join(testDir, 'nonexistent');
      const result = dataIngestion.ingestAccountingData(nonExistentPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('MISSING_FOLDER');
        expect(result.error.message).toContain('Accounting folder not found');
        expect(result.error.details.folderType).toBe('accounting');
      }
    });

    it('should return error when path is not a directory', () => {
      const filePath = path.join(testDir, 'notadir.txt');
      fs.writeFileSync(filePath, 'test');

      const result = dataIngestion.ingestAccountingData(filePath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('MISSING_FOLDER');
        expect(result.error.message).toContain('Path is not a directory');
      }
    });

    it('should read all JSON files from accounting folder', () => {
      const data1: RawFinancialData = {
        date: '2024-01-01',
        category: 'Sales',
        revenue: 1000,
        expenses: 200,
        description: 'Product sales',
      };
      const data2: RawFinancialData = {
        date: '2024-01-02',
        category: 'Services',
        revenue: 500,
        expenses: 100,
        description: 'Consulting',
      };

      fs.writeFileSync(
        path.join(accountingDir, 'file1.json'),
        JSON.stringify(data1)
      );
      fs.writeFileSync(
        path.join(accountingDir, 'file2.json'),
        JSON.stringify(data2)
      );

      const result = dataIngestion.ingestAccountingData(accountingDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(2);
        expect(result.data).toContainEqual(data1);
        expect(result.data).toContainEqual(data2);
      }
    });

    it('should handle array of records in a single file', () => {
      const dataArray: RawFinancialData[] = [
        {
          date: '2024-01-01',
          category: 'Sales',
          revenue: 1000,
          expenses: 200,
          description: 'Product sales',
        },
        {
          date: '2024-01-02',
          category: 'Services',
          revenue: 500,
          expenses: 100,
          description: 'Consulting',
        },
      ];

      fs.writeFileSync(
        path.join(accountingDir, 'batch.json'),
        JSON.stringify(dataArray)
      );

      const result = dataIngestion.ingestAccountingData(accountingDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(2);
        expect(result.data).toEqual(dataArray);
      }
    });

    it('should skip non-JSON files', () => {
      const data: RawFinancialData = {
        date: '2024-01-01',
        category: 'Sales',
        revenue: 1000,
        expenses: 200,
        description: 'Product sales',
      };

      fs.writeFileSync(
        path.join(accountingDir, 'data.json'),
        JSON.stringify(data)
      );
      fs.writeFileSync(path.join(accountingDir, 'readme.txt'), 'Some text');

      const result = dataIngestion.ingestAccountingData(accountingDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(1);
        expect(result.data[0]).toEqual(data);
      }
    });

    it('should log warning for unreadable files but continue processing', () => {
      const validData: RawFinancialData = {
        date: '2024-01-01',
        category: 'Sales',
        revenue: 1000,
        expenses: 200,
        description: 'Product sales',
      };

      fs.writeFileSync(
        path.join(accountingDir, 'valid.json'),
        JSON.stringify(validData)
      );
      fs.writeFileSync(
        path.join(accountingDir, 'invalid.json'),
        'not valid json {'
      );

      const result = dataIngestion.ingestAccountingData(accountingDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(1);
        expect(result.data[0]).toEqual(validData);
        expect(result.warnings).toHaveLength(1);
        expect(result.warnings[0].type).toBe('FILE_READ_ERROR');
        expect(result.warnings[0].message).toContain('invalid.json');
      }
    });

    it('should return empty array when folder is empty', () => {
      const result = dataIngestion.ingestAccountingData(accountingDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(0);
        expect(result.warnings).toHaveLength(0);
      }
    });
  });

  describe('ingestCompletedTasks', () => {
    it('should return error when folder does not exist', () => {
      const nonExistentPath = path.join(testDir, 'nonexistent');
      const result = dataIngestion.ingestCompletedTasks(nonExistentPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('MISSING_FOLDER');
        expect(result.error.message).toContain('Done folder not found');
        expect(result.error.details.folderType).toBe('done');
      }
    });

    it('should return error when path is not a directory', () => {
      const filePath = path.join(testDir, 'notadir.txt');
      fs.writeFileSync(filePath, 'test');

      const result = dataIngestion.ingestCompletedTasks(filePath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('MISSING_FOLDER');
        expect(result.error.message).toContain('Path is not a directory');
      }
    });

    it('should read all JSON files from done folder', () => {
      const task1: RawTask = {
        id: 'task-1',
        title: 'Complete feature',
        completedDate: '2024-01-01',
        expectedDuration: 8,
        actualDuration: 10,
        blockers: ['dependency delay'],
        relatedGoals: ['goal-1'],
      };
      const task2: RawTask = {
        id: 'task-2',
        title: 'Fix bug',
        completedDate: '2024-01-02',
        expectedDuration: 2,
        actualDuration: 3,
        blockers: [],
        relatedGoals: ['goal-2'],
      };

      fs.writeFileSync(
        path.join(doneDir, 'task1.json'),
        JSON.stringify(task1)
      );
      fs.writeFileSync(
        path.join(doneDir, 'task2.json'),
        JSON.stringify(task2)
      );

      const result = dataIngestion.ingestCompletedTasks(doneDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(2);
        expect(result.data).toContainEqual(task1);
        expect(result.data).toContainEqual(task2);
      }
    });

    it('should handle array of tasks in a single file', () => {
      const taskArray: RawTask[] = [
        {
          id: 'task-1',
          title: 'Complete feature',
          completedDate: '2024-01-01',
          expectedDuration: 8,
          actualDuration: 10,
          blockers: ['dependency delay'],
          relatedGoals: ['goal-1'],
        },
        {
          id: 'task-2',
          title: 'Fix bug',
          completedDate: '2024-01-02',
          expectedDuration: 2,
          actualDuration: 3,
          blockers: [],
          relatedGoals: ['goal-2'],
        },
      ];

      fs.writeFileSync(
        path.join(doneDir, 'batch.json'),
        JSON.stringify(taskArray)
      );

      const result = dataIngestion.ingestCompletedTasks(doneDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(2);
        expect(result.data).toEqual(taskArray);
      }
    });

    it('should log warning for unreadable files but continue processing', () => {
      const validTask: RawTask = {
        id: 'task-1',
        title: 'Complete feature',
        completedDate: '2024-01-01',
        expectedDuration: 8,
        actualDuration: 10,
        blockers: [],
        relatedGoals: ['goal-1'],
      };

      fs.writeFileSync(
        path.join(doneDir, 'valid.json'),
        JSON.stringify(validTask)
      );
      fs.writeFileSync(
        path.join(doneDir, 'invalid.json'),
        'not valid json {'
      );

      const result = dataIngestion.ingestCompletedTasks(doneDir);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toHaveLength(1);
        expect(result.data[0]).toEqual(validTask);
        expect(result.warnings).toHaveLength(1);
        expect(result.warnings[0].type).toBe('FILE_READ_ERROR');
        expect(result.warnings[0].message).toContain('invalid.json');
      }
    });
  });

  describe('loadBusinessGoals', () => {
    it('should return error when file does not exist', () => {
      const nonExistentPath = path.join(testDir, 'nonexistent.json');
      const result = dataIngestion.loadBusinessGoals(nonExistentPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('INVALID_CONFIG');
        expect(result.error.message).toContain('Configuration file not found');
      }
    });

    it('should load valid business goals configuration', () => {
      const config: BusinessGoals = {
        goals: [
          {
            id: 'goal-1',
            title: 'Increase revenue',
            targetMetric: 100000,
            currentMetric: 75000,
            deadline: new Date('2024-12-31'),
          },
        ],
        budgets: [
          {
            category: 'Marketing',
            amount: 10000,
            period: 'monthly',
          },
        ],
        thresholds: {
          delayThreshold: 50,
          budgetOverrunThreshold: 10,
          expenseIncreaseThreshold: 15,
        },
      };

      fs.writeFileSync(configPath, JSON.stringify(config));

      const result = dataIngestion.loadBusinessGoals(configPath);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.goals).toHaveLength(1);
        expect(result.data.budgets).toHaveLength(1);
        expect(result.data.thresholds).toEqual(config.thresholds);
      }
    });

    it('should return error when goals array is missing', () => {
      const invalidConfig = {
        budgets: [],
        thresholds: {},
      };

      fs.writeFileSync(configPath, JSON.stringify(invalidConfig));

      const result = dataIngestion.loadBusinessGoals(configPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('INVALID_CONFIG');
        expect(result.error.message).toContain('missing required "goals" array');
      }
    });

    it('should return error when budgets array is missing', () => {
      const invalidConfig = {
        goals: [],
        thresholds: {},
      };

      fs.writeFileSync(configPath, JSON.stringify(invalidConfig));

      const result = dataIngestion.loadBusinessGoals(configPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('INVALID_CONFIG');
        expect(result.error.message).toContain('missing required "budgets" array');
      }
    });

    it('should return error when thresholds object is missing', () => {
      const invalidConfig = {
        goals: [],
        budgets: [],
      };

      fs.writeFileSync(configPath, JSON.stringify(invalidConfig));

      const result = dataIngestion.loadBusinessGoals(configPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('INVALID_CONFIG');
        expect(result.error.message).toContain('missing required "thresholds" object');
      }
    });

    it('should return error when file contains invalid JSON', () => {
      fs.writeFileSync(configPath, 'not valid json {');

      const result = dataIngestion.loadBusinessGoals(configPath);

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.type).toBe('INVALID_CONFIG');
        expect(result.error.message).toContain('Failed to parse configuration file');
      }
    });
  });
});
