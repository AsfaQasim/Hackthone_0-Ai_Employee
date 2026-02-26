/**
 * Duplicate Tracker Component
 * Prevents duplicate markdown file creation by maintaining an index of processed emails
 * 
 * Requirements: 10.1, 10.2, 10.4, 10.5
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { ProcessedEmailIndex, ProcessedEmailEntry, PriorityLevel } from '../models';

/**
 * DuplicateTracker manages an index of processed emails to prevent duplicates
 */
export class DuplicateTracker {
  private indexPath: string;
  private index: ProcessedEmailIndex;
  private loaded: boolean = false;

  /**
   * Creates a new DuplicateTracker instance
   * @param indexPath Path to the JSON index file
   */
  constructor(indexPath: string) {
    this.indexPath = indexPath;
    this.index = {};
  }

  /**
   * Ensures the index is loaded from disk
   * Creates a new index file if it doesn't exist
   */
  private async ensureLoaded(): Promise<void> {
    if (this.loaded) {
      return;
    }

    try {
      // Ensure the directory exists
      const dir = path.dirname(this.indexPath);
      await fs.mkdir(dir, { recursive: true });

      // Try to read the index file
      const content = await fs.readFile(this.indexPath, 'utf-8');
      const parsed = JSON.parse(content);
      
      // Convert date strings back to Date objects
      this.index = this.deserializeIndex(parsed);
      this.loaded = true;
    } catch (error: any) {
      // If file doesn't exist or is invalid, start with empty index
      if (error.code === 'ENOENT') {
        this.index = {};
        this.loaded = true;
        await this.saveIndex();
      } else {
        // For other errors (parse errors, etc.), start fresh
        this.index = {};
        this.loaded = true;
        await this.saveIndex();
      }
    }
  }

  /**
   * Saves the current index to disk
   */
  private async saveIndex(): Promise<void> {
    // Ensure the directory exists
    const dir = path.dirname(this.indexPath);
    await fs.mkdir(dir, { recursive: true });
    
    const serialized = this.serializeIndex(this.index);
    await fs.writeFile(this.indexPath, JSON.stringify(serialized, null, 2), 'utf-8');
  }

  /**
   * Serializes the index for JSON storage
   * Converts Date objects to ISO strings
   */
  private serializeIndex(index: ProcessedEmailIndex): any {
    const serialized: any = {};
    for (const [emailId, entry] of Object.entries(index)) {
      serialized[emailId] = {
        filename: entry.filename,
        processedAt: entry.processedAt.toISOString(),
        priority: entry.priority
      };
    }
    return serialized;
  }

  /**
   * Deserializes the index from JSON storage
   * Converts ISO strings back to Date objects
   */
  private deserializeIndex(serialized: any): ProcessedEmailIndex {
    const index: ProcessedEmailIndex = {};
    for (const [emailId, entry] of Object.entries(serialized)) {
      const e = entry as any;
      index[emailId] = {
        filename: e.filename,
        processedAt: new Date(e.processedAt),
        priority: e.priority as PriorityLevel
      };
    }
    return index;
  }

  /**
   * Checks if an email has already been processed
   * @param emailId Gmail message ID
   * @returns true if email has been processed, false otherwise
   * 
   * Requirements: 10.1, 10.2
   */
  async isProcessed(emailId: string): Promise<boolean> {
    await this.ensureLoaded();
    return emailId in this.index;
  }

  /**
   * Marks an email as processed
   * @param emailId Gmail message ID
   * @param filename Generated markdown filename
   * @param priority Priority level assigned to the email
   * 
   * Requirements: 10.4
   */
  async markProcessed(emailId: string, filename: string, priority: PriorityLevel = 'medium'): Promise<void> {
    await this.ensureLoaded();
    
    this.index[emailId] = {
      filename,
      processedAt: new Date(),
      priority
    };
    
    await this.saveIndex();
  }

  /**
   * Rebuilds the index by scanning markdown files in the specified folder
   * Extracts email IDs from frontmatter
   * @param folder Path to the folder containing markdown files
   * 
   * Requirements: 10.5
   */
  async rebuildIndex(folder: string): Promise<void> {
    this.index = {};
    this.loaded = true;

    try {
      // Read all files in the folder
      const files = await fs.readdir(folder);
      
      // Filter for markdown files
      const markdownFiles = files.filter(file => file.endsWith('.md'));
      
      // Process each markdown file
      for (const file of markdownFiles) {
        const filePath = path.join(folder, file);
        try {
          const content = await fs.readFile(filePath, 'utf-8');
          
          // Extract frontmatter
          const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
          if (frontmatterMatch) {
            const frontmatter = frontmatterMatch[1];
            
            // Extract email_id
            const emailIdMatch = frontmatter.match(/email_id:\s*"([^"]+)"/);
            if (emailIdMatch) {
              const emailId = emailIdMatch[1];
              
              // Extract priority (default to medium if not found)
              const priorityMatch = frontmatter.match(/priority:\s*"([^"]+)"/);
              const priority = (priorityMatch ? priorityMatch[1] : 'medium') as PriorityLevel;
              
              // Extract processed_at (use file modification time if not found)
              const processedAtMatch = frontmatter.match(/processed_at:\s*"([^"]+)"/);
              let processedAt: Date;
              if (processedAtMatch) {
                processedAt = new Date(processedAtMatch[1]);
              } else {
                // Fallback to file stats
                const stats = await fs.stat(filePath);
                processedAt = stats.mtime;
              }
              
              // Add to index
              this.index[emailId] = {
                filename: file,
                processedAt,
                priority
              };
            }
          }
        } catch (error) {
          // Skip files that can't be read or parsed
          continue;
        }
      }
      
      // Save the rebuilt index
      await this.saveIndex();
    } catch (error) {
      // If folder doesn't exist or can't be read, start with empty index
      this.index = {};
      await this.saveIndex();
    }
  }

  /**
   * Gets the entry for a processed email
   * @param emailId Gmail message ID
   * @returns ProcessedEmailEntry if found, undefined otherwise
   */
  async getEntry(emailId: string): Promise<ProcessedEmailEntry | undefined> {
    await this.ensureLoaded();
    return this.index[emailId];
  }

  /**
   * Gets all processed email IDs
   * @returns Array of email IDs
   */
  async getAllEmailIds(): Promise<string[]> {
    await this.ensureLoaded();
    return Object.keys(this.index);
  }

  /**
   * Clears the entire index
   * Useful for testing or resetting state
   */
  async clear(): Promise<void> {
    this.index = {};
    this.loaded = true;
    await this.saveIndex();
  }
}
