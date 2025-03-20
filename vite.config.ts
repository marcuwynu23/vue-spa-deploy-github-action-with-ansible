import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  base: "/vue-spa-deploy-github-action-with-ansible/",
  plugins: [vue()],
  build: {
    outDir: "build",
  },
});
