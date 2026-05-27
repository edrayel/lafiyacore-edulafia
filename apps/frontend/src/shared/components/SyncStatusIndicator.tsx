import { useState, useEffect } from 'react';
import { Box, Tooltip } from '@mui/material';
import {
  CloudDone as SyncedIcon,
  CloudSync as SyncingIcon,
  CloudOff as PausedIcon,
  ErrorOutline as ErrorIcon,
} from '@mui/icons-material';
import { getSyncStatus, subscribeToSyncStatus, type SyncStatusType } from '../api/offline/sync';

export function SyncStatusIndicator() {
  const [status, setStatus] = useState<SyncStatusType>(getSyncStatus());

  useEffect(() => {
    const unsubscribe = subscribeToSyncStatus(setStatus);
    return () => unsubscribe();
  }, []);

  const getStatusConfig = () => {
    switch (status) {
      case 'active':
        return {
          icon: <SyncingIcon fontSize="small" sx={{ color: 'info.main' }} />,
          label: 'Sync in progress',
          spin: true,
        };
      case 'paused':
        return {
          icon: <PausedIcon fontSize="small" sx={{ color: 'warning.main' }} />,
          label: 'Sync paused (offline)',
          spin: false,
        };
      case 'error':
        return {
          icon: <ErrorIcon fontSize="small" sx={{ color: 'error.main' }} />,
          label: 'Sync error',
          spin: false,
        };
      case 'idle':
      default:
        return {
          icon: <SyncedIcon fontSize="small" sx={{ color: 'success.main' }} />,
          label: 'All data synced',
          spin: false,
        };
    }
  };

  const config = getStatusConfig();

  return (
    <Tooltip title={config.label}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: 40,
          height: 40,
          borderRadius: '50%',
          '& svg': {
            animation: config.spin ? 'spin 2s linear infinite' : 'none',
          },
          '@keyframes spin': {
            '0%': { transform: 'rotate(0deg)' },
            '100%': { transform: 'rotate(360deg)' },
          },
        }}
        aria-label={config.label}
        role="status"
      >
        {config.icon}
      </Box>
    </Tooltip>
  );
}
