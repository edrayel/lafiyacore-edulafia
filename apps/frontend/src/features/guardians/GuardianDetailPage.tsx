import { useState } from 'react';
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
  Grid,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Edit as EditIcon,
  DeleteOutline as ArchiveIcon,
  LinkOff as UnlinkIcon,
  Link as LinkIcon,
} from '@mui/icons-material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getGuardian, updateGuardian, archiveGuardian, unlinkFromStudent } from './api';
import { getStudents } from '../students/api';
import type { Guardian, Student } from '@/shared/types';

interface GuardianDetailPageProps {
  guardianId: string;
  onBack: () => void;
}

export function GuardianDetailPage({ guardianId, onBack }: GuardianDetailPageProps) {
  const queryClient = useQueryClient();
  const [editOpen, setEditOpen] = useState(false);
  const [archiveConfirmOpen, setArchiveConfirmOpen] = useState(false);
  const [editForm, setEditForm] = useState<Partial<Guardian>>({});

  const { data: guardian, isLoading } = useQuery({
    queryKey: ['guardian', guardianId],
    queryFn: () => getGuardian(guardianId),
    enabled: !!guardianId,
  });

  const { data: students, isLoading: _studentsLoading } = useQuery({
    queryKey: ['students', { guardian_id: guardianId }],
    queryFn: () => getStudents({ per_page: 100, guardian_id: guardianId }),
  });

  const linkedStudents = students?.items || [];

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<Guardian> }) =>
      updateGuardian(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['guardian', guardianId] });
      setEditOpen(false);
    },
  });

  const archiveMutation = useMutation({
    mutationFn: (id: string) => archiveGuardian(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['guardian', guardianId] });
      setArchiveConfirmOpen(false);
    },
  });

  const unlinkMutation = useMutation({
    mutationFn: ({ guardianId, studentId }: { guardianId: string; studentId: string }) =>
      unlinkFromStudent(guardianId, studentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['guardian', guardianId] });
    },
  });

  const handleEdit = () => {
    if (guardian) {
      setEditForm({
        first_name: guardian.first_name,
        last_name: guardian.last_name,
        phone_number: guardian.phone_number,
        relationship_type: guardian.relationship_type,
        email: guardian.email,
        whatsapp_number: guardian.whatsapp_number,
        occupation: guardian.occupation,
        address: guardian.address,
        nin: guardian.nin,
      });
      setEditOpen(true);
    }
  };

  const handleSaveEdit = () => {
    updateMutation.mutate({ id: guardianId, payload: editForm });
  };

  const handleArchive = () => {
    archiveMutation.mutate(guardianId);
  };

  const handleUnlinkStudent = (studentId: string) => {
    unlinkMutation.mutate({ guardianId, studentId });
  };

  if (isLoading) return <SkeletonPage rows={5} cardCount={4} />;

  if (!guardian) {
    return <Typography>Guardian not found</Typography>;
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
            {guardian.first_name} {guardian.last_name}
          </Typography>
        </Box>
        <Chip
          label={guardian.relationship_type}
          variant="outlined"
          sx={{ ml: 2, textTransform: 'capitalize' }}
        />
      </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 8 }}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Guardian Information
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Phone Number
                  </Typography>
                  <Typography>{guardian.phone_number}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Email
                  </Typography>
                  <Typography>{guardian.email ?? 'Not provided'}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    WhatsApp
                  </Typography>
                  <Typography>{guardian.whatsapp_number ?? 'Not provided'}</Typography>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Occupation
                  </Typography>
                  <Typography>{guardian.occupation ?? 'Not provided'}</Typography>
                </Grid>
                {guardian.nin && (
                  <Grid size={{ xs: 12, sm: 6 }}>
                    <Typography variant="caption" color="textSecondary">
                      NIN
                    </Typography>
                    <Typography>{guardian.nin}</Typography>
                  </Grid>
                )}
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Typography variant="caption" color="textSecondary">
                    Portal Access
                  </Typography>
                  <Typography>
                    <Chip
                      label={guardian.portal_access ? 'Enabled' : 'Disabled'}
                      color={guardian.portal_access ? 'success' : 'default'}
                      size="small"
                    />
                  </Typography>
                </Grid>
                {guardian.address && (
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="caption" color="textSecondary">
                      Address
                    </Typography>
                    <Typography>{guardian.address}</Typography>
                  </Grid>
                )}
              </Grid>
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
                <Typography variant="h6">Linked Students</Typography>
                <Button variant="outlined" size="small" startIcon={<LinkIcon />}>
                  Link Student
                </Button>
              </Box>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Class</TableCell>
                      <TableCell>Admission #</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {linkedStudents.map((student) => (
                      <TableRow key={student.id}>
                        <TableCell>
                          {student.first_name} {student.last_name}
                        </TableCell>
                        <TableCell>{(student as Student & { current_class_id?: string }).current_class_id || 'N/A'}</TableCell>
                        <TableCell>{student.admission_number || 'N/A'}</TableCell>
                        <TableCell align="right">
                          <IconButton
                            size="small"
                            color="error"
                            aria-label="Unlink student"
                            onClick={() => handleUnlinkStudent(student.id)}
                          >
                            <UnlinkIcon fontSize="small" />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
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
                  Edit Guardian
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<ArchiveIcon />}
                  onClick={() => setArchiveConfirmOpen(true)}
                  fullWidth
                >
                  Archive Guardian
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Guardian</DialogTitle>
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
            label="Phone Number"
            value={editForm.phone_number ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, phone_number: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Email"
            value={editForm.email ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, email: e.target.value }))}
            fullWidth
          />
          <TextField
            label="WhatsApp Number"
            value={editForm.whatsapp_number ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, whatsapp_number: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Occupation"
            value={editForm.occupation ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, occupation: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Address"
            value={editForm.address ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, address: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="NIN"
            value={editForm.nin ?? ''}
            onChange={(e) => setEditForm((f) => ({ ...f, nin: e.target.value }))}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained" disabled={updateMutation.isPending}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={archiveConfirmOpen} onClose={() => setArchiveConfirmOpen(false)}>
        <DialogTitle>Archive Guardian</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to archive {guardian.first_name} {guardian.last_name}? This will
            remove their access to the parent portal.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setArchiveConfirmOpen(false)}>Cancel</Button>
          <Button
            onClick={handleArchive}
            color="error"
            variant="contained"
            disabled={archiveMutation.isPending}
          >
            Archive
          </Button>
        </DialogActions>
      </Dialog>
    </PageTransition>
  );
}
