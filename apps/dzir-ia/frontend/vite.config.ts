import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Frontend appelle /api/... => proxy vers backend DZIR
      "/api": {
        changeOrigin: true,
        secure: false,
        target: "http://localhost:4000",
      },
      // Health check si tu en as besoin depuis le navigateur
      "/health": {
        changeOrigin: true,
        secure: false,
        target: "http://localhost:4000",
      },
    },
  },
});
