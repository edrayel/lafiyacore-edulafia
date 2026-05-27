import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Typography,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useMutation } from '@tanstack/react-query';
import { initiateOnlinePayment, type RecordPaymentPayload } from '../api';

const onlinePaymentSchema = z.object({
  student_id: z.string().min(1, 'Student ID is required'),
  fee_schedule_id: z.string().min(1, 'Fee Schedule ID is required'),
  amount_paid: z.number().min(1, 'Amount must be greater than 0'),
});

type FormValues = z.infer<typeof onlinePaymentSchema>;

interface Props {
  open: boolean;
  onClose: () => void;
}

export function InitiateOnlinePaymentDialog({ open, onClose }: Props) {
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(onlinePaymentSchema),
    defaultValues: {
      student_id: '',
      fee_schedule_id: '',
      amount_paid: 0,
    },
  });

  const onlinePaymentMutation = useMutation({
    mutationFn: (p: RecordPaymentPayload) => initiateOnlinePayment(p),
    onSuccess: (data) => {
      onClose();
      reset();
      if (data?.payment_url) {
        window.open(data.payment_url, '_blank');
      }
    },
  });

  const onSubmit = (data: FormValues) => {
    onlinePaymentMutation.mutate({ ...data, payment_method: 'online' });
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Initiate Online Payment</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Provide the details below to generate an online payment link via the gateway.
          </Typography>
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
                label="Amount (₦)"
                type="number"
                fullWidth
                error={!!errors.amount_paid}
                helperText={errors.amount_paid?.message}
                onChange={(e) => field.onChange(parseFloat(e.target.value))}
              />
            )}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button
            type="submit"
            variant="contained"
            disabled={isSubmitting || onlinePaymentMutation.isPending}
          >
            {onlinePaymentMutation.isPending ? 'Processing...' : 'Pay Online'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
