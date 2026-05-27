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
import { getSMCReports, createSMCReport, type SMCReport, type CreateSMCReportPayload } from './api';

export function SMCPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateSMCReportPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['smcReports'], queryFn: getSMCReports });

  const create = useMutation({
    mutationFn: (p: CreateSMCReportPayload) => createSMCReport(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['smcReports'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<SMCReport>[] = [
    {
      field: 'report_date',
      headerName: 'Date',
      width: 130,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    { field: 'attendance_count', headerName: 'Attendance', width: 120 },
    { field: 'financial_summary', headerName: 'Financial Summary', width: 250 },
    { field: 'challenges', headerName: 'Challenges', width: 250 },
    { field: 'resolutions', headerName: 'Resolutions', width: 250 },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          SMC Reporting
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
            New Report
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
        <DialogTitle>New SMC Report</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Report Date"
            type="date"
            value={form.report_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, report_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Attendance Count"
            type="number"
            value={form.attendance_count ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, attendance_count: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Financial Summary"
            value={form.financial_summary ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, financial_summary: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Challenges"
            value={form.challenges ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, challenges: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Resolutions"
            value={form.resolutions ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, resolutions: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateSMCReportPayload)}
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
