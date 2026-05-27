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
import { getBusRoutes, createBusRoute, type BusRoute, type CreateBusRoutePayload } from './api';

export function BusPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateBusRoutePayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['busRoutes'], queryFn: () => getBusRoutes() });

  const create = useMutation({
    mutationFn: (p: CreateBusRoutePayload) => createBusRoute(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['busRoutes'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<BusRoute>[] = [
    { field: 'name', headerName: 'Route Name', width: 180 },
    { field: 'driver_name', headerName: 'Driver', width: 180 },
    { field: 'capacity', headerName: 'Capacity', width: 100 },
    { field: 'current_riders', headerName: 'Riders', width: 100 },
    { field: 'route_description', headerName: 'Route', width: 300 },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value ? 'Active' : 'Inactive'}
          size="small"
          color={p.value ? 'success' : 'default'}
        />
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
          Bus Tracking
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
            New Route
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
        <DialogTitle>New Bus Route</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Route Name"
            value={form.name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Driver Name"
            value={form.driver_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, driver_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Capacity"
            type="number"
            value={form.capacity ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, capacity: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Route Description"
            value={form.route_description ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, route_description: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateBusRoutePayload)}
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
