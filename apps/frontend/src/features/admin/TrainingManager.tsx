import { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
} from '@mui/material';
import { Grid } from '@mui/material';
import { PlayCircleOutline as PlayIcon, Add as AddIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listTrainingResources, createTrainingResource, type TrainingResource } from './api';

interface TrainingForm {
  title: string;
  description: string;
  resource_type: string;
  url: string;
  category: string;
  target_role: string;
}

export function TrainingManager() {
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<TrainingForm>({
    title: '',
    description: '',
    resource_type: 'video',
    url: '',
    category: 'onboarding',
    target_role: 'teacher',
  });

  const { data: resources, isLoading } = useQuery({
    queryKey: ['training-resources'],
    queryFn: listTrainingResources,
  });

  const createMutation = useMutation({
    mutationFn: createTrainingResource,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['training-resources'] });
      setOpen(false);
      setForm({
        title: '',
        description: '',
        resource_type: 'video',
        url: '',
        category: 'onboarding',
        target_role: 'teacher',
      });
    },
  });

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Training Resource Library
        </Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)}>
          Upload New Module
        </Button>
      </Box>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : resources && resources.length > 0 ? (
        <Grid container spacing={3}>
          {resources.map((m: TrainingResource) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={m.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" sx={{ mb: 1 }}>
                    {m.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    {m.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                    <Chip label={m.resource_type} size="small" color="primary" variant="outlined" />
                    <Chip label={m.category} size="small" />
                    <Chip label={m.target_role} size="small" />
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<PlayIcon />}
                      onClick={() => window.open(m.url, '_blank')}
                    >
                      Preview
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <Typography color="textSecondary" sx={{ textAlign: 'center', p: 4 }}>
          No training resources available.
        </Typography>
      )}

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Upload Training Module</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Title"
            fullWidth
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
          <TextField
            label="Description"
            fullWidth
            multiline
            rows={2}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
          <TextField
            label="URL (Video or PDF link)"
            fullWidth
            value={form.url}
            onChange={(e) => setForm({ ...form, url: e.target.value })}
          />
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Resource Type</InputLabel>
              <Select
                value={form.resource_type}
                label="Resource Type"
                onChange={(e) => setForm({ ...form, resource_type: e.target.value })}
              >
                <MenuItem value="video">Video</MenuItem>
                <MenuItem value="document">Document (PDF)</MenuItem>
                <MenuItem value="interactive">Interactive</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={form.category}
                label="Category"
                onChange={(e) => setForm({ ...form, category: e.target.value })}
              >
                <MenuItem value="onboarding">Onboarding</MenuItem>
                <MenuItem value="sentinel">Sentinel Surveillance</MenuItem>
                <MenuItem value="general">General</MenuItem>
              </Select>
            </FormControl>
          </Box>
          <FormControl fullWidth>
            <InputLabel>Target Role</InputLabel>
            <Select
              value={form.target_role}
              label="Target Role"
              onChange={(e) => setForm({ ...form, target_role: e.target.value })}
            >
              <MenuItem value="all">All Staff</MenuItem>
              <MenuItem value="teacher">Teachers</MenuItem>
              <MenuItem value="nurse">School Nurses</MenuItem>
              <MenuItem value="admin">Administrators</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => createMutation.mutate(form)}
            disabled={!form.title || !form.url || createMutation.isPending}
          >
            {createMutation.isPending ? 'Uploading...' : 'Upload'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
