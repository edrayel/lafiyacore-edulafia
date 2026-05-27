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
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getPayrollRuns,
  createPayrollRun,
  processPayrollRun,
  type PayrollRun,
  type CreatePayrollPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  draft: 'default',
  processing: 'warning',
  completed: 'success',
  failed: 'error',
};

export function PayrollPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreatePayrollPayload>>({
    month: new Date().getMonth() + 1,
    year: new Date().getFullYear(),
  });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['payrollRuns'],
    queryFn: () => getPayrollRuns(),
  });

  const create = useMutation({
    mutationFn: (p: CreatePayrollPayload) => createPayrollRun(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payrollRuns'] });
      setOpen(false);
      setForm({});
    },
  });
  const process = useMutation({
    mutationFn: processPayrollRun,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['payrollRuns'] }),
  });

  const fmt = (n: number) => `₦${n.toLocaleString()}`;

  const columns: GridColDef<PayrollRun>[] = [
    {
      field: 'month',
      headerName: 'Month',
      width: 100,
      valueGetter: (v: number) =>
        new Date(2000, v - 1).toLocaleString('default', { month: 'short' }),
    },
    { field: 'year', headerName: 'Year', width: 80 },
    { field: 'total_gross', headerName: 'Gross', width: 140, valueGetter: (v: number) => fmt(v) },
    {
      field: 'total_deductions',
      headerName: 'Deductions',
      width: 140,
      valueGetter: (v: number) => fmt(v),
    },
    { field: 'total_net', headerName: 'Net Pay', width: 140, valueGetter: (v: number) => fmt(v) },
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
          <Button size="small" onClick={() => process.mutate(p.row.id)}>
            Process
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
          Payroll
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
            New Payroll Run
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
          slots={{ noRowsOverlay: () => <DataEmptyState title="No payroll runs found" message="There are no payroll runs to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Payroll Run</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Month</InputLabel>
            <Select
              value={form.month ?? ''}
              label="Month"
              onChange={(e) => setForm((f) => ({ ...f, month: +e.target.value }))}
            >
              {Array.from({ length: 12 }, (_, i) => (
                <MenuItem key={i + 1} value={i + 1}>
                  {new Date(2000, i).toLocaleString('default', { month: 'long' })}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Year</InputLabel>
            <Select
              value={form.year ?? ''}
              label="Year"
              onChange={(e) => setForm((f) => ({ ...f, year: +e.target.value }))}
            >
              {[2024, 2025, 2026].map((y) => (
                <MenuItem key={y} value={y}>
                  {y}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreatePayrollPayload)}
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
