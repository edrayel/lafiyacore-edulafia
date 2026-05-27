import { useState, useCallback, useEffect } from 'react';
import {
  Box,
  Button,
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
  Alert,
} from '@mui/material';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import {
  Add as AddIcon,
  Edit as EditIcon,
  DeleteOutline as DeleteIcon,
  UploadFile as UploadFileIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAcademicMetadata } from '../academics/api';
import {
  getAssignments,
  createAssignment,
  updateAssignment,
  deleteAssignment,
  uploadAssignmentFile,
  type Assignment,
  type CreateAssignmentPayload,
} from './api';

export function AssignmentsPage() {
  const queryClient = useQueryClient();
  const { data: metadata } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
  });

  const activeClassId = metadata?.class?.id || '';
  const activeSubjectId = metadata?.subject?.id || '';

  const [classFilter, setClassFilter] = useState(activeClassId);
  const [subjectFilter, setSubjectFilter] = useState(activeSubjectId);

  useEffect(() => {
    if (activeClassId && !classFilter) setClassFilter(activeClassId);
    if (activeSubjectId && !subjectFilter) setSubjectFilter(activeSubjectId);
  }, [activeClassId, activeSubjectId, classFilter, subjectFilter]);
  const [selectedAssignment, setSelectedAssignment] = useState<Assignment | null>(null);

  const [createOpen, setCreateOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);

  const [formError, setFormError] = useState<string | null>(null);

  const [createForm, setCreateForm] = useState<Partial<CreateAssignmentPayload>>({
    due_date: new Date().toISOString().split('T')[0],
  });
  const [editForm, setEditForm] = useState<Partial<CreateAssignmentPayload>>({});

  const [uploading, setUploading] = useState(false);

  const { data: assignments, isLoading } = useQuery({
    queryKey: ['assignments', classFilter, subjectFilter],
    queryFn: () =>
      getAssignments({
        class_id: classFilter || undefined,
        course_id: subjectFilter || undefined,
      }),
    enabled: !!classFilter && !!subjectFilter,
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateAssignmentPayload) => createAssignment(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments'] });
      setCreateOpen(false);
      setCreateForm({
        due_date: new Date().toISOString().split('T')[0],
      });
      setFormError(null);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<CreateAssignmentPayload> }) =>
      updateAssignment(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments'] });
      setEditOpen(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteAssignment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments'] });
      setDeleteConfirmOpen(false);
    },
  });

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>, isEdit: boolean) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      const { file_path } = await uploadAssignmentFile(file);
      if (isEdit) {
        setEditForm((f) => ({ ...f, file_path }));
      } else {
        setCreateForm((f) => ({ ...f, file_path }));
      }
    } catch (_err) {
      setFormError('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleCreate = useCallback(() => {
    setFormError(null);
    if (!createForm.title || createForm.title.trim().length === 0) {
      setFormError('Title is required');
      return;
    }
    if (!createForm.due_date) {
      setFormError('Due date is required');
      return;
    }

    // Convert date string to ISO format if needed by backend
    const payload = {
      ...createForm,
      course_id: activeSubjectId,
      max_score: createForm.max_score ? Number(createForm.max_score) : undefined,
      due_date: new Date(createForm.due_date as string).toISOString(),
    } as CreateAssignmentPayload;

    createMutation.mutate(payload);
  }, [activeSubjectId, createForm, createMutation]);

  const handleEdit = useCallback((assignment: Assignment) => {
    setSelectedAssignment(assignment);
    setEditForm({
      title: assignment.title,
      description: assignment.description,
      due_date: assignment.due_date ? assignment.due_date.split('T')[0] : '', // strip time for date input
      course_id: assignment.course_id,
      max_score: assignment.max_score,
      file_path: assignment.file_path,
    });
    setEditOpen(true);
  }, []);

  const handleSaveEdit = useCallback(() => {
    if (selectedAssignment) {
      const payload = {
        ...editForm,
        course_id: activeSubjectId,
        max_score: editForm.max_score ? Number(editForm.max_score) : undefined,
        due_date: editForm.due_date
          ? new Date(editForm.due_date as string).toISOString()
          : undefined,
      };
      updateMutation.mutate({ id: selectedAssignment.id, payload });
    }
  }, [activeSubjectId, selectedAssignment, editForm, updateMutation]);

  const handleDelete = useCallback((assignment: Assignment) => {
    setSelectedAssignment(assignment);
    setDeleteConfirmOpen(true);
  }, []);

  const handleConfirmDelete = useCallback(() => {
    if (selectedAssignment) {
      deleteMutation.mutate(selectedAssignment.id);
    }
  }, [selectedAssignment, deleteMutation]);

  const columns: GridColDef<Assignment>[] = [
    { field: 'title', headerName: 'Title', width: 250 },
    {
      field: 'due_date',
      headerName: 'Due Date',
      width: 150,
      valueGetter: (value: string) => new Date(value).toLocaleDateString(),
    },
    {
      field: 'file_path',
      headerName: 'File',
      width: 150,
      renderCell: (params) =>
        params.value ? (
          <Tooltip title="Has attachment">
            <UploadFileIcon color="primary" fontSize="small" />
          </Tooltip>
        ) : null,
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Tooltip title="Edit">
            <Button aria-label="Edit" size="small" onClick={() => handleEdit(params.row)}>
              <EditIcon fontSize="small" />
            </Button>
          </Tooltip>
          <Tooltip title="Delete">
            <Button
              aria-label="Delete"
              size="small"
              color="error"
              onClick={() => handleDelete(params.row)}
            >
              <DeleteIcon fontSize="small" />
            </Button>
          </Tooltip>
        </Box>
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
          Assignments
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
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Class</InputLabel>
            <Select
              value={classFilter}
              label="Class"
              onChange={(e) => setClassFilter(e.target.value as string)}
            >
              <MenuItem value="">All Classes</MenuItem>
              <MenuItem value={activeClassId}>Class 1</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Subject</InputLabel>
            <Select
              value={subjectFilter}
              label="Subject"
              onChange={(e) => setSubjectFilter(e.target.value as string)}
            >
              <MenuItem value="">All Subjects</MenuItem>
              <MenuItem value={activeSubjectId}>Subject 1</MenuItem>
            </Select>
          </FormControl>
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
            onClick={() => setCreateOpen(true)}
          >
            Add Assignment
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
        <DataGrid
          rows={assignments ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(row) => row.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ noRowsOverlay: () => <DataEmptyState title="No assignments found" message="There are no assignments to display at this time." /> }}
        />
      </Paper>

      {/* Create Dialog */}
      <Dialog open={createOpen} onClose={() => setCreateOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Assignment</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {formError && <Alert severity="error">{formError}</Alert>}
          <TextField
            label="Title"
            value={createForm.title ?? ''}
            onChange={(e) => setCreateForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Description"
            multiline
            rows={3}
            value={createForm.description ?? ''}
            onChange={(e) => setCreateForm((f) => ({ ...f, description: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Due Date"
            type="date"
            value={createForm.due_date ?? ''}
            onChange={(e) => setCreateForm((f) => ({ ...f, due_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button variant="outlined" component="label" disabled={uploading}>
              {uploading ? 'Uploading...' : 'Upload File'}
              <input type="file" hidden onChange={(e) => handleFileUpload(e, false)} />
            </Button>
            {createForm.file_path && (
              <Typography variant="body2" color="success.main">
                File attached
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreate}
            variant="contained"
            disabled={createMutation.isPending || uploading}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Assignment</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Title"
            value={editForm.title ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Description"
            multiline
            rows={3}
            value={editForm.description ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, description: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Due Date"
            type="date"
            value={editForm.due_date ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, due_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button variant="outlined" component="label" disabled={uploading}>
              {uploading ? 'Uploading...' : 'Upload New File'}
              <input type="file" hidden onChange={(e) => handleFileUpload(e, true)} />
            </Button>
            {editForm.file_path && (
              <Typography variant="body2" color="success.main">
                File attached
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSaveEdit}
            variant="contained"
            disabled={updateMutation.isPending || uploading}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Delete Assignment</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{selectedAssignment?.title}"? This action cannot be
            undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Cancel</Button>
          <Button
            onClick={handleConfirmDelete}
            color="error"
            variant="contained"
            disabled={deleteMutation.isPending}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
