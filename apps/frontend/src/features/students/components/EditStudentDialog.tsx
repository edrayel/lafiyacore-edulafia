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
import { updateStudent } from '../api';
import type { Student } from '@/shared/types';
import { useEffect } from 'react';

const editStudentSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  admission_number: z.string().min(1, 'Admission number is required'),
  status: z.enum(['active', 'archived', 'graduated', 'withdrawn', 'suspended']),
});

type EditFormValues = z.infer<typeof editStudentSchema>;

interface EditStudentDialogProps {
  open: boolean;
  onClose: () => void;
  student: Student | null;
}

export function EditStudentDialog({ open, onClose, student }: EditStudentDialogProps) {
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<EditFormValues>({
    resolver: zodResolver(editStudentSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      admission_number: '',
      status: 'active',
    },
  });

  useEffect(() => {
    if (student && open) {
      reset({
        first_name: student.first_name,
        last_name: student.last_name,
        admission_number: student.admission_number,
        status: student.status as EditFormValues['status'],
      });
    }
  }, [student, open, reset]);

  const updateMutation = useMutation({
    mutationFn: (payload: EditFormValues) => updateStudent(student!.id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: EditFormValues) => {
    if (!student) return;
    updateMutation.mutate(data);
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Edit Student</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Controller
            name="first_name"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="First Name"
                fullWidth
                error={!!errors.first_name}
                helperText={errors.first_name?.message}
              />
            )}
          />
          <Controller
            name="last_name"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Last Name"
                fullWidth
                error={!!errors.last_name}
                helperText={errors.last_name?.message}
              />
            )}
          />
          <Controller
            name="admission_number"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Admission Number"
                fullWidth
                error={!!errors.admission_number}
                helperText={errors.admission_number?.message}
              />
            )}
          />
          <Controller
            name="status"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth error={!!errors.status}>
                <InputLabel>Status</InputLabel>
                <Select {...field} label="Status">
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="archived">Archived</MenuItem>
                  <MenuItem value="graduated">Graduated</MenuItem>
                  <MenuItem value="withdrawn">Withdrawn</MenuItem>
                  <MenuItem value="suspended">Suspended</MenuItem>
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
            disabled={isSubmitting || updateMutation.isPending}
          >
            {updateMutation.isPending ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
