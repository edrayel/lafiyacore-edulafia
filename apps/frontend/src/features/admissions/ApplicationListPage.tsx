import { useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import {
  Add as AddIcon,
  Check as CheckIcon,
  Close as CloseIcon,
  School as SchoolIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getApplications,
  createApplication,
  approveApplication,
  rejectApplication,
  enrollApplication,
  type Application,
  type CreateApplicationPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  approved: 'success',
  pending: 'warning',
  rejected: 'error',
  enrolled: 'success',
};

export function ApplicationListPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateApplicationPayload>>({ gender: 'male' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['applications'],
    queryFn: () => getApplications({ per_page: 100 }),
  });

  const create = useMutation({
    mutationFn: (p: CreateApplicationPayload) => createApplication(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      setOpen(false);
      setForm({ gender: 'male' });
    },
  });
  const approve = useMutation({
    mutationFn: approveApplication,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['applications'] }),
  });
  const reject = useMutation({
    mutationFn: (id: string) => rejectApplication(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['applications'] }),
  });
  const enroll = useMutation({
    mutationFn: enrollApplication,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['applications'] }),
  });

  const columns: GridColDef<Application>[] = [
    { field: 'first_name', headerName: 'First Name', width: 140 },
    { field: 'last_name', headerName: 'Last Name', width: 140 },
    { field: 'class_applied', headerName: 'Class', width: 100 },
    { field: 'exam_score', headerName: 'Exam Score', width: 110 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 200,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          {p.row.status === 'pending' && (
            <Button aria-label="Approve" size="small" onClick={() => approve.mutate(p.row.id)}>
              <CheckIcon fontSize="small" />
            </Button>
          )}
          {p.row.status === 'pending' && (
            <Button
              aria-label="Reject"
              size="small"
              color="error"
              onClick={() => reject.mutate(p.row.id)}
            >
              <CloseIcon fontSize="small" />
            </Button>
          )}
          {p.row.status === 'approved' && (
            <Button
              aria-label="Enroll"
              size="small"
              color="primary"
              onClick={() => enroll.mutate(p.row.id)}
            >
              <SchoolIcon fontSize="small" />
            </Button>
          )}
        </Box>
      ),
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Admissions
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
            New Application
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
          rows={data?.items ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(r) => r.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[10, 25, 50]}
          slots={{ noRowsOverlay: () => <DataEmptyState title="No applications found" message="There are no applications to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Application</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="First Name"
            value={form.first_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, first_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Last Name"
            value={form.last_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, last_name: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Class</InputLabel>
            <Select
              value={form.class_applied ?? ''}
              label="Class"
              onChange={(e) => setForm((f) => ({ ...f, class_applied: e.target.value }))}
            >
              <MenuItem value="jss1">JSS 1</MenuItem>
              <MenuItem value="jss2">JSS 2</MenuItem>
              <MenuItem value="jss3">JSS 3</MenuItem>
              <MenuItem value="ss1">SS 1</MenuItem>
              <MenuItem value="ss2">SS 2</MenuItem>
              <MenuItem value="ss3">SS 3</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Parent Name"
            value={form.parent_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, parent_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Parent Phone"
            value={form.parent_phone ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, parent_phone: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Date of Birth"
            type="date"
            value={form.date_of_birth ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, date_of_birth: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <FormControl fullWidth>
            <InputLabel>Gender</InputLabel>
            <Select
              value={form.gender ?? 'male'}
              label="Gender"
              onChange={(e) => setForm((f) => ({ ...f, gender: e.target.value }))}
            >
              <MenuItem value="male">Male</MenuItem>
              <MenuItem value="female">Female</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateApplicationPayload)}
            variant="contained"
            disabled={create.isPending}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
