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
import { createFeeSchedule, type CreateFeeSchedulePayload } from '../api';

const feeScheduleSchema = z.object({
  fee_type: z.string().min(1, 'Fee type is required'),
  class_id: z.string().min(1, 'Class is required'),
  amount: z.number().min(1, 'Amount must be greater than 0'),
  due_date: z.string().min(1, 'Due date is required'),
  is_mandatory: z.boolean().optional(),
});

type FormValues = z.infer<typeof feeScheduleSchema>;

interface Props {
  open: boolean;
  onClose: () => void;
}

export function CreateFeeScheduleDialog({ open, onClose }: Props) {
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(feeScheduleSchema),
    defaultValues: {
      fee_type: '',
      class_id: '',
      amount: 0,
      due_date: '',
      is_mandatory: true,
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateFeeSchedulePayload) => createFeeSchedule(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['feeSchedules'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: FormValues) => {
    createMutation.mutate({ ...data, is_mandatory: data.is_mandatory ?? true });
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Add Fee Schedule</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller
            name="fee_type"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Fee Type"
                fullWidth
                error={!!errors.fee_type}
                helperText={errors.fee_type?.message}
              />
            )}
          />
          <Controller
            name="class_id"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth error={!!errors.class_id}>
                <InputLabel>Class</InputLabel>
                <Select {...field} label="Class">
                  <MenuItem value="jss1">JSS 1</MenuItem>
                  <MenuItem value="jss2">JSS 2</MenuItem>
                  <MenuItem value="jss3">JSS 3</MenuItem>
                  <MenuItem value="ss1">SS 1</MenuItem>
                  <MenuItem value="ss2">SS 2</MenuItem>
                  <MenuItem value="ss3">SS 3</MenuItem>
                </Select>
              </FormControl>
            )}
          />
          <Controller
            name="amount"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Amount (₦)"
                type="number"
                fullWidth
                error={!!errors.amount}
                helperText={errors.amount?.message}
                onChange={(e) => field.onChange(parseFloat(e.target.value))}
              />
            )}
          />
          <Controller
            name="due_date"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Due Date"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                error={!!errors.due_date}
                helperText={errors.due_date?.message}
              />
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
            {createMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
