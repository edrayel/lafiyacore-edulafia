import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Typography,
} from '@mui/material';
import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { reversePayment, type Payment } from '../api';

interface Props {
  open: boolean;
  onClose: () => void;
  payment: Payment | null;
}

export function ReversePaymentDialog({ open, onClose, payment }: Props) {
  const queryClient = useQueryClient();
  const [reason, setReason] = useState('');

  const reversePaymentMutation = useMutation({
    mutationFn: ({ id, reasonText }: { id: string; reasonText: string }) =>
      reversePayment(id, reasonText),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payments'] });
      setReason('');
      onClose();
    },
  });

  const handleConfirm = () => {
    if (payment && reason.trim()) {
      reversePaymentMutation.mutate({ id: payment.id, reasonText: reason });
    }
  };

  const handleClose = () => {
    setReason('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Reverse Payment</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Are you sure you want to reverse this payment? This action will mark the payment as
          reversed and restore the student's balance. A mandatory reason is required for auditing
          purposes.
        </Typography>
        <TextField
          label="Reversal Reason (Mandatory)"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          fullWidth
          multiline
          rows={3}
          required
          error={reason.length === 0}
          helperText={reason.length === 0 ? 'Reason is required' : ''}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button
          onClick={handleConfirm}
          variant="contained"
          color="error"
          disabled={!reason.trim() || reversePaymentMutation.isPending}
        >
          {reversePaymentMutation.isPending ? 'Reversing...' : 'Confirm Reversal'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
