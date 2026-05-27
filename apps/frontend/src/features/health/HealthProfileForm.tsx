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
  Box,
  Typography,
  FormHelperText,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createHealthProfile, type HealthProfile } from './api';
import { useAuthStore } from '@/shared/stores/authStore';

const profileSchema = z.object({
  student_id: z.string().min(1, 'Student ID is required'),
  blood_group: z.string().optional(),
  genotype: z.string().optional(),
  allergies: z.string().optional(),
  chronic_conditions: z.string().optional(),
  current_medications: z.string().optional(),
  disability_status: z.string().optional(),
  emergency_notes: z.string().optional(),
  parental_consent_given: z.boolean(),
});

type ProfileFormValues = z.infer<typeof profileSchema>;

interface HealthProfileFormProps {
  open: boolean;
  onClose: () => void;
}

export function HealthProfileForm({ open, onClose }: HealthProfileFormProps) {
  const queryClient = useQueryClient();
  const schoolId = useAuthStore((s) => s.user?.school_id);

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      student_id: '',
      blood_group: '',
      genotype: '',
      allergies: '',
      chronic_conditions: '',
      current_medications: '',
      disability_status: '',
      emergency_notes: '',
      parental_consent_given: false,
    },
  });

  const createMutation = useMutation({
    mutationFn: (
      payload: Omit<HealthProfile, 'id' | 'created_at' | 'updated_at' | 'version'>
    ) => createHealthProfile(payload.student_id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['healthProfile'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: ProfileFormValues) => {
    // Transform comma-separated strings back to arrays
    const payload: Omit<HealthProfile, 'id' | 'created_at' | 'updated_at' | 'version'> = {
      student_id: data.student_id,
      school_id: schoolId ?? '',
      blood_group: data.blood_group || undefined,
      genotype: data.genotype || undefined,
      disability_status: data.disability_status || undefined,
      emergency_notes: data.emergency_notes || undefined,
      parental_consent_given: data.parental_consent_given,
      allergies: data.allergies
        ? data.allergies
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean)
        : [],
      chronic_conditions: data.chronic_conditions
        ? data.chronic_conditions
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean)
        : [],
      current_medications: data.current_medications
        ? data.current_medications
            .split(',')
            .map((s) => s.trim())
            .filter(Boolean)
        : [],
    };
    createMutation.mutate(payload);
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Student Health Profile</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Box>
            <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
              Basic Info
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
          </Box>

          <Box>
            <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
              Blood & Physical
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Controller
                name="blood_group"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.blood_group}>
                    <InputLabel>Blood Group</InputLabel>
                    <Select {...field} label="Blood Group">
                      <MenuItem value="">
                        <em>None</em>
                      </MenuItem>
                      {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map((bg) => (
                        <MenuItem key={bg} value={bg}>
                          {bg}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.blood_group && (
                      <FormHelperText>{errors.blood_group.message}</FormHelperText>
                    )}
                  </FormControl>
                )}
              />
              <Controller
                name="genotype"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.genotype}>
                    <InputLabel>Genotype</InputLabel>
                    <Select {...field} label="Genotype">
                      <MenuItem value="">
                        <em>None</em>
                      </MenuItem>
                      {['AA', 'AS', 'SS', 'AC', 'SC'].map((g) => (
                        <MenuItem key={g} value={g}>
                          {g}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.genotype && <FormHelperText>{errors.genotype.message}</FormHelperText>}
                  </FormControl>
                )}
              />
            </Box>
          </Box>

          <Box>
            <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
              Conditions & Allergies
            </Typography>
            <Controller
              name="allergies"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Allergies (comma separated)"
                  fullWidth
                  sx={{ mb: 2 }}
                />
              )}
            />
            <Controller
              name="chronic_conditions"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Chronic Conditions (comma separated)"
                  fullWidth
                  sx={{ mb: 2 }}
                />
              )}
            />
            <Controller
              name="current_medications"
              control={control}
              render={({ field }) => (
                <TextField {...field} label="Current Medications (comma separated)" fullWidth />
              )}
            />
          </Box>

          <Box>
            <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
              Consent & Notes
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Controller
                name="parental_consent_given"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Parental Consent</InputLabel>
                    <Select
                      value={field.value ? 'yes' : 'no'}
                      label="Parental Consent"
                      onChange={(e) => field.onChange(e.target.value === 'yes')}
                    >
                      <MenuItem value="no">No</MenuItem>
                      <MenuItem value="yes">Yes</MenuItem>
                    </Select>
                  </FormControl>
                )}
              />
              <Controller
                name="disability_status"
                control={control}
                render={({ field }) => <TextField {...field} label="Disability Status" fullWidth />}
              />
            </Box>
            <Controller
              name="emergency_notes"
              control={control}
              render={({ field }) => (
                <TextField {...field} label="Emergency Notes" fullWidth multiline rows={3} sx={{ mt: 2 }} />
              )}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button
            type="submit"
            variant="contained"
            disabled={isSubmitting || createMutation.isPending}
          >
            {createMutation.isPending ? 'Saving...' : 'Save Profile'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
