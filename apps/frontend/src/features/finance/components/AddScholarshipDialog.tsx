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
import { createScholarship, type CreateScholarshipPayload } from '../api';

const scholarshipSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
  discount_type: z.enum(['percentage', 'fixed']),
  discount_value: z.number().min(1, 'Value must be greater than 0'),
  is_active: z.boolean().optional(),
});

type FormValues = z.infer<typeof scholarshipSchema>;

interface Props {
  open: boolean;
  onClose: () => void;
}

export function AddScholarshipDialog({ open, onClose }: Props) {
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(scholarshipSchema),
    defaultValues: {
      name: '',
      description: '',
      discount_type: 'percentage',
      discount_value: 0,
      is_active: true,
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateScholarshipPayload) => createScholarship(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scholarships'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: FormValues) => {
    createMutation.mutate({ ...data, is_active: data.is_active ?? true });
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Add Scholarship</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller
            name="name"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Name"
                fullWidth
                error={!!errors.name}
                helperText={errors.name?.message}
              />
            )}
          />
          <Controller
            name="description"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Description"
                fullWidth
                multiline
                rows={2}
                error={!!errors.description}
                helperText={errors.description?.message}
              />
            )}
          />
          <Controller
            name="discount_type"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth error={!!errors.discount_type}>
                <InputLabel>Discount Type</InputLabel>
                <Select {...field} label="Discount Type">
                  <MenuItem value="percentage">Percentage</MenuItem>
                  <MenuItem value="fixed">Fixed Amount</MenuItem>
                </Select>
              </FormControl>
            )}
          />
          <Controller
            name="discount_value"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Discount Value"
                type="number"
                fullWidth
                error={!!errors.discount_value}
                helperText={errors.discount_value?.message}
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
            disabled={isSubmitting || createMutation.isPending}
          >
            {createMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
