import { useState } from 'react';
import {
  Box,
  Button,
  Chip,
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
  getInspections,
  createInspection,
  type Inspection,
  type CreateInspectionPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  passed: 'success',
  pending: 'warning',
  failed: 'error',
};

export function InspectionPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateInspectionPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['inspections'], queryFn: getInspections });

  const create = useMutation({
    mutationFn: (p: CreateInspectionPayload) => createInspection(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inspections'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<Inspection>[] = [
    {
      field: 'inspection_date',
      headerName: 'Date',
      width: 130,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    { field: 'inspector_name', headerName: 'Inspector', width: 180 },
    {
      field: 'status',
      headerName: 'Status',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'compliance_score',
      headerName: 'Compliance %',
      width: 130,
      valueGetter: (v: number) => `${v}%`,
    },
    { field: 'findings', headerName: 'Findings', width: 300 },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Inspection Tracking
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
            New Inspection
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
        <DialogTitle>New Inspection</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Inspector Name"
            value={form.inspector_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, inspector_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Inspection Date"
            type="date"
            value={form.inspection_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, inspection_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Compliance Score %"
            type="number"
            value={form.compliance_score ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, compliance_score: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Findings"
            value={form.findings ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, findings: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Recommendations"
            value={form.recommendations ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, recommendations: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateInspectionPayload)}
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
