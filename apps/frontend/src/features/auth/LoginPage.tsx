import { useState, useRef } from 'react';
import { useNavigate } from '@tanstack/react-router';
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Mail, Lock, GraduationCap, Eye, EyeOff } from 'lucide-react';
import { useAuthStore } from '@/shared/stores/authStore';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [password, setPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoading, error, clearError } = useAuthStore();
  const navigate = useNavigate();
  const formRef = useRef<HTMLFormElement>(null);

  const validateEmail = (value: string): boolean => {
    if (!value) {
      setEmailError('Email is required');
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      setEmailError('Please enter a valid email address');
      return false;
    }
    setEmailError('');
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    let valid = true;
    if (!validateEmail(email)) valid = false;
    if (!password) {
      setPasswordError('Password is required');
      valid = false;
    }
    if (!valid) return;
    try {
      await login(email, password);
      navigate({ to: '/' });
    } catch {
      // Error is surfaced through authStore.error
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: '#0a0f1c',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          width: '600px',
          height: '600px',
          background: 'radial-gradient(circle, rgba(45, 212, 191, 0.15) 0%, rgba(10, 15, 28, 0) 70%)',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 0,
          pointerEvents: 'none',
        }
      }}
    >
      <Paper
        elevation={0}
        sx={{
          p: { xs: 4, md: 6 },
          width: '100%',
          maxWidth: 440,
          borderRadius: '24px',
          bgcolor: 'rgba(17, 24, 39, 0.8)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
          position: 'relative',
          zIndex: 1,
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
        }}
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 1 }}>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: '16px',
              bgcolor: 'rgba(45, 212, 191, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mb: 3,
              color: '#2dd4bf',
            }}
          >
            <GraduationCap size={32} strokeWidth={1.5} />
          </Box>
          <Typography
            variant="h4"
            component="h1"
            sx={{
              fontWeight: 700,
              color: 'white',
              mb: 1
            }}
          >
            Welcome back
          </Typography>
          <Typography
            variant="body2"
            sx={{ color: 'rgba(255, 255, 255, 0.6)' }}
          >
            Please enter your details to sign in to EduLafia
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={clearError} role="alert">
            {error}
          </Alert>
        )}

        <Box
          component="form"
          ref={formRef}
          onSubmit={handleSubmit}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
        >
          <TextField
            fullWidth
            autoFocus
            label="Email address"
            placeholder="you@school.edu"
            value={email}
            onChange={(e) => { setEmail(e.target.value); if (emailError) setEmailError(''); }}
            onBlur={() => validateEmail(email)}
            error={!!emailError}
            helperText={emailError}
            disabled={isLoading}
            variant="outlined"
            required
            inputProps={{ autoComplete: 'email' }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Mail size={20} color="rgba(255, 255, 255, 0.4)" />
                </InputAdornment>
              ),
              sx: {
                borderRadius: '12px',
                bgcolor: 'rgba(0, 0, 0, 0.2)',
                color: 'white',
                '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.1)' },
                '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.2)' },
                '&.Mui-focused fieldset': { borderColor: '#2dd4bf' },
              }
            }}
          />
          <TextField
            fullWidth
            label="Password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => { setPassword(e.target.value); if (passwordError) setPasswordError(''); }}
            error={!!passwordError}
            helperText={passwordError}
            disabled={isLoading}
            variant="outlined"
            required
            inputProps={{ autoComplete: 'current-password' }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Lock size={20} color="rgba(255, 255, 255, 0.4)" />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={() => setShowPassword(!showPassword)}
                    edge="end"
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    sx={{ color: 'rgba(255, 255, 255, 0.5)' }}
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </IconButton>
                </InputAdornment>
              ),
              sx: {
                borderRadius: '12px',
                bgcolor: 'rgba(0, 0, 0, 0.2)',
                color: 'white',
                '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.1)' },
                '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.2)' },
                '&.Mui-focused fieldset': { borderColor: '#2dd4bf' },
              }
            }}
          />
          <Button
            fullWidth
            type="submit"
            variant="contained"
            disabled={isLoading}
            sx={{
              mt: 2,
              py: 1.5,
              borderRadius: '9999px',
              bgcolor: '#0d9488',
              color: 'white',
              fontSize: '1rem',
              fontWeight: 600,
              textTransform: 'none',
              boxShadow: 'none',
              '&:hover': {
                bgcolor: '#14b8a6',
                boxShadow: '0 4px 12px rgba(45, 212, 191, 0.2)',
              },
              '&.Mui-disabled': {
                bgcolor: 'rgba(255, 255, 255, 0.1)',
                color: 'rgba(255, 255, 255, 0.3)',
              }
            }}
          >
            {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
          </Button>
        </Box>

        <Typography
          variant="body2"
          align="center"
          onClick={() => navigate({ to: '/forgot-password' })}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') navigate({ to: '/forgot-password' }); }}
          sx={{
            mt: 2,
            color: 'rgba(255, 255, 255, 0.5)',
            cursor: 'pointer',
            transition: 'color 0.2s',
            '&:hover': { color: 'white' },
            '&:focus-visible': { outline: '2px solid #2dd4bf', outlineOffset: '4px', borderRadius: '4px' },
          }}
        >
          Forgot your password? Reset password
        </Typography>
      </Paper>
    </Box>
  );
}
