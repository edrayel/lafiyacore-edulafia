import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
} from '@mui/material';
import { DataGrid, type GridColDef, type GridRowModel } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAcademicMetadata } from '../academics/api';
import { getStudents } from '../students/api';
import { batchCreateScreenings, type Screening } from './api';
import type { Student } from '@/shared/types';

interface BatchScreeningsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function BatchScreeningsDialog({ open, onClose }: BatchScreeningsDialogProps) {
  const queryClient = useQueryClient();
  const [screeningType, setScreeningType] = useState('annual');
  const [rows, setRows] = useState<any[]>([]);

  const { data: metadata, isLoading: metaLoading } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
    enabled: open,
  });

  const classId = metadata?.class?.id;

  const { data: studentsData, isLoading: studentsLoading } = useQuery({
    queryKey: ['students', classId],
    queryFn: () => getStudents({ per_page: 100, class_id: classId }),
    enabled: open,
  });

  useEffect(() => {
    if (studentsData?.items) {
      const formattedRows = studentsData.items.map((student: Student) => ({
        id: student.id,
        name: `${student.first_name} ${student.last_name}`,
        height: null,
        weight: null,
        phq_a_score: null,
        sdq_score: null,
      }));
      setRows(formattedRows);
    } else {
      setRows([]);
    }
  }, [studentsData]);

  const saveMutation = useMutation({
    mutationFn: (payload: Partial<Screening>[]) => batchCreateScreenings(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['screenings'] });
      onClose();
    },
  });

  const processRowUpdate = (newRow: GridRowModel, _oldRow: GridRowModel) => {
    const updatedRows = rows.map((r) => (r.id === newRow.id ? newRow : r));
    setRows(updatedRows);
    return newRow;
  };

  const handleSave = () => {
    if (!classId) return;

    const payload = rows
      .filter(
        (r) =>
          r.height !== null || r.weight !== null || r.phq_a_score !== null || r.sdq_score !== null
      )
      .map((r) => ({
        student_id: r.id,
        screening_type: screeningType,
        screening_date: new Date().toISOString().split('T')[0],
        height: r.height ? Number(r.height) : undefined,
        weight: r.weight ? Number(r.weight) : undefined,
        phq_a_score: r.phq_a_score ? Number(r.phq_a_score) : undefined,
        sdq_score: r.sdq_score ? Number(r.sdq_score) : undefined,
      }));

    if (payload.length > 0) {
      saveMutation.mutate(payload);
    } else {
      onClose();
    }
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Student Name', width: 250, editable: false },
    { field: 'height', headerName: 'Height (cm)', width: 120, editable: true, type: 'number' },
    { field: 'weight', headerName: 'Weight (kg)', width: 120, editable: true, type: 'number' },
    {
      field: 'phq_a_score',
      headerName: 'PHQ-A (Mental Health)',
      width: 180,
      editable: true,
      type: 'number',
    },
    {
      field: 'sdq_score',
      headerName: 'SDQ (Wellbeing)',
      width: 180,
      editable: true,
      type: 'number',
    },
  ];

  const isLoading = metaLoading || studentsLoading;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>Batch Health Screening</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Screening Type</InputLabel>
            <Select
              value={screeningType}
              label="Screening Type"
              onChange={(e) => setScreeningType(e.target.value)}
            >
              <MenuItem value="annual">Annual General</MenuItem>
              <MenuItem value="mental_health">Mental Health & Wellbeing</MenuItem>
              <MenuItem value="pre_sports">Pre-Sports</MenuItem>
              <MenuItem value="special">Special</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Class</InputLabel>
            <Select value={classId || ''} label="Class" disabled>
              <MenuItem value={classId || ''}>{metadata?.class?.name || 'Loading...'}</MenuItem>
            </Select>
          </FormControl>
        </Box>

        {isLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{ height: 400, width: '100%' }}>
            <DataGrid
              rows={rows}
              columns={columns}
              processRowUpdate={processRowUpdate}
              disableRowSelectionOnClick
            />
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSave} disabled={saveMutation.isPending}>
          {saveMutation.isPending ? 'Saving...' : 'Save Screenings'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
