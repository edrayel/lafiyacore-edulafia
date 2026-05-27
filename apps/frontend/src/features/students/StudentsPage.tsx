import { useState, useCallback, useRef } from 'react';
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
  Tooltip,
  Typography,
} from '@mui/material';
import {
  Add as AddIcon,
  CloudUpload as UploadIcon,
  Edit as EditIcon,
  DeleteOutline as ArchiveIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getStudents, archiveStudent, batchImportStudents } from './api';
import type { Student } from '@/shared/types';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { DataErrorAlert } from '@/shared/components/DataErrorAlert';
import { DEFAULT_CLASS_OPTIONS } from '@/shared/config/constants';
import { CreateStudentDialog } from './components/CreateStudentDialog';
import { EditStudentDialog } from './components/EditStudentDialog';

const statusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  archived: 'default',
  graduated: 'success',
  withdrawn: 'error',
  suspended: 'warning',
};

export function StudentsPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const [classFilter, setClassFilter] = useState('');
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 25 });
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [editOpen, setEditOpen] = useState(false);
  const [createOpen, setCreateOpen] = useState(false);
  const [archiveConfirmOpen, setArchiveConfirmOpen] = useState(false);
  const [importOpen, setImportOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: [
      'students',
      {
        search,
        classId: classFilter,
        page: paginationModel.page,
        pageSize: paginationModel.pageSize,
      },
    ],
    queryFn: () =>
      getStudents({
        search: search || undefined,
        class_id: classFilter || undefined,
        page: paginationModel.page + 1,
        per_page: paginationModel.pageSize,
      }),
  });

  const archiveMutation = useMutation({
    mutationFn: (id: string) => archiveStudent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      setArchiveConfirmOpen(false);
    },
  });

  const importMutation = useMutation({
    mutationFn: (formData: FormData) => batchImportStudents(formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      setImportOpen(false);
    },
  });

  const handleImportSubmit = () => {
    if (!fileInputRef.current?.files?.[0]) return;
    const formData = new FormData();
    formData.append('file', fileInputRef.current.files[0]);
    importMutation.mutate(formData);
  };

  const handleEdit = useCallback((student: Student) => {
    setSelectedStudent(student);
    setEditOpen(true);
  }, []);

  const handleArchive = useCallback((student: Student) => {
    setSelectedStudent(student);
    setArchiveConfirmOpen(true);
  }, []);

  const handleConfirmArchive = useCallback(() => {
    if (selectedStudent) {
      archiveMutation.mutate(selectedStudent.id);
    }
  }, [selectedStudent, archiveMutation]);

  const columns: GridColDef<Student>[] = [
    { field: 'admission_number', headerName: 'Admission #', width: 140 },
    {
      field: 'name',
      headerName: 'Name',
      width: 220,
      valueGetter: (_, row: Student) => `${row.first_name} ${row.last_name}`,
    },
    { field: 'gender', headerName: 'Gender', width: 90 },
    {
      field: 'date_of_birth',
      headerName: 'Date of Birth',
      width: 130,
      valueGetter: (value: string) => new Date(value).toLocaleDateString(),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip label={params.value} color={statusColors[params.value] || 'default'} size="small" />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Tooltip title="Edit">
            <Button aria-label="Edit" size="small" onClick={() => handleEdit(params.row)}>
              <EditIcon fontSize="small" />
            </Button>
          </Tooltip>
          <Tooltip title="Archive">
            <Button
              aria-label="Archive"
              size="small"
              color="error"
              onClick={() => handleArchive(params.row)}
            >
              <ArchiveIcon fontSize="small" />
            </Button>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Students Directory
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
        <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
          <TextField
            size="small"
            placeholder="Search students..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{ startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} /> }}
            sx={{ minWidth: 250 }}
          />
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Class</InputLabel>
            <Select
              value={classFilter}
              label="Class"
              onChange={(e) => setClassFilter(e.target.value)}
            >
              <MenuItem value="">All Classes</MenuItem>
              {DEFAULT_CLASS_OPTIONS.map((cls) => (
                <MenuItem key={cls.value} value={cls.value}>{cls.label}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <Box sx={{ flexGrow: 1 }} />
          <Button
            variant="outlined"
            startIcon={<UploadIcon />}
            sx={{ borderRadius: 2, px: 3, py: 1, fontWeight: 600 }}
            onClick={() => setImportOpen(true)}
          >
            Batch Import
          </Button>
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
            onClick={() => setCreateOpen(true)}
          >
            Add Student
          </Button>
        </Toolbar>
      </Paper>

      <Paper
        elevation={0}
        sx={{
          height: 600,
          width: '100%',
          border: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
          overflow: 'hidden',
        }}
      >
        {isError && (
          <DataErrorAlert 
            message={error instanceof Error ? error.message : 'Failed to load students directory.'} 
            onRetry={refetch} 
          />
        )}
        {!isError && (
          <DataGrid
            rows={data?.items ?? []}
            columns={columns}
            loading={isLoading}
            rowCount={data?.total ?? 0}
            pageSizeOptions={[10, 25, 50]}
            paginationMode="server"
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            getRowId={(row) => row.id}
            initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No students found" message="There are no students to display at this time." /> }}
          />
        )}
      </Paper>

      <CreateStudentDialog open={createOpen} onClose={() => setCreateOpen(false)} />

      <EditStudentDialog
        open={editOpen}
        onClose={() => setEditOpen(false)}
        student={selectedStudent}
      />

      <Dialog open={archiveConfirmOpen} onClose={() => setArchiveConfirmOpen(false)}>
        <DialogTitle>Archive Student</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to archive {selectedStudent?.first_name}{' '}
            {selectedStudent?.last_name}?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setArchiveConfirmOpen(false)}>Cancel</Button>
          <Button
            onClick={handleConfirmArchive}
            color="error"
            variant="contained"
            disabled={archiveMutation.isPending}
          >
            Archive
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={importOpen} onClose={() => setImportOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Batch Import Students</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Upload a CSV file containing student records. The file must include at least:
            first_name, last_name, date_of_birth.
          </Typography>
          <Button
            variant="outlined"
            component="label"
            fullWidth
            sx={{ py: 3, borderStyle: 'dashed' }}
          >
            Select CSV File
            <input type="file" accept=".csv" hidden ref={fileInputRef} />
          </Button>
          {importMutation.isError && (
            <Typography color="error" variant="caption">
              Error importing students. Please check your CSV format.
            </Typography>
          )}
          {importMutation.isSuccess && (
            <Typography color="success.main" variant="caption">
              Students imported successfully!
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setImportOpen(false)}>Cancel</Button>
          <Button
            onClick={handleImportSubmit}
            variant="contained"
            disabled={importMutation.isPending}
          >
            {importMutation.isPending ? 'Importing...' : 'Import'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
