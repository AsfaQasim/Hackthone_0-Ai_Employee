# Implementation Plan: Next.js Dashboard UI

## Overview

This implementation plan breaks down the Next.js Dashboard UI into incremental coding tasks. The approach follows a bottom-up strategy: build core data layer components first, then service layer for business logic, then API routes, and finally UI components. Each task builds on previous work, with testing integrated throughout to validate functionality early.

## Tasks

- [ ] 1. Project setup and core infrastructure
  - Initialize Next.js 14+ project with TypeScript and App Router
  - Configure Tailwind CSS for styling
  - Set up Vitest for testing with fast-check for property-based tests
  - Create project directory structure (lib/, components/, app/, tests/)
  - Configure environment variables for vault path
  - _Requirements: 15.1_

- [ ] 2. Implement VaultReader for file system access
  - [ ] 2.1 Create VaultReader class with file discovery methods
    - Implement recursive directory traversal
    - Implement .md file filtering
    - Add error handling for file read failures
    - _Requirements: 1.1, 1.3, 1.4, 1.5_
  
  - [ ]* 2.2 Write property test for complete file discovery
    - **Property 1: Complete file discovery**
    - **Validates: Requirements 1.1, 1.4**
  
  - [ ]* 2.3 Write property test for extension filtering
    - **Property 2: Extension filtering**
    - **Validates: Requirements 1.5**
  
  - [ ]* 2.4 Write property test for error resilience
    - **Property 3: Error resilience**
    - **Validates: Requirements 1.3**
  
  - [ ]* 2.5 Write unit tests for edge cases
    - Test empty directory
    - Test deeply nested directories
    - Test permission errors
    - _Requirements: 1.1, 1.3, 1.4, 1.5_

- [ ] 3. Implement MarkdownParser for content extraction
  - [ ] 3.1 Create MarkdownParser class using gray-matter and remark
    - Implement frontmatter extraction
    - Implement content body extraction
    - Add graceful error handling for invalid YAML
    - Implement markdown-to-HTML conversion
    - _Requirements: 2.1, 2.2, 2.3, 2.5_
  
  - [ ]* 3.2 Write property test for frontmatter extraction
    - **Property 4: Frontmatter extraction**
    - **Validates: Requirements 2.1, 2.5**
  
  - [ ]* 3.3 Write property test for content extraction
    - **Property 5: Content extraction**
    - **Validates: Requirements 2.2, 2.5**
  
  - [ ]* 3.4 Write property test for graceful parsing failure
    - **Property 6: Graceful parsing failure**
    - **Validates: Requirements 2.3**
  
  - [ ]* 3.5 Write unit tests for parsing edge cases
    - Test file with no frontmatter
    - Test file with only frontmatter
    - Test malformed YAML
    - Test special characters in content
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 4. Implement MetricsAggregator for data analysis
  - [ ] 4.1 Create MetricsAggregator class with calculation methods
    - Implement total counts calculation (specs, skills, plans, logs)
    - Implement specs-by-status grouping
    - Implement date-based activity filtering
    - Implement email metrics calculation
    - Implement skill usage statistics
    - _Requirements: 3.1, 3.2, 3.3, 5.1, 5.2, 5.3, 5.4, 8.5_
  
  - [ ]* 4.2 Write property test for accurate metric calculation
    - **Property 7: Accurate metric calculation**
    - **Validates: Requirements 3.1, 3.2, 5.1, 5.2, 6.5**
  
  - [ ]* 4.3 Write property test for date-based activity filtering
    - **Property 8: Date-based activity filtering**
    - **Validates: Requirements 3.3**
  
  - [ ]* 4.4 Write property test for email metrics aggregation
    - **Property 13: Email metrics aggregation**
    - **Validates: Requirements 5.3**
  
  - [ ]* 4.5 Write property test for time-series aggregation
    - **Property 14: Time-series aggregation**
    - **Validates: Requirements 5.4**
  
  - [ ]* 4.6 Write unit tests for metrics edge cases
    - Test empty dataset
    - Test missing metadata fields
    - Test invalid date formats
    - _Requirements: 3.1, 3.2, 3.3, 5.1, 5.2, 5.3_

- [ ] 5. Implement DataCache for performance optimization
  - [ ] 5.1 Create DataCache class with get/set/invalidate methods
    - Implement in-memory cache with TTL support
    - Add cache key generation utilities
    - Implement cache invalidation logic
    - _Requirements: 14.1_
  
  - [ ]* 5.2 Write property test for cache hit avoids re-parsing
    - **Property 27: Cache hit avoids re-parsing**
    - **Validates: Requirements 14.1**
  
  - [ ]* 5.3 Write unit tests for cache behavior
    - Test cache expiration
    - Test cache invalidation
    - Test cache miss behavior
    - _Requirements: 14.1_

- [ ] 6. Checkpoint - Ensure data layer tests pass
  - Run all data layer tests (VaultReader, MarkdownParser, MetricsAggregator, DataCache)
  - Verify property tests run 100+ iterations
  - Ask the user if questions arise

- [ ] 7. Implement filtering and search utilities
  - [ ] 7.1 Create filtering utility functions
    - Implement multi-criteria filter (status, date, type, priority)
    - Implement folder-based filtering
    - Implement search across multiple fields
    - Implement sorting (priority, date, chronological)
    - _Requirements: 4.4, 6.1, 6.3, 7.1, 8.1, 11.1, 11.2, 11.4_
  
  - [ ]* 7.2 Write property test for multi-criteria filtering
    - **Property 12: Multi-criteria filtering**
    - **Validates: Requirements 4.4, 11.3, 11.4**
  
  - [ ]* 7.3 Write property test for folder filtering
    - **Property 15: Folder filtering**
    - **Validates: Requirements 6.1, 8.1**
  
  - [ ]* 7.4 Write property test for multi-field search
    - **Property 20: Multi-field search**
    - **Validates: Requirements 11.1, 11.2**
  
  - [ ]* 7.5 Write property test for priority and date sorting
    - **Property 16: Priority and date sorting**
    - **Validates: Requirements 6.3**
  
  - [ ]* 7.6 Write property test for filter clearing
    - **Property 21: Filter clearing**
    - **Validates: Requirements 11.5**

- [ ] 8. Implement VaultWatcher for live updates (optional feature)
  - [ ] 8.1 Create VaultWatcher class using chokidar
    - Implement file system watching
    - Implement change detection and callback triggering
    - Add start/stop methods
    - _Requirements: 12.4_
  
  - [ ]* 8.2 Write property test for file watcher change detection
    - **Property 25: File watcher change detection**
    - **Validates: Requirements 12.4**
  
  - [ ]* 8.3 Write unit tests for watcher behavior
    - Test file added event
    - Test file modified event
    - Test file deleted event
    - _Requirements: 12.4_

- [ ] 9. Implement API routes for data access
  - [ ] 9.1 Create GET /api/vault/metrics route
    - Integrate VaultReader, MarkdownParser, MetricsAggregator
    - Implement caching with DataCache
    - Add error handling
    - _Requirements: 3.1, 3.2, 3.3, 5.1, 5.2, 5.3, 5.4_
  
  - [ ] 9.2 Create GET /api/vault/specs route
    - Implement query parameter handling (status, search, folder)
    - Integrate filtering utilities
    - Add pagination support
    - _Requirements: 4.1, 4.2, 4.4_
  
  - [ ] 9.3 Create GET /api/vault/specs/[id] route
    - Implement single spec retrieval by path
    - Add error handling for not found
    - _Requirements: 4.2_
  
  - [ ] 9.4 Create GET /api/vault/skills route
    - Filter files from Skills folder
    - Include usage statistics
    - _Requirements: 8.1, 8.2, 8.4, 8.5_
  
  - [ ] 9.5 Create GET /api/vault/logs route
    - Implement pagination with limit/offset
    - Implement date range filtering
    - Sort chronologically
    - _Requirements: 7.1, 7.3, 7.4, 7.5_
  
  - [ ] 9.6 Create POST /api/vault/refresh route
    - Implement cache invalidation
    - Trigger data reload
    - _Requirements: 12.2, 12.3_
  
  - [ ]* 9.7 Write integration tests for API routes
    - Test each route with various query parameters
    - Test error responses
    - Test caching behavior
    - _Requirements: 3.1, 4.1, 7.1, 8.1, 12.3_

- [ ] 10. Checkpoint - Ensure API layer tests pass
  - Run all API route tests
  - Verify routes return correct data structures
  - Test error handling
  - Ask the user if questions arise

- [ ] 11. Create reusable UI components
  - [ ] 11.1 Create MetricCard component
    - Display single metric with label and value
    - Support different visual styles (color, icon)
    - _Requirements: 3.1, 3.2_
  
  - [ ] 11.2 Create SearchBar component
    - Input field with search icon
    - Debounced search input
    - Clear button
    - _Requirements: 11.1_
  
  - [ ] 11.3 Create FilterPanel component
    - Multi-select filters (status, type, priority)
    - Date range picker
    - Clear filters button
    - _Requirements: 11.4, 11.5_
  
  - [ ] 11.4 Create LoadingSpinner component
    - Animated loading indicator
    - _Requirements: 13.4_
  
  - [ ] 11.5 Create ErrorMessage component
    - Display error title and message
    - Optional action button
    - _Requirements: 13.1, 13.3_
  
  - [ ]* 11.6 Write unit tests for UI components
    - Test rendering with various props
    - Test user interactions
    - Test conditional display
    - _Requirements: 3.1, 11.1, 11.4, 13.1_

- [ ] 12. Implement Dashboard Overview page
  - [ ] 12.1 Create app/page.tsx (dashboard home)
    - Fetch metrics from API
    - Display metric cards for totals
    - Display specs-by-status breakdown
    - Display recent activity timeline
    - Add manual refresh button
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 12.2_
  
  - [ ]* 12.2 Write property test for reactive metric updates
    - **Property 9: Reactive metric updates**
    - **Validates: Requirements 3.4**
  
  - [ ]* 12.3 Write property test for data refresh triggers UI update
    - **Property 24: Data refresh triggers UI update**
    - **Validates: Requirements 12.3, 12.4, 12.5**
  
  - [ ]* 12.4 Write unit tests for dashboard page
    - Test loading state
    - Test error state
    - Test refresh button click
    - _Requirements: 3.1, 3.2, 12.2, 13.4_

- [ ] 13. Implement Specs Browser page
  - [ ] 13.1 Create app/specs/page.tsx
    - Fetch specs from API
    - Display specs grouped by folder
    - Integrate SearchBar and FilterPanel
    - Implement click to navigate to detail view
    - _Requirements: 4.1, 4.2, 4.4, 11.1, 11.4_
  
  - [ ]* 13.2 Write property test for folder-based grouping
    - **Property 10: Folder-based grouping**
    - **Validates: Requirements 4.1**
  
  - [ ]* 13.3 Write property test for required metadata rendering
    - **Property 11: Required metadata rendering**
    - **Validates: Requirements 4.2, 6.2, 7.2, 8.2**
  
  - [ ]* 13.4 Write unit tests for specs browser
    - Test filtering interaction
    - Test search interaction
    - Test navigation to detail
    - _Requirements: 4.1, 4.2, 4.4_

- [ ] 14. Implement Spec Detail page
  - [ ] 14.1 Create app/specs/[id]/page.tsx
    - Fetch single spec from API using encoded path
    - Display full metadata
    - Render markdown content as HTML
    - Add back navigation
    - _Requirements: 4.2_
  
  - [ ]* 14.2 Write unit tests for spec detail page
    - Test loading state
    - Test not found error
    - Test markdown rendering
    - _Requirements: 4.2, 13.1_

- [ ] 15. Implement Skills Library page
  - [ ] 15.1 Create app/skills/page.tsx
    - Fetch skills from API
    - Display skills with metadata
    - Integrate SearchBar
    - Sort by usage count
    - Implement click to view detail
    - _Requirements: 8.1, 8.2, 8.4, 8.5_
  
  - [ ]* 15.2 Write property test for skill usage statistics
    - **Property 30: Skill usage statistics**
    - **Validates: Requirements 8.5**
  
  - [ ]* 15.3 Write unit tests for skills page
    - Test search functionality
    - Test sorting by usage
    - Test navigation to detail
    - _Requirements: 8.1, 8.2, 8.4, 8.5_

- [ ] 16. Implement Activity Timeline page
  - [ ] 16.1 Create app/logs/page.tsx
    - Fetch logs from API with pagination
    - Display log entries chronologically
    - Implement filter by date range and action type
    - Implement "load more" pagination
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [ ]* 16.2 Write property test for chronological log ordering
    - **Property 17: Chronological log ordering**
    - **Validates: Requirements 7.1**
  
  - [ ]* 16.3 Write property test for log filtering
    - **Property 18: Log filtering**
    - **Validates: Requirements 7.3**
  
  - [ ]* 16.4 Write property test for incremental pagination
    - **Property 19: Incremental pagination**
    - **Validates: Requirements 7.5**
  
  - [ ]* 16.5 Write unit tests for activity timeline
    - Test initial load
    - Test filter application
    - Test load more button
    - _Requirements: 7.1, 7.3, 7.4, 7.5_

- [ ] 17. Implement Approval Queue page
  - [ ] 17.1 Create app/queue/page.tsx
    - Fetch specs from Pending_Approval folder
    - Display with priority and date
    - Sort by priority then date
    - Display count prominently
    - Implement click to view detail
    - _Requirements: 6.1, 6.2, 6.3, 6.5_
  
  - [ ]* 17.2 Write unit tests for approval queue
    - Test sorting behavior
    - Test count display
    - Test navigation to detail
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [ ] 18. Implement navigation and layout
  - [ ] 18.1 Create app/layout.tsx with navigation
    - Create sidebar navigation menu
    - Add links to all major sections (Home, Specs, Skills, Logs, Queue)
    - Highlight active section
    - Add header with logo and refresh button
    - _Requirements: 9.1, 9.2, 9.5_
  
  - [ ]* 18.2 Write property test for navigation state preservation
    - **Property 22: Navigation state preservation**
    - **Validates: Requirements 9.4**
  
  - [ ]* 18.3 Write unit tests for navigation
    - Test navigation links
    - Test active section highlighting
    - Test refresh button in header
    - _Requirements: 9.1, 9.2, 9.5_

- [ ] 19. Implement responsive design
  - [ ] 19.1 Add responsive CSS with Tailwind
    - Mobile layout (sidebar collapses to hamburger menu)
    - Tablet layout (optimized spacing)
    - Desktop layout (full sidebar)
    - Ensure no horizontal scrolling at any width
    - _Requirements: 10.1, 10.2, 10.3, 10.5_
  
  - [ ]* 19.2 Write property test for responsive layout adaptation
    - **Property 23: Responsive layout adaptation**
    - **Validates: Requirements 10.5**
  
  - [ ]* 19.3 Write unit tests for responsive behavior
    - Test mobile viewport rendering
    - Test tablet viewport rendering
    - Test desktop viewport rendering
    - _Requirements: 10.1, 10.2, 10.3_

- [ ] 20. Implement error handling and loading states
  - [ ] 20.1 Add error boundaries to pages
    - Wrap pages in error boundaries
    - Display ErrorMessage component on errors
    - Add retry functionality
    - _Requirements: 13.1, 13.2, 13.3_
  
  - [ ] 20.2 Add loading states to all data-fetching components
    - Display LoadingSpinner while fetching
    - Show skeleton loaders for lists
    - _Requirements: 13.4_
  
  - [ ]* 20.3 Write property test for parsing error isolation
    - **Property 26: Parsing error isolation**
    - **Validates: Requirements 13.2**
  
  - [ ]* 20.4 Write unit tests for error handling
    - Test error boundary activation
    - Test loading state display
    - Test error message display
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 21. Implement configuration and setup
  - [ ] 21.1 Create configuration loading logic
    - Read VAULT_PATH from environment variables
    - Validate vault path exists
    - Display setup wizard if not configured
    - Support configurable refresh interval
    - _Requirements: 15.1, 15.2, 15.3_
  
  - [ ]* 21.2 Write property test for configuration hot-reload
    - **Property 29: Configuration hot-reload**
    - **Validates: Requirements 15.5**
  
  - [ ]* 21.3 Write unit tests for configuration
    - Test environment variable reading
    - Test missing configuration handling
    - Test configuration validation
    - _Requirements: 15.1, 15.2, 15.3_

- [ ] 22. Implement lazy loading for performance
  - [ ] 22.1 Add lazy loading to list components
    - Implement virtual scrolling or pagination for large lists
    - Lazy load off-screen content
    - _Requirements: 14.2, 14.3_
  
  - [ ]* 22.2 Write property test for lazy loading defers off-screen content
    - **Property 28: Lazy loading defers off-screen content**
    - **Validates: Requirements 14.3**
  
  - [ ]* 22.3 Write unit tests for lazy loading
    - Test initial visible items loaded
    - Test off-screen items not loaded
    - Test loading on scroll
    - _Requirements: 14.2, 14.3_

- [ ] 23. Final integration and polish
  - [ ] 23.1 Wire all components together
    - Verify all pages are accessible via navigation
    - Verify all API routes are called correctly
    - Verify caching works across pages
    - Test file watcher integration (if enabled)
    - _Requirements: 9.1, 9.2, 12.4, 14.1_
  
  - [ ] 23.2 Add documentation
    - Create README with setup instructions
    - Document environment variables
    - Document vault structure requirements
    - Add inline code comments
    - _Requirements: 15.1, 15.2_
  
  - [ ]* 23.3 Run full test suite
    - Run all unit tests
    - Run all property tests (verify 100+ iterations)
    - Run integration tests
    - Verify test coverage meets goals
    - _Requirements: All_

- [ ] 24. Final checkpoint - Ensure all tests pass
  - Run complete test suite
  - Verify all 30 correctness properties are tested
  - Check test coverage reports
  - Test dashboard manually with real vault data
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples, edge cases, and error conditions
- The implementation follows a bottom-up approach: data layer → service layer → API layer → UI layer
- Checkpoints ensure incremental validation and provide opportunities for user feedback
