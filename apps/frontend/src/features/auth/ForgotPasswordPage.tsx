import { useState } from 'react';
import { useNavigate, Link } from '@tanstack/react-router';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  InputAdornment,
} from '@mui/material';
import { Mail, ArrowLeft } from 'lucide-react';
import { useAuthStore } from '@/shared/stores/authStore';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [success, setSuccess] = useState(false);
  const { forgotPassword, isLoading, error, clearError } = useAuthStore();
  const navigate = useNavigate();

  const validateEmail = (value: string): boolean => {
    if (!value) { setEmailError('Email is required'); return false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) { setEmailError('Please enter a valid email'); return false; }
    setEmailError('');
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateEmail(email)) return;
    try {
      await forgotPassword(email);
      setSuccess(true);
    } catch (e) {
      console.error(e);
    }
  };

  if (success) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Paper sx={{ p: 4, width: '100%' }}>
            <Typography variant="h4" sx={{ mb: 3, textAlign: 'center' }}>
              Password Reset Sent
            </Typography>
            <Alert severity="success" sx={{ mb: 2 }} role="alert">
              If an account exists with {email}, a reset link has been sent to your email address.
            </Alert>
            <Button variant="contained" size="large" onClick={() => navigate({ to: '/login' })}>
              Back to Login
            </Button>
          </Paper>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper sx={{ p: 4, width: '100%' }}>
          <Typography variant="h4" sx={{ mb: 3, textAlign: 'center' }}>
            Forgot Password
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={clearError} role="alert">
              {error}
            </Alert>
          )}
          <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
          >
            <TextField
              autoFocus
              fullWidth
              label="Email address"
              placeholder="you@school.edu"
              type="email"
              value={email}
              onChange={(e) => { setEmail(e.target.value); if (emailError) setEmailError(''); }}
              error={!!emailError}
              helperText={emailError}
              required
              inputProps={{ autoComplete: 'email' }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Mail size={20} />
                  </InputAdornment>
                ),
              }}
            />
            <Button type="submit" variant="contained" size="large" disabled={isLoading || !email}>
              {isLoading ? <CircularProgress size={24} /> : 'Send Reset Link'}
            </Button>
          </Box>
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              Remember your password?{' '}
              <Link to="/login" style={{ textDecoration: 'none' }}>
                Sign in
              </Link>
            </Typography>
          </Box>
          <Box sx={{ mt: 1, textAlign: 'center' }}>
            <Button
              variant="text"
              size="small"
              startIcon={<ArrowLeft size={16} />}
              onClick={() => navigate({ to: '/login' })}
            >
              Back to Login
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}
