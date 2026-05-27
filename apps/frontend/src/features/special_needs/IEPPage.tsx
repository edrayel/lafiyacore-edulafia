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
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getIEPs, createIEP, type IEP, type CreateIEPPayload } from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  pending: 'warning',
  completed: 'default',
  expired: 'error',
};

export function IEPPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateIEPPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['ieps'], queryFn: () => getIEPs() });

  const create = useMutation({
    mutationFn: (p: CreateIEPPayload) => createIEP(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ieps'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<IEP>[] = [
    { field: 'student_name', headerName: 'Student', width: 180 },
    { field: 'disability_type', headerName: 'Disability Type', width: 160 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'review_date',
      headerName: 'Review Date',
      width: 140,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    { field: 'goals', headerName: 'Goals', width: 250 },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Special Needs / IEPs
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
            New IEP
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
        <DialogTitle>New IEP</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={form.student_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Disability Type</InputLabel>
            <Select
              value={form.disability_type ?? ''}
              label="Disability Type"
              onChange={(e) => setForm((f) => ({ ...f, disability_type: e.target.value }))}
            >
              <MenuItem value="visual">Visual Impairment</MenuItem>
              <MenuItem value="hearing">Hearing Impairment</MenuItem>
              <MenuItem value="learning">Learning Disability</MenuItem>
              <MenuItem value="physical">Physical Disability</MenuItem>
              <MenuItem value="autism">Autism Spectrum</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Goals"
            value={form.goals ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, goals: e.target.value }))}
            fullWidth
            multiline
            rows={3}
          />
          <TextField
            label="Accommodations"
            value={form.accommodations ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, accommodations: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Review Date"
            type="date"
            value={form.review_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, review_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateIEPPayload)}
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
