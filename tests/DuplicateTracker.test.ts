/**
 * Unit tests for DuplicateTracker
 * Tests duplicate detection, index management, and index rebuilding
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { DuplicateTracker } from '../src/components/DuplicateTracker';
import * as fs from 'fs/promises';
import * as path from 'path';

describe('DuplicateTracker', () => {
  const testDir = path.join(__dirname, 'test-duplicate-tracker');
  const indexPath = path.join(testDir, '.index', 'gmail-watcher-processed.json');
  const markdownFolder = path.join(testDir, 'markdown');
  let tracker: DuplicateTracker;
  
  beforeEach(async () => {
    // Create test directories
    await fs.mkdir(testDir, { recursive: true });
    await fs.mkdir(markdownFolder, { recursive: true });
    
    tracker = new DuplicateTracker(indexPath);
  });
  
  afterEach(async () => {
    // Clean up test directory
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });
  
  describe('isProcessed', () => {
    it('should return false for unprocessed email', async () => {
      const result = await tracker.isProcessed('email-123');
      expect(result).toBe(false);
    });
    
    it('should return true for processed email', async () => {
      await tracker.markProcessed('email-123', 'test-file.md', 'high');
      const result = await tracker.isProcessed('email-123');
      expect(result).toBe(true);
    });
    
    it('should persist across instances', async () => {
      await tracker.markProcessed('email-456', 'another-file.md', 'medium');
      
      // Create new tracker instance
      const newTracker = new DuplicateTracker(indexPath);
      const result = await newTracker.isProcessed('email-456');
      
      expect(result).toBe(true);
    });
  });
  
  describe('markProcessed', () => {
    it('should mark email as processed', async () => {
      await tracker.markProcessed('email-789', 'file.md', 'low');
      
      const entry = await tracker.getEntry('email-789');
      expect(entry).toBeDefined();
      expect(entry?.filename).toBe('file.md');
      expect(entry?.priority).toBe('low');
      expect(entry?.processedAt).toBeInstanceOf(Date);
    });
    
    it('should use default priority if not specified', async () => {
      await tracker.markProcessed('email-default', 'default.md');
      
      const entry = await tracker.getEntry('email-default');
      expect(entry?.priority).toBe('medium');
    });
    
    it('should update existing entry', async () => {
      await tracker.markProcessed('email-update', 'old.md', 'low');
      await tracker.markProcessed('email-update', 'new.md', 'high');
      
      const entry = await tracker.getEntry('email-update');
      expect(entry?.filename).toBe('new.md');
      expect(entry?.priority).toBe('high');
    });
  });
  
  describe('rebuildIndex', () => {
    it('should rebuild index from markdown files', async () => {
      // Create test markdown files with frontmatter
      const markdown1 = `---
email_id: "rebuild-email-1"
sender: "Test Sender <test@example.com>"
subject: "Test Subject"
date: "2024-01-15T10:30:00Z"
priority: "high"
labels: ["INBOX"]
processed_at: "2024-01-15T10:35:00Z"
---

# Test Email Content
`;
      
      const markdown2 = `---
email_id: "rebuild-email-2"
sender: "Another Sender <another@example.com>"
subject: "Another Subject"
date: "2024-01-16T11:00:00Z"
priority: "medium"
labels: ["INBOX", "IMPORTANT"]
processed_at: "2024-01-16T11:05:00Z"
---

# Another Email Content
`;
      
      await fs.writeFile(path.join(markdownFolder, 'email1.md'), markdown1, 'utf-8');
      await fs.writeFile(path.join(markdownFolder, 'email2.md'), markdown2, 'utf-8');
      
      // Rebuild index
      await tracker.rebuildIndex(markdownFolder);
      
      // Verify both emails are in index
      expect(await tracker.isProcessed('rebuild-email-1')).toBe(true);
      expect(await tracker.isProcessed('rebuild-email-2')).toBe(true);
      
      const entry1 = await tracker.getEntry('rebuild-email-1');
      expect(entry1?.filename).toBe('email1.md');
      expect(entry1?.priority).toBe('high');
      
      const entry2 = await tracker.getEntry('rebuild-email-2');
      expect(entry2?.filename).toBe('email2.md');
      expect(entry2?.priority).toBe('medium');
    });
    
    it('should handle markdown files without frontmatter', async () => {
      const markdownNoFrontmatter = `# Email without frontmatter`;
      await fs.writeFile(path.join(markdownFolder, 'no-frontmatter.md'), markdownNoFrontmatter, 'utf-8');
      
      await tracker.rebuildIndex(markdownFolder);
      
      // Should not crash, just skip the file
      const allIds = await tracker.getAllEmailIds();
      expect(allIds).toHaveLength(0);
    });
    
    it('should handle empty folder', async () => {
      await tracker.rebuildIndex(markdownFolder);
      
      const allIds = await tracker.getAllEmailIds();
      expect(allIds).toHaveLength(0);
    });
    
    it('should handle non-existent folder', async () => {
      const nonExistentFolder = path.join(testDir, 'does-not-exist');
      
      await tracker.rebuildIndex(nonExistentFolder);
      
      const allIds = await tracker.getAllEmailIds();
      expect(allIds).toHaveLength(0);
    });
    
    it('should use file modification time if processed_at is missing', async () => {
      const markdownNoProcessedAt = `---
email_id: "no-processed-at"
sender: "Test <test@example.com>"
subject: "Test"
date: "2024-01-15T10:30:00Z"
priority: "low"
labels: ["INBOX"]
---

# Content
`;
      
      await fs.writeFile(path.join(markdownFolder, 'no-date.md'), markdownNoProcessedAt, 'utf-8');
      await tracker.rebuildIndex(markdownFolder);
      
      const entry = await tracker.getEntry('no-processed-at');
      expect(entry).toBeDefined();
      expect(entry?.processedAt).toBeInstanceOf(Date);
    });
  });
  
  describe('getAllEmailIds', () => {
    it('should return empty array for empty index', async () => {
      const ids = await tracker.getAllEmailIds();
      expect(ids).toEqual([]);
    });
    
    it('should return all email IDs', async () => {
      await tracker.markProcessed('email-1', 'file1.md', 'high');
      await tracker.markProcessed('email-2', 'file2.md', 'medium');
      await tracker.markProcessed('email-3', 'file3.md', 'low');
      
      const ids = await tracker.getAllEmailIds();
      expect(ids).toHaveLength(3);
      expect(ids).toContain('email-1');
      expect(ids).toContain('email-2');
      expect(ids).toContain('email-3');
    });
  });
  
  describe('clear', () => {
    it('should clear all entries', async () => {
      await tracker.markProcessed('email-1', 'file1.md', 'high');
      await tracker.markProcessed('email-2', 'file2.md', 'medium');
      
      await tracker.clear();
      
      const ids = await tracker.getAllEmailIds();
      expect(ids).toHaveLength(0);
      expect(await tracker.isProcessed('email-1')).toBe(false);
      expect(await tracker.isProcessed('email-2')).toBe(false);
    });
  });
});
