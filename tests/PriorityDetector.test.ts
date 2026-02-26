/**
 * Unit tests for PriorityDetector
 */

import { describe, it, expect } from 'vitest';
import { PriorityDetector } from '../src/components/PriorityDetector';
import { Email } from '../src/models/Email';
import { PriorityRules } from '../src/models/Config';

describe('PriorityDetector', () => {
  const detector = new PriorityDetector();

  const createTestEmail = (overrides: Partial<Email> = {}): Email => ({
    id: 'test-id',
    threadId: 'test-thread',
    sender: { name: 'Test Sender', email: 'test@example.com' },
    subject: 'Test Subject',
    date: new Date(),
    labels: ['INBOX'],
    bodyHtml: '<p>Test body</p>',
    bodyText: 'Test body',
    snippet: 'Test snippet',
    ...overrides
  });

  const createTestRules = (overrides: Partial<PriorityRules> = {}): PriorityRules => ({
    highPriorityKeywords: ['urgent', 'asap', 'critical'],
    vipSenders: ['vip@example.com', 'boss@company.com'],
    highPriorityLabels: ['IMPORTANT', 'STARRED'],
    mediumPriorityKeywords: ['follow up', 'reminder'],
    ...overrides
  });

  describe('detectPriority', () => {
    it('should return high priority for email with urgent keyword in subject', () => {
      const email = createTestEmail({ subject: 'URGENT: Please review' });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should return high priority for email with urgent keyword in body', () => {
      const email = createTestEmail({ 
        bodyText: 'This is critical and needs immediate attention' 
      });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should return high priority for email from VIP sender', () => {
      const email = createTestEmail({ 
        sender: { name: 'VIP Person', email: 'vip@example.com' }
      });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should return high priority for email with high-priority label', () => {
      const email = createTestEmail({ labels: ['INBOX', 'IMPORTANT'] });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should return medium priority for email with medium keyword', () => {
      const email = createTestEmail({ subject: 'Reminder: Meeting tomorrow' });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('medium');
    });

    it('should return low priority for email with no priority indicators', () => {
      const email = createTestEmail({ 
        subject: 'Regular email',
        bodyText: 'Just a normal message'
      });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('low');
    });

    it('should be case-insensitive for keyword matching', () => {
      const email = createTestEmail({ subject: 'ASAP: Need this done' });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should be case-insensitive for VIP sender matching', () => {
      const email = createTestEmail({ 
        sender: { name: 'Boss', email: 'BOSS@COMPANY.COM' }
      });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });

    it('should return low priority when all rule arrays are empty', () => {
      const email = createTestEmail();
      const rules = createTestRules({
        highPriorityKeywords: [],
        vipSenders: [],
        highPriorityLabels: [],
        mediumPriorityKeywords: []
      });
      
      expect(detector.detectPriority(email, rules)).toBe('low');
    });

    it('should prioritize high over medium when both match', () => {
      const email = createTestEmail({ 
        subject: 'URGENT reminder: Critical task'
      });
      const rules = createTestRules();
      
      expect(detector.detectPriority(email, rules)).toBe('high');
    });
  });
});
