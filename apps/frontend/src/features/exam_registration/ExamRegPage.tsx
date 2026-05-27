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
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getExamRegistrations,
  createExamRegistration,
  type ExamRegistration,
  type CreateExamRegPayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  registered: 'success',
  pending: 'warning',
  cancelled: 'error',
};

export function ExamRegPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateExamRegPayload>>({
    exam_type: 'waec',
    exam_year: 2026,
    subjects: [],
  });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['examRegistrations'],
    queryFn: () => getExamRegistrations(),
  });

  const create = useMutation({
    mutationFn: (p: CreateExamRegPayload) => createExamRegistration(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['examRegistrations'] });
      setOpen(false);
      setForm({ exam_type: 'waec', exam_year: 2026, subjects: [] });
    },
  });

  const columns: GridColDef<ExamRegistration>[] = [
    { field: 'student_name', headerName: 'Student', width: 200 },
    { field: 'exam_type', headerName: 'Exam Type', width: 120 },
    { field: 'exam_year', headerName: 'Year', width: 80 },
    { field: 'registration_number', headerName: 'Reg. Number', width: 160 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
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
          Exam Registration
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
            Register Student
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
        <DialogTitle>Register for Exam</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={form.student_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Exam Type</InputLabel>
            <Select
              value={form.exam_type ?? 'waec'}
              label="Exam Type"
              onChange={(e) => setForm((f) => ({ ...f, exam_type: e.target.value }))}
            >
              <MenuItem value="waec">WAEC</MenuItem>
              <MenuItem value="neco">NECO</MenuItem>
              <MenuItem value=" jamb">JAMB</MenuItem>
              <MenuItem value="common_entrance">Common Entrance</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Year</InputLabel>
            <Select
              value={form.exam_year ?? 2026}
              label="Year"
              onChange={(e) => setForm((f) => ({ ...f, exam_year: +e.target.value }))}
            >
              <MenuItem value={2025}>2025</MenuItem>
              <MenuItem value={2026}>2026</MenuItem>
              <MenuItem value={2027}>2027</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Subjects (comma-separated)"
            value={form.subjects?.join(', ') ?? ''}
            onChange={(e) =>
              setForm((f) => ({
                ...f,
                subjects: e.target.value
                  .split(',')
                  .map((s) => s.trim())
                  .filter(Boolean),
              }))
            }
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateExamRegPayload)}
            variant="contained"
            disabled={create.isPending}
          >
            Register
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
