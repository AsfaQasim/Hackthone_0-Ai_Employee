/**
 * Task Validator Component
 * 
 * Validates task files before they are added to the assignment queue.
 * Checks required metadata fields, priority values, task types, and YAML syntax.
 * 
 * Requirements: 18.1, 18.2, 18.3, 18.4, 18.5
 */

import * as yaml from 'js-yaml';
import { isValidTaskPriority, type TaskPriority } from '../models/TaskMetadata';

export interface ValidationError {
  field: string;
  message: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}

export interface TaskValidatorConfig {
  requiredFields?: string[];
  registeredTaskTypes?: string[];
  allowUnregisteredTypes?: boolean;
}

export class TaskValidator {
  private config: TaskValidatorConfig;

  constructor(config: TaskValidatorConfig = {}) {
    this.config = {
      requiredFields: config.requiredFields || ['taskId'],
      registeredTaskTypes: config.registeredTaskTypes || [],
      allowUnregisteredTypes: config.allowUnregisteredTypes !== false // Default to true
    };
  }

  /**
   * Validate a task file's content
   * Requirements: 18.1, 18.2, 18.5
   */
  validateTaskFile(fileContent: string): ValidationResult {
    const errors: ValidationError[] = [];

    // First, validate YAML syntax
    const yamlResult = this.validateYAML(fileContent);
    if (!yamlResult.valid) {
      return yamlResult;
    }

    // Extract and parse frontmatter
    const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      errors.push({
        field: 'frontmatter',
        message: 'Task file missing frontmatter section'
      });
      return { valid: false, errors };
    }

    let frontmatter: any;
    try {
      frontmatter = yaml.load(frontmatterMatch[1]);
    } catch (error) {
      // This should have been caught by validateYAML, but handle it anyway
      errors.push({
        field: 'frontmatter',
        message: `Failed to parse frontmatter: ${(error as Error).message}`
      });
      return { valid: false, errors };
    }

    // Validate metadata
    const metadataResult = this.validateTaskMetadata(frontmatter);
    errors.push(...metadataResult.errors);

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate task metadata object
   * Requirements: 18.1, 18.2
   */
  validateTaskMetadata(metadata: any): ValidationResult {
    const errors: ValidationError[] = [];

    if (typeof metadata !== 'object' || metadata === null) {
      errors.push({
        field: 'metadata',
        message: 'Task metadata must be an object'
      });
      return { valid: false, errors };
    }

    // Check required fields
    for (const field of this.config.requiredFields || []) {
      if (!(field in metadata) || metadata[field] === null || metadata[field] === undefined) {
        errors.push({
          field,
          message: `Required field '${field}' is missing`
        });
      }
    }

    // Validate priority if present
    if ('priority' in metadata && metadata.priority !== null && metadata.priority !== undefined) {
      const priorityResult = this.validatePriority(metadata.priority);
      errors.push(...priorityResult.errors);
    }

    // Validate task type if present
    if ('taskType' in metadata && metadata.taskType !== null && metadata.taskType !== undefined) {
      const taskTypeResult = this.validateTaskType(metadata.taskType);
      errors.push(...taskTypeResult.errors);
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate priority value
   * Requirements: 18.3
   */
  validatePriority(priority: any): ValidationResult {
    const errors: ValidationError[] = [];

    if (typeof priority !== 'string') {
      errors.push({
        field: 'priority',
        message: 'Priority must be a string'
      });
      return { valid: false, errors };
    }

    if (!isValidTaskPriority(priority)) {
      errors.push({
        field: 'priority',
        message: `Invalid priority value '${priority}'. Must be one of: critical, high, medium, low`
      });
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate task type against registered types
   * Requirements: 18.4
   */
  validateTaskType(taskType: any): ValidationResult {
    const errors: ValidationError[] = [];

    if (typeof taskType !== 'string') {
      errors.push({
        field: 'taskType',
        message: 'Task type must be a string'
      });
      return { valid: false, errors };
    }

    // Only validate against registered types if we have them and aren't allowing unregistered types
    if (!this.config.allowUnregisteredTypes && 
        this.config.registeredTaskTypes && 
        this.config.registeredTaskTypes.length > 0) {
      if (!this.config.registeredTaskTypes.includes(taskType)) {
        errors.push({
          field: 'taskType',
          message: `Task type '${taskType}' is not registered. Registered types: ${this.config.registeredTaskTypes.join(', ')}`
        });
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate YAML syntax
   * Requirements: 18.5
   */
  validateYAML(content: string): ValidationResult {
    const errors: ValidationError[] = [];

    // Extract frontmatter section
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      // No frontmatter found - this is handled by validateTaskFile
      return { valid: true, errors: [] };
    }

    try {
      yaml.load(frontmatterMatch[1]);
    } catch (error) {
      errors.push({
        field: 'yaml',
        message: `Invalid YAML syntax: ${(error as Error).message}`
      });
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Update validator configuration
   */
  updateConfig(config: Partial<TaskValidatorConfig>): void {
    this.config = {
      ...this.config,
      ...config
    };
  }

  /**
   * Get current configuration
   */
  getConfig(): TaskValidatorConfig {
    return { ...this.config };
  }
}
