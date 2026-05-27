import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { PremiumCard } from './PremiumCard';
import { ThemeProvider, createTheme } from '@mui/material';

describe('PremiumCard Component', () => {
  const theme = createTheme();

  describe('Basic Functionality', () => {
    it('renders basic PremiumCard', () => {
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card">
            <p>Test content</p>
          </PremiumCard>
        </ThemeProvider>
      );

      const card = screen.getByText('Test Card').closest('.MuiPaper-root');
      expect(card).toBeInTheDocument();
    });

    it('renders card with subtitle', () => {
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card" subtitle="Test subtitle">
            <p>Test content</p>
          </PremiumCard>
        </ThemeProvider>
      );

      const subtitle = screen.getByText('Test subtitle');
      expect(subtitle).toBeInTheDocument();
    });

    it('renders card with badge', () => {
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card" badge="New">
            <p>Test content</p>
          </PremiumCard>
        </ThemeProvider>
      );

      const badge = screen.getByText('New');
      expect(badge).toBeInTheDocument();
    });

    it('renders card with icon', () => {
      const testIcon = '🎓';
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card" icon={testIcon}>
            <p>Test content</p>
          </PremiumCard>
        </ThemeProvider>
      );

      const iconContainer = screen.getByText(testIcon).closest('div');
      expect(iconContainer).toBeInTheDocument();
    });

    it('renders card with action', () => {
      const handleAction = vi.fn();
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card" action={<button onClick={handleAction}>Click Me</button>}>
            <p>Test content</p>
          </PremiumCard>
        </ThemeProvider>
      );

      const button = screen.getByText('Click Me');
      expect(button).toBeInTheDocument();

      fireEvent.click(button);
      expect(handleAction).toHaveBeenCalled();
    });
  });

  describe('Content Rendering', () => {
    it('renders children', () => {
      render(
        <ThemeProvider theme={theme}>
          <PremiumCard title="Test Card">
            <div data-testid="test-content">Test content</div>
          </PremiumCard>
        </ThemeProvider>
      );

      const content = screen.getByTestId('test-content');
      expect(content).toBeInTheDocument();
    });
  });
});
