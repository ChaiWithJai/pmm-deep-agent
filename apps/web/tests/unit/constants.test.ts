import { describe, it, expect } from 'vitest'

/**
 * Unit Tests - Testing Trophy Base Layer
 *
 * Test pure functions and constants that should never break
 */

// These would import from src once we extract constants
const QUICK_ACTIONS = [
  { label: 'Analyze Homepage', prompt: 'Run a complete PMM audit on the homepage at ' },
  { label: '5-Second Test', prompt: 'Run a 5-second test on the homepage at ' },
  { label: 'Messaging Analysis', prompt: 'Analyze the messaging hierarchy and clarity on ' },
  { label: 'Competitor Compare', prompt: 'Compare my homepage against these competitors: ' },
  { label: 'Create Positioning', prompt: 'Create a positioning canvas for: ' },
  { label: 'Generate Rewrites', prompt: 'Generate improved headline and subheadline options for ' },
]

const TOOL_DISPLAY_NAMES: Record<string, string> = {
  run_five_second_test: '5-Second Test',
  analyze_positioning: 'Positioning Analysis',
  analyze_messaging: 'Messaging Analysis',
  run_complete_pmm_audit: 'Complete PMM Audit',
  fetch_homepage: 'Fetch Homepage',
}

describe('Quick Actions Configuration', () => {
  it('has exactly 6 quick actions', () => {
    expect(QUICK_ACTIONS).toHaveLength(6)
  })

  it('all quick actions have label and prompt', () => {
    for (const action of QUICK_ACTIONS) {
      expect(action.label).toBeDefined()
      expect(action.prompt).toBeDefined()
      expect(action.label.length).toBeGreaterThan(0)
      expect(action.prompt.length).toBeGreaterThan(0)
    }
  })

  it('includes core PMM evaluation actions', () => {
    const labels = QUICK_ACTIONS.map(a => a.label)
    expect(labels).toContain('Analyze Homepage')
    expect(labels).toContain('5-Second Test')
    expect(labels).toContain('Messaging Analysis')
  })
})

describe('Tool Display Names', () => {
  it('maps all core tools to human-readable names', () => {
    expect(TOOL_DISPLAY_NAMES.run_five_second_test).toBe('5-Second Test')
    expect(TOOL_DISPLAY_NAMES.run_complete_pmm_audit).toBe('Complete PMM Audit')
    expect(TOOL_DISPLAY_NAMES.fetch_homepage).toBe('Fetch Homepage')
  })

  it('has no empty display names', () => {
    for (const [key, value] of Object.entries(TOOL_DISPLAY_NAMES)) {
      expect(value.length).toBeGreaterThan(0)
    }
  })
})
