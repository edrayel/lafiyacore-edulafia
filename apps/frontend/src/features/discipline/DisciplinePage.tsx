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
  getDisciplineRecords,
  createDisciplineRecord,
  type DisciplineRecord,
  type CreateDisciplinePayload,
} from './api';

const severityColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  minor: 'success',
  moderate: 'warning',
  severe: 'error',
};

export function DisciplinePage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateDisciplinePayload>>({ severity: 'minor' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['disciplineRecords'],
    queryFn: () => getDisciplineRecords(),
  });

  const create = useMutation({
    mutationFn: (p: CreateDisciplinePayload) => createDisciplineRecord(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['disciplineRecords'] });
      setOpen(false);
      setForm({ severity: 'minor' });
    },
  });

  const columns: GridColDef<DisciplineRecord>[] = [
    { field: 'student_name', headerName: 'Student', width: 180 },
    { field: 'offense', headerName: 'Offense', width: 220 },
    { field: 'action_taken', headerName: 'Action', width: 160 },
    {
      field: 'severity',
      headerName: 'Severity',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={severityColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'incident_date',
      headerName: 'Date',
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
          Discipline
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
            New Record
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
          slots={{ noRowsOverlay: () => <DataEmptyState title="No discipline records found" message="There are no discipline records to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Discipline Record</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={form.student_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Offense"
            value={form.offense ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, offense: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Action Taken"
            value={form.action_taken ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, action_taken: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Severity</InputLabel>
            <Select
              value={form.severity ?? 'minor'}
              label="Severity"
              onChange={(e) => setForm((f) => ({ ...f, severity: e.target.value }))}
            >
              <MenuItem value="minor">Minor</MenuItem>
              <MenuItem value="moderate">Moderate</MenuItem>
              <MenuItem value="severe">Severe</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Incident Date"
            type="date"
            value={form.incident_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, incident_date: e.target.value }))}
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
            onClick={() => create.mutate(form as CreateDisciplinePayload)}
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
