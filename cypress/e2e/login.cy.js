const { test, expect } = require("@playwright/test");

test.describe("Login Test", () => {
  test("should allow a user to log in", async ({ page }) => {
    // Go to login page
    await page.goto("https://facebook.com");

    // Type email
    await page.fill("[id=email]", "09693470605");

    // Type password
    await page.fill("[id=pass]", "password123");

    // Click login button
    await page.click("[name=login]");

    // Verify user is redirected to the dashboard
    await expect(page).toHaveURL(/dashboard/);

    // Check if the dashboard contains a greeting
    await expect(page.locator("text=Welcome, Test User")).toBeVisible();
  });
});
