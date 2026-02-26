/**
 * Configuration Manager for Gmail Watcher Agent Skill
 * Handles loading, validating, and providing default configuration
 */

import * as fs from 'fs/promises';
import * as yaml from 'js-yaml';
import * as path from 'path';
import {
  WatcherConfig,
  ImportanceCriteria,
  PriorityRules,
  RateLimitConfig,
  isValidWatcherConfig
} from '../models/Config';
import { ConfigurationError } from '../models/Errors';

/**
 * Validation result for configuration
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Configuration Manager class
 * Responsible for loading, validating, and providing configuration
 */
export class ConfigurationManager {
  /**
   * Load configuration from a file
   * Supports both YAML and JSON formats
   * Returns default config if file is missing or malformed
   * 
   * @param configPath - Path to configuration file
   * @returns Promise resolving to WatcherConfig
   */
  async loadConfig(configPath: string): Promise<WatcherConfig> {
    try {
      // Check if file exists
      await fs.access(configPath);
      
      // Read file content
      const fileContent = await fs.readFile(configPath, 'utf-8');
      
      // Parse based on file extension
      const ext = path.extname(configPath).toLowerCase();
      let config: any;
      
      if (ext === '.yaml' || ext === '.yml') {
        config = yaml.load(fileContent);
      } else if (ext === '.json') {
        config = JSON.parse(fileContent);
      } else {
        throw new ConfigurationError(
          `Unsupported configuration file format: ${ext}. Use .yaml, .yml, or .json`
        );
      }
      
      // Validate the parsed configuration
      const validationResult = this.validateConfig(config);
      
      if (!validationResult.valid) {
        console.warn(
          `Configuration validation failed: ${validationResult.errors.join(', ')}. Using default configuration.`
        );
        return this.getDefaultConfig();
      }
      
      return config as WatcherConfig;
      
    } catch (error) {
      // Handle file not found
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        console.warn(
          `Configuration file not found at ${configPath}. Using default configuration.`
        );
        return this.getDefaultConfig();
      }
      
      // Handle parse errors
      if (error instanceof SyntaxError || error instanceof yaml.YAMLException) {
        console.warn(
          `Configuration file is malformed: ${(error as Error).message}. Using default configuration.`
        );
        return this.getDefaultConfig();
      }
      
      // Handle configuration errors
      if (error instanceof ConfigurationError) {
        console.warn(`${(error as Error).message}. Using default configuration.`);
        return this.getDefaultConfig();
      }
      
      // Re-throw unexpected errors
      throw error;
    }
  }

  /**
   * Validate configuration structure and values
   * 
   * @param config - Configuration object to validate
   * @returns ValidationResult with valid flag and error messages
   */
  validateConfig(config: any): ValidationResult {
    const errors: string[] = [];
    
    // Check if config is an object
    if (typeof config !== 'object' || config === null) {
      errors.push('Configuration must be an object');
      return { valid: false, errors };
    }
    
    // Use type guard for comprehensive validation
    if (!isValidWatcherConfig(config)) {
      // Detailed validation for better error messages
      if (typeof config.pollingIntervalMs !== 'number' || config.pollingIntervalMs <= 0) {
        errors.push('pollingIntervalMs must be a positive number');
      }
      
      if (!config.importanceCriteria) {
        errors.push('importanceCriteria is required');
      }
      
      if (!config.priorityRules) {
        errors.push('priorityRules is required');
      }
      
      if (!config.rateLimitConfig) {
        errors.push('rateLimitConfig is required');
      }
      
      if (typeof config.needsActionFolder !== 'string') {
        errors.push('needsActionFolder must be a string');
      }
      
      if (typeof config.logFolder !== 'string') {
        errors.push('logFolder must be a string');
      }
      
      return { valid: false, errors };
    }
    
    return { valid: true, errors: [] };
  }

  /**
   * Get default configuration with sensible values
   * Used when configuration file is missing or invalid
   * 
   * @returns Default WatcherConfig
   */
  getDefaultConfig(): WatcherConfig {
    const defaultImportanceCriteria: ImportanceCriteria = {
      senderWhitelist: [],
      keywordPatterns: ['urgent', 'important', 'action required'],
      requiredLabels: ['IMPORTANT'],
      logicMode: 'OR'
    };
    
    const defaultPriorityRules: PriorityRules = {
      highPriorityKeywords: ['urgent', 'asap', 'critical', 'emergency'],
      vipSenders: [],
      highPriorityLabels: ['IMPORTANT', 'STARRED'],
      mediumPriorityKeywords: ['follow up', 'reminder', 'deadline']
    };
    
    const defaultRateLimitConfig: RateLimitConfig = {
      maxRequestsPerMinute: 60,
      maxRequestsPerDay: 10000,
      initialBackoffMs: 1000,
      maxBackoffMs: 60000,
      backoffMultiplier: 2
    };
    
    return {
      pollingIntervalMs: 300000, // 5 minutes
      importanceCriteria: defaultImportanceCriteria,
      priorityRules: defaultPriorityRules,
      rateLimitConfig: defaultRateLimitConfig,
      needsActionFolder: 'Needs_Action',
      logFolder: '.logs'
    };
  }
}
