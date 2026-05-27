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
import { Edit as EditIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getGirlChildRecords,
  updateGirlChildRecord,
  type GirlChildRecord,
  type UpdateGirlChildPayload,
} from './api';

const riskColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  low: 'success',
  medium: 'warning',
  high: 'error',
};

export function GirlChildPage() {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<GirlChildRecord | null>(null);
  const [form, setForm] = useState<Partial<UpdateGirlChildPayload>>({
    risk_level: 'low',
    interventions: [],
  });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['girlChildRecords'],
    queryFn: getGirlChildRecords,
  });

  const update = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: UpdateGirlChildPayload }) =>
      updateGirlChildRecord(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['girlChildRecords'] });
      setOpen(false);
      setSelected(null);
      setForm({ risk_level: 'low', interventions: [] });
    },
  });

  const columns: GridColDef<GirlChildRecord>[] = [
    { field: 'student_name', headerName: 'Student', width: 180 },
    {
      field: 'risk_level',
      headerName: 'Risk Level',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={riskColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'attendance_rate',
      headerName: 'Attendance %',
      width: 120,
      valueGetter: (v: number) => `${v}%`,
    },
    {
      field: 'academic_performance',
      headerName: 'Performance %',
      width: 140,
      valueGetter: (v: number) => `${v}%`,
    },
    {
      field: 'interventions',
      headerName: 'Interventions',
      width: 250,
      valueGetter: (v: string[]) => v?.join(', ') ?? '—',
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
      width: 80,
      sortable: false,
      renderCell: (p) => (
        <Button
          aria-label="Edit"
          size="small"
          onClick={() => {
            setSelected(p.row);
            setForm({
              risk_level: p.row.risk_level,
              interventions: p.row.interventions,
              notes: p.row.notes,
            });
            setOpen(true);
          }}
        >
          <EditIcon fontSize="small" />
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
          Girl-Child Tracking
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
        <DialogTitle>Update Girl-Child Record</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary">
            {selected?.student_name}
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Risk Level</InputLabel>
            <Select
              value={form.risk_level ?? 'low'}
              label="Risk Level"
              onChange={(e) => setForm((f) => ({ ...f, risk_level: e.target.value }))}
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Interventions (comma-separated)"
            value={form.interventions?.join(', ') ?? ''}
            onChange={(e) =>
              setForm((f) => ({
                ...f,
                interventions: e.target.value
                  .split(',')
                  .map((s) => s.trim())
                  .filter(Boolean),
              }))
            }
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
              update.mutate({ id: selected.id, payload: form as UpdateGirlChildPayload })
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
