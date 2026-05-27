import { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { WifiOff as WifiOffIcon } from '@mui/icons-material';

export function OfflineBanner() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (isOnline) return null;

  return (
    <Box
      sx={{
        backgroundColor: 'warning.light',
        color: 'warning.dark',
        py: 1,
        px: 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 1,
        width: '100%',
        zIndex: (theme) => theme.zIndex.appBar - 1,
      }}
    >
      <WifiOffIcon fontSize="small" />
      <Typography variant="body2" fontWeight={600}>
        You're offline. Changes will sync.
      </Typography>
    </Box>
  );
}
