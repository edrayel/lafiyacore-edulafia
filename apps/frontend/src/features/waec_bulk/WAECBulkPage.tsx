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
  Toolbar,
  Typography,
} from '@mui/material';
import { Add as AddIcon, Upload as UploadIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getWAECBulkRegistrations,
  createWAECBulkRegistration,
  submitWAECBulkRegistration,
  type WAECBulkRegistration,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  draft: 'default',
  submitted: 'success',
  processing: 'warning',
  completed: 'success',
  failed: 'error',
};

export function WAECBulkPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ exam_year: 2026, class_id: '' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['waecBulk'],
    queryFn: () => getWAECBulkRegistrations(),
  });

  const create = useMutation({
    mutationFn: createWAECBulkRegistration,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['waecBulk'] });
      setOpen(false);
      setForm({ exam_year: 2026, class_id: '' });
    },
  });
  const submit = useMutation({
    mutationFn: submitWAECBulkRegistration,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['waecBulk'] }),
  });

  const columns: GridColDef<WAECBulkRegistration>[] = [
    { field: 'exam_year', headerName: 'Year', width: 80 },
    { field: 'class_name', headerName: 'Class', width: 120 },
    { field: 'total_registered', headerName: 'Registered', width: 120 },
    { field: 'total_students', headerName: 'Total Students', width: 140 },
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
      width: 120,
      sortable: false,
      renderCell: (p) =>
        p.row.status === 'draft' ? (
          <Button aria-label="Submit" size="small" onClick={() => submit.mutate(p.row.id)}>
            <UploadIcon fontSize="small" />
          </Button>
        ) : null,
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          WAEC Bulk Registration
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
            New Registration
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
        <DialogTitle>New WAEC Bulk Registration</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Exam Year</InputLabel>
            <Select
              value={form.exam_year}
              label="Exam Year"
              onChange={(e) => setForm((f) => ({ ...f, exam_year: +e.target.value }))}
            >
              <MenuItem value={2025}>2025</MenuItem>
              <MenuItem value={2026}>2026</MenuItem>
              <MenuItem value={2027}>2027</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Class</InputLabel>
            <Select
              value={form.class_id}
              label="Class"
              onChange={(e) => setForm((f) => ({ ...f, class_id: e.target.value }))}
            >
              <MenuItem value="ss3">SS 3</MenuItem>
              <MenuItem value="ss2">SS 2</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form)}
            variant="contained"
            disabled={create.isPending}
          >
            Register
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
