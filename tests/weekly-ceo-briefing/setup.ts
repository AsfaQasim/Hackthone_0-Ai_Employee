/**
 * Test setup and utilities for Weekly CEO Briefing tests
 */

import { describe, it, expect } from 'vitest';
import * as fc from 'fast-check';

/**
 * Helper to run property-based tests with consistent configuration
 */
export function testProperty(
  description: string,
  property: fc.IProperty<unknown>,
  params?: fc.Parameters<unknown>
) {
  it(description, () => {
    fc.assert(property, {
      numRuns: 100,
      ...params,
    });
  });
}

/**
 * Helper to create test suites for properties
 */
export function propertyTestSuite(
  suiteName: string,
  tests: () => void
) {
  describe(suiteName, tests);
}
