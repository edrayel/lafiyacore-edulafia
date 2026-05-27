import { useState } from 'react';
import {
  Alert,
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
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import {
  Add as AddIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getEmergencies,
  getActiveEmergency,
  activateEmergency,
  deactivateEmergency,
  type Emergency,
  type ActivateEmergencyPayload,
} from './api';

export function EmergencyPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<ActivateEmergencyPayload>>({});
  const queryClient = useQueryClient();

  const { data: active } = useQuery({ queryKey: ['activeEmergency'], queryFn: getActiveEmergency });
  const { data, isLoading } = useQuery({ queryKey: ['emergencies'], queryFn: getEmergencies });

  const activate = useMutation({
    mutationFn: (p: ActivateEmergencyPayload) => activateEmergency(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emergencies'] });
      queryClient.invalidateQueries({ queryKey: ['activeEmergency'] });
      setOpen(false);
      setForm({});
    },
  });
  const deactivate = useMutation({
    mutationFn: deactivateEmergency,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emergencies'] });
      queryClient.invalidateQueries({ queryKey: ['activeEmergency'] });
    },
  });

  const columns: GridColDef<Emergency>[] = [
    { field: 'title', headerName: 'Title', width: 200 },
    { field: 'description', headerName: 'Description', width: 300 },
    { field: 'status', headerName: 'Status', width: 120 },
    {
      field: 'activated_at',
      headerName: 'Activated',
      width: 180,
      valueGetter: (v: string) => new Date(v).toLocaleString(),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) =>
        p.row.status === 'active' ? (
          <Button size="small" color="error" onClick={() => deactivate.mutate(p.row.id)}>
            Deactivate
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
          Emergency Management
        </Typography>
      </Box>
      {active && (
        <Alert severity="error" icon={<WarningIcon />} sx={{ mb: 2 }}>
          Active Emergency: {active.title} — {active.description}
        </Alert>
      )}
      {!active && (
        <Alert severity="success" icon={<CheckCircleIcon />} sx={{ mb: 2 }}>
          No active emergencies
        </Alert>
      )}
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
            disabled={!!active}
          >
            Activate Emergency
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
          slots={{ noRowsOverlay: () => <DataEmptyState title="No emergencies found" message="There are no emergencies to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Activate Emergency</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Title"
            value={form.title ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Description"
            value={form.description ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            fullWidth
            multiline
            rows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => activate.mutate(form as ActivateEmergencyPayload)}
            variant="contained"
            disabled={activate.isPending}
          >
            Activate
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
