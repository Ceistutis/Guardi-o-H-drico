
import '@/global.css';

import { Platform } from 'react-native';

export const Colors = {
  light: {
    text: '#0B1220',
    background: '#F1F5F9',
    backgroundElement: '#FFFFFF',
    backgroundSelected: '#DCE8F0',
    textSecondary: '#475569',
    primary: '#0891B2',
    border: '#CBD5E1',
    success: '#059669',
    warning: '#B45309',
    danger: '#E11D48',
  },
  dark: {
    text: '#F1F5F9',
    background: '#0B1220',
    backgroundElement: '#142238',
    backgroundSelected: '#20364D',
    textSecondary: '#94A3B8',
    primary: '#36C5D8',
    border: '#365065',
    success: '#34D399',
    warning: '#FBBF24',
    danger: '#FB7185',
  },
} as const;

export type ThemeColor =
  keyof typeof Colors.light & keyof typeof Colors.dark;

export const Fonts = Platform.select({
  ios: {
    sans: 'system-ui',
    serif: 'ui-serif',
    rounded: 'ui-rounded',
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
  web: {
    sans: 'var(--font-display)',
    serif: 'var(--font-serif)',
    rounded: 'var(--font-rounded)',
    mono: 'var(--font-mono)',
  },
});

export const Spacing = {
  half: 2,
  one: 4,
  two: 8,
  three: 16,
  four: 24,
  five: 32,
  six: 64,
} as const;

export const BottomTabInset =
  Platform.select({ ios: 50, android: 80 }) ?? 0;

export const MaxContentWidth = 800;
