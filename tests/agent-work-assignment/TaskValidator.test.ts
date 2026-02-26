/**
 * Unit tests for TaskValidator
 * Tests validation of task metadata, priority, task type, and YAML syntax
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { TaskValidator } from '../../src/agent-work-assignment/components/TaskValidator';

describe('TaskValidator', () => {
  let validator: TaskValidator;

  beforeEach(() => {
    validator = new TaskValidator({
      requiredFields: ['taskId', 'priority'],
      registeredTaskTypes: ['email_processing', 'invoice_generation', 'social_media_post'],
      allowUnregisteredTypes: false
    });
  });

  describe('validateTaskFile', () => {
    it('should validate a well-formed task file', () => {
      const taskContent = `---
taskId: task_001
priority: high
taskType: email_processing
requiredCapabilities: [email, nlp]
---

# Task: Process Email
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject task file with missing frontmatter', () => {
      const taskContent = `# Task: Process Email

No frontmatter here!
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(false);
      expect(result.errors).toHaveLength(1);
      expect(result.errors[0].field).toBe('frontmatter');
      expect(result.errors[0].message).toContain('missing frontmatter');
    });

    it('should reject task file with invalid YAML', () => {
      const taskContent = `---
taskId: task_001
priority: high
  invalid: indentation
taskType: email_processing
---

# Task
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors[0].field).toBe('yaml');
    });

    it('should reject task file with missing required fields', () => {
      const taskContent = `---
priority: high
taskType: email_processing
---

# Task
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.field === 'taskId')).toBe(true);
    });

    it('should reject task file with invalid priority', () => {
      const taskContent = `---
taskId: task_001
priority: super_urgent
taskType: email_processing
---

# Task
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.field === 'priority')).toBe(true);
    });

    it('should reject task file with unregistered task type', () => {
      const taskContent = `---
taskId: task_001
priority: high
taskType: unknown_type
---

# Task
`;

      const result = validator.validateTaskFile(taskContent);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.field === 'taskType')).toBe(true);
    });
  });

  describe('validateTaskMetadata', () => {
    it('should validate valid metadata', () => {
      const metadata = {
        taskId: 'task_001',
        priority: 'high',
        taskType: 'email_processing',
        requiredCapabilities: ['email']
      };

      const result = validator.validateTaskMetadata(metadata);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject non-object metadata', () => {
      const result = validator.validateTaskMetadata('not an object');
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('metadata');
    });

    it('should reject metadata missing required fields', () => {
      const metadata = {
        priority: 'high',
        taskType: 'email_processing'
      };

      const result = validator.validateTaskMetadata(metadata);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.field === 'taskId')).toBe(true);
    });

    it('should validate metadata with null required field', () => {
      const metadata = {
        taskId: null,
        priority: 'high'
      };

      const result = validator.validateTaskMetadata(metadata);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.field === 'taskId')).toBe(true);
    });
  });

  describe('validatePriority', () => {
    it('should accept valid priority values', () => {
      const priorities = ['critical', 'high', 'medium', 'low'];
      
      for (const priority of priorities) {
        const result = validator.validatePriority(priority);
        expect(result.valid).toBe(true);
        expect(result.errors).toHaveLength(0);
      }
    });

    it('should reject invalid priority values', () => {
      const result = validator.validatePriority('super_urgent');
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('priority');
      expect(result.errors[0].message).toContain('critical, high, medium, low');
    });

    it('should reject non-string priority', () => {
      const result = validator.validatePriority(123);
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('priority');
      expect(result.errors[0].message).toContain('must be a string');
    });
  });

  describe('validateTaskType', () => {
    it('should accept registered task types', () => {
      const result = validator.validateTaskType('email_processing');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject unregistered task types when not allowed', () => {
      const result = validator.validateTaskType('unknown_type');
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('taskType');
      expect(result.errors[0].message).toContain('not registered');
    });

    it('should accept unregistered task types when allowed', () => {
      const permissiveValidator = new TaskValidator({
        registeredTaskTypes: ['email_processing'],
        allowUnregisteredTypes: true
      });

      const result = permissiveValidator.validateTaskType('unknown_type');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject non-string task type', () => {
      const result = validator.validateTaskType(123);
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('taskType');
      expect(result.errors[0].message).toContain('must be a string');
    });

    it('should accept any task type when no registered types configured', () => {
      const noTypesValidator = new TaskValidator({
        registeredTaskTypes: [],
        allowUnregisteredTypes: false
      });

      const result = noTypesValidator.validateTaskType('any_type');
      expect(result.valid).toBe(true);
    });
  });

  describe('validateYAML', () => {
    it('should accept valid YAML frontmatter', () => {
      const content = `---
taskId: task_001
priority: high
---

# Task
`;

      const result = validator.validateYAML(content);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject invalid YAML syntax', () => {
      const content = `---
taskId: task_001
  invalid: indentation
priority: high
---

# Task
`;

      const result = validator.validateYAML(content);
      expect(result.valid).toBe(false);
      expect(result.errors[0].field).toBe('yaml');
    });

    it('should accept content without frontmatter', () => {
      const content = `# Task

Just a regular markdown file.
`;

      const result = validator.validateYAML(content);
      expect(result.valid).toBe(true);
    });
  });

  describe('configuration management', () => {
    it('should update configuration', () => {
      validator.updateConfig({
        allowUnregisteredTypes: true
      });

      const config = validator.getConfig();
      expect(config.allowUnregisteredTypes).toBe(true);
    });

    it('should preserve existing config when updating', () => {
      const originalTypes = validator.getConfig().registeredTaskTypes;
      
      validator.updateConfig({
        allowUnregisteredTypes: true
      });

      const config = validator.getConfig();
      expect(config.registeredTaskTypes).toEqual(originalTypes);
    });

    it('should use default configuration when not provided', () => {
      const defaultValidator = new TaskValidator();
      const config = defaultValidator.getConfig();

      expect(config.requiredFields).toEqual(['taskId']);
      expect(config.allowUnregisteredTypes).toBe(true);
    });
  });

  describe('edge cases', () => {
    it('should handle empty frontmatter', () => {
      const content = `---
---

# Task
`;

      const result = validator.validateTaskFile(content);
      expect(result.valid).toBe(false);
      // Empty frontmatter parses as null, which triggers metadata validation error
      expect(result.errors.length).toBeGreaterThan(0);
    });

    it('should handle frontmatter with only whitespace', () => {
      const content = `---
   
---

# Task
`;

      const result = validator.validateTaskFile(content);
      expect(result.valid).toBe(false);
    });

    it('should handle multiple validation errors', () => {
      const content = `---
priority: invalid_priority
taskType: unregistered_type
---

# Task
`;

      const result = validator.validateTaskFile(content);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(1);
    });
  });
});
