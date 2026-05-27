import { useState, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import { apiClient } from '@/shared/api/client';
import { getStudentGuardians, unlinkFromStudent } from '../guardians/api';
import type { Guardian, Student } from '@/shared/types';
import {
  CloudUpload as UploadIcon,
  Download as DownloadIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  LinkOff as UnlinkIcon,
  DeleteOutline as ArchiveIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';
import {
  getStudent,
  getStudentDocuments,
  uploadStudentDocument,
  deleteStudentDocument,
  updateStudent,
  archiveStudent,
  exportStudentData,
} from './api';

const statusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  active: 'success',
  archived: 'default',
  graduated: 'success',
  withdrawn: 'error',
  suspended: 'warning',
};

interface StudentDetailPageProps {
  studentId: string;
  onBack: () => void;
}

export function StudentDetailPage({ studentId, onBack }: StudentDetailPageProps) {
  const queryClient = useQueryClient();
  const [editOpen, setEditOpen] = useState(false);
  const [archiveConfirmOpen, setArchiveConfirmOpen] = useState(false);
  const [editForm, setEditForm] = useState<Partial<Student>>({});

  const { data: student, isLoading } = useQuery({
    queryKey: ['student', studentId],
    queryFn: () => getStudent(studentId),
    enabled: !!studentId,
  });

  const { data: guardians } = useQuery({
    queryKey: ['student-guardians', studentId],
    queryFn: () => getStudentGuardians(studentId),
    enabled: !!studentId,
  });

  const { data: documents } = useQuery({
    queryKey: ['student-documents', studentId],
    queryFn: () => getStudentDocuments(studentId),
    enabled: !!studentId,
  });

  const [uploadOpen, setUploadOpen] = useState(false);
  const [uploadForm, setUploadForm] = useState({ document_type: '', title: '' });
  const fileInputRef = useRef<HTMLInputElement>(null);

  const uploadMutation = useMutation({
    mutationFn: (formData: FormData) => uploadStudentDocument(studentId, formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['student-documents', studentId] });
      setUploadOpen(false);
      setUploadForm({ document_type: '', title: '' });
    },
  });

  const deleteDocMutation = useMutation({
    mutationFn: (documentId: string) => deleteStudentDocument(studentId, documentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['student-documents', studentId] });
    },
  });

  const handleUploadSubmit = () => {
    if (!fileInputRef.current?.files?.[0] || !uploadForm.document_type || !uploadForm.title) return;
    const formData = new FormData();
    formData.append('document_type', uploadForm.document_type);
    formData.append('title', uploadForm.title);
    formData.append('file', fileInputRef.current.files[0]);
    uploadMutation.mutate(formData);
  };

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<Student> }) =>
      updateStudent(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['student', studentId] });
      setEditOpen(false);
    },
  });

  const archiveMutation = useMutation({
    mutationFn: (id: string) => archiveStudent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['student', studentId] });
      setArchiveConfirmOpen(false);
    },
  });

  const exportMutation = useMutation({
    mutationFn: (id: string) => exportStudentData(id),
    onSuccess: (data) => {
      // Download the JSON file
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `student_export_${studentId}.json`;
      a.click();
      URL.revokeObjectURL(url);
    },
  });

  const handleEdit = () => {
    if (student) {
      setEditForm({
        first_name: student.first_name,
        last_name: student.last_name,
        middle_name: student.middle_name,
        nin: student.nin,
        date_of_birth: student.date_of_birth,
        gender: student.gender,
        admission_number: student.admission_number,
        class_id: student.class_id,
        nationality: student.nationality,
        state_of_origin: student.state_of_origin,
        address: student.address,
        medical_conditions: student.medical_conditions,
        special_needs: student.special_needs,
        status: student.status,
      });
      setEditOpen(true);
    }
  };

  const handleSaveEdit = () => {
    updateMutation.mutate({ id: studentId, payload: editForm });
  };

  const handleUnlink = async (guardianId: string) => {
    try {
      await unlinkFromStudent(guardianId, studentId);
      queryClient.invalidateQueries({ queryKey: ['student-guardians', studentId] });
    } catch (e) {
      console.error('Failed to unlink guardian', e);
    }
  };

  if (isLoading) return <SkeletonPage rows={5} cardCount={4} />;

  if (!student) {
    return <Typography>Student not found</Typography>;
  }

  return (
    <PageTransition isLoading={isLoading}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, gap: 1 }}>
        <IconButton aria-label="Go back" onClick={onBack}>
          <ArrowBackIcon />
        </IconButton>
        <Box sx={{ mb: 4 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
          >
            {student.first_name} {student.last_name}
          </Typography>
        </Box>
        <Chip
          label={student.status}
          color={statusColors[student.status] || 'default'}
          sx={{ ml: 2 }}
        />
      </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 8 }}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Student Information
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Admission Number
                  </Typography>
                  <Typography>{student.admission_number}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Date of Birth
                  </Typography>
                  <Typography>{new Date(student.date_of_birth).toLocaleDateString()}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Gender
                  </Typography>
                  <Typography>{student.gender}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Class
                  </Typography>
                  <Typography>{student.class_id ?? 'Not assigned'}</Typography>
                </Grid>
                {student.nin && (
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="caption" color="textSecondary">
                      NIN
                    </Typography>
                    <Typography>{student.nin}</Typography>
                  </Grid>
                )}
                {student.nationality && (
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="caption" color="textSecondary">
                      Nationality
                    </Typography>
                    <Typography>{student.nationality}</Typography>
                  </Grid>
                )}
                {student.state_of_origin && (
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="caption" color="textSecondary">
                      State of Origin
                    </Typography>
                    <Typography>{student.state_of_origin}</Typography>
                  </Grid>
                )}
                {student.address && (
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="caption" color="textSecondary">
                      Address
                    </Typography>
                    <Typography>{student.address}</Typography>
                  </Grid>
                )}
                {student.medical_conditions && (
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="caption" color="textSecondary">
                      Medical Conditions
                    </Typography>
                    <Typography color="error">{student.medical_conditions}</Typography>
                  </Grid>
                )}
                {student.special_needs && (
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="caption" color="textSecondary">
                      Special Needs
                    </Typography>
                    <Typography>{student.special_needs}</Typography>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Linked Guardians
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Relationship</TableCell>
                      <TableCell>Phone</TableCell>
                      <TableCell>Email</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {guardians && guardians.length > 0 ? (
                      guardians.map((guardian: Guardian) => (
                        <TableRow key={guardian.id}>
                          <TableCell>
                            {guardian.first_name} {guardian.last_name}
                          </TableCell>
                          <TableCell>{guardian.relationship_type}</TableCell>
                          <TableCell>{guardian.phone_number}</TableCell>
                          <TableCell>{guardian.email || '—'}</TableCell>
                          <TableCell align="right">
                            <IconButton
                              size="small"
                              color="error"
                              aria-label="Unlink guardian"
                              onClick={() => handleUnlink(guardian.id)}
                            >
                              <UnlinkIcon fontSize="small" />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell
                          colSpan={5}
                          sx={{ textAlign: 'center', py: 3, color: 'text.secondary' }}
                        >
                          No guardians linked
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
          <Card>
            <CardContent>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  mb: 2,
                }}
              >
                <Typography variant="h6">Documents</Typography>
                <Button size="small" startIcon={<UploadIcon />} onClick={() => setUploadOpen(true)}>
                  Upload Document
                </Button>
              </Box>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Title</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Date Uploaded</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {documents && documents.length > 0 ? (
                      documents.map((doc: { id: string; title: string; document_type: string; filename?: string; file_url?: string; created_at?: string; uploaded_at: string }) => (
                        <TableRow key={doc.id}>
                          <TableCell>{doc.title}</TableCell>
                          <TableCell>{doc.document_type.replace('_', ' ')}</TableCell>
                          <TableCell>{new Date(doc.uploaded_at).toLocaleDateString()}</TableCell>
                          <TableCell align="right">
                            <IconButton
                              size="small"
                              component="a"
                              aria-label="Download document"
                              href={`${apiClient.defaults.baseURL?.replace('/api/v1', '') ?? ''}${doc.file_url}`}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <DownloadIcon fontSize="small" />
                            </IconButton>
                            <IconButton
                              size="small"
                              color="error"
                              aria-label="Delete document"
                              onClick={() => deleteDocMutation.mutate(doc.id)}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell
                          colSpan={4}
                          sx={{ textAlign: 'center', py: 3, color: 'text.secondary' }}
                        >
                          No documents uploaded
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Button variant="outlined" startIcon={<EditIcon />} onClick={handleEdit} fullWidth>
                  Edit Student
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<DownloadIcon />}
                  onClick={() => exportMutation.mutate(studentId)}
                  fullWidth
                  disabled={exportMutation.isPending}
                >
                  {exportMutation.isPending ? 'Exporting...' : 'Export Data Package'}
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<ArchiveIcon />}
                  onClick={() => setArchiveConfirmOpen(true)}
                  fullWidth
                >
                  Archive Student
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Student</DialogTitle>
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
            label="Middle Name"
            value={editForm.middle_name ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, middle_name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="NIN (National Identification Number)"
            value={editForm.nin ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, nin: e.target.value }))}
            fullWidth
            placeholder="11-digit NIN"
          />
          <TextField
            label="Date of Birth"
            type="date"
            value={editForm.date_of_birth ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, date_of_birth: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <FormControl fullWidth>
            <InputLabel>Gender</InputLabel>
            <Select
              value={editForm.gender ?? ''}
              label="Gender"
              onChange={(e) => setEditForm((f) => ({ ...f, gender: e.target.value }))}
            >
              <MenuItem value="male">Male</MenuItem>
              <MenuItem value="female">Female</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Address"
            value={editForm.address ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, address: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Medical Conditions"
            value={editForm.medical_conditions ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, medical_conditions: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <FormControl fullWidth>
            <InputLabel>Status</InputLabel>
            <Select
              value={editForm.status ?? 'active'}
              label="Status"
              onChange={(e) => setEditForm((f) => ({ ...f, status: e.target.value }))}
            >
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="archived">Archived</MenuItem>
              <MenuItem value="graduated">Graduated</MenuItem>
              <MenuItem value="withdrawn">Withdrawn</MenuItem>
              <MenuItem value="suspended">Suspended</MenuItem>
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
        <DialogTitle>Archive Student</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to archive {student.first_name} {student.last_name}? This action
            will mark the student as archived.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setArchiveConfirmOpen(false)}>Cancel</Button>
          <Button
            onClick={() => archiveMutation.mutate(studentId)}
            color="error"
            variant="contained"
            disabled={archiveMutation.isPending}
          >
            Archive
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={uploadOpen} onClose={() => setUploadOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Upload Document</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Document Type</InputLabel>
            <Select
              value={uploadForm.document_type}
              label="Document Type"
              onChange={(e) => setUploadForm({ ...uploadForm, document_type: e.target.value })}
            >
              <MenuItem value="admission_letter">Admission Letter</MenuItem>
              <MenuItem value="birth_certificate">Birth Certificate</MenuItem>
              <MenuItem value="medical_record">Medical Record</MenuItem>
              <MenuItem value="transfer_letter">Transfer Letter</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Document Title"
            value={uploadForm.title}
            onChange={(e) => setUploadForm({ ...uploadForm, title: e.target.value })}
            fullWidth
          />
          <Button variant="outlined" component="label" fullWidth sx={{ py: 2 }}>
            Select File
            <input type="file" hidden ref={fileInputRef} />
          </Button>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadOpen(false)}>Cancel</Button>
          <Button
            onClick={handleUploadSubmit}
            variant="contained"
            disabled={!uploadForm.document_type || !uploadForm.title || uploadMutation.isPending}
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload'}
          </Button>
        </DialogActions>
      </Dialog>
    </PageTransition>
  );
}
