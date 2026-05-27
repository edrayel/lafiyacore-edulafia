import { useState } from 'react';
import { useNavigate, useSearch, Link } from '@tanstack/react-router';
import {
  Container,
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
  LinearProgress,
} from '@mui/material';
import { Lock, Eye, EyeOff, ArrowLeft } from 'lucide-react';
import { useAuthStore } from '@/shared/stores/authStore';

export default function ResetPasswordPage() {
  const search = useSearch({ from: '/reset-password' });
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const { resetPassword, isLoading } = useAuthStore();
  const token = search?.token;

  const getPasswordStrength = (pw: string): { score: number; label: string; color: 'error' | 'warning' | 'success' | 'info' } => {
    let score = 0;
    if (pw.length >= 8) score++;
    if (pw.length >= 12) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/[a-z]/.test(pw)) score++;
    if (/[0-9]/.test(pw)) score++;
    if (/[^A-Za-z0-9]/.test(pw)) score++;
    if (score <= 2) return { score: score / 6 * 100, label: 'Weak', color: 'error' };
    if (score <= 4) return { score: score / 6 * 100, label: 'Medium', color: 'warning' };
    return { score: score / 6 * 100, label: 'Strong', color: 'success' };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (!token) {
      setError('Invalid reset token');
      return;
    }

    try {
      await resetPassword(token, newPassword);
      setSuccess(true);
    } catch (e: unknown) {
      setError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to reset password');
    }
  };

  if (success) {
    return (
      <Container component="main" maxWidth="sm">
        <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              Password Reset Successful
            </Typography>
            <Typography variant="body1" align="center" sx={{ mb: 4 }}>
              Your password has been successfully reset. You can now sign in with your new password.
            </Typography>
            <Box sx={{ textAlign: 'center' }}>
              <Button variant="contained" size="large" onClick={() => navigate({ to: '/login' })}>
                Sign In
              </Button>
            </Box>
          </Paper>
        </Box>
      </Container>
    );
  }

  if (!token) {
    return (
      <Container component="main" maxWidth="sm">
        <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              Invalid Reset Link
            </Typography>
            <Typography variant="body1" align="center" sx={{ mb: 4 }}>
              The password reset link is invalid or has expired. Please request a new reset link.
            </Typography>
            <Box sx={{ textAlign: 'center' }}>
              <Button variant="contained" size="large" onClick={() => navigate({ to: '/forgot-password' })}>
                Request New Reset Link
              </Button>
            </Box>
          </Paper>
        </Box>
      </Container>
    );
  }

  const strength = newPassword ? getPasswordStrength(newPassword) : null;

  return (
    <Container component="main" maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Reset Your Password
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }} role="alert">
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              autoFocus
              label="New Password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              disabled={isLoading}
              helperText="At least 8 characters with uppercase, lowercase, and numbers"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock size={20} />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            {strength && (
              <Box sx={{ mt: 1, mb: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={strength.score}
                  color={strength.color}
                  sx={{ height: 4, borderRadius: 2 }}
                />
                <Typography variant="caption" color={`${strength.color}.main`} sx={{ mt: 0.5, display: 'block' }}>
                  {strength.label}
                </Typography>
              </Box>
            )}
            <TextField
              margin="normal"
              required
              fullWidth
              label="Confirm New Password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="off"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={isLoading}
              error={!!confirmPassword && confirmPassword !== newPassword}
              helperText={confirmPassword && confirmPassword !== newPassword ? 'Passwords do not match' : ''}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={isLoading || !newPassword || !confirmPassword || newPassword !== confirmPassword}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Reset Password'}
            </Button>
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
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}
