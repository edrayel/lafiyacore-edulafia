import { Box, Typography, Button } from '@mui/material';
import { Inbox as InboxIcon } from '@mui/icons-material';

interface DataEmptyStateProps {
  title?: string;
  message?: string;
  action?: { label: string; onClick: () => void };
  icon?: React.ReactNode;
}

export function DataEmptyState({
  title = 'No data found',
  message = 'There are no items to display at this time.',
  action,
  icon,
}: DataEmptyStateProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        py: 8,
        px: 3,
        textAlign: 'center',
      }}
    >
      <Box
        sx={{
          width: 72,
          height: 72,
          borderRadius: '50%',
          bgcolor: 'action.hover',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 3,
          color: 'text.disabled',
        }}
      >
        {icon || <InboxIcon sx={{ fontSize: 36 }} />}
      </Box>
      <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
        {title}
      </Typography>
      <Typography variant="body2" sx={{ color: 'text.secondary', maxWidth: 360, mb: action ? 3 : 0 }}>
        {message}
      </Typography>
      {action && (
        <Button variant="outlined" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </Box>
  );
}
