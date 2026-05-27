import { useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getAlumniProfiles,
  createAlumniProfile,
  type AlumniProfile,
  type CreateAlumniProfilePayload,
} from './api';

export function AlumniPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateAlumniProfilePayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['alumni'],
    queryFn: () => getAlumniProfiles(),
  });

  const create = useMutation({
    mutationFn: (p: CreateAlumniProfilePayload) => createAlumniProfile(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alumni'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<AlumniProfile>[] = [
    { field: 'student_id', headerName: 'Student ID', width: 280 },
    { field: 'graduation_year', headerName: 'Graduation Year', width: 140 },
    { field: 'current_occupation', headerName: 'Current Occupation', width: 200 },
    { field: 'university', headerName: 'University', width: 200 },
    { field: 'linkedin_url', headerName: 'LinkedIn URL', width: 200 },
    { field: 'contact_email', headerName: 'Contact Email', width: 200 },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Alumni Network
        </Typography>
      </Box>
      <Paper
        elevation={0}
        sx={{
          p: 2,
          mb: 3,
          border: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
        }}
      >
        <Toolbar>
          <Box sx={{ flexGrow: 1 }} />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{
              borderRadius: 2,
              px: 3,
              py: 1,
              fontWeight: 600,
              boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)',
              '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' },
            }}
            onClick={() => setOpen(true)}
          >
            New Alumni
          </Button>
        </Toolbar>
      </Paper>
      <Paper
        elevation={0}
        sx={{
          height: 500,
          width: '100%',
          border: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
          overflow: 'hidden',
        }}
      >
        <DataGrid
          rows={data ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(r) => r.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[10, 25, 50]}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Alumni Profile</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID (UUID)"
            value={form.student_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
            sx={{ mt: 1 }}
          />
          <TextField
            label="Graduation Year"
            type="number"
            value={form.graduation_year ?? ''}
            onChange={(e) =>
              setForm((f) => ({ ...f, graduation_year: parseInt(e.target.value, 10) }))
            }
            fullWidth
          />
          <TextField
            label="Current Occupation"
            value={form.current_occupation ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, current_occupation: e.target.value }))}
            fullWidth
          />
          <TextField
            label="University"
            value={form.university ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, university: e.target.value }))}
            fullWidth
          />
          <TextField
            label="LinkedIn URL"
            value={form.linkedin_url ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, linkedin_url: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Contact Email"
            type="email"
            value={form.contact_email ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, contact_email: e.target.value }))}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateAlumniProfilePayload)}
            variant="contained"
            disabled={create.isPending || !form.student_id || !form.graduation_year}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
