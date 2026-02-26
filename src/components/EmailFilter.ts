/**
 * Email Filter Component
 * Evaluates emails against importance criteria to determine if they should be processed
 */

import { Email } from '../models/Email';
import { ImportanceCriteria } from '../models/Config';

/**
 * EmailFilter evaluates emails against configured importance criteria
 * Uses OR logic: email is important if it matches ANY criterion
 */
export class EmailFilter {
  /**
   * Determines if an email is important based on configured criteria
   * 
   * @param email - The email to evaluate
   * @param criteria - The importance criteria to check against
   * @returns true if email matches any importance criterion, false otherwise
   * 
   * Evaluation logic (OR):
   * - Sender email matches whitelist
   * - Subject or body contains any keyword pattern (case-insensitive)
   * - Email has any required label
   */
  isImportant(email: Email, criteria: ImportanceCriteria): boolean {
    // Check sender whitelist
    if (this.matchesSenderWhitelist(email, criteria.senderWhitelist)) {
      return true;
    }

    // Check keyword patterns
    if (this.matchesKeywordPatterns(email, criteria.keywordPatterns)) {
      return true;
    }

    // Check required labels
    if (this.matchesRequiredLabels(email, criteria.requiredLabels)) {
      return true;
    }

    // No criteria matched
    return false;
  }

  /**
   * Checks if email sender is in the whitelist
   * 
   * @param email - The email to check
   * @param whitelist - Array of whitelisted email addresses
   * @returns true if sender email matches any whitelisted address
   */
  private matchesSenderWhitelist(email: Email, whitelist: string[]): boolean {
    if (whitelist.length === 0) {
      return false;
    }

    const senderEmail = email.sender.email.toLowerCase();
    return whitelist.some(whitelistedEmail => 
      whitelistedEmail.toLowerCase() === senderEmail
    );
  }

  /**
   * Checks if email subject or body contains any keyword pattern
   * Matching is case-insensitive
   * 
   * @param email - The email to check
   * @param patterns - Array of keyword patterns to search for
   * @returns true if any pattern is found in subject or body
   */
  private matchesKeywordPatterns(email: Email, patterns: string[]): boolean {
    if (patterns.length === 0) {
      return false;
    }

    const subjectLower = email.subject.toLowerCase();
    const bodyTextLower = email.bodyText.toLowerCase();

    return patterns.some(pattern => {
      const patternLower = pattern.toLowerCase();
      return subjectLower.includes(patternLower) || 
             bodyTextLower.includes(patternLower);
    });
  }

  /**
   * Checks if email has any of the required labels
   * 
   * @param email - The email to check
   * @param requiredLabels - Array of labels to check for
   * @returns true if email has any required label
   */
  private matchesRequiredLabels(email: Email, requiredLabels: string[]): boolean {
    if (requiredLabels.length === 0) {
      return false;
    }

    return requiredLabels.some(requiredLabel => 
      email.labels.includes(requiredLabel)
    );
  }
}
