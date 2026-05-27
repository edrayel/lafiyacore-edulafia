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
import { createStudent, generateAdmissionNumber, type CreateStudentPayload } from '../api';

const createStudentSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  middle_name: z.string().optional(),
  nin: z.string().optional(),
  admission_number: z.string().min(1, 'Admission number is required'),
  date_of_birth: z.string().min(1, 'Date of birth is required'),
  gender: z.enum(['male', 'female']),
});

type CreateFormValues = z.infer<typeof createStudentSchema>;

interface CreateStudentDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CreateStudentDialog({ open, onClose }: CreateStudentDialogProps) {
  const queryClient = useQueryClient();

  const {
    control,
    handleSubmit,
    reset,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<CreateFormValues>({
    resolver: zodResolver(createStudentSchema),
    defaultValues: {
      first_name: '',
      last_name: '',
      middle_name: '',
      nin: '',
      admission_number: '',
      date_of_birth: new Date().toISOString().split('T')[0],
      gender: 'male',
    },
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateStudentPayload) => createStudent(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: CreateFormValues) => {
    createMutation.mutate({
      ...data,
      admission_date: new Date().toISOString().split('T')[0],
    });
  };

  const handleAutoGenerateAdmission = async () => {
    try {
      const { admission_number } = await generateAdmissionNumber();
      setValue('admission_number', admission_number);
    } catch {
      console.warn('Could not auto-generate admission number');
      // Admission number can be entered manually
    }
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Add Student</DialogTitle>
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
            name="middle_name"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Middle Name"
                fullWidth
                error={!!errors.middle_name}
                helperText={errors.middle_name?.message}
              />
            )}
          />
          <Controller
            name="nin"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="NIN (National Identification Number)"
                fullWidth
                placeholder="11-digit NIN"
                error={!!errors.nin}
                helperText={errors.nin?.message}
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
                InputProps={{
                  endAdornment: (
                    <Button size="small" onClick={handleAutoGenerateAdmission}>
                      Auto
                    </Button>
                  ),
                }}
              />
            )}
          />
          <Controller
            name="date_of_birth"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                type="date"
                label="Date of Birth"
                fullWidth
                InputLabelProps={{ shrink: true }}
                error={!!errors.date_of_birth}
                helperText={errors.date_of_birth?.message}
              />
            )}
          />
          <Controller
            name="gender"
            control={control}
            render={({ field }) => (
              <FormControl fullWidth error={!!errors.gender}>
                <InputLabel>Gender</InputLabel>
                <Select {...field} label="Gender">
                  <MenuItem value="male">Male</MenuItem>
                  <MenuItem value="female">Female</MenuItem>
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
            {createMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
