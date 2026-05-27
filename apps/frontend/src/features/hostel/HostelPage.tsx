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
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getHostels,
  createHostel,
  deleteHostel,
  getRooms,
  createRoom,
  deleteRoom,
  getAllocationsByRoom,
  createAllocation,
  deleteAllocation,
  type Hostel,
  type Room,
  type BedAllocation,
  type CreateHostelPayload,
  type CreateRoomPayload,
  type CreateAllocationPayload,
} from './api';

import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { useTabState } from '@/shared/hooks/useTabState';
import { getAcademicMetadata } from '../academics/api';

export function HostelPage() {
  const [tab, setTab] = useTabState('tab');
  const queryClient = useQueryClient();
  const { data: metadata } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
  });

  const activeSchoolId = metadata?.school_id || '';
  const activeAcademicYearId = metadata?.academic_year?.id || '';

  // Dialogs
  const [hostelDialogOpen, setHostelDialogOpen] = useState(false);
  const [roomDialogOpen, setRoomDialogOpen] = useState(false);
  const [allocationDialogOpen, setAllocationDialogOpen] = useState(false);

  // Forms
  const [hostelForm, setHostelForm] = useState<Partial<CreateHostelPayload>>({ gender: 'mixed' });
  const [roomForm, setRoomForm] = useState<Partial<CreateRoomPayload>>({});
  const [allocationForm, setAllocationForm] = useState<Partial<CreateAllocationPayload>>({});

  // Selection state for cascading
  const [selectedHostelId, setSelectedHostelId] = useState<string>('');
  const [selectedRoomId, setSelectedRoomId] = useState<string>('');

  // Queries
  const { data: hostels, isLoading: hostelsLoading } = useQuery({
    queryKey: ['hostels', activeSchoolId],
    queryFn: () => getHostels(activeSchoolId),
    enabled: !!activeSchoolId,
  });

  const { data: rooms, isLoading: roomsLoading } = useQuery({
    queryKey: ['rooms', selectedHostelId],
    queryFn: () => getRooms(selectedHostelId),
    enabled: !!selectedHostelId,
  });

  const { data: allocations, isLoading: allocationsLoading } = useQuery({
    queryKey: ['allocations', selectedRoomId],
    queryFn: () => getAllocationsByRoom(selectedRoomId),
    enabled: !!selectedRoomId,
  });

  // Mutations
  const createHostelMutation = useMutation({
    mutationFn: createHostel,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hostels'] });
      setHostelDialogOpen(false);
      setHostelForm({ gender: 'mixed' });
    },
  });

  const deleteHostelMutation = useMutation({
    mutationFn: deleteHostel,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['hostels'] }),
  });

  const createRoomMutation = useMutation({
    mutationFn: createRoom,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['rooms'] });
      setRoomDialogOpen(false);
      setRoomForm({});
    },
  });

  const deleteRoomMutation = useMutation({
    mutationFn: deleteRoom,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['rooms'] }),
  });

  const createAllocationMutation = useMutation({
    mutationFn: createAllocation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['allocations'] });
      setAllocationDialogOpen(false);
      setAllocationForm({});
    },
  });

  const deleteAllocationMutation = useMutation({
    mutationFn: deleteAllocation,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['allocations'] }),
  });

  // Columns
  const hostelColumns: GridColDef<Hostel>[] = [
    { field: 'name', headerName: 'Hostel Name', width: 200 },
    { field: 'capacity', headerName: 'Capacity', width: 120 },
    {
      field: 'gender',
      headerName: 'Gender',
      width: 120,
      renderCell: (p) => <Chip label={p.value} size="small" />,
    },
    {
      field: 'actions',
      headerName: '',
      width: 150,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            onClick={() => {
              setSelectedHostelId(p.row.id);
              setTab(1); // switch to rooms
            }}
          >
            View Rooms
          </Button>
          <Button size="small" color="error" onClick={() => deleteHostelMutation.mutate(p.row.id)}>
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  const roomColumns: GridColDef<Room>[] = [
    { field: 'room_number', headerName: 'Room Number', width: 150 },
    { field: 'capacity', headerName: 'Capacity', width: 120 },
    {
      field: 'actions',
      headerName: '',
      width: 150,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            onClick={() => {
              setSelectedRoomId(p.row.id);
              setTab(2); // switch to allocations
            }}
          >
            View Beds
          </Button>
          <Button size="small" color="error" onClick={() => deleteRoomMutation.mutate(p.row.id)}>
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  const allocationColumns: GridColDef<BedAllocation>[] = [
    { field: 'student_id', headerName: 'Student ID', width: 300 },
    {
      field: 'created_at',
      headerName: 'Allocated On',
      width: 200,
      valueGetter: (_value: unknown, row: BedAllocation) => new Date(row.created_at).toLocaleDateString(),
    },
    {
      field: 'actions',
      headerName: '',
      width: 100,
      sortable: false,
      renderCell: (p) => (
        <Button
          size="small"
          color="error"
          onClick={() => deleteAllocationMutation.mutate(p.row.id)}
        >
          Unassign
        </Button>
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
          Hostel & Boarding
        </Typography>
      </Box>

      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Hostels" />
          <Tab label="Rooms" disabled={!selectedHostelId} />
          <Tab label="Bed Allocations" disabled={!selectedRoomId} />
        </Tabs>
      </Paper>

      {/* HOSTELS TAB */}
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
                onClick={() => setHostelDialogOpen(true)}
              >
                Add Hostel
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
              rows={hostels ?? []}
              columns={hostelColumns}
              loading={hostelsLoading}
              getRowId={(r) => r.id}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No hostels found" message="There are no hostels to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {/* ROOMS TAB */}
      {tab === 1 && (
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
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                Rooms for Selected Hostel
              </Typography>
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
                  setRoomForm({ hostel_id: selectedHostelId });
                  setRoomDialogOpen(true);
                }}
              >
                Add Room
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
              rows={rooms ?? []}
              columns={roomColumns}
              loading={roomsLoading}
              getRowId={(r) => r.id}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No rooms found" message="There are no rooms to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {/* ALLOCATIONS TAB */}
      {tab === 2 && (
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
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                Bed Allocations for Selected Room
              </Typography>
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
                  setAllocationForm({
                    room_id: selectedRoomId,
                    academic_year_id: activeAcademicYearId,
                  });
                  setAllocationDialogOpen(true);
                }}
              >
                Allocate Bed
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
              rows={allocations ?? []}
              columns={allocationColumns}
              loading={allocationsLoading}
              getRowId={(r) => r.id}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No allocations found" message="There are no bed allocations to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {/* DIALOGS */}
      <Dialog
        open={hostelDialogOpen}
        onClose={() => setHostelDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add Hostel</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Name"
            value={hostelForm.name ?? ''}
            onChange={(e) => setHostelForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Capacity"
            type="number"
            value={hostelForm.capacity ?? ''}
            onChange={(e) =>
              setHostelForm((f) => ({ ...f, capacity: parseInt(e.target.value) || 0 }))
            }
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Gender</InputLabel>
            <Select
              value={hostelForm.gender ?? 'mixed'}
              label="Gender"
              onChange={(e) => setHostelForm((f) => ({ ...f, gender: e.target.value }))}
            >
              <MenuItem value="mixed">Mixed</MenuItem>
              <MenuItem value="male">Male</MenuItem>
              <MenuItem value="female">Female</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setHostelDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() =>
              createHostelMutation.mutate({
                ...hostelForm,
                school_id: activeSchoolId,
              } as CreateHostelPayload)
            }
            variant="contained"
            disabled={createHostelMutation.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={roomDialogOpen}
        onClose={() => setRoomDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add Room</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Room Number"
            value={roomForm.room_number ?? ''}
            onChange={(e) => setRoomForm((f) => ({ ...f, room_number: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Capacity"
            type="number"
            value={roomForm.capacity ?? ''}
            onChange={(e) =>
              setRoomForm((f) => ({ ...f, capacity: parseInt(e.target.value) || 0 }))
            }
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRoomDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => createRoomMutation.mutate(roomForm as CreateRoomPayload)}
            variant="contained"
            disabled={createRoomMutation.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={allocationDialogOpen}
        onClose={() => setAllocationDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Allocate Bed</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID (UUID)"
            value={allocationForm.student_id ?? ''}
            onChange={(e) => setAllocationForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
            helperText="Enter valid student UUID for now"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAllocationDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() =>
              createAllocationMutation.mutate(allocationForm as CreateAllocationPayload)
            }
            variant="contained"
            disabled={createAllocationMutation.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
