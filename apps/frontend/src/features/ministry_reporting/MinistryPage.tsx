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
import { Add as AddIcon, Upload as UploadIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getMinistryReports, generateReport, submitReport, type MinistryReport } from './api';

export function MinistryPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ report_type: 'enrollment', period: '' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['ministryReports'],
    queryFn: () => getMinistryReports(),
  });

  const generate = useMutation({
    mutationFn: generateReport,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ministryReports'] });
      setOpen(false);
      setForm({ report_type: 'enrollment', period: '' });
    },
  });
  const submit = useMutation({
    mutationFn: submitReport,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['ministryReports'] }),
  });

  const columns: GridColDef<MinistryReport>[] = [
    { field: 'report_type', headerName: 'Type', width: 180 },
    { field: 'period', headerName: 'Period', width: 140 },
    {
      field: 'submitted',
      headerName: 'Submitted',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value ? 'Yes' : 'No'} size="small" color={p.value ? 'success' : 'warning'} />
      ),
    },
    {
      field: 'submitted_at',
      headerName: 'Submitted At',
      width: 160,
      valueGetter: (v: string) => (v ? new Date(v).toLocaleDateString() : '—'),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) =>
        !p.row.submitted ? (
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
          Ministry Reporting
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
            Generate Report
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
        <DialogTitle>Generate Report</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Report Type</InputLabel>
            <Select
              value={form.report_type}
              label="Report Type"
              onChange={(e) => setForm((f) => ({ ...f, report_type: e.target.value }))}
            >
              <MenuItem value="enrollment">Enrollment</MenuItem>
              <MenuItem value="attendance">Attendance</MenuItem>
              <MenuItem value="academic">Academic Performance</MenuItem>
              <MenuItem value="financial">Financial</MenuItem>
              <MenuItem value="staff">Staff</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Period"
            value={form.period}
            onChange={(e) => setForm((f) => ({ ...f, period: e.target.value }))}
            fullWidth
            placeholder="e.g. 2025-Q4"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => generate.mutate(form)}
            variant="contained"
            disabled={generate.isPending}
          >
            Generate
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
