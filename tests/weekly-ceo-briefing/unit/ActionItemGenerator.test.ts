/**
 * Unit tests for ActionItemGenerator
 */

import { describe, it, expect } from 'vitest';
import { ActionItemGenerator } from '../../../src/weekly-ceo-briefing/components/ActionItemGenerator.js';
import {
  RankedBottleneck,
  RankedOpportunity,
  BusinessGoals,
  GoalProgress,
  ActionItem
} from '../../../src/weekly-ceo-briefing/types.js';

describe('ActionItemGenerator', () => {
  let generator: ActionItemGenerator;

  beforeEach(() => {
    generator = new ActionItemGenerator();
  });

  describe('generateFromBottlenecks', () => {
    it('should generate action items from delayed task bottlenecks', () => {
      const bottlenecks: RankedBottleneck[] = [
        {
          type: 'delayed_task',
          title: 'Project Alpha',
          description: 'Task took 50% longer than expected due to technical issues',
          impactScore: 85,
          affectedGoals: ['goal1'],
          rank: 1
        }
      ];

      const actions = generator.generateFromBottlenecks(bottlenecks);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Address task delays in Project Alpha');
      expect(actions[0].source).toBe('bottleneck');
      expect(actions[0].priority).toBeGreaterThan(0);
      expect(actions[0].estimatedImpact).toContain('High');
    });

    it('should generate action items from recurring issue bottlenecks', () => {
      const bottlenecks: RankedBottleneck[] = [
        {
          type: 'recurring_issue',
          title: 'Database Connection Issues',
          description: 'Same connection timeout error occurred 5 times this week',
          impactScore: 60,
          affectedGoals: ['goal1', 'goal2'],
          rank: 1
        }
      ];

      const actions = generator.generateFromBottlenecks(bottlenecks);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Resolve recurring issue: Database Connection Issues');
      expect(actions[0].source).toBe('bottleneck');
      expect(actions[0].estimatedImpact).toContain('High');
    });

    it('should generate action items from goal progress bottlenecks', () => {
      const bottlenecks: RankedBottleneck[] = [
        {
          type: 'goal_progress',
          title: 'Revenue Target Q1',
          description: 'Only 15% progress toward quarterly revenue goal',
          impactScore: 90,
          affectedGoals: ['revenue-q1'],
          rank: 1
        }
      ];

      const actions = generator.generateFromBottlenecks(bottlenecks);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Accelerate progress on Revenue Target Q1');
      expect(actions[0].source).toBe('bottleneck');
      expect(actions[0].estimatedImpact).toContain('Medium');
    });
  });

  describe('generateFromCostOpportunities', () => {
    it('should generate action items from budget overrun opportunities', () => {
      const opportunities: RankedOpportunity[] = [
        {
          type: 'budget_overrun',
          category: 'Marketing',
          currentAmount: 15000,
          targetAmount: 12000,
          potentialSavings: 3000,
          suggestion: 'Review marketing spend efficiency and eliminate underperforming campaigns',
          rank: 1
        }
      ];

      const actions = generator.generateFromCostOpportunities(opportunities);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Reduce Marketing expenses');
      expect(actions[0].source).toBe('cost');
      expect(actions[0].estimatedImpact).toContain('$3000.00');
      expect(actions[0].description).toContain('$15000.00');
    });

    it('should generate action items from increasing expense opportunities', () => {
      const opportunities: RankedOpportunity[] = [
        {
          type: 'increasing_expense',
          category: 'Cloud Services',
          currentAmount: 8000,
          targetAmount: 6000,
          potentialSavings: 2000,
          suggestion: 'Optimize cloud resource usage and review service tiers',
          rank: 1
        }
      ];

      const actions = generator.generateFromCostOpportunities(opportunities);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Control rising Cloud Services costs');
      expect(actions[0].source).toBe('cost');
      expect(actions[0].estimatedImpact).toContain('$2000.00');
    });
  });

  describe('generateFromGoalProgress', () => {
    it('should generate action items for lagging goals', () => {
      const goals: BusinessGoals = {
        goals: [
          {
            id: 'goal1',
            title: 'Customer Acquisition',
            targetMetric: 1000,
            currentMetric: 150,
            deadline: new Date('2024-03-31')
          }
        ],
        budgets: [],
        thresholds: {
          delayThreshold: 50,
          budgetOverrunThreshold: 10,
          expenseIncreaseThreshold: 15
        }
      };

      const progress: GoalProgress[] = [
        {
          goalId: 'goal1',
          goalTitle: 'Customer Acquisition',
          expectedProgress: 500,
          actualProgress: 100,
          progressPercentage: 20 // 20% < 25% threshold
        }
      ];

      const actions = generator.generateFromGoalProgress(goals, progress);

      expect(actions).toHaveLength(1);
      expect(actions[0].title).toBe('Accelerate progress on Customer Acquisition');
      expect(actions[0].source).toBe('goal');
      expect(actions[0].description).toContain('20.0%');
    });

    it('should not generate actions for goals meeting progress threshold', () => {
      const goals: BusinessGoals = {
        goals: [],
        budgets: [],
        thresholds: {
          delayThreshold: 50,
          budgetOverrunThreshold: 10,
          expenseIncreaseThreshold: 15
        }
      };

      const progress: GoalProgress[] = [
        {
          goalId: 'goal1',
          goalTitle: 'Customer Acquisition',
          expectedProgress: 500,
          actualProgress: 400,
          progressPercentage: 80 // 80% > 25% threshold
        }
      ];

      const actions = generator.generateFromGoalProgress(goals, progress);

      expect(actions).toHaveLength(0);
    });
  });

  describe('prioritizeActions', () => {
    it('should sort actions by priority in descending order', () => {
      const actions: ActionItem[] = [
        {
          title: 'Low Priority',
          description: 'Low priority task',
          priority: 10,
          source: 'bottleneck',
          estimatedImpact: 'Low'
        },
        {
          title: 'High Priority',
          description: 'High priority task',
          priority: 50,
          source: 'cost',
          estimatedImpact: 'High'
        },
        {
          title: 'Medium Priority',
          description: 'Medium priority task',
          priority: 30,
          source: 'goal',
          estimatedImpact: 'Medium'
        }
      ];

      const prioritized = generator.prioritizeActions(actions);

      expect(prioritized).toHaveLength(3);
      expect(prioritized[0].title).toBe('High Priority');
      expect(prioritized[0].rank).toBe(1);
      expect(prioritized[1].title).toBe('Medium Priority');
      expect(prioritized[1].rank).toBe(2);
      expect(prioritized[2].title).toBe('Low Priority');
      expect(prioritized[2].rank).toBe(3);
    });
  });

  describe('limitActions', () => {
    it('should limit actions to specified maximum', () => {
      const actions = Array.from({ length: 15 }, (_, i) => ({
        title: `Action ${i + 1}`,
        description: `Description ${i + 1}`,
        priority: 100 - i,
        source: 'bottleneck' as const,
        estimatedImpact: 'Medium',
        rank: i + 1
      }));

      const limited = generator.limitActions(actions, 10);

      expect(limited).toHaveLength(10);
      expect(limited[0].title).toBe('Action 1');
      expect(limited[9].title).toBe('Action 10');
    });

    it('should return all actions if under limit', () => {
      const actions = Array.from({ length: 5 }, (_, i) => ({
        title: `Action ${i + 1}`,
        description: `Description ${i + 1}`,
        priority: 100 - i,
        source: 'bottleneck' as const,
        estimatedImpact: 'Medium',
        rank: i + 1
      }));

      const limited = generator.limitActions(actions, 10);

      expect(limited).toHaveLength(5);
    });
  });

  describe('generateActionItems', () => {
    it('should combine and prioritize actions from all sources', () => {
      const bottlenecks: RankedBottleneck[] = [
        {
          type: 'delayed_task',
          title: 'Project Alpha',
          description: 'Delayed project',
          impactScore: 80,
          affectedGoals: ['goal1'],
          rank: 1
        }
      ];

      const opportunities: RankedOpportunity[] = [
        {
          type: 'budget_overrun',
          category: 'Marketing',
          currentAmount: 15000,
          targetAmount: 12000,
          potentialSavings: 3000,
          suggestion: 'Reduce marketing spend',
          rank: 1
        }
      ];

      const goals: BusinessGoals = {
        goals: [
          {
            id: 'goal1',
            title: 'Revenue Target',
            targetMetric: 1000000,
            currentMetric: 200000,
            deadline: new Date('2024-12-31')
          }
        ],
        budgets: [],
        thresholds: {
          delayThreshold: 50,
          budgetOverrunThreshold: 10,
          expenseIncreaseThreshold: 15
        }
      };

      const progress: GoalProgress[] = [
        {
          goalId: 'goal1',
          goalTitle: 'Revenue Target',
          expectedProgress: 500000,
          actualProgress: 100000,
          progressPercentage: 20
        }
      ];

      const actions = generator.generateActionItems(bottlenecks, opportunities, goals, progress);

      expect(actions.length).toBeGreaterThan(0);
      expect(actions.length).toBeLessThanOrEqual(10);
      expect(actions[0].rank).toBe(1);
      
      // Verify all sources are represented
      const sources = actions.map(a => a.source);
      expect(sources).toContain('bottleneck');
      expect(sources).toContain('cost');
      expect(sources).toContain('goal');
    });
  });
});