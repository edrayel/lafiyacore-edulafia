import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { requestOTP, verifyOTP } from './api';

export function ParentLoginPage() {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');

  const requestMutation = useMutation({
    mutationFn: (phone: string) => requestOTP({ phone }),
    onSuccess: () => {
      setActiveStep(1);
      setError('');
    },
    onError: () => {
      setError('Failed to send OTP. Please check the phone number and try again.');
    },
  });

  const verifyMutation = useMutation({
    mutationFn: (otpCode: string) => verifyOTP({ phone: phoneNumber, otp_code: otpCode }),
    onSuccess: () => {
      navigate({ to: '/parent/children' });
    },
    onError: () => {
      setError('Invalid OTP. Please try again.');
    },
  });

  const handleRequestOTP = (e: React.FormEvent) => {
    e.preventDefault();
    if (!phoneNumber.trim()) return;
    requestMutation.mutate(phoneNumber);
  };

  const handleVerifyOTP = (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length < 6) return;
    verifyMutation.mutate(otp);
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper sx={{ p: 4, width: '100%' }}>
          <Typography variant="h4" sx={{ mb: 1, textAlign: 'center' }}>
            Parent Portal
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3, textAlign: 'center' }}>
            Sign in to view your children&apos;s information
          </Typography>

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            <Step>
              <StepLabel>Phone Number</StepLabel>
            </Step>
            <Step>
              <StepLabel>Verify OTP</StepLabel>
            </Step>
          </Stepper>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {activeStep === 0 && (
            <Box
              component="form"
              onSubmit={handleRequestOTP}
              sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
            >
              <TextField
                label="Phone Number"
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="+234..."
                required
                fullWidth
              />
              <Button
                type="submit"
                variant="contained"
                size="large"
                disabled={requestMutation.isPending}
              >
                {requestMutation.isPending ? <CircularProgress size={24} /> : 'Send OTP'}
              </Button>
            </Box>
          )}

          {activeStep === 0 && (
            <Button variant="text" sx={{ mt: 2 }} onClick={() => navigate({ to: '/login' })}>
              Back to Staff Login
            </Button>
          )}

          {activeStep === 1 && (
            <Box
              component="form"
              onSubmit={handleVerifyOTP}
              sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
            >
              <Alert severity="info" sx={{ mb: 1 }}>
                Enter the OTP sent to {phoneNumber}
              </Alert>
              <TextField
                label="OTP Code"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                inputProps={{ maxLength: 6 }}
                required
                fullWidth
                autoFocus
              />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="outlined"
                  onClick={() => {
                    setActiveStep(0);
                    setOtp('');
                    setError('');
                  }}
                  sx={{ flex: 1 }}
                >
                  Back
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  disabled={verifyMutation.isPending}
                  sx={{ flex: 2 }}
                >
                  {verifyMutation.isPending ? <CircularProgress size={24} /> : 'Verify & Sign In'}
                </Button>
              </Box>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  );
}
