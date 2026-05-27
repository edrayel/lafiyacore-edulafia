import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { LoadingSpinner } from './LoadingSpinner';
import { ThemeProvider, createTheme } from '@mui/material';

describe('LoadingSpinner Component', () => {
  const theme = createTheme();

  describe('Basic Functionality', () => {
    it('renders loading spinner without text', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });

    it('renders loading spinner with text', () => {
      const testText = 'Loading data...';
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner text={testText} />
        </ThemeProvider>
      );

      const textElement = screen.getByText(testText);
      expect(textElement).toBeInTheDocument();
    });
  });

  describe('Size Variations', () => {
    it('renders small spinner', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner size="small" text="Loading..." />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });

    it('renders medium spinner', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner size="medium" text="Loading..." />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });

    it('renders large spinner', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner size="large" text="Loading..." />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });
  });

  describe('Full Screen Mode', () => {
    it('renders in full screen mode', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner fullScreen text="Loading..." />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has correct ARIA role', () => {
      render(
        <ThemeProvider theme={theme}>
          <LoadingSpinner />
        </ThemeProvider>
      );

      const spinner = screen.getByRole('progressbar');
      expect(spinner).toBeInTheDocument();
    });
  });
});
