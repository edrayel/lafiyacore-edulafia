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
  LinearProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getCampaigns,
  createCampaign,
  type FundraisingCampaign,
  type CreateCampaignPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  completed: 'default',
  draft: 'warning',
  cancelled: 'error',
};

export function FundraisingPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateCampaignPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['campaigns'], queryFn: () => getCampaigns() });

  const create = useMutation({
    mutationFn: (p: CreateCampaignPayload) => createCampaign(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
      setOpen(false);
      setForm({});
    },
  });

  const fmt = (n: number) => `₦${n.toLocaleString()}`;

  const columns: GridColDef<FundraisingCampaign>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    {
      field: 'target_amount',
      headerName: 'Target',
      width: 140,
      valueGetter: (v: number) => fmt(v),
    },
    {
      field: 'raised_amount',
      headerName: 'Raised',
      width: 140,
      valueGetter: (v: number) => fmt(v),
    },
    {
      field: 'progress',
      headerName: 'Progress',
      width: 180,
      renderCell: (p) => (
        <LinearProgress
          variant="determinate"
          value={Math.min((p.row.raised_amount / p.row.target_amount) * 100, 100)}
          sx={{ width: '100%' }}
        />
      ),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'end_date',
      headerName: 'End Date',
      width: 130,
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
          Fundraising
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
            New Campaign
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
        <DialogTitle>New Campaign</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Name"
            value={form.name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Description"
            value={form.description ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Target Amount"
            type="number"
            value={form.target_amount ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, target_amount: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Start Date"
            type="date"
            value={form.start_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, start_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End Date"
            type="date"
            value={form.end_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, end_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateCampaignPayload)}
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
