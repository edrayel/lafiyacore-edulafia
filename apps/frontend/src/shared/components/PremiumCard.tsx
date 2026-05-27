import { Paper, Box, Typography, Stack, Chip, useTheme } from '@mui/material';
import { SxProps } from '@mui/system';

interface PremiumCardProps {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  badge?: string;
  children: React.ReactNode;
  action?: React.ReactNode;
  sx?: SxProps;
  elevation?: 0 | 1 | 2 | 3 | 4 | 5;
}

export function PremiumCard({
  title,
  subtitle,
  icon,
  badge,
  children,
  action,
  sx = {},
  elevation = 1,
}: PremiumCardProps) {
  const theme = useTheme();
  return (
    <Paper
      elevation={elevation}
      sx={{
        borderRadius: 3,
        p: 0,
        position: 'relative',
        overflow: 'hidden',
        transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        },
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 4,
          background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main}, ${theme.palette.primary.main})`,
          backgroundSize: '200% 100%',
          animation: 'shimmer 3s ease-in-out infinite',
        },
        ...sx,
      }}
    >
      <Box sx={{ p: 3 }}>
        <Stack
          direction="row"
          alignItems="flex-start"
          justifyContent="space-between"
          sx={{ mb: 2 }}
        >
          <Stack direction="row" alignItems="center" spacing={2}>
            {icon && (
              <Box
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: 2,
                  bgcolor: 'primary.main',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '1.25rem',
                }}
              >
                {icon}
              </Box>
            )}
            <Stack>
              {title && (
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: 700,
                    color: 'text.primary',
                    mb: subtitle ? 0.5 : 0,
                  }}
                >
                  {title}
                </Typography>
              )}
              {subtitle && (
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  {subtitle}
                </Typography>
              )}
            </Stack>
          </Stack>
          {badge && (
            <Chip
              label={badge}
              size="small"
              color="primary"
              sx={{
                borderRadius: 12,
                fontWeight: 600,
              }}
            />
          )}
        </Stack>

        <Box sx={children ? undefined : { minHeight: 0, display: 'none' }}>
          {children}
        </Box>

        {action && <Box sx={{ mt: 2 }}>{action}</Box>}
      </Box>
    </Paper>
  );
}
