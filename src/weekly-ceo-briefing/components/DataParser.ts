import {
  RawFinancialData,
  RawTask,
  FinancialRecord,
  Task,
  ValidationResult,
} from '../types';

/**
 * DataParser module handles parsing raw data into structured objects
 * Implements Requirement 7.3: Date parsing with error handling
 * Implements Requirements 7.1, 7.2, 7.4, 7.5: Data validation
 */
export class DataParser {
  /**
   * Parses raw financial data into FinancialRecord objects
   * Converts date strings to Date objects with error handling
   * Converts string numbers to actual numbers
   */
  parseFinancialData(rawData: RawFinancialData[]): FinancialRecord[] {
    const parsed: FinancialRecord[] = [];

    for (const raw of rawData) {
      try {
        const record: FinancialRecord = {
          date: this.parseDate(raw.date),
          category: raw.category,
          revenue: typeof raw.revenue === 'string' ? parseFloat(raw.revenue) : raw.revenue,
          expenses: typeof raw.expenses === 'string' ? parseFloat(raw.expenses) : raw.expenses,
          description: raw.description,
        };

        parsed.push(record);
      } catch (error) {
        // Skip records that fail to parse
        // Validation will handle logging in the next step
        continue;
      }
    }

    return parsed;
  }

  /**
   * Parses raw task data into Task objects
   * Converts date strings to Date objects with error handling
   * Converts string durations to numbers
   */
  parseTaskData(rawData: RawTask[]): Task[] {
    const parsed: Task[] = [];

    for (const raw of rawData) {
      try {
        const task: Task = {
          id: raw.id,
          title: raw.title,
          completedDate: this.parseDate(raw.completedDate),
          expectedDuration: typeof raw.expectedDuration === 'string' 
            ? parseFloat(raw.expectedDuration) 
            : raw.expectedDuration,
          actualDuration: typeof raw.actualDuration === 'string' 
            ? parseFloat(raw.actualDuration) 
            : raw.actualDuration,
          blockers: raw.blockers,
          relatedGoals: raw.relatedGoals,
        };

        parsed.push(task);
      } catch (error) {
        // Skip tasks that fail to parse
        // Validation will handle logging in the next step
        continue;
      }
    }

    return parsed;
  }

  /**
   * Parses date strings to ISO format Date objects
   * Supports multiple date formats:
   * - ISO 8601 (YYYY-MM-DD, YYYY-MM-DDTHH:mm:ss.sssZ)
   * - MM/DD/YYYY
   * - DD-MM-YYYY
   * - YYYY/MM/DD
   * 
   * Requirement 7.3: Parse dates to ISO format with error handling
   * 
   * @throws Error if date format is not recognized or invalid
   */
  parseDate(dateString: string): Date {
    // Try parsing as ISO 8601 first (most common)
    const isoDate = new Date(dateString);
    if (!isNaN(isoDate.getTime())) {
      return isoDate;
    }

    // Try MM/DD/YYYY format
    const mmddyyyyMatch = dateString.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    if (mmddyyyyMatch) {
      const [, month, day, year] = mmddyyyyMatch;
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
      if (!isNaN(date.getTime())) {
        return date;
      }
    }

    // Try DD-MM-YYYY format
    const ddmmyyyyMatch = dateString.match(/^(\d{1,2})-(\d{1,2})-(\d{4})$/);
    if (ddmmyyyyMatch) {
      const [, day, month, year] = ddmmyyyyMatch;
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
      if (!isNaN(date.getTime())) {
        return date;
      }
    }

    // Try YYYY/MM/DD format
    const yyyymmddMatch = dateString.match(/^(\d{4})\/(\d{1,2})\/(\d{1,2})$/);
    if (yyyymmddMatch) {
      const [, year, month, day] = yyyymmddMatch;
      const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
      if (!isNaN(date.getTime())) {
        return date;
      }
    }

    // If no format matched, throw error
    throw new Error(`Unable to parse date: ${dateString}`);
  }

  /**
   * Validates a financial record for data integrity
   * Requirements 7.1, 7.2: Revenue and expense values must be non-negative
   * Requirement 7.4: Log warnings for invalid data
   * Requirement 7.5: Exclude invalid records from results
   * 
   * @param record The financial record to validate
   * @returns ValidationResult indicating if the record is valid
   */
  validateFinancialRecord(record: FinancialRecord): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Validate revenue is non-negative (Requirement 7.1)
    if (record.revenue < 0) {
      errors.push(`Revenue must be non-negative, got ${record.revenue}`);
    }

    // Validate expenses are non-negative (Requirement 7.2)
    if (record.expenses < 0) {
      errors.push(`Expenses must be non-negative, got ${record.expenses}`);
    }

    // Validate revenue and expenses are valid numbers
    if (isNaN(record.revenue)) {
      errors.push(`Revenue must be a valid number, got ${record.revenue}`);
    }

    if (isNaN(record.expenses)) {
      errors.push(`Expenses must be a valid number, got ${record.expenses}`);
    }

    // Validate date is valid
    if (isNaN(record.date.getTime())) {
      errors.push(`Date is invalid`);
    }

    // Log warnings for invalid data (Requirement 7.4)
    if (errors.length > 0) {
      const warningMessage = `Invalid financial record for ${record.category} on ${record.date}: ${errors.join(', ')}`;
      console.warn(warningMessage);
      warnings.push(warningMessage);
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Validates a task for required fields and data integrity
   * Requirement 7.4: Log warnings for invalid data
   * Requirement 7.5: Exclude invalid records from results
   * 
   * @param task The task to validate
   * @returns ValidationResult indicating if the task is valid
   */
  validateTask(task: Task): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Validate required fields
    if (!task.id || task.id.trim() === '') {
      errors.push('Task ID is required');
    }

    if (!task.title || task.title.trim() === '') {
      errors.push('Task title is required');
    }

    // Validate durations are non-negative
    if (task.expectedDuration < 0) {
      errors.push(`Expected duration must be non-negative, got ${task.expectedDuration}`);
    }

    if (task.actualDuration < 0) {
      errors.push(`Actual duration must be non-negative, got ${task.actualDuration}`);
    }

    // Validate durations are valid numbers
    if (isNaN(task.expectedDuration)) {
      errors.push(`Expected duration must be a valid number, got ${task.expectedDuration}`);
    }

    if (isNaN(task.actualDuration)) {
      errors.push(`Actual duration must be a valid number, got ${task.actualDuration}`);
    }

    // Validate date is valid
    if (isNaN(task.completedDate.getTime())) {
      errors.push(`Completed date is invalid`);
    }

    // Validate arrays are present
    if (!Array.isArray(task.blockers)) {
      errors.push('Blockers must be an array');
    }

    if (!Array.isArray(task.relatedGoals)) {
      errors.push('Related goals must be an array');
    }

    // Log warnings for invalid data (Requirement 7.4)
    if (errors.length > 0) {
      const warningMessage = `Invalid task ${task.id} - ${task.title}: ${errors.join(', ')}`;
      console.warn(warningMessage);
      warnings.push(warningMessage);
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }
}
