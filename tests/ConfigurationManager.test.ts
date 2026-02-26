/**
 * Unit tests for ConfigurationManager
 * Tests configuration loading, validation, and default values
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { ConfigurationManager } from '../src/components/ConfigurationManager';
import * as fs from 'fs/promises';
import * as path from 'path';

describe('ConfigurationManager', () => {
  let configManager: ConfigurationManager;
  const testConfigDir = path.join(__dirname, 'test-configs');
  
  beforeEach(async () => {
    configManager = new ConfigurationManager();
    // Create test config directory
    await fs.mkdir(testConfigDir, { recursive: true });
  });
  
  afterEach(async () => {
    // Clean up test config directory
    try {
      await fs.rm(testConfigDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });
  
  describe('getDefaultConfig', () => {
    it('should return valid default configuration', () => {
      const config = configManager.getDefaultConfig();
      
      expect(config.pollingIntervalMs).toBe(300000);
      expect(config.needsActionFolder).toBe('Needs_Action');
      expect(config.logFolder).toBe('.logs');
      expect(config.importanceCriteria.logicMode).toBe('OR');
      expect(config.rateLimitConfig.maxRequestsPerMinute).toBe(60);
    });
    
    it('should include default importance criteria', () => {
      const config = configManager.getDefaultConfig();
      
      expect(config.importanceCriteria.keywordPatterns).toContain('urgent');
      expect(config.importanceCriteria.keywordPatterns).toContain('important');
      expect(config.importanceCriteria.requiredLabels).toContain('IMPORTANT');
    });
    
    it('should include default priority rules', () => {
      const config = configManager.getDefaultConfig();
      
      expect(config.priorityRules.highPriorityKeywords).toContain('urgent');
      expect(config.priorityRules.highPriorityKeywords).toContain('critical');
      expect(config.priorityRules.highPriorityLabels).toContain('IMPORTANT');
    });
  });
  
  describe('validateConfig', () => {
    it('should validate correct configuration', () => {
      const validConfig = configManager.getDefaultConfig();
      const result = configManager.validateConfig(validConfig);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
    
    it('should reject null configuration', () => {
      const result = configManager.validateConfig(null);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });
    
    it('should reject configuration with invalid pollingIntervalMs', () => {
      const invalidConfig = {
        ...configManager.getDefaultConfig(),
        pollingIntervalMs: -1
      };
      const result = configManager.validateConfig(invalidConfig);
      
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('pollingIntervalMs'))).toBe(true);
    });
    
    it('should reject configuration missing required fields', () => {
      const invalidConfig = {
        pollingIntervalMs: 300000
        // Missing other required fields
      };
      const result = configManager.validateConfig(invalidConfig);
      
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });
  });
  
  describe('loadConfig', () => {
    it('should load valid YAML configuration', async () => {
      const configPath = path.join(testConfigDir, 'valid-config.yaml');
      const yamlContent = `
pollingIntervalMs: 600000
importanceCriteria:
  senderWhitelist:
    - test@example.com
  keywordPatterns:
    - urgent
  requiredLabels:
    - IMPORTANT
  logicMode: OR
priorityRules:
  highPriorityKeywords:
    - urgent
  vipSenders: []
  highPriorityLabels:
    - IMPORTANT
  mediumPriorityKeywords: []
rateLimitConfig:
  maxRequestsPerMinute: 60
  maxRequestsPerDay: 10000
  initialBackoffMs: 1000
  maxBackoffMs: 60000
  backoffMultiplier: 2
needsActionFolder: Needs_Action
logFolder: .logs
`;
      await fs.writeFile(configPath, yamlContent, 'utf-8');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config.pollingIntervalMs).toBe(600000);
      expect(config.importanceCriteria.senderWhitelist).toContain('test@example.com');
    });
    
    it('should load valid JSON configuration', async () => {
      const configPath = path.join(testConfigDir, 'valid-config.json');
      const defaultConfig = configManager.getDefaultConfig();
      await fs.writeFile(configPath, JSON.stringify(defaultConfig, null, 2), 'utf-8');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config.pollingIntervalMs).toBe(defaultConfig.pollingIntervalMs);
    });
    
    it('should return default config when file is missing', async () => {
      const configPath = path.join(testConfigDir, 'nonexistent.yaml');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config.pollingIntervalMs).toBe(300000);
      expect(config).toEqual(configManager.getDefaultConfig());
    });
    
    it('should return default config when file is malformed YAML', async () => {
      const configPath = path.join(testConfigDir, 'malformed.yaml');
      await fs.writeFile(configPath, 'invalid: yaml: content: [', 'utf-8');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config).toEqual(configManager.getDefaultConfig());
    });
    
    it('should return default config when file is malformed JSON', async () => {
      const configPath = path.join(testConfigDir, 'malformed.json');
      await fs.writeFile(configPath, '{ invalid json }', 'utf-8');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config).toEqual(configManager.getDefaultConfig());
    });
    
    it('should return default config when validation fails', async () => {
      const configPath = path.join(testConfigDir, 'invalid-config.yaml');
      const invalidYaml = `
pollingIntervalMs: -1
needsActionFolder: test
`;
      await fs.writeFile(configPath, invalidYaml, 'utf-8');
      
      const config = await configManager.loadConfig(configPath);
      
      expect(config).toEqual(configManager.getDefaultConfig());
    });
  });
});
