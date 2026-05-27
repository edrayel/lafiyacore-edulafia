import { ReactNode } from 'react';
import { Fade, Box } from '@mui/material';

interface PageTransitionProps {
  children: ReactNode;
  isLoading?: boolean;
}

export function PageTransition({ children, isLoading }: PageTransitionProps) {
  return (
    <Fade in={!isLoading} timeout={{ enter: 300, exit: 150 }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
        {children}
      </Box>
    </Fade>
  );
}
