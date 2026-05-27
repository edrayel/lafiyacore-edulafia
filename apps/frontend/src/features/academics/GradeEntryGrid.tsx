import { useState, useMemo, useCallback } from 'react';
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
  Chip,
  Typography,
  Alert,
} from '@mui/material';
import { DataGrid, type GridColDef, type GridRowModel } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAcademicMetadata, getSubjects, enterScoresBulk, getScores, type AcademicResult, type BulkScoreEntryPayload, type Subject } from './api';
import { getStudents } from '../students/api';
import type { Student } from '@/shared/types';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { useToastStore } from '@/shared/stores/toastStore';

interface GradeEntryGridProps {
  open: boolean;
  onClose: () => void;
}

function validateScore(value: number, max: number): string | null {
  if (value < 0) return 'Score cannot be negative';
  if (value > max) return `Score cannot exceed ${max}`;
  return null;
}

export function GradeEntryGrid({ open, onClose }: GradeEntryGridProps) {
  const queryClient = useQueryClient();
  const [subjectId, setSubjectId] = useState('');
  const [editedRows, setEditedRows] = useState<Record<string, any>>({});
  const [pendingSubjectChange, setPendingSubjectChange] = useState<string | null>(null);
  const [confirmClose, setConfirmClose] = useState(false);

  const hasEdits = Object.keys(editedRows).length > 0;

  const handleSubjectChange = useCallback((newSubjectId: string) => {
    if (hasEdits && newSubjectId !== subjectId) {
      setPendingSubjectChange(newSubjectId);
      return;
    }
    setSubjectId(newSubjectId);
    setEditedRows({});
  }, [hasEdits, subjectId]);

  const confirmSubjectChange = useCallback(() => {
    if (pendingSubjectChange) {
      setSubjectId(pendingSubjectChange);
      setEditedRows({});
      setPendingSubjectChange(null);
    }
  }, [pendingSubjectChange]);

  const cancelSubjectChange = useCallback(() => {
    setPendingSubjectChange(null);
  }, []);

  const handleClose = useCallback(() => {
    if (hasEdits) {
      setConfirmClose(true);
      return;
    }
    onClose();
  }, [hasEdits, onClose]);

  const handleConfirmClose = useCallback(() => {
    setConfirmClose(false);
    onClose();
  }, [onClose]);

  const { data: metadata, isLoading: metaLoading } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
    enabled: open,
  });

  const classId = metadata?.class?.id;
  const termId = metadata?.term?.id;
  const academicYearId = metadata?.academic_year?.id;

  const { data: subjects, isLoading: subjectsLoading } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => getSubjects(),
    enabled: open,
  });

  const { data: studentsData, isLoading: studentsLoading } = useQuery({
    queryKey: ['students', classId],
    queryFn: () => getStudents({ per_page: 100, class_id: classId }),
    enabled: open,
  });

  const { data: existingScores, isLoading: scoresLoading } = useQuery({
    queryKey: ['scores', classId, subjectId, termId],
    queryFn: () => getScores(classId!, subjectId, termId!),
    enabled: !!(classId && subjectId && termId),
  });

  const rows = useMemo(() => {
    if (!studentsData?.items || !subjectId) return [];

    return studentsData.items.map((student: Student) => {
      // Prefer local edits if they exist
      if (editedRows[student.id]) {
        return editedRows[student.id];
      }

      // Fallback to server data
      const score = existingScores?.find((s: AcademicResult) => s.student_id === student.id);
      return {
        id: student.id,
        name: `${student.first_name} ${student.last_name}`,
        assignment: score?.ca_total || 0,
        exam: score?.exam_score || 0,
      };
    });
  }, [studentsData, existingScores, subjectId, editedRows]);

  const saveMutation = useMutation({
    mutationFn: (payload: BulkScoreEntryPayload) => enterScoresBulk(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scores'] });
      useToastStore.getState().addToast('Grades saved successfully!', 'success');
      onClose();
    },
    onError: (err) => {
      useToastStore.getState().addToast(err instanceof Error ? err.message : 'Failed to save grades', 'error');
    },
  });

  const processRowUpdate = (newRow: GridRowModel, _oldRow: GridRowModel) => {
    setEditedRows((prev) => ({ ...prev, [newRow.id]: newRow }));
    return newRow;
  };

  const handleSave = () => {
    if (!classId || !termId || !academicYearId || !subjectId) return;

    const payload = {
      subject_id: subjectId,
      class_id: classId,
      term_id: termId,
      scores: rows.map((r) => ({
        student_id: r.id,
        subject_id: subjectId,
        class_id: classId,
        term_id: termId,
        academic_year_id: academicYearId,
        ca_scores: { assignment: Number(r.assignment) },
        exam_score: Number(r.exam),
      })),
    };
    saveMutation.mutate(payload);
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Student Name', width: 250, editable: false },
    {
      field: 'assignment',
      headerName: 'CA Score (Max 30)',
      width: 150,
      editable: true,
      type: 'number',
      preProcessEditCellProps: (params) => {
        const error = validateScore(params.props.value, 30);
        return { ...params.props, error: !!error };
      },
    },
    {
      field: 'exam',
      headerName: 'Exam Score (Max 70)',
      width: 150,
      editable: true,
      type: 'number',
      preProcessEditCellProps: (params) => {
        const error = validateScore(params.props.value, 70);
        return { ...params.props, error: !!error };
      },
    },
    {
      field: 'total',
      headerName: 'Total',
      width: 100,
      valueGetter: (_params, row) => Number(row.assignment || 0) + Number(row.exam || 0),
    },
  ];

  const isLoading = metaLoading || subjectsLoading || studentsLoading || scoresLoading;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Grade Entry Grid</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Subject</InputLabel>
              <Select
                  value={subjectId}
                  label="Subject"
                  onChange={(e) => handleSubjectChange(e.target.value)}
                >
              {subjects?.map((s: Subject) => (
                <MenuItem key={s.id} value={s.id}>
                  {s.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Class</InputLabel>
            <Select value={classId || ''} label="Class" disabled>
              <MenuItem value={classId || ''}>{metadata?.class?.name || 'Loading...'}</MenuItem>
            </Select>
          </FormControl>
        </Box>

        {isLoading ? (
          <SkeletonPage rows={5} cardCount={4} />
        ) : (
          <Box sx={{ height: 400, width: '100%' }}>
            {subjectId ? (
              <>
                {hasEdits && (
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
                    <Chip
                      label={`${Object.keys(editedRows).length} unsaved changes`}
                      color="warning"
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                )}
                <DataGrid
                  rows={rows}
                  columns={columns}
                  processRowUpdate={processRowUpdate}
                  disableRowSelectionOnClick
                  pageSizeOptions={[10, 25, 50]}
                  initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
                  slots={{ noRowsOverlay: () => <DataEmptyState title="No student grades found" message="There are no grades to display at this time." /> }}
                  getRowClassName={(params) =>
                    editedRows[params.id] ? 'MuiDataGrid-row--edited' : ''
                  }
                  sx={{
                    '& .MuiDataGrid-row--edited': {
                      bgcolor: (theme) =>
                        theme.palette.mode === 'dark'
                          ? 'rgba(255, 255, 0, 0.05)'
                          : 'rgba(255, 255, 0, 0.08)',
                    },
                  }}
                />
              </>
            ) : (
              <Box sx={{ p: 4, textAlign: 'center', color: 'text.secondary' }}>
                Please select a subject to enter grades.
              </Box>
            )}
          </Box>
        )}

        {pendingSubjectChange && (
          <Alert
            severity="warning"
            action={
              <>
                <Button size="small" onClick={confirmSubjectChange} color="inherit">
                  Discard
                </Button>
                <Button size="small" onClick={cancelSubjectChange} color="inherit">
                  Keep
                </Button>
              </>
            }
          >
            You have unsaved changes. Switching subjects will discard them.
          </Alert>
        )}
      </DialogContent>
      {confirmClose && (
        <Dialog open={confirmClose} onClose={() => setConfirmClose(false)}>
          <DialogTitle>Discard changes?</DialogTitle>
          <DialogContent>
            <Typography>You have unsaved grade changes. Are you sure you want to discard them?</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmClose(false)}>Keep Editing</Button>
            <Button onClick={handleConfirmClose} color="error">Discard</Button>
          </DialogActions>
        </Dialog>
      )}

      <DialogActions>
        <Button onClick={handleClose} color={hasEdits ? 'error' : 'inherit'}>
          {hasEdits ? 'Discard Changes' : 'Cancel'}
        </Button>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={!subjectId || saveMutation.isPending}
        >
          {saveMutation.isPending ? 'Saving...' : 'Save Grades'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
