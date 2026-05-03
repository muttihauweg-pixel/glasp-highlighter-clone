import { test, expect } from '@playwright/test';

test('Governance OS Dashboard Loads and Accepts Input', async ({ page }) => {
  // 1. Mock Backend API
  await page.route('**/process', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        result: {
          risk: 'MINIMAL',
          steps: ['User Input Received', 'Compliance Check', 'Final Policy Decision'],
          processed_output: 'Mocked successful compliance check.'
        },
        audit: {
          hash: 'mock-sha256-hash',
          timestamp: new Date().toISOString(),
          policy_version: 'EU-AI-ACT-2024-V1'
        },
        compliance_report: 'This is a mocked compliance report analysis.'
      })
    });
  });

  // 2. Go to app
  await page.goto('http://localhost:5173');

  // 3. Verify title and input terminal
  await expect(page.locator('h1')).toContainText('AI Governance OS');
  await expect(page.locator('h2')).toContainText('Governance Input Terminal');

  // 4. Fill input and submit
  await page.fill('textarea', 'Analyze a credit scoring model for bias.');
  await page.click('button:has-text("Run Compliance Check")');

  // 5. Verify Dashboard updates
  await expect(page.locator('.risk-badge')).toContainText('MINIMAL RISK');
  await expect(page.locator('.flow-item')).toHaveCount(3);
  await expect(page.locator('.compliance-report')).toBeVisible();

  // 6. Screenshot for verification
  await page.screenshot({ path: 'governance_dashboard_verify.png' });
});
