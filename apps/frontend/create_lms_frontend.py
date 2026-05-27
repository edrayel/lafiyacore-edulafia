import os

base_dir = "/Users/edrayel/GitHub/edward_rajah/lafiyacore-edulafia/apps/frontend/src/features/lms"
os.makedirs(base_dir, exist_ok=True)

api_code = """import { apiClient } from '../../shared/api/client';

export interface Assignment {
  id: string;
  title: string;
  description?: string;
  due_date: string;
  class_id: string;
  subject_id: string;
  file_path?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateAssignmentPayload {
  title: string;
  description?: string;
  due_date: string;
  class_id: string;
  subject_id: string;
  file_path?: string;
}

export interface UpdateAssignmentPayload extends Partial<CreateAssignmentPayload> {}

export async function getAssignments(params?: { class_id?: string; subject_id?: string }): Promise<Assignment[]> {
  const { data } = await apiClient.get('/lms/assignments', { params });
  return data;
}

export async function getAssignment(id: string): Promise<Assignment> {
  const { data } = await apiClient.get(`/lms/assignments/${id}`);
  return data;
}

export async function createAssignment(payload: CreateAssignmentPayload): Promise<Assignment> {
  const { data } = await apiClient.post('/lms/assignments', payload);
  return data;
}

export async function updateAssignment(id: string, payload: UpdateAssignmentPayload): Promise<Assignment> {
  const { data } = await apiClient.patch(`/lms/assignments/${id}`, payload);
  return data;
}

export async function deleteAssignment(id: string): Promise<void> {
  await apiClient.delete(`/lms/assignments/${id}`);
}

export async function uploadAssignmentFile(file: File): Promise<{ file_path: string; filename: string }> {
  const formData = new FormData();
  formData.append('file', file);
  
  const { data } = await apiClient.post('/lms/uploads/assignments', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return data;
}
"""

page_code = """import { useState, useCallback, useRef } from 'react';
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
import {
  Add as AddIcon,
  Edit as EditIcon,
  DeleteOutline as DeleteIcon,
  UploadFile as UploadFileIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getAssignments,
  createAssignment,
  updateAssignment,
  deleteAssignment,
  uploadAssignmentFile,
  type Assignment,
  type CreateAssignmentPayload,
} from './api';

// Generate some dummy UUIDs for default selections
const DEFAULT_CLASS_ID = "00000000-0000-0000-0000-000000000001";
const DEFAULT_SUBJECT_ID = "00000000-0000-0000-0000-000000000002";

export function AssignmentsPage() {
  const queryClient = useQueryClient();
  const [classFilter, setClassFilter] = useState('');
  const [subjectFilter, setSubjectFilter] = useState('');
  const [selectedAssignment, setSelectedAssignment] = useState<Assignment | null>(null);
  
  const [createOpen, setCreateOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  
  const [formError, setFormError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [createForm, setCreateForm] = useState<Partial<CreateAssignmentPayload>>({
    class_id: DEFAULT_CLASS_ID,
    subject_id: DEFAULT_SUBJECT_ID,
    due_date: new Date().toISOString().split('T')[0],
  });
  const [editForm, setEditForm] = useState<Partial<CreateAssignmentPayload>>({});
  
  const [uploading, setUploading] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['assignments', { class_id: classFilter, subject_id: subjectFilter }],
    queryFn: () => getAssignments({ 
      class_id: classFilter || undefined, 
      subject_id: subjectFilter || undefined 
    }),
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateAssignmentPayload) => createAssignment(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assignments'] });
      setCreateOpen(false);
      setCreateForm({
        class_id: DEFAULT_CLASS_ID,
        subject_id: DEFAULT_SUBJECT_ID,
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
    } catch (err) {
      setFormError("Failed to upload file");
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
      due_date: new Date(createForm.due_date as string).toISOString()
    } as CreateAssignmentPayload;
    
    createMutation.mutate(payload);
  }, [createForm, createMutation]);

  const handleEdit = useCallback((assignment: Assignment) => {
    setSelectedAssignment(assignment);
    setEditForm({
      title: assignment.title,
      description: assignment.description,
      due_date: assignment.due_date.split('T')[0], // strip time for date input
      class_id: assignment.class_id,
      subject_id: assignment.subject_id,
      file_path: assignment.file_path,
    });
    setEditOpen(true);
  }, []);

  const handleSaveEdit = useCallback(() => {
    if (selectedAssignment) {
      const payload = {
        ...editForm,
        due_date: editForm.due_date ? new Date(editForm.due_date as string).toISOString() : undefined
      };
      updateMutation.mutate({ id: selectedAssignment.id, payload });
    }
  }, [selectedAssignment, editForm, updateMutation]);

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
      renderCell: (params) => (
        params.value ? (
          <Tooltip title="Has attachment">
            <UploadFileIcon color="primary" fontSize="small" />
          </Tooltip>
        ) : null
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Tooltip title="Edit">
            <Button size="small" onClick={() => handleEdit(params.row)}>
              <EditIcon fontSize="small" />
            </Button>
          </Tooltip>
          <Tooltip title="Delete">
            <Button size="small" color="error" onClick={() => handleDelete(params.row)}>
              <DeleteIcon fontSize="small" />
            </Button>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <>
      <Typography variant="h2" sx={{ mb: 3 }}>
        Assignments
      </Typography>

      <Paper sx={{ p: 2, mb: 2 }}>
        <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Class</InputLabel>
            <Select
              value={classFilter}
              label="Class"
              onChange={(e) => setClassFilter(e.target.value)}
            >
              <MenuItem value="">All Classes</MenuItem>
              <MenuItem value={DEFAULT_CLASS_ID}>Class 1</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Subject</InputLabel>
            <Select
              value={subjectFilter}
              label="Subject"
              onChange={(e) => setSubjectFilter(e.target.value)}
            >
              <MenuItem value="">All Subjects</MenuItem>
              <MenuItem value={DEFAULT_SUBJECT_ID}>Subject 1</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ flexGrow: 1 }} />
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => setCreateOpen(true)}>
            Add Assignment
          </Button>
        </Toolbar>
      </Paper>

      <Paper sx={{ height: 600 }}>
        <DataGrid
          rows={data ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(row) => row.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
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
              <Typography variant="body2" color="success.main">File attached</Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateOpen(false)}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained" disabled={createMutation.isPending || uploading}>
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
              <Typography variant="body2" color="success.main">File attached</Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained" disabled={updateMutation.isPending || uploading}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Delete Assignment</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{selectedAssignment?.title}"? This action cannot be undone.
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
"""

with open(f"{base_dir}/api.ts", "w") as f:
    f.write(api_code)

with open(f"{base_dir}/AssignmentsPage.tsx", "w") as f:
    f.write(page_code)

print("Frontend files created successfully.")
