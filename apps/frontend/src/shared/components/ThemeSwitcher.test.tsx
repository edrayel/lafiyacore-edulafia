import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeSwitcher } from './ThemeSwitcher';
import { ThemeProvider, createTheme } from '@mui/material';

describe('ThemeSwitcher Component', () => {
  const theme = createTheme();

  describe('Basic Functionality', () => {
    it('renders theme switcher button', () => {
      render(
        <ThemeProvider theme={theme}>
          <ThemeSwitcher />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('opens menu when button is clicked', async () => {
      render(
        <ThemeProvider theme={theme}>
          <ThemeSwitcher />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      fireEvent.click(button);

      const menu = document.querySelector('[role="menu"]');
      expect(menu).toBeInTheDocument();
    });
  });

  describe('Theme Options', () => {
    it('displays all available theme options', async () => {
      render(
        <ThemeProvider theme={theme}>
          <ThemeSwitcher />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      fireEvent.click(button);

      const lightModeOption = screen.getByText('Light Mode');
      const darkModeOption = screen.getByText('Dark Mode');
      const autoModeOption = screen.getByText('Auto (System)');
      const highContrastOption = screen.getByText('High Contrast');

      expect(lightModeOption).toBeInTheDocument();
      expect(darkModeOption).toBeInTheDocument();
      expect(autoModeOption).toBeInTheDocument();
      expect(highContrastOption).toBeInTheDocument();
    });
  });
});
