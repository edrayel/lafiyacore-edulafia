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
  LinearProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getProjects, createProject, type BuildingProject, type CreateProjectPayload } from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  planning: 'default',
  in_progress: 'warning',
  completed: 'success',
  on_hold: 'error',
};

export function ProjectsPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateProjectPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['projects'], queryFn: () => getProjects() });

  const create = useMutation({
    mutationFn: (p: CreateProjectPayload) => createProject(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      setOpen(false);
      setForm({});
    },
  });

  const fmt = (n: number) => `₦${n.toLocaleString()}`;

  const columns: GridColDef<BuildingProject>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'project_type', headerName: 'Type', width: 140 },
    { field: 'budget', headerName: 'Budget', width: 140, valueGetter: (v: number) => fmt(v) },
    {
      field: 'progress',
      headerName: 'Progress',
      width: 180,
      renderCell: (p) => (
        <LinearProgress variant="determinate" value={p.value} sx={{ width: '100%' }} />
      ),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'estimated_completion',
      headerName: 'Completion',
      width: 140,
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
          Building Projects
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
            New Project
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
        <DialogTitle>New Project</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Name"
            value={form.name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Type</InputLabel>
            <Select
              value={form.project_type ?? ''}
              label="Type"
              onChange={(e) => setForm((f) => ({ ...f, project_type: e.target.value }))}
            >
              <MenuItem value="construction">Construction</MenuItem>
              <MenuItem value="renovation">Renovation</MenuItem>
              <MenuItem value="maintenance">Maintenance</MenuItem>
              <MenuItem value="expansion">Expansion</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Budget"
            type="number"
            value={form.budget ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, budget: +e.target.value }))}
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
            label="Est. Completion"
            type="date"
            value={form.estimated_completion ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, estimated_completion: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateProjectPayload)}
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
