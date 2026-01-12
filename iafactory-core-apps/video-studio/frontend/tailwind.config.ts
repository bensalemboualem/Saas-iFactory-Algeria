import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0f",
        surface: "#12121a",
        "surface-hover": "#1a1a24",
        border: "#2a2a3a",
        primary: {
          DEFAULT: "#6366f1",
          hover: "#818cf8",
        },
        accent: "#22d3ee",
        success: "#10b981",
        warning: "#f59e0b",
        error: "#ef4444",
        "text-primary": "#f4f4f5",
        "text-muted": "#a1a1aa",
      },
      fontFamily: {
        sans: ["Inter", "DM Sans", "sans-serif"],
        heading: ["Space Grotesk", "Outfit", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
        arabic: ["IBM Plex Sans Arabic", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
