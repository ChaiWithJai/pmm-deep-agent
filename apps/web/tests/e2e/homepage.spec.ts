import { test, expect } from '@playwright/test'

/**
 * E2E Tests - Testing Trophy Top Layer
 *
 * JTBD: Enterprise Champion needs to prove their team has a PMM skills gap
 * Core flows that must never break:
 * 1. Can see the value proposition clearly (5-second test)
 * 2. Can run an audit on their homepage
 * 3. Can navigate to training/expert options
 */

test.describe('Homepage - 5 Second Test', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('displays clear value proposition', async ({ page }) => {
    // JTBD: Enterprise Champion needs to immediately understand what this does
    await expect(page.getByRole('heading', { level: 2 })).toContainText('PMM Skills Gap')
    await expect(page.getByText('positioning audit')).toBeVisible()
  })

  test('shows who this is for', async ({ page }) => {
    // JTBD: Enterprise Champion needs to know this is for teams
    await expect(page.getByText("Your Team's Messaging")).toBeVisible()
  })

  test('displays clear CTAs for the funnel', async ({ page }) => {
    // JTBD: Enterprise Champion needs clear next steps
    await expect(page.getByRole('button', { name: /audit your homepage/i })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Train Your Team', exact: true })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Bring In An Expert', exact: true })).toBeVisible()
  })

  test('shows 6 quick action options', async ({ page }) => {
    // JTBD: Enterprise Champion needs multiple evaluation options
    const quickActions = [
      'Analyze Homepage',
      '5-Second Test',
      'Messaging Analysis',
      'Competitor Compare',
      'Create Positioning',
      'Generate Rewrites',
    ]

    for (const action of quickActions) {
      await expect(page.getByRole('button', { name: action })).toBeVisible()
    }
  })
})

test.describe('Homepage - Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('header shows CashIsClay branding', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'CashIsClay' })).toBeVisible()
    await expect(page.getByText('powered by')).toBeVisible()
  })

  test('Train Your Team links to CashIsClay course', async ({ page }) => {
    const trainLink = page.getByRole('link', { name: 'Train Your Team', exact: true })
    await expect(trainLink).toHaveAttribute('href', 'https://cashisclay.com')
  })

  test('Bring In An Expert links to Calendly', async ({ page }) => {
    const expertLink = page.getByRole('link', { name: /bring in an expert/i })
    await expect(expertLink).toHaveAttribute('href', 'https://calendly.com/chaiwithjai/30min')
  })
})

test.describe('Homepage - Chat Interaction', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('chat input is visible and focusable', async ({ page }) => {
    const input = page.getByRole('textbox', { name: /ask about positioning/i })
    await expect(input).toBeVisible()
    await input.focus()
    await expect(input).toBeFocused()
  })

  test('Audit Your Homepage button focuses input', async ({ page }) => {
    await page.getByRole('button', { name: /audit your homepage/i }).click()
    const input = page.getByRole('textbox', { name: /ask about positioning/i })
    await expect(input).toBeFocused()
  })

  test('quick action populates input with prompt', async ({ page }) => {
    await page.getByRole('button', { name: '5-Second Test' }).click()
    const input = page.getByRole('textbox', { name: /ask about positioning/i })
    await expect(input).toHaveValue(/5-second test/i)
  })
})
