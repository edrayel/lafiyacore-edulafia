import { Box, CircularProgress, Typography, Paper } from '@mui/material';
import type { TypographyProps } from '@mui/material';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  text?: string;
  fullScreen?: boolean;
}

export function LoadingSpinner({ size = 'medium', text, fullScreen = false }: LoadingSpinnerProps) {
  const spinnerSizes = {
    small: 32,
    medium: 60,
    large: 96,
  };

  const textSizes: Record<'small' | 'medium' | 'large', TypographyProps['variant']> = {
    small: 'caption',
    medium: 'body2',
    large: 'subtitle1',
  };

  const containerStyles = fullScreen
    ? {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: (theme: any) => theme.palette.mode === 'dark'
          ? 'rgba(2, 6, 23, 0.9)'
          : 'rgba(255, 255, 255, 0.9)',
        zIndex: 9999,
      }
    : {};

  return (
    <Box
      sx={{
        ...containerStyles,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
      }}
      role="status"
      aria-live="polite"
    >
      <Paper
        elevation={0}
        sx={(theme: any) => ({
          p: 4,
          borderRadius: 24,
          bgcolor: theme.palette.mode === 'dark' ? 'rgba(15, 23, 42, 0.9)' : 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid',
          borderColor: theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.08)' : 'rgba(255, 255, 255, 0.18)',
          boxShadow: theme.palette.mode === 'dark'
            ? '0 8px 32px rgba(0, 0, 0, 0.4)'
            : '0 8px 32px rgba(0, 0, 0, 0.1)',
        })}
      >
        <Box sx={{ position: 'relative' }}>
          <CircularProgress
            size={spinnerSizes[size]}
            thickness={4}
            sx={{
              color: 'primary.main',
              '& .MuiCircularProgress-circle': {
                strokeLinecap: 'round',
              },
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              '&::before': {
                content: '""',
                position: 'absolute',
                width: spinnerSizes[size] * 0.6,
                height: spinnerSizes[size] * 0.6,
                borderRadius: '50%',
                background: 'conic-gradient(transparent 20%, primary.main, secondary.main)',
                filter: 'blur(8px)',
                opacity: 0.5,
                animation: 'pulse 2s ease-in-out infinite',
              },
            }}
          />
        </Box>
        {text && (
          <Typography
            variant={textSizes[size]}
            sx={{
              textAlign: 'center',
              mt: 2,
              fontWeight: 500,
              color: 'text.secondary',
              animation: 'fadeIn 0.6s ease-out 0.3s backwards',
            }}
          >
            {text}
          </Typography>
        )}
      </Paper>
    </Box>
  );
}
