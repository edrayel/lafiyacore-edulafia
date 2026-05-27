import { useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Paper,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getRetentionPolicies,
  createRetentionPolicy,
  type RetentionPolicy,
  type CreateRetentionPolicyPayload,
} from './api';

export function RetentionPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateRetentionPolicyPayload>>({ auto_delete: false });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['retentionPolicies'],
    queryFn: getRetentionPolicies,
  });

  const create = useMutation({
    mutationFn: (p: CreateRetentionPolicyPayload) => createRetentionPolicy(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['retentionPolicies'] });
      setOpen(false);
      setForm({ auto_delete: false });
    },
  });

  const columns: GridColDef<RetentionPolicy>[] = [
    { field: 'data_type', headerName: 'Data Type', width: 200 },
    { field: 'retention_years', headerName: 'Retention (Years)', width: 160 },
    {
      field: 'auto_delete',
      headerName: 'Auto Delete',
      width: 130,
      renderCell: (p) => (
        <Chip label={p.value ? 'Yes' : 'No'} size="small" color={p.value ? 'error' : 'default'} />
      ),
    },
    {
      field: 'last_reviewed',
      headerName: 'Last Reviewed',
      width: 160,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Data Retention
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
            New Policy
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
        <DialogTitle>New Retention Policy</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Data Type"
            value={form.data_type ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, data_type: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Retention Years"
            type="number"
            value={form.retention_years ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, retention_years: +e.target.value }))}
            fullWidth
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={form.auto_delete ?? false}
                onChange={(e) => setForm((f) => ({ ...f, auto_delete: e.target.checked }))}
              />
            }
            label="Auto Delete"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateRetentionPolicyPayload)}
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
