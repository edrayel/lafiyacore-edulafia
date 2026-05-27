import { Box, Typography, Button } from '@mui/material';
import { useNavigate } from '@tanstack/react-router';

export function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: '#0a0f1c',
        gap: 2,
        p: 4,
      }}
    >
      <Typography variant="h1" sx={{ color: '#2dd4bf', fontWeight: 800, fontSize: '6rem' }}>
        404
      </Typography>
      <Typography variant="h5" sx={{ color: 'white', mb: 2 }}>
        Page not found
      </Typography>
      <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.6)', mb: 3 }}>
        The page you are looking for does not exist or has been moved.
      </Typography>
      <Button
        variant="contained"
        onClick={() => navigate({ to: '/' })}
        sx={{
          borderRadius: '9999px',
          bgcolor: '#0d9488',
          textTransform: 'none',
          px: 4,
          py: 1.5,
        }}
      >
        Go Home
      </Button>
    </Box>
  );
}