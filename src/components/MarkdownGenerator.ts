/**
 * Markdown Generator for Gmail Watcher Agent Skill
 * Creates markdown files from email data with frontmatter
 */

import TurndownService from 'turndown';
import { promises as fs } from 'fs';
import { join, dirname } from 'path';
import type { Email, PriorityLevel } from '../models/index.js';

/**
 * MarkdownGenerator creates markdown files from email data
 * Handles frontmatter generation, HTML to markdown conversion, and file writing
 */
export class MarkdownGenerator {
  private turndownService: TurndownService;

  constructor() {
    this.turndownService = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced',
      emDelimiter: '*',
    });
  }

  /**
   * Generate markdown content with frontmatter from email
   * @param email Email to convert to markdown
   * @param priority Priority level assigned to email
   * @returns Complete markdown content with frontmatter
   */
  generateMarkdown(email: Email, priority: PriorityLevel): string {
    const frontmatter = this.generateFrontmatter(email, priority);
    const body = this.htmlToMarkdown(email.bodyHtml || email.bodyText);
    
    return `---
${frontmatter}---

# ${email.subject}

${body}
`;
  }

  /**
   * Generate YAML frontmatter for email
   * @param email Email data
   * @param priority Priority level
   * @returns YAML frontmatter string
   */
  private generateFrontmatter(email: Email, priority: PriorityLevel): string {
    const processedAt = new Date().toISOString();
    const senderFormatted = `"${email.sender.name} <${email.sender.email}>"`;
    const subjectEscaped = email.subject.replace(/"/g, '\\"');
    const labelsFormatted = email.labels.length > 0 
      ? `[${email.labels.map(l => `"${l}"`).join(', ')}]`
      : '[]';

    return `email_id: "${email.id}"
sender: ${senderFormatted}
subject: "${subjectEscaped}"
date: "${email.date.toISOString()}"
priority: "${priority}"
labels: ${labelsFormatted}
processed_at: "${processedAt}"
`;
  }

  /**
   * Convert HTML content to markdown
   * @param html HTML content to convert
   * @returns Markdown formatted content
   */
  htmlToMarkdown(html: string): string {
    if (!html || html.trim() === '') {
      return '';
    }
    
    try {
      return this.turndownService.turndown(html);
    } catch (error) {
      // If conversion fails, return plain text
      return html.replace(/<[^>]*>/g, '');
    }
  }

  /**
   * Generate unique filename from email data
   * Format: YYYYMMDD_HHMMSS_sanitized-subject.md
   * @param email Email to generate filename for
   * @returns Sanitized filename
   */
  generateFilename(email: Email): string {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    const timestamp = `${year}${month}${day}_${hours}${minutes}${seconds}`;
    const sanitizedSubject = this.sanitizeFilename(email.subject);
    
    return `${timestamp}_${sanitizedSubject}.md`;
  }

  /**
   * Sanitize subject for use in filename
   * @param subject Email subject
   * @returns Sanitized subject suitable for filename
   */
  private sanitizeFilename(subject: string): string {
    if (!subject || subject.trim() === '') {
      return 'no-subject';
    }
    
    // Remove or replace invalid filename characters
    let sanitized = subject
      .toLowerCase()
      .replace(/[<>:"/\\|?*\x00-\x1F]/g, '') // Remove invalid chars
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .replace(/[^\w\-]/g, '') // Remove non-word chars except hyphens
      .replace(/-+/g, '-') // Replace multiple hyphens with single
      .replace(/^-|-$/g, ''); // Remove leading/trailing hyphens
    
    // Limit length to 50 characters
    if (sanitized.length > 50) {
      sanitized = sanitized.substring(0, 50);
    }
    
    // Ensure we have something
    if (sanitized === '') {
      sanitized = 'no-subject';
    }
    
    return sanitized;
  }

  /**
   * Create markdown file in specified folder
   * @param markdown Markdown content to write
   * @param filename Filename for the markdown file
   * @param folder Target folder path
   */
  async createFile(markdown: string, filename: string, folder: string): Promise<void> {
    const filePath = join(folder, filename);
    
    // Ensure directory exists
    await fs.mkdir(dirname(filePath), { recursive: true });
    
    // Write file
    await fs.writeFile(filePath, markdown, 'utf-8');
  }
}
