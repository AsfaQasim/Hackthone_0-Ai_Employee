/**
 * Priority Detector Component
 * Assigns priority levels to important emails based on configurable rules
 */

import { Email } from '../models/Email';
import { PriorityRules } from '../models/Config';
import { PriorityLevel } from '../models/ProcessedEmailIndex';

/**
 * PriorityDetector analyzes emails and assigns priority levels
 * Priority levels: high, medium, low
 * 
 * High priority: urgent keywords OR VIP sender OR high-priority labels
 * Medium priority: medium-priority keywords OR default when not high
 * Low priority: fallback when no other criteria match
 */
export class PriorityDetector {
  /**
   * Detects and assigns a priority level to an email
   * 
   * @param email - The email to analyze
   * @param rules - The priority rules to apply
   * @returns The assigned priority level (high, medium, or low)
   * 
   * Priority logic:
   * 1. High: Contains urgent keywords OR from VIP sender OR has high-priority labels
   * 2. Medium: Contains medium-priority keywords OR doesn't match high criteria
   * 3. Low: Default fallback
   */
  detectPriority(email: Email, rules: PriorityRules): PriorityLevel {
    // Check high priority conditions
    if (this.isHighPriority(email, rules)) {
      return 'high';
    }

    // Check medium priority conditions
    if (this.isMediumPriority(email, rules)) {
      return 'medium';
    }

    // Default to low priority
    return 'low';
  }

  /**
   * Checks if email meets high priority criteria
   * 
   * @param email - The email to check
   * @param rules - The priority rules
   * @returns true if email is high priority
   */
  private isHighPriority(email: Email, rules: PriorityRules): boolean {
    // Check for urgent keywords in subject or body
    if (this.containsHighPriorityKeywords(email, rules.highPriorityKeywords)) {
      return true;
    }

    // Check if sender is a VIP
    if (this.isFromVIPSender(email, rules.vipSenders)) {
      return true;
    }

    // Check for high-priority labels
    if (this.hasHighPriorityLabels(email, rules.highPriorityLabels)) {
      return true;
    }

    return false;
  }

  /**
   * Checks if email meets medium priority criteria
   * 
   * @param email - The email to check
   * @param rules - The priority rules
   * @returns true if email is medium priority
   */
  private isMediumPriority(email: Email, rules: PriorityRules): boolean {
    // Check for medium-priority keywords in subject or body
    return this.containsMediumPriorityKeywords(email, rules.mediumPriorityKeywords);
  }

  /**
   * Checks if email contains high-priority keywords
   * Matching is case-insensitive
   * 
   * @param email - The email to check
   * @param keywords - Array of high-priority keywords
   * @returns true if any keyword is found in subject or body
   */
  private containsHighPriorityKeywords(email: Email, keywords: string[]): boolean {
    if (keywords.length === 0) {
      return false;
    }

    const subjectLower = email.subject.toLowerCase();
    const bodyTextLower = email.bodyText.toLowerCase();

    return keywords.some(keyword => {
      const keywordLower = keyword.toLowerCase();
      return subjectLower.includes(keywordLower) || 
             bodyTextLower.includes(keywordLower);
    });
  }

  /**
   * Checks if email is from a VIP sender
   * 
   * @param email - The email to check
   * @param vipSenders - Array of VIP email addresses
   * @returns true if sender is in VIP list
   */
  private isFromVIPSender(email: Email, vipSenders: string[]): boolean {
    if (vipSenders.length === 0) {
      return false;
    }

    const senderEmail = email.sender.email.toLowerCase();
    return vipSenders.some(vipEmail => 
      vipEmail.toLowerCase() === senderEmail
    );
  }

  /**
   * Checks if email has high-priority labels
   * 
   * @param email - The email to check
   * @param highPriorityLabels - Array of high-priority labels
   * @returns true if email has any high-priority label
   */
  private hasHighPriorityLabels(email: Email, highPriorityLabels: string[]): boolean {
    if (highPriorityLabels.length === 0) {
      return false;
    }

    return highPriorityLabels.some(label => 
      email.labels.includes(label)
    );
  }

  /**
   * Checks if email contains medium-priority keywords
   * Matching is case-insensitive
   * 
   * @param email - The email to check
   * @param keywords - Array of medium-priority keywords
   * @returns true if any keyword is found in subject or body
   */
  private containsMediumPriorityKeywords(email: Email, keywords: string[]): boolean {
    if (keywords.length === 0) {
      return false;
    }

    const subjectLower = email.subject.toLowerCase();
    const bodyTextLower = email.bodyText.toLowerCase();

    return keywords.some(keyword => {
      const keywordLower = keyword.toLowerCase();
      return subjectLower.includes(keywordLower) || 
             bodyTextLower.includes(keywordLower);
    });
  }
}
