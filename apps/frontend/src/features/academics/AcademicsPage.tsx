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
  Tab,
  Tabs,
  TextField,
  Toolbar,
  Typography,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon, Calculate as ComputeIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getSubjects,
  getClasses,
  createSubject,
  updateSubject,
  archiveSubject,
  getGradingScales,
  getAcademicMetadata,
  computeGrades,
  type Subject,
  type GradingScale,
  type CreateSubjectPayload,
  type AcademicClass,
} from './api';

import { GradeEntryGrid } from './GradeEntryGrid';
import { ReportCardPreview } from './ReportCardPreview';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { useTabState } from '@/shared/hooks/useTabState';
import { DataErrorAlert } from '@/shared/components/DataErrorAlert';
import { useToastStore } from '@/shared/stores/toastStore';

export function AcademicsPage() {
  const [tab, setTab] = useTabState('tab');
  const queryClient = useQueryClient();
  const [subjectDialogOpen, setSubjectDialogOpen] = useState(false);
  const [subjectForm, setSubjectForm] = useState<Partial<CreateSubjectPayload> & { id?: string }>({
    is_core: true,
  });
  const [gradeEntryOpen, setGradeEntryOpen] = useState(false);
  const [reportCardOpen, setReportCardOpen] = useState(false);

  const { 
    data: subjects, 
    isLoading: subjectsLoading,
    isError: isSubjectsError,
    error: subjectsError,
    refetch: refetchSubjects
  } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => getSubjects(),
  });
  const { 
    data: scales,
    isError: isScalesError,
    error: scalesError,
    refetch: refetchScales
  } = useQuery({ queryKey: ['gradingScales'], queryFn: getGradingScales });

  const { data: classes } = useQuery({
    queryKey: ['classes'],
    queryFn: getClasses,
  });

  const updateSubj = useMutation({
    mutationFn: (data: Partial<CreateSubjectPayload> & { id: string }) =>
      updateSubject(data.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subjects'] });
      setSubjectDialogOpen(false);
      setSubjectForm({ is_core: true });
    },
  });

  const createSubj = useMutation({
    mutationFn: createSubject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subjects'] });
      setSubjectDialogOpen(false);
      setSubjectForm({ is_core: true });
    },
  });
  const archiveSubj = useMutation({
    mutationFn: archiveSubject,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['subjects'] }),
  });

  const { data: metadata } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
  });

  const computeMutation = useMutation({
    mutationFn: async () => {
      if (!metadata?.class?.id || !metadata?.term?.id) {
        throw new Error('Missing class or term metadata');
      }
      await computeGrades(metadata.class.id, metadata.term.id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scores'] });
      useToastStore.getState().addToast('Grades and class ranks computed successfully!', 'success');
    },
    onError: () => {
      useToastStore.getState().addToast('Failed to compute grades.', 'error');
    },
  });

  const subjectColumns: GridColDef<Subject>[] = [
    { field: 'code', headerName: 'Code', width: 100 },
    { field: 'name', headerName: 'Subject Name', width: 200 },
    { field: 'class_id', headerName: 'Class', width: 100 },
    { field: 'waec_code', headerName: 'WAEC', width: 100 },
    { field: 'neco_code', headerName: 'NECO', width: 100 },
    {
      field: 'is_core',
      headerName: 'Core',
      width: 80,
      renderCell: (p) => (
        <Chip label={p.value ? 'Yes' : 'No'} size="small" color={p.value ? 'primary' : 'default'} />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Button
            size="small"
            onClick={() => {
              setSubjectForm(p.row);
              setSubjectDialogOpen(true);
            }}
          >
            Edit
          </Button>
          <Button size="small" color="error" onClick={() => archiveSubj.mutate(p.row.id)}>
            Archive
          </Button>
        </Box>
      ),
    },
  ];

  const scaleColumns: GridColDef<GradingScale>[] = [
    {
      field: 'grade',
      headerName: 'Grade',
      width: 80,
      renderCell: (p) => (
        <Chip
          label={p.value}
          size="small"
          color={
            p.value.startsWith('A') ? 'success' : p.value.startsWith('F') ? 'error' : 'default'
          }
        />
      ),
    },
    { field: 'min_score', headerName: 'Min', width: 80 },
    { field: 'max_score', headerName: 'Max', width: 80 },
    { field: 'remark', headerName: 'Remark', width: 200 },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Academics
        </Typography>
      </Box>

      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Subjects" />
          <Tab label="Grade Entry" />
          <Tab label="Results & Reports" />
          <Tab label="Grading Scale" />
        </Tabs>
      </Paper>

      {tab === 0 && (
        <>
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
                onClick={() => {
                  setSubjectForm({ is_core: true });
                  setSubjectDialogOpen(true);
                }}
              >
                Add Subject
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
            {isSubjectsError && (
              <DataErrorAlert 
                message={subjectsError instanceof Error ? subjectsError.message : 'Failed to load subjects.'} 
                onRetry={refetchSubjects} 
              />
            )}
            {!isSubjectsError && (
              <DataGrid
                rows={subjects ?? []}
                columns={subjectColumns}
                loading={subjectsLoading}
                getRowId={(r) => r.id}
                initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
                pageSizeOptions={[10, 25, 50]}
                slots={{ noRowsOverlay: () => <DataEmptyState title="No subjects found" message="There are no subjects to display at this time." /> }}
              />
            )}
          </Paper>
        </>
      )}

      {tab === 1 && (
        <Box
          sx={{
            p: 4,
            textAlign: 'center',
            bgcolor: 'background.paper',
            borderRadius: 2,
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Typography variant="h6" sx={{ mb: 2 }}>
            Enter Student Grades
          </Typography>
          <Typography color="textSecondary" sx={{ mb: 4 }}>
            Select a class and subject to enter continuous assessment and exam scores.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button variant="contained" onClick={() => setGradeEntryOpen(true)}>
              Open Grade Entry Grid
            </Button>
            <Button
              variant="outlined"
              color="secondary"
              startIcon={
                computeMutation.isPending ? <CircularProgress size={20} /> : <ComputeIcon />
              }
              onClick={() => computeMutation.mutate()}
              disabled={computeMutation.isPending || !metadata?.class?.id || !metadata?.term?.id}
            >
              Compute Grades & Ranks
            </Button>
          </Box>
        </Box>
      )}

      {tab === 2 && (
        <Box
          sx={{
            p: 4,
            textAlign: 'center',
            bgcolor: 'background.paper',
            borderRadius: 2,
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Typography variant="h6" sx={{ mb: 2 }}>
            Generate Termly Reports
          </Typography>
          <Typography color="textSecondary" sx={{ mb: 4 }}>
            Compile and print academic report cards for students.
          </Typography>
          <Button variant="contained" onClick={() => setReportCardOpen(true)}>
            Open Report Cards
          </Button>
        </Box>
      )}

      {tab === 3 && (
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
          {isScalesError && (
            <DataErrorAlert 
              message={scalesError instanceof Error ? scalesError.message : 'Failed to load grading scales.'} 
              onRetry={refetchScales} 
            />
          )}
          {!isScalesError && (
            <DataGrid
              rows={scales ?? []}
              columns={scaleColumns}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No grading scales found" message="There are no grading scales to display at this time." /> }}
            />
          )}
        </Paper>
      )}

      {/* Subject Dialog */}
      <Dialog
        open={subjectDialogOpen}
        onClose={() => setSubjectDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>{subjectForm?.id ? 'Edit' : 'Add'} Subject</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Subject Name"
            value={subjectForm.name ?? ''}
            onChange={(e) => setSubjectForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Subject Code"
            value={subjectForm.code ?? ''}
            onChange={(e) => setSubjectForm((f) => ({ ...f, code: e.target.value }))}
            fullWidth
          />
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              label="WAEC Code (Optional)"
              value={subjectForm.waec_code ?? ''}
              onChange={(e) => setSubjectForm((f) => ({ ...f, waec_code: e.target.value }))}
              fullWidth
            />
            <TextField
              label="NECO Code (Optional)"
              value={subjectForm.neco_code ?? ''}
              onChange={(e) => setSubjectForm((f) => ({ ...f, neco_code: e.target.value }))}
              fullWidth
            />
          </Box>
          <FormControl fullWidth>
            <InputLabel>Class</InputLabel>
            <Select
              value={subjectForm.class_id ?? ''}
              label="Class"
              onChange={(e) => setSubjectForm((f) => ({ ...f, class_id: e.target.value }))}
            >
              <MenuItem value="">All Classes</MenuItem>
              {classes?.map((c: AcademicClass) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Core Subject</InputLabel>
            <Select
              value={subjectForm.is_core ? 'true' : 'false'}
              label="Core Subject"
              onChange={(e) =>
                setSubjectForm((f) => ({ ...f, is_core: e.target.value === 'true' }))
              }
            >
              <MenuItem value="true">Yes</MenuItem>
              <MenuItem value="false">No</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSubjectDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => {
              if (subjectForm.id) {
                updateSubj.mutate(subjectForm as Partial<CreateSubjectPayload> & { id: string });
              } else {
                createSubj.mutate(subjectForm as CreateSubjectPayload);
              }
            }}
            variant="contained"
            disabled={createSubj.isPending || updateSubj.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <GradeEntryGrid open={gradeEntryOpen} onClose={() => setGradeEntryOpen(false)} />
      <ReportCardPreview open={reportCardOpen} onClose={() => setReportCardOpen(false)} />
    </>
  );
}
