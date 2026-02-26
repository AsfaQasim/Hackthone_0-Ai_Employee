/**
 * Action Item Generator for the Weekly CEO Briefing system
 * 
 * Generates prioritized action items from analysis results including:
 * - Bottlenecks that need addressing
 * - Cost optimization opportunities to pursue
 * - Goals with insufficient progress
 * 
 * Priority scoring: (business_impact * 3) + (urgency * 2) + (effort_inverse * 1)
 */

import {
  ActionItem,
  PrioritizedActionItem,
  RankedBottleneck,
  RankedOpportunity,
  BusinessGoals,
  GoalProgress
} from '../types.js';

export class ActionItemGenerator {
  /**
   * Generate action items from identified bottlenecks
   * Each bottleneck generates 1 action item to address the constraint
   */
  generateFromBottlenecks(bottlenecks: RankedBottleneck[]): ActionItem[] {
    return bottlenecks.map(bottleneck => {
      let title: string;
      let description: string;
      let estimatedImpact: string;
      
      switch (bottleneck.type) {
        case 'delayed_task':
          title = `Address task delays in ${bottleneck.title}`;
          description = `Investigate and resolve the factors causing delays in ${bottleneck.title}. ${bottleneck.description}`;
          estimatedImpact = 'High - Reduces project delays and improves delivery timelines';
          break;
          
        case 'recurring_issue':
          title = `Resolve recurring issue: ${bottleneck.title}`;
          description = `Implement systematic solution for recurring blocker: ${bottleneck.description}`;
          estimatedImpact = 'High - Eliminates repeated productivity losses';
          break;
          
        case 'goal_progress':
          title = `Accelerate progress on ${bottleneck.title}`;
          description = `Review and adjust strategy for goal: ${bottleneck.description}. Consider resource reallocation or process improvements.`;
          estimatedImpact = 'Medium - Improves goal achievement likelihood';
          break;
          
        default:
          title = `Address bottleneck: ${bottleneck.title}`;
          description = bottleneck.description;
          estimatedImpact = 'Medium - General operational improvement';
      }
      
      // Calculate priority based on impact score and type
      const businessImpact = Math.min(10, Math.max(1, Math.floor(bottleneck.impactScore / 10)));
      const urgency = bottleneck.type === 'delayed_task' ? 9 : 
                     bottleneck.type === 'recurring_issue' ? 8 : 6;
      const effortInverse = 7; // Assume moderate effort for bottleneck resolution
      
      const priority = (businessImpact * 3) + (urgency * 2) + (effortInverse * 1);
      
      return {
        title,
        description,
        priority,
        source: 'bottleneck' as const,
        estimatedImpact
      };
    });
  }

  /**
   * Generate action items from cost optimization opportunities
   * Each opportunity generates 1 action item to pursue savings
   */
  generateFromCostOpportunities(opportunities: RankedOpportunity[]): ActionItem[] {
    return opportunities.map(opportunity => {
      let title: string;
      let description: string;
      let estimatedImpact: string;
      
      switch (opportunity.type) {
        case 'budget_overrun':
          title = `Reduce ${opportunity.category} expenses`;
          description = `Review and optimize ${opportunity.category} spending. Current: $${opportunity.currentAmount.toFixed(2)}, Target: $${opportunity.targetAmount.toFixed(2)}. ${opportunity.suggestion}`;
          estimatedImpact = `High - Potential savings of $${opportunity.potentialSavings.toFixed(2)}`;
          break;
          
        case 'increasing_expense':
          title = `Control rising ${opportunity.category} costs`;
          description = `Investigate and address increasing expenses in ${opportunity.category}. ${opportunity.suggestion}`;
          estimatedImpact = `Medium - Prevent further cost escalation, potential savings of $${opportunity.potentialSavings.toFixed(2)}`;
          break;
          
        default:
          title = `Optimize ${opportunity.category} costs`;
          description = opportunity.suggestion;
          estimatedImpact = `Medium - Cost optimization opportunity`;
      }
      
      // Calculate priority based on potential savings and urgency
      const businessImpact = Math.min(10, Math.max(1, Math.floor(opportunity.potentialSavings / 1000)));
      const urgency = opportunity.type === 'budget_overrun' ? 8 : 6;
      const effortInverse = 8; // Cost optimization often has good ROI
      
      const priority = (businessImpact * 3) + (urgency * 2) + (effortInverse * 1);
      
      return {
        title,
        description,
        priority,
        source: 'cost' as const,
        estimatedImpact
      };
    });
  }

  /**
   * Generate action items from goals with insufficient progress
   * Each lagging goal generates 1 action item to accelerate progress
   */
  generateFromGoalProgress(goals: BusinessGoals, progress: GoalProgress[]): ActionItem[] {
    // Find goals with insufficient progress (< 25% of expected)
    const laggingGoals = progress.filter(p => p.progressPercentage < 25);
    
    return laggingGoals.map(goalProgress => {
      const goal = goals.goals.find(g => g.id === goalProgress.goalId);
      
      const title = `Accelerate progress on ${goalProgress.goalTitle}`;
      const description = `Goal is at ${goalProgress.progressPercentage.toFixed(1)}% of expected progress. ` +
                         `Current: ${goalProgress.actualProgress}, Expected: ${goalProgress.expectedProgress}. ` +
                         `Review strategy, allocate additional resources, or adjust timeline.`;
      const estimatedImpact = goal ? 
        `High - Critical for achieving ${goal.targetMetric} target by ${goal.deadline.toDateString()}` :
        'Medium - Important for strategic goal achievement';
      
      // Calculate priority based on goal importance and progress gap
      const progressGap = goalProgress.expectedProgress - goalProgress.actualProgress;
      const businessImpact = Math.min(10, Math.max(1, Math.floor(progressGap / 10)));
      const urgency = goalProgress.progressPercentage < 10 ? 9 : 7; // Very urgent if < 10%
      const effortInverse = 6; // Goal acceleration often requires significant effort
      
      const priority = (businessImpact * 3) + (urgency * 2) + (effortInverse * 1);
      
      return {
        title,
        description,
        priority,
        source: 'goal' as const,
        estimatedImpact
      };
    });
  }

  /**
   * Prioritize action items by calculating and sorting by priority score
   * Priority score = (business_impact * 3) + (urgency * 2) + (effort_inverse * 1)
   */
  prioritizeActions(actions: ActionItem[]): PrioritizedActionItem[] {
    // Sort by priority in descending order (highest priority first)
    const sortedActions = [...actions].sort((a, b) => b.priority - a.priority);
    
    // Add rank to each action
    return sortedActions.map((action, index) => ({
      ...action,
      rank: index + 1
    }));
  }

  /**
   * Limit action items to top N items to maintain focus
   * Default limit is 10 as specified in requirements
   */
  limitActions(actions: PrioritizedActionItem[], maxActions: number = 10): PrioritizedActionItem[] {
    return actions.slice(0, maxActions);
  }

  /**
   * Generate complete set of prioritized action items from all sources
   * Combines bottlenecks, cost opportunities, and goal progress into unified list
   */
  generateActionItems(
    bottlenecks: RankedBottleneck[],
    opportunities: RankedOpportunity[],
    goals: BusinessGoals,
    progress: GoalProgress[]
  ): PrioritizedActionItem[] {
    // Generate actions from all sources
    const bottleneckActions = this.generateFromBottlenecks(bottlenecks);
    const costActions = this.generateFromCostOpportunities(opportunities);
    const goalActions = this.generateFromGoalProgress(goals, progress);
    
    // Combine all actions
    const allActions = [...bottleneckActions, ...costActions, ...goalActions];
    
    // Prioritize and limit to top 10
    const prioritizedActions = this.prioritizeActions(allActions);
    return this.limitActions(prioritizedActions, 10);
  }
}