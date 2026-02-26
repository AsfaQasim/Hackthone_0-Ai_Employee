import * as fs from 'fs';
import * as path from 'path';
import {
  RawFinancialData,
  RawTask,
  BusinessGoals,
  Response,
  Warning,
} from '../types';

/**
 * DataIngestion module handles loading raw data from file system sources
 * Implements Requirements 1.1, 1.2, 1.3, 1.4, 1.5
 */
export class DataIngestion {
  private warnings: Warning[] = [];

  /**
   * Ingests all financial data files from the accounting folder
   * Requirement 1.1: Read all files from Accounting_Folder
   * Requirement 1.4: Return error if folder is missing
   * Requirement 1.5: Log errors for unreadable files but continue
   */
  ingestAccountingData(folderPath: string): Response<RawFinancialData[]> {
    this.warnings = [];

    // Check if folder exists
    if (!fs.existsSync(folderPath)) {
      return {
        success: false,
        error: {
          type: 'MISSING_FOLDER',
          message: `Accounting folder not found: ${folderPath}`,
          details: { folderPath, folderType: 'accounting' },
        },
        warnings: this.warnings,
      };
    }

    // Check if it's a directory
    const stats = fs.statSync(folderPath);
    if (!stats.isDirectory()) {
      return {
        success: false,
        error: {
          type: 'MISSING_FOLDER',
          message: `Path is not a directory: ${folderPath}`,
          details: { folderPath, folderType: 'accounting' },
        },
        warnings: this.warnings,
      };
    }

    const allData: RawFinancialData[] = [];
    const files = fs.readdirSync(folderPath);

    for (const file of files) {
      const filePath = path.join(folderPath, file);
      
      try {
        const fileStats = fs.statSync(filePath);
        
        // Skip directories
        if (fileStats.isDirectory()) {
          continue;
        }

        // Only process JSON files
        if (!file.endsWith('.json')) {
          continue;
        }

        const content = fs.readFileSync(filePath, 'utf-8');
        const data = JSON.parse(content);

        // Handle both single record and array of records
        if (Array.isArray(data)) {
          allData.push(...data);
        } else {
          allData.push(data);
        }
      } catch (error) {
        // Log error but continue processing (Requirement 1.5)
        this.warnings.push({
          type: 'FILE_READ_ERROR',
          message: `Failed to read file: ${file}`,
          context: {
            filePath,
            error: error instanceof Error ? error.message : String(error),
          },
        });
      }
    }

    return {
      success: true,
      data: allData,
      warnings: this.warnings,
    };
  }

  /**
   * Ingests all completed task files from the done folder
   * Requirement 1.2: Read all files from Done_Folder
   * Requirement 1.4: Return error if folder is missing
   * Requirement 1.5: Log errors for unreadable files but continue
   */
  ingestCompletedTasks(folderPath: string): Response<RawTask[]> {
    this.warnings = [];

    // Check if folder exists
    if (!fs.existsSync(folderPath)) {
      return {
        success: false,
        error: {
          type: 'MISSING_FOLDER',
          message: `Done folder not found: ${folderPath}`,
          details: { folderPath, folderType: 'done' },
        },
        warnings: this.warnings,
      };
    }

    // Check if it's a directory
    const stats = fs.statSync(folderPath);
    if (!stats.isDirectory()) {
      return {
        success: false,
        error: {
          type: 'MISSING_FOLDER',
          message: `Path is not a directory: ${folderPath}`,
          details: { folderPath, folderType: 'done' },
        },
        warnings: this.warnings,
      };
    }

    const allTasks: RawTask[] = [];
    const files = fs.readdirSync(folderPath);

    for (const file of files) {
      const filePath = path.join(folderPath, file);
      
      try {
        const fileStats = fs.statSync(filePath);
        
        // Skip directories
        if (fileStats.isDirectory()) {
          continue;
        }

        // Only process JSON files
        if (!file.endsWith('.json')) {
          continue;
        }

        const content = fs.readFileSync(filePath, 'utf-8');
        const data = JSON.parse(content);

        // Handle both single task and array of tasks
        if (Array.isArray(data)) {
          allTasks.push(...data);
        } else {
          allTasks.push(data);
        }
      } catch (error) {
        // Log error but continue processing (Requirement 1.5)
        this.warnings.push({
          type: 'FILE_READ_ERROR',
          message: `Failed to read file: ${file}`,
          context: {
            filePath,
            error: error instanceof Error ? error.message : String(error),
          },
        });
      }
    }

    return {
      success: true,
      data: allTasks,
      warnings: this.warnings,
    };
  }

  /**
   * Loads business goals configuration from a file
   * Requirement 1.3: Load Business_Goals configuration
   * Requirement 1.4: Return error if file is missing
   */
  loadBusinessGoals(configPath: string): Response<BusinessGoals> {
    this.warnings = [];

    // Check if file exists
    if (!fs.existsSync(configPath)) {
      return {
        success: false,
        error: {
          type: 'INVALID_CONFIG',
          message: `Configuration file not found: ${configPath}`,
          details: { configPath },
        },
        warnings: this.warnings,
      };
    }

    try {
      const content = fs.readFileSync(configPath, 'utf-8');
      const config = JSON.parse(content) as BusinessGoals;

      // Basic validation of structure
      if (!config.goals || !Array.isArray(config.goals)) {
        return {
          success: false,
          error: {
            type: 'INVALID_CONFIG',
            message: 'Configuration file missing required "goals" array',
            details: { configPath },
          },
          warnings: this.warnings,
        };
      }

      if (!config.budgets || !Array.isArray(config.budgets)) {
        return {
          success: false,
          error: {
            type: 'INVALID_CONFIG',
            message: 'Configuration file missing required "budgets" array',
            details: { configPath },
          },
          warnings: this.warnings,
        };
      }

      if (!config.thresholds || typeof config.thresholds !== 'object') {
        return {
          success: false,
          error: {
            type: 'INVALID_CONFIG',
            message: 'Configuration file missing required "thresholds" object',
            details: { configPath },
          },
          warnings: this.warnings,
        };
      }

      return {
        success: true,
        data: config,
        warnings: this.warnings,
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'INVALID_CONFIG',
          message: `Failed to parse configuration file: ${error instanceof Error ? error.message : String(error)}`,
          details: {
            configPath,
            error: error instanceof Error ? error.message : String(error),
          },
        },
        warnings: this.warnings,
      };
    }
  }
}
