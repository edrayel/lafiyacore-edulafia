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
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getInventory,
  createInventoryItem,
  type InventoryItem,
  type CreateInventoryPayload,
} from './api';

const conditionColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  good: 'success',
  fair: 'warning',
  poor: 'error',
  new: 'success',
};

export function InventoryPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateInventoryPayload>>({ condition: 'good' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['inventory'], queryFn: () => getInventory() });

  const create = useMutation({
    mutationFn: (p: CreateInventoryPayload) => createInventoryItem(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      setOpen(false);
      setForm({ condition: 'good' });
    },
  });

  const columns: GridColDef<InventoryItem>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'category', headerName: 'Category', width: 140 },
    { field: 'quantity', headerName: 'Quantity', width: 100 },
    { field: 'location', headerName: 'Location', width: 160 },
    {
      field: 'condition',
      headerName: 'Condition',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={conditionColor[p.value] ?? 'default'} />
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
          Inventory
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
            Add Item
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
          slots={{ noRowsOverlay: () => <DataEmptyState title="No inventory items found" message="There are no inventory items to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Inventory Item</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Name"
            value={form.name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Category</InputLabel>
            <Select
              value={form.category ?? ''}
              label="Category"
              onChange={(e) => setForm((f) => ({ ...f, category: e.target.value }))}
            >
              <MenuItem value="furniture">Furniture</MenuItem>
              <MenuItem value="electronics">Electronics</MenuItem>
              <MenuItem value="books">Books</MenuItem>
              <MenuItem value="sports">Sports</MenuItem>
              <MenuItem value="lab">Lab Equipment</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Quantity"
            type="number"
            value={form.quantity ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, quantity: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Location"
            value={form.location ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, location: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Condition</InputLabel>
            <Select
              value={form.condition ?? 'good'}
              label="Condition"
              onChange={(e) => setForm((f) => ({ ...f, condition: e.target.value }))}
            >
              <MenuItem value="new">New</MenuItem>
              <MenuItem value="good">Good</MenuItem>
              <MenuItem value="fair">Fair</MenuItem>
              <MenuItem value="poor">Poor</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateInventoryPayload)}
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
