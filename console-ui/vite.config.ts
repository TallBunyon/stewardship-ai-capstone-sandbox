import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Minimal Vite config for the Console UI scaffold.
export default defineConfig({
  plugins: [react()],
});
