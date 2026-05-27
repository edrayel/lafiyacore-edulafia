import { Box, Typography, Paper, TextField, Button, Alert } from '@mui/material';
import { useState } from 'react';
import { VerifiedUser as VerifiedIcon } from '@mui/icons-material';

import { verifyCertificate } from './api';

export function VerificationPage() {
  const [certId, setCertId] = useState('');
  const [result, setResult] = useState<'success' | 'error' | null>(null);
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    setLoading(true);
    try {
      await verifyCertificate(certId.trim());
      setResult('success');
    } catch {
      setResult('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 800, mb: 2, textAlign: 'center' }}>
        Public Certificate Verification
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 4, textAlign: 'center' }}>
        Enter the Certificate ID or Document Hash below to verify its authenticity across the
        EduLafia network.
      </Typography>

      <Paper sx={{ p: 4, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
        <TextField
          fullWidth
          label="Certificate ID / Hash"
          value={certId}
          onChange={(e) => setCertId(e.target.value)}
          sx={{ mb: 3 }}
        />
        <Button
          fullWidth
          variant="contained"
          size="large"
          onClick={handleVerify}
          disabled={loading || !certId}
        >
          {loading ? 'Verifying...' : 'Verify Document'}
        </Button>
      </Paper>

      {result === 'success' && (
        <Alert icon={<VerifiedIcon fontSize="inherit" />} severity="success" sx={{ mt: 3 }}>
          <strong>Document Verified!</strong> The provided ID matches a valid record in the EduLafia
          registry.
        </Alert>
      )}

      {result === 'error' && (
        <Alert severity="error" sx={{ mt: 3 }}>
          <strong>Verification Failed!</strong> The provided ID could not be found or is invalid.
        </Alert>
      )}
    </Box>
  );
}
