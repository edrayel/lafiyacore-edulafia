import { useState, useCallback } from 'react';
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
  Edit as EditIcon,
  DeleteOutline as ArchiveIcon,
  Search as SearchIcon,
  UploadFile as UploadIcon,
  AssignmentInd as AssignIcon,
  AccessTime as AttendanceIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useDebounce } from '@/shared/hooks/useDebounce';
import {
  getStaff,
  updateStaff,
  archiveStaff,
  uploadStaffDocument,
  getStaffAssignments,
  createStaffAssignment,
  deleteStaffAssignment,
  getStaffAttendance,
} from './api';
import type { StaffMember, CreateStaffAssignmentPayload } from './api';
import { getAcademicMetadata, getClasses, getSubjects, type AcademicClass, type Subject } from '../academics/api';
import { DataEmptyState }
import { SkeletonPage } from "@/shared/components/SkeletonPage"; from '@/shared/components/DataEmptyState';
import { DataErrorAlert } from '@/shared/components/DataErrorAlert';

const roleColors: Record<string, 'primary' | 'secondary' | 'success' | 'warning' | 'info'> = {
  teacher: 'primary',
  'head-teacher': 'secondary',
  'vice-principal': 'warning',
  principal: 'success',
  'admin-staff': 'info',
};

const statusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  on_leave: 'warning',
  suspended: 'error',
  archived: 'default',
};

export function StaffPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  const [roleFilter, setRoleFilter] = useState('');
  const [selectedStaff, setSelectedStaff] = useState<StaffMember | null>(null);
  const [editOpen, setEditOpen] = useState(false);
  const [archiveConfirmOpen, setArchiveConfirmOpen] = useState(false);
  const [editForm, setEditForm] = useState<Partial<StaffMember>>({});

  const [uploadOpen, setUploadOpen] = useState(false);
  const [uploadDocType, setUploadDocType] = useState('cv');
  const [uploadFile, setUploadFile] = useState<File | null>(null);

  const [assignmentsOpen, setAssignmentsOpen] = useState(false);
  const [assignmentForm, setAssignmentForm] = useState<Partial<CreateStaffAssignmentPayload>>({});

  const [attendanceOpen, setAttendanceOpen] = useState(false);

  const { data: metadata } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
  });

  const { data: classes } = useQuery({
    queryKey: ['classes'],
    queryFn: getClasses,
  });

  const { data: subjects } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => getSubjects(),
  });

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['staff', debouncedSearch, roleFilter],
    queryFn: () =>
      getStaff({ search: debouncedSearch || undefined, role: roleFilter || undefined }),
  });

  const { data: assignments, isLoading: assignmentsLoading } = useQuery({
    queryKey: ['staffAssignments', selectedStaff?.id],
    queryFn: () => getStaffAssignments({ staff_id: selectedStaff?.id }),
    enabled: !!selectedStaff && assignmentsOpen,
  });

  const { data: attendanceData, isLoading: attendanceLoading } = useQuery({
    queryKey: ['staffAttendance', selectedStaff?.id],
    queryFn: () => getStaffAttendance({ staff_id: selectedStaff?.id }),
    enabled: !!selectedStaff && attendanceOpen,
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<StaffMember> }) =>
      updateStaff(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
      setEditOpen(false);
    },
  });

  const archiveMutation = useMutation({
    mutationFn: (id: string) => archiveStaff(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
      setArchiveConfirmOpen(false);
    },
  });

  const uploadMutation = useMutation({
    mutationFn: ({ id, formData }: { id: string; formData: FormData }) =>
      uploadStaffDocument(id, formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
      setUploadOpen(false);
      setUploadFile(null);
    },
  });

  const createAssignmentMutation = useMutation({
    mutationFn: (payload: CreateStaffAssignmentPayload) => createStaffAssignment(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staffAssignments'] });
      setAssignmentForm({});
    },
  });

  const deleteAssignmentMutation = useMutation({
    mutationFn: (id: string) => deleteStaffAssignment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staffAssignments'] });
    },
  });

  const handleEdit = useCallback((staff: StaffMember) => {
    setSelectedStaff(staff);
    setEditForm({
      first_name: staff.first_name,
      last_name: staff.last_name,
      email: staff.email,
      phone_number: staff.phone_number,
      role: staff.role,
      department: staff.department,
      status: staff.status,
    });
    setEditOpen(true);
  }, []);

  const handleArchive = useCallback((staff: StaffMember) => {
    setSelectedStaff(staff);
    setArchiveConfirmOpen(true);
  }, []);

  const handleSaveEdit = useCallback(() => {
    if (selectedStaff) {
      updateMutation.mutate({ id: selectedStaff.id, payload: editForm });
    }
  }, [selectedStaff, editForm, updateMutation]);

  const handleConfirmArchive = useCallback(() => {
    if (selectedStaff) {
      archiveMutation.mutate(selectedStaff.id);
    }
  }, [selectedStaff, archiveMutation]);

  const handleUploadSubmit = useCallback(() => {
    if (selectedStaff && uploadFile) {
      const formData = new FormData();
      formData.append('document_type', uploadDocType);
      formData.append('file', uploadFile);
      uploadMutation.mutate({ id: selectedStaff.id, formData });
    }
  }, [selectedStaff, uploadDocType, uploadFile, uploadMutation]);

  const handleAssignmentSubmit = useCallback(() => {
    if (selectedStaff && metadata?.academic_year?.id) {
      createAssignmentMutation.mutate({
        ...assignmentForm,
        staff_id: selectedStaff.id,
        academic_year_id: metadata.academic_year.id,
      } as CreateStaffAssignmentPayload);
    }
  }, [selectedStaff, metadata, assignmentForm, createAssignmentMutation]);

  const columns: GridColDef<StaffMember>[] = [
    { field: 'staff_id', headerName: 'Staff ID', width: 120 },
    {
      field: 'name',
      headerName: 'Name',
      width: 200,
      valueGetter: (_, row: StaffMember) => `${row.first_name} ${row.last_name}`,
    },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phone_number', headerName: 'Phone', width: 140 },
    {
      field: 'role',
      headerName: 'Role',
      width: 140,
      renderCell: (params) => (
        <Chip label={params.value} color={roleColors[params.value] || 'default'} size="small" />
      ),
    },
    { field: 'department', headerName: 'Department', width: 140 },
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
      width: 220,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Tooltip title="Upload Document">
            <Button
              aria-label="Upload"
              size="small"
              onClick={() => {
                setSelectedStaff(params.row);
                setUploadOpen(true);
              }}
            >
              <UploadIcon fontSize="small" />
            </Button>
          </Tooltip>
          <Tooltip title="Assign Class/Subject">
            <Button
              aria-label="Assign"
              size="small"
              onClick={() => {
                setSelectedStaff(params.row);
                setAssignmentsOpen(true);
              }}
            >
              <AssignIcon fontSize="small" />
            </Button>
          </Tooltip>
          <Tooltip title="View Attendance">
            <Button
              aria-label="Attendance"
              size="small"
              onClick={() => {
                setSelectedStaff(params.row);
                setAttendanceOpen(true);
              }}
            >
              <AttendanceIcon fontSize="small" />
            </Button>
          </Tooltip>
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
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Staff
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
            placeholder="Search staff..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />,
            }}
            sx={{ minWidth: 250 }}
          />
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Role</InputLabel>
            <Select value={roleFilter} label="Role" onChange={(e) => setRoleFilter(e.target.value)}>
              <MenuItem value="">All Roles</MenuItem>
              <MenuItem value="teacher">Teacher</MenuItem>
              <MenuItem value="head-teacher">Head Teacher</MenuItem>
              <MenuItem value="vice-principal">Vice Principal</MenuItem>
              <MenuItem value="principal">Principal</MenuItem>
              <MenuItem value="admin-staff">Admin Staff</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ flexGrow: 1 }} />
          <Tooltip title="Staff creation is handled through the registration workflow. Use the Edit action on existing staff to update their information.">
            <span>
              <Button variant="contained" startIcon={<AddIcon />} disabled>
                Add Staff
              </Button>
            </span>
          </Tooltip>
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
            message={error instanceof Error ? error.message : 'Failed to load staff directory.'} 
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
            getRowId={(row) => row.id}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No staff found" message="There are no staff members to display at this time." /> }}
          />
        )}
      </Paper>

      <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Staff Member</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="First Name"
            value={editForm.first_name ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, first_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Last Name"
            value={editForm.last_name ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, last_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Email"
            type="email"
            value={editForm.email ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, email: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Phone Number"
            value={editForm.phone_number ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, phone_number: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Role</InputLabel>
            <Select
              value={editForm.role ?? ''}
              label="Role"
              onChange={(e) => setEditForm((f) => ({ ...f, role: e.target.value }))}
            >
              <MenuItem value="teacher">Teacher</MenuItem>
              <MenuItem value="head-teacher">Head Teacher</MenuItem>
              <MenuItem value="vice-principal">Vice Principal</MenuItem>
              <MenuItem value="principal">Principal</MenuItem>
              <MenuItem value="admin-staff">Admin Staff</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Department"
            value={editForm.department ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, department: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              value={editForm.status ?? 'active'}
              label="Status"
              onChange={(e) => setEditForm((f) => ({ ...f, status: e.target.value }))}
            >
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="on_leave">On Leave</MenuItem>
              <MenuItem value="suspended">Suspended</MenuItem>
              <MenuItem value="archived">Archived</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained" disabled={updateMutation.isPending}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={archiveConfirmOpen} onClose={() => setArchiveConfirmOpen(false)}>
        <DialogTitle>Archive Staff Member</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to archive {selectedStaff?.first_name} {selectedStaff?.last_name}?
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

      <Dialog
        open={uploadOpen}
        onClose={() => {
          setUploadOpen(false);
          setUploadFile(null);
        }}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Upload Staff Document</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Upload documents for {selectedStaff?.first_name} {selectedStaff?.last_name}.
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Document Type</InputLabel>
            <Select
              value={uploadDocType}
              label="Document Type"
              onChange={(e) => setUploadDocType(e.target.value)}
            >
              <MenuItem value="cv">CV / Resume</MenuItem>
              <MenuItem value="degree">Degree Certificate</MenuItem>
              <MenuItem value="certification">Professional Certification</MenuItem>
              <MenuItem value="id">Identification Document</MenuItem>
              <MenuItem value="contract">Employment Contract</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <Button variant="outlined" component="label" fullWidth sx={{ py: 2 }}>
            {uploadFile ? uploadFile.name : 'Select File'}
            <input
              type="file"
              hidden
              onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
            />
          </Button>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => {
              setUploadOpen(false);
              setUploadFile(null);
            }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleUploadSubmit}
            variant="contained"
            disabled={!uploadFile || uploadMutation.isPending}
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={assignmentsOpen}
        onClose={() => setAssignmentsOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Manage Class & Subject Assignments</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Assign {selectedStaff?.first_name} {selectedStaff?.last_name} to a class or subject for
            the active academic year.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Class</InputLabel>
              <Select
                value={assignmentForm.class_id ?? ''}
                label="Class"
                onChange={(e) => setAssignmentForm((f) => ({ ...f, class_id: e.target.value }))}
              >
                <MenuItem value="">None</MenuItem>
                {classes?.map((c: AcademicClass) => (
                  <MenuItem key={c.id} value={c.id}>
                    {c.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Subject (Optional)</InputLabel>
              <Select
                value={assignmentForm.subject_id ?? ''}
                label="Subject (Optional)"
                onChange={(e) => setAssignmentForm((f) => ({ ...f, subject_id: e.target.value }))}
              >
                <MenuItem value="">None</MenuItem>
                {subjects?.map((s: Subject) => (
                  <MenuItem key={s.id} value={s.id}>
                    {s.name} ({s.code})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
            <FormControl fullWidth>
              <InputLabel>Assignment Type</InputLabel>
              <Select
                value={assignmentForm.assignment_type ?? 'regular'}
                label="Assignment Type"
                onChange={(e) =>
                  setAssignmentForm((f) => ({ ...f, assignment_type: e.target.value }))
                }
              >
                <MenuItem value="regular">Regular</MenuItem>
                <MenuItem value="substitute">Substitute</MenuItem>
                <MenuItem value="temporary">Temporary</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth sx={{ display: 'flex', justifyContent: 'center' }}>
              <label
                style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}
              >
                <input
                  type="checkbox"
                  checked={assignmentForm.is_form_teacher ?? false}
                  onChange={(e) =>
                    setAssignmentForm((f) => ({ ...f, is_form_teacher: e.target.checked }))
                  }
                />
                Is Form Teacher?
              </label>
            </FormControl>
          </Box>
          <Button
            onClick={handleAssignmentSubmit}
            variant="contained"
            disabled={!assignmentForm.class_id || createAssignmentMutation.isPending}
            sx={{ mt: 1, mb: 2 }}
          >
            {createAssignmentMutation.isPending ? 'Assigning...' : 'Add Assignment'}
          </Button>

          <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
            Current Assignments
          </Typography>
          <Paper elevation={0} sx={{ height: 250, border: '1px solid', borderColor: 'divider' }}>
            <DataGrid
              rows={assignments ?? []}
              columns={[
                { field: 'class_id', headerName: 'Class', width: 150 },
                { field: 'subject_id', headerName: 'Subject', width: 150 },
                { field: 'assignment_type', headerName: 'Type', width: 120 },
                {
                  field: 'is_form_teacher',
                  headerName: 'Form Teacher',
                  width: 120,
                  type: 'boolean',
                },
                {
                  field: 'actions',
                  headerName: '',
                  width: 80,
                  renderCell: (p) => (
                    <Button
                      color="error"
                      size="small"
                      onClick={() => deleteAssignmentMutation.mutate(p.row.id)}
                    >
                      Remove
                    </Button>
                  ),
                },
              ]}
              loading={assignmentsLoading}
              hideFooter
              slots={{ noRowsOverlay: () => <DataEmptyState title="No assignments found" message="There are no assignments to display at this time." /> }}
            />
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAssignmentsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={attendanceOpen}
        onClose={() => setAttendanceOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Staff Attendance Record</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Attendance history for {selectedStaff?.first_name} {selectedStaff?.last_name}.
          </Typography>
          <Paper elevation={0} sx={{ height: 400, border: '1px solid', borderColor: 'divider' }}>
            <DataGrid
              rows={attendanceData?.items ?? []}
              columns={[
                { field: 'date', headerName: 'Date', width: 120 },
                {
                  field: 'status',
                  headerName: 'Status',
                  width: 120,
                  renderCell: (p) => (
                    <Chip
                      label={p.value}
                      size="small"
                      color={
                        p.value === 'present'
                          ? 'success'
                          : p.value === 'absent'
                            ? 'error'
                            : 'warning'
                      }
                    />
                  ),
                },
                {
                  field: 'check_in_time',
                  headerName: 'Check In',
                  width: 180,
                  valueGetter: (v) => (v ? new Date(v).toLocaleTimeString() : '-'),
                },
                {
                  field: 'check_out_time',
                  headerName: 'Check Out',
                  width: 180,
                  valueGetter: (v) => (v ? new Date(v).toLocaleTimeString() : '-'),
                },
                { field: 'notes', headerName: 'Notes', width: 200 },
              ]}
              loading={attendanceLoading}
              initialState={{ pagination: { paginationModel: { pageSize: 10 } } }}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No attendance records found" message="There are no attendance records to display at this time." /> }}
            />
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAttendanceOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
