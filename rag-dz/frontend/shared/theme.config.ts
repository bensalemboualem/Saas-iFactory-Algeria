/**
 * IAFACTORY DESIGN SYSTEM - THEME CONFIGURATION
 * Version: 3.0 - Décembre 2025
 * Source: Landing Page iafactoryalgeria.com (Single Source of Truth)
 *
 * Usage in React/Vue/Svelte:
 * import { theme, colors, spacing } from './shared/theme.config';
 */

// === BRAND COLORS ===
export const colors = {
  // Primary - Algerian Green
  primary: {
    DEFAULT: '#00a651',
    light: '#00c761',
    dark: '#008c45',
    50: '#e6f9ef',
    100: '#ccf3df',
    200: '#99e7bf',
    300: '#66db9f',
    400: '#33cf7f',
    500: '#00a651',
    600: '#008c45',
    700: '#007339',
    800: '#00592d',
    900: '#004021',
  },

  // Danger - Algerian Red
  danger: {
    DEFAULT: '#ef4444',
    light: '#f87171',
    dark: '#dc2626',
    50: '#fef2f2',
    100: '#fee2e2',
    200: '#fecaca',
    300: '#fca5a5',
    400: '#f87171',
    500: '#ef4444',
    600: '#dc2626',
    700: '#b91c1c',
    800: '#991b1b',
    900: '#7f1d1d',
  },

  // Semantic
  success: '#10b981',
  warning: '#f59e0b',
  info: '#3b82f6',

  // Dark Mode
  dark: {
    bg: '#020617',
    bgAlt: '#020617',
    card: '#020617',
    text: '#f8fafc',
    textSecondary: 'rgba(255, 255, 255, 0.7)',
    textMuted: 'rgba(255, 255, 255, 0.5)',
    border: 'rgba(255, 255, 255, 0.12)',
    borderLight: 'rgba(255, 255, 255, 0.06)',
    borderStrong: 'rgba(255, 255, 255, 0.2)',
    glass: 'rgba(255, 255, 255, 0.08)',
    hover: 'rgba(255, 255, 255, 0.05)',
  },

  // Light Mode
  light: {
    bg: '#f7f5f0',
    bgAlt: '#f7f5f0',
    card: '#ffffff',
    text: '#0f172a',
    textSecondary: 'rgba(0, 0, 0, 0.7)',
    textMuted: 'rgba(0, 0, 0, 0.5)',
    border: 'rgba(0, 0, 0, 0.08)',
    borderLight: 'rgba(0, 0, 0, 0.04)',
    borderStrong: 'rgba(0, 0, 0, 0.15)',
    glass: 'rgba(0, 0, 0, 0.04)',
    hover: 'rgba(0, 0, 0, 0.04)',
  },
} as const;

// === SPACING ===
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  '2xl': '32px',
  '3xl': '48px',
  '4xl': '64px',
} as const;

// === BORDER RADIUS ===
export const borderRadius = {
  xs: '4px',
  sm: '6px',
  md: '8px',
  lg: '10px',
  xl: '12px',
  '2xl': '16px',
  '3xl': '24px',
  full: '999px',
} as const;

// === SHADOWS ===
export const shadows = {
  dark: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.2)',
    sm: '0 2px 8px rgba(0, 0, 0, 0.2)',
    md: '0 4px 16px rgba(0, 0, 0, 0.25)',
    lg: '0 8px 32px rgba(0, 0, 0, 0.3)',
    xl: '0 20px 60px rgba(0, 0, 0, 0.55)',
    glow: '0 0 20px rgba(0, 166, 81, 0.3)',
    glowIntense: '0 0 30px rgba(0, 166, 81, 0.5)',
  },
  light: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.04)',
    sm: '0 2px 8px rgba(0, 0, 0, 0.06)',
    md: '0 4px 16px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 32px rgba(0, 0, 0, 0.12)',
    xl: '0 20px 60px rgba(15, 23, 42, 0.25)',
    glow: '0 0 20px rgba(0, 166, 81, 0.2)',
    glowIntense: '0 0 30px rgba(0, 166, 81, 0.35)',
  },
} as const;

// === TYPOGRAPHY ===
export const typography = {
  fontFamily: {
    sans: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif",
    mono: "'SF Mono', 'Fira Code', 'Consolas', 'Monaco', monospace",
  },
  fontSize: {
    xs: '12px',
    sm: '13px',
    md: '14px',
    lg: '15px',
    xl: '16px',
    '2xl': '18px',
    '3xl': '20px',
    '4xl': '24px',
    '5xl': '30px',
    '6xl': '36px',
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

// === TRANSITIONS ===
export const transitions = {
  fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
  base: '250ms cubic-bezier(0.4, 0, 0.2, 1)',
  slow: '350ms cubic-bezier(0.4, 0, 0.2, 1)',
  slower: '500ms cubic-bezier(0.4, 0, 0.2, 1)',
} as const;

// === LAYOUT ===
export const layout = {
  headerHeight: '60px',
  sidebarWidth: '260px',
  sidebarCollapsed: '60px',
  containerSm: '640px',
  containerMd: '768px',
  containerLg: '1024px',
  containerXl: '1280px',
  container2xl: '1400px',
} as const;

// === Z-INDEX ===
export const zIndex = {
  base: 0,
  dropdown: 100,
  sticky: 200,
  fixed: 300,
  sidebar: 900,
  header: 1000,
  modalBackdrop: 1100,
  modal: 1200,
  popover: 1300,
  tooltip: 1400,
  toast: 1500,
} as const;

// === GRADIENTS ===
export const gradients = {
  primary: 'linear-gradient(135deg, #00a651 0%, #00c761 100%)',
  danger: 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)',
  dark: 'linear-gradient(180deg, #020617 0%, #0f172a 100%)',
  glass: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
} as const;

// === COMPLETE THEME OBJECT ===
export const theme = {
  colors,
  spacing,
  borderRadius,
  shadows,
  typography,
  transitions,
  layout,
  zIndex,
  gradients,
} as const;

// === THEME MODE HELPERS ===
export type ThemeMode = 'dark' | 'light';

export const getThemeColors = (mode: ThemeMode) => ({
  ...colors,
  bg: mode === 'dark' ? colors.dark.bg : colors.light.bg,
  bgAlt: mode === 'dark' ? colors.dark.bgAlt : colors.light.bgAlt,
  card: mode === 'dark' ? colors.dark.card : colors.light.card,
  text: mode === 'dark' ? colors.dark.text : colors.light.text,
  textSecondary: mode === 'dark' ? colors.dark.textSecondary : colors.light.textSecondary,
  textMuted: mode === 'dark' ? colors.dark.textMuted : colors.light.textMuted,
  border: mode === 'dark' ? colors.dark.border : colors.light.border,
  borderLight: mode === 'dark' ? colors.dark.borderLight : colors.light.borderLight,
  borderStrong: mode === 'dark' ? colors.dark.borderStrong : colors.light.borderStrong,
  glass: mode === 'dark' ? colors.dark.glass : colors.light.glass,
  hover: mode === 'dark' ? colors.dark.hover : colors.light.hover,
});

export const getThemeShadows = (mode: ThemeMode) =>
  mode === 'dark' ? shadows.dark : shadows.light;

// === CSS VARIABLES GENERATOR ===
export const generateCSSVariables = (mode: ThemeMode = 'dark'): string => {
  const themeColors = getThemeColors(mode);
  const themeShadows = getThemeShadows(mode);

  return `
    --iaf-primary: ${colors.primary.DEFAULT};
    --iaf-primary-light: ${colors.primary.light};
    --iaf-primary-dark: ${colors.primary.dark};
    --iaf-danger: ${colors.danger.DEFAULT};
    --iaf-success: ${colors.success};
    --iaf-warning: ${colors.warning};
    --iaf-info: ${colors.info};
    --iaf-bg: ${themeColors.bg};
    --iaf-bg-alt: ${themeColors.bgAlt};
    --iaf-bg-card: ${themeColors.card};
    --iaf-bg-glass: ${themeColors.glass};
    --iaf-bg-hover: ${themeColors.hover};
    --iaf-text: ${themeColors.text};
    --iaf-text-secondary: ${themeColors.textSecondary};
    --iaf-text-muted: ${themeColors.textMuted};
    --iaf-border: ${themeColors.border};
    --iaf-border-light: ${themeColors.borderLight};
    --iaf-border-strong: ${themeColors.borderStrong};
    --iaf-shadow-sm: ${themeShadows.sm};
    --iaf-shadow-md: ${themeShadows.md};
    --iaf-shadow-lg: ${themeShadows.lg};
    --iaf-shadow-xl: ${themeShadows.xl};
    --iaf-shadow-glow: ${themeShadows.glow};
  `.trim();
};

// === REACT CONTEXT HELPER ===
export interface ThemeContextValue {
  mode: ThemeMode;
  colors: ReturnType<typeof getThemeColors>;
  shadows: typeof shadows.dark | typeof shadows.light;
  toggleTheme: () => void;
}

// === DEFAULT EXPORT ===
export default theme;
