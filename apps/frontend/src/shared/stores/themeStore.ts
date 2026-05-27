import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ThemeMode } from '../theme';

interface ThemeState {
  mode: ThemeMode;
  setMode: (mode: ThemeMode) => void;
  toggle: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      mode: 'auto',
      setMode: (mode) => set({ mode }),
      toggle: () => {
        const currentMode = get().mode;
        if (currentMode === 'light') {
          set({ mode: 'dark' });
        } else if (currentMode === 'dark') {
          set({ mode: 'high-contrast' });
        } else if (currentMode === 'high-contrast') {
          set({ mode: 'auto' });
        } else {
          set({ mode: 'light' });
        }
      },
    }),
    {
      name: 'edulafia-theme',
      version: 1,
    }
  )
);
