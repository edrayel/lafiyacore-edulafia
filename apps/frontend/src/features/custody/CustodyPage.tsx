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
  getCustodyOrders,
  createCustodyOrder,
  type CustodyOrder,
  type CreateCustodyPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  expired: 'default',
  pending: 'warning',
  revoked: 'error',
};

export function CustodyPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateCustodyPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['custodyOrders'],
    queryFn: () => getCustodyOrders(),
  });

  const create = useMutation({
    mutationFn: (p: CreateCustodyPayload) => createCustodyOrder(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['custodyOrders'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<CustodyOrder>[] = [
    { field: 'student_name', headerName: 'Student', width: 180 },
    { field: 'custodial_parent', headerName: 'Custodial Parent', width: 200 },
    { field: 'court', headerName: 'Court', width: 180 },
    {
      field: 'order_date',
      headerName: 'Order Date',
      width: 130,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
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
          Custody Orders
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
            New Order
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
        <DialogTitle>New Custody Order</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={form.student_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Custodial Parent"
            value={form.custodial_parent ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, custodial_parent: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Non-Custodial Parent"
            value={form.non_custodial_parent ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, non_custodial_parent: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Court"
            value={form.court ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, court: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Order Date"
            type="date"
            value={form.order_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, order_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Notes"
            value={form.notes ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateCustodyPayload)}
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
