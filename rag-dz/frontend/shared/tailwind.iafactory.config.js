/**
 * IAFACTORY DESIGN SYSTEM - TAILWIND CSS CONFIGURATION
 * Version: 3.0 - Décembre 2025
 * Source: Landing Page iafactoryalgeria.com (Single Source of Truth)
 *
 * Usage: Extend your tailwind.config.js with this preset
 *
 * // tailwind.config.js
 * const iafactoryPreset = require('./shared/tailwind.iafactory.config.js');
 * module.exports = {
 *   presets: [iafactoryPreset],
 *   // your customizations...
 * }
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      // === BRAND COLORS ===
      colors: {
        // Primary - Algerian Green
        primary: {
          DEFAULT: '#00a651',
          50: '#e6f9ef',
          100: '#ccf3df',
          200: '#99e7bf',
          300: '#66db9f',
          400: '#33cf7f',
          500: '#00a651',  // Main
          600: '#008c45',
          700: '#007339',
          800: '#00592d',
          900: '#004021',
        },
        // Danger - Algerian Red
        danger: {
          DEFAULT: '#ef4444',
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',  // Main
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
        // Backgrounds (Dark Mode Default)
        dark: {
          DEFAULT: '#020617',
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',  // Main dark bg
        },
        // Light Mode Background
        cream: {
          DEFAULT: '#f7f5f0',
          50: '#fdfcfb',
          100: '#faf9f6',
          200: '#f7f5f0',  // Main light bg
          300: '#ebe7dc',
          400: '#d9d3c3',
          500: '#c7bfaa',
          600: '#a89d84',
          700: '#8a7c5e',
          800: '#6b5e3e',
          900: '#4d401f',
        },
        // Semantic Colors
        success: '#10b981',
        warning: '#f59e0b',
        info: '#3b82f6',
      },

      // === BACKGROUND COLORS ===
      backgroundColor: {
        'iaf-dark': '#020617',
        'iaf-light': '#f7f5f0',
        'iaf-card-dark': '#020617',
        'iaf-card-light': '#ffffff',
        'iaf-glass-dark': 'rgba(255, 255, 255, 0.08)',
        'iaf-glass-light': 'rgba(0, 0, 0, 0.04)',
      },

      // === TEXT COLORS ===
      textColor: {
        'iaf-primary': 'var(--iaf-text, #f8fafc)',
        'iaf-secondary': 'var(--iaf-text-secondary, rgba(255, 255, 255, 0.7))',
        'iaf-muted': 'var(--iaf-text-muted, rgba(255, 255, 255, 0.5))',
      },

      // === BORDER COLORS ===
      borderColor: {
        'iaf-default': 'var(--iaf-border, rgba(255, 255, 255, 0.12))',
        'iaf-light': 'var(--iaf-border-light, rgba(255, 255, 255, 0.06))',
        'iaf-strong': 'var(--iaf-border-strong, rgba(255, 255, 255, 0.2))',
      },

      // === FONT FAMILY ===
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Oxygen',
          'Ubuntu',
          'Cantarell',
          'sans-serif',
        ],
        mono: [
          'SF Mono',
          'Fira Code',
          'Consolas',
          'Monaco',
          'monospace',
        ],
      },

      // === FONT SIZE ===
      fontSize: {
        'xs': ['12px', { lineHeight: '16px' }],
        'sm': ['13px', { lineHeight: '18px' }],
        'base': ['14px', { lineHeight: '20px' }],
        'lg': ['15px', { lineHeight: '22px' }],
        'xl': ['16px', { lineHeight: '24px' }],
        '2xl': ['18px', { lineHeight: '28px' }],
        '3xl': ['20px', { lineHeight: '28px' }],
        '4xl': ['24px', { lineHeight: '32px' }],
        '5xl': ['30px', { lineHeight: '36px' }],
        '6xl': ['36px', { lineHeight: '40px' }],
      },

      // === SPACING ===
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
        '3xl': '48px',
        '4xl': '64px',
        'header': '60px',
        'sidebar': '260px',
        'sidebar-collapsed': '60px',
      },

      // === BORDER RADIUS ===
      borderRadius: {
        'xs': '4px',
        'sm': '6px',
        'DEFAULT': '8px',
        'lg': '10px',
        'xl': '12px',
        '2xl': '16px',
        '3xl': '24px',
      },

      // === BOX SHADOW ===
      boxShadow: {
        'xs': '0 1px 2px rgba(0, 0, 0, 0.2)',
        'sm': '0 2px 8px rgba(0, 0, 0, 0.2)',
        'DEFAULT': '0 4px 16px rgba(0, 0, 0, 0.25)',
        'lg': '0 8px 32px rgba(0, 0, 0, 0.3)',
        'xl': '0 20px 60px rgba(0, 0, 0, 0.55)',
        'glow': '0 0 20px rgba(0, 166, 81, 0.3)',
        'glow-intense': '0 0 30px rgba(0, 166, 81, 0.5)',
        // Light mode shadows
        'light-xs': '0 1px 2px rgba(0, 0, 0, 0.04)',
        'light-sm': '0 2px 8px rgba(0, 0, 0, 0.06)',
        'light-DEFAULT': '0 4px 16px rgba(0, 0, 0, 0.1)',
        'light-lg': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'light-xl': '0 20px 60px rgba(15, 23, 42, 0.25)',
      },

      // === TRANSITION ===
      transitionDuration: {
        'fast': '150ms',
        'base': '250ms',
        'slow': '350ms',
        'slower': '500ms',
      },

      transitionTimingFunction: {
        'iaf': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },

      // === Z-INDEX ===
      zIndex: {
        'dropdown': '100',
        'sticky': '200',
        'fixed': '300',
        'sidebar': '900',
        'header': '1000',
        'modal-backdrop': '1100',
        'modal': '1200',
        'popover': '1300',
        'tooltip': '1400',
        'toast': '1500',
      },

      // === BACKDROP BLUR ===
      backdropBlur: {
        'iaf': '24px',
        'iaf-light': '12px',
      },

      // === ANIMATIONS ===
      animation: {
        'fade-in': 'fadeIn 250ms ease-out',
        'slide-up': 'slideUp 250ms ease-out',
        'slide-down': 'slideDown 250ms ease-out',
        'scale-in': 'scaleIn 250ms ease-out',
        'pulse-slow': 'pulse 2s ease-in-out infinite',
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },

      // === CONTAINER ===
      maxWidth: {
        'container-sm': '640px',
        'container-md': '768px',
        'container-lg': '1024px',
        'container-xl': '1280px',
        'container-2xl': '1400px',
      },

      // === BACKGROUND IMAGE (Gradients) ===
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #00a651 0%, #00c761 100%)',
        'gradient-danger': 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)',
        'gradient-dark': 'linear-gradient(180deg, #020617 0%, #0f172a 100%)',
        'gradient-glass': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
      },
    },
  },
  plugins: [],
};
