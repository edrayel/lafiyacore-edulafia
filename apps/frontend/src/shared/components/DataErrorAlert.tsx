import React from 'react';
import { Alert, AlertTitle, Button } from '@mui/material';

interface DataErrorAlertProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const DataErrorAlert: React.FC<DataErrorAlertProps> = ({
  title = 'Failed to load data',
  message = 'There was an error fetching this information. Please try again.',
  onRetry,
}) => {
  return (
    <Alert
      severity="error"
      sx={{ mb: 3 }}
      action={
        onRetry ? (
          <Button color="inherit" size="small" onClick={onRetry}>
            Retry
          </Button>
        ) : null
      }
    >
      <AlertTitle>{title}</AlertTitle>
      {message}
    </Alert>
  );
};
