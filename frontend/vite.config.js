import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: process.env.VITE_API_PROXY || "http://127.0.0.1:8002",
        changeOrigin: true,
      },
      "/accounts": {
        target: process.env.VITE_API_PROXY || "http://127.0.0.1:8002",
        changeOrigin: true,
      },
      "/media": {
        target: process.env.VITE_API_PROXY || "http://127.0.0.1:8002",
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "react-router-dom"],
        },
      },
    },
  },
});
