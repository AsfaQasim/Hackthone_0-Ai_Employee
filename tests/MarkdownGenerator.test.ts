/**
 * Tests for MarkdownGenerator
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { MarkdownGenerator } from '../src/components/MarkdownGenerator.js';
import type { Email } from '../src/models/index.js';
import { promises as fs } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

describe('MarkdownGenerator', () => {
  let generator: MarkdownGenerator;
  let testDir: string;

  beforeEach(async () => {
    generator = new MarkdownGenerator();
    // Create a temporary directory for test files
    testDir = join(tmpdir(), `markdown-test-${Date.now()}`);
    await fs.mkdir(testDir, { recursive: true });
  });

  afterEach(async () => {
    // Clean up test directory
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  describe('generateMarkdown', () => {
    it('should generate markdown with frontmatter and body', () => {
      const email: Email = {
        id: 'test-123',
        threadId: 'thread-456',
        sender: { name: 'John Doe', email: 'john@example.com' },
        subject: 'Test Email',
        date: new Date('2024-01-15T10:30:00Z'),
        labels: ['INBOX', 'IMPORTANT'],
        bodyHtml: '<p>Hello <strong>World</strong></p>',
        bodyText: 'Hello World',
        snippet: 'Hello World'
      };

      const markdown = generator.generateMarkdown(email, 'high');

      expect(markdown).toContain('---');
      expect(markdown).toContain('email_id: "test-123"');
      expect(markdown).toContain('sender: "John Doe <john@example.com>"');
      expect(markdown).toContain('subject: "Test Email"');
      expect(markdown).toContain('priority: "high"');
      expect(markdown).toContain('labels: ["INBOX", "IMPORTANT"]');
      expect(markdown).toContain('# Test Email');
      expect(markdown).toContain('Hello **World**');
    });

    it('should handle empty labels array', () => {
      const email: Email = {
        id: 'test-123',
        threadId: 'thread-456',
        sender: { name: 'Jane Doe', email: 'jane@example.com' },
        subject: 'No Labels',
        date: new Date('2024-01-15T10:30:00Z'),
        labels: [],
        bodyHtml: '<p>Test</p>',
        bodyText: 'Test',
        snippet: 'Test'
      };

      const markdown = generator.generateMarkdown(email, 'low');

      expect(markdown).toContain('labels: []');
    });

    it('should escape quotes in subject', () => {
      const email: Email = {
        id: 'test-123',
        threadId: 'thread-456',
        sender: { name: 'Test', email: 'test@example.com' },
        subject: 'Subject with "quotes"',
        date: new Date('2024-01-15T10:30:00Z'),
        labels: [],
        bodyHtml: '<p>Test</p>',
        bodyText: 'Test',
        snippet: 'Test'
      };

      const markdown = generator.generateMarkdown(email, 'medium');

      expect(markdown).toContain('subject: "Subject with \\"quotes\\""');
    });
  });

  describe('htmlToMarkdown', () => {
    it('should convert HTML to markdown', () => {
      const html = '<h1>Title</h1><p>Paragraph with <strong>bold</strong> and <em>italic</em></p>';
  