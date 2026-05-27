import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { recordPayment, type RecordPaymentPayload } from '../api';

const recordPaymentSchema = z.object({
  student_id: z.string().min(1, 'Student ID is required'),
  fee_schedule_id: z.string().min(1, 'Fee Schedule ID is required'),
  amount_paid: z.number().min(1, 'Amount must be greater than 0'),
  payment_method: z.enum(['cash', 'transfer', 'pos', 'cheque']),
});

type FormValues = z.infer<typeof recordPaymentSchema>;

interface Props {
  open: boolean;
  onClose: () => void;
}

export function RecordPaymentDialog({ open, onClose }: Props) {
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(recordPaymentSchema),
    defaultValues: {
      student_id: '',
      fee_schedule_id: '',
      amount_paid: 0,
      payment_method: 'cash',
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload: RecordPaymentPayload) => recordPayment(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payments'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: FormValues) => {
    createMutation.mutate(data);
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Record Payment</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller
            name="student_id"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Student ID"
                fullWidth
                error={!!errors.student_id}
                helperText={errors.student_id?.message}
              />
            )}
          />
          <Controller
            name="fee_schedule_id"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Fee Schedule ID"
                fullWidth
                error={!!errors.fee_schedule_id}
                helperText={errors.fee_schedule_id?.message}
              />
            )}
          />
          <Controller
            name="amount_paid"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Amount Paid (₦)"
                type="number"
                fullWidth
                error={!!errors.amount_paid}
                helperText={errors.amount_paid?.message}
                onChange={(e) => field.onChange(parseFloat(e.target.value))}
              />
            )}
          />
          <Controller
            name="payment_method"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth error={!!errors.payment_method}>
                <InputLabel>Payment Method</InputLabel>
                <Select {...field} label="Payment Method">
                  <MenuItem value="cash">Cash</MenuItem>
                  <MenuItem value="transfer">Bank Transfer</MenuItem>
                  <MenuItem value="pos">POS</MenuItem>
                  <MenuItem value="cheque">Cheque</MenuItem>
                </Select>
              </FormControl>
            )}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button
            type="submit"
            variant="contained"
            disabled={isSubmitting || createMutation.isPending}
          >
            {createMutation.isPending ? 'Recording...' : 'Record'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
