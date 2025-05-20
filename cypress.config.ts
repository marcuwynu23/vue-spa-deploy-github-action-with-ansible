const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    browser: "electron", // Set Electron as the default browser
    setupNodeEvents(on, config) {
      // Implement node event listeners if needed
    },
  },

  component: {
    devServer: {
      framework: "vue",
      bundler: "vite",
    },
  },
});
