import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Port 3000 matches the backend's default CORS_ORIGINS.
export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
});
