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
  Typography,
} from '@mui/material';
import { Save as SaveIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getAccreditationItems,
  updateAccreditationItem,
  type AccreditationItem,
  type UpdateAccreditationPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  compliant: 'success',
  partial: 'warning',
  non_compliant: 'error',
  pending: 'default',
};

export function AccreditationPage() {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<AccreditationItem | null>(null);
  const [form, setForm] = useState<Partial<UpdateAccreditationPayload>>({ status: 'compliant' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['accreditationItems'],
    queryFn: () => getAccreditationItems(),
  });

  const update = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: UpdateAccreditationPayload }) =>
      updateAccreditationItem(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accreditationItems'] });
      setOpen(false);
      setSelected(null);
      setForm({ status: 'compliant' });
    },
  });

  const columns: GridColDef<AccreditationItem>[] = [
    { field: 'category', headerName: 'Category', width: 160 },
    { field: 'requirement', headerName: 'Requirement', width: 300 },
    {
      field: 'status',
      headerName: 'Status',
      width: 140,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'last_reviewed',
      headerName: 'Last Reviewed',
      width: 140,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'actions',
      headerName: '',
      width: 100,
      sortable: false,
      renderCell: (p) => (
        <Button
          aria-label="Review"
          size="small"
          onClick={() => {
            setSelected(p.row);
            setForm({ status: p.row.status, notes: p.row.notes });
            setOpen(true);
          }}
        >
          <SaveIcon fontSize="small" />
        </Button>
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
          Accreditation
        </Typography>
      </Box>
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
        <DialogTitle>Update Accreditation Item</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary">
            {selected?.requirement}
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              value={form.status ?? 'compliant'}
              label="Status"
              onChange={(e) => setForm((f) => ({ ...f, status: e.target.value }))}
            >
              <MenuItem value="compliant">Compliant</MenuItem>
              <MenuItem value="partial">Partial</MenuItem>
              <MenuItem value="non_compliant">Non-Compliant</MenuItem>
              <MenuItem value="pending">Pending</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Evidence"
            value={form.evidence ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, evidence: e.target.value }))}
            fullWidth
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
            onClick={() =>
              selected &&
              update.mutate({ id: selected.id, payload: form as UpdateAccreditationPayload })
            }
            variant="contained"
            disabled={update.isPending}
          >
            Update
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
