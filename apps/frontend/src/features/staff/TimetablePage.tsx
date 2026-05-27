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
  ToggleButtonGroup,
  ToggleButton,
  Toolbar,
  Typography,
  Alert,
  Grid,
} from '@mui/material';
import { Add as AddIcon, Warning as WarningIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { TimetableGrid } from '../timetable/TimetableGrid';
import {
  getTimetables,
  createTimetable,
  updateTimetable,
  deleteTimetable,
  getTimetableEntries,
  addTimetableEntry,
  updateTimetableEntry,
  deleteTimetableEntry,
  publishTimetable,
  checkTimetableClashes,
  type Timetable,
  type TimetableEntry,
  type CreateTimetablePayload,
  type CreateTimetableEntryPayload,
} from './api';

const statusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  draft: 'warning',
  published: 'success',
  archived: 'default',
};

const DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export function TimetablePage() {
  const queryClient = useQueryClient();
  const [selectedTimetable, setSelectedTimetable] = useState<string | null>(null);
  const [timetableDialogOpen, setTimetableDialogOpen] = useState(false);
  const [entryDialogOpen, setEntryDialogOpen] = useState(false);
  const [timetableForm, setTimetableForm] = useState<Partial<Timetable & CreateTimetablePayload>>(
    {}
  );
  const [entryForm, setEntryForm] = useState<Partial<TimetableEntry & CreateTimetableEntryPayload>>(
    {
      day_of_week: 0,
    }
  );
  const [clashes, setClashes] = useState<any[]>([]);
  const [view, setView] = useState<'grid' | 'list'>('list');

  // Queries
  const { data: timetables, isLoading: timetablesLoading } = useQuery({
    queryKey: ['timetables'],
    queryFn: () => getTimetables(),
  });

  const { data: entries, isLoading: entriesLoading } = useQuery({
    queryKey: ['timetable-entries', selectedTimetable, view],
    queryFn: () =>
      selectedTimetable
        ? getTimetableEntries(selectedTimetable, view === 'grid')
        : Promise.resolve([] as TimetableEntry[]),
    enabled: !!selectedTimetable,
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: createTimetable,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
      setTimetableDialogOpen(false);
      setTimetableForm({});
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<CreateTimetablePayload> }) =>
      updateTimetable(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
      setTimetableDialogOpen(false);
      setTimetableForm({});
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTimetable,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
      if (selectedTimetable) setSelectedTimetable(null);
    },
  });

  const addEntryMutation = useMutation({
    mutationFn: ({
      timetableId,
      payload,
    }: {
      timetableId: string;
      payload: CreateTimetableEntryPayload;
    }) => addTimetableEntry(timetableId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetable-entries', selectedTimetable] });
      setEntryDialogOpen(false);
      setEntryForm({ day_of_week: 0 });
    },
  });

  const updateEntryMutation = useMutation({
    mutationFn: ({
      timetableId,
      entryId,
      payload,
    }: {
      timetableId: string;
      entryId: string;
      payload: Partial<CreateTimetableEntryPayload>;
    }) => updateTimetableEntry(timetableId, entryId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetable-entries', selectedTimetable] });
      setEntryDialogOpen(false);
      setEntryForm({ day_of_week: 0 });
    },
  });

  const deleteEntryMutation = useMutation({
    mutationFn: ({ timetableId, entryId }: { timetableId: string; entryId: string }) =>
      deleteTimetableEntry(timetableId, entryId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetable-entries', selectedTimetable] });
    },
  });

  const publishMutation = useMutation({
    mutationFn: publishTimetable,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
    },
  });

  const checkClashesMutation = useMutation({
    mutationFn: checkTimetableClashes,
    onSuccess: (data) => {
      setClashes(data.clashes);
    },
  });

  // Handlers
  const handleCreateTimetable = useCallback(() => {
    createMutation.mutate(timetableForm as CreateTimetablePayload);
  }, [timetableForm, createMutation]);

  const handleUpdateTimetable = useCallback((timetable: Timetable) => {
    setTimetableForm(timetable);
    setTimetableDialogOpen(true);
  }, []);

  const handleSaveTimetable = useCallback(() => {
    if (timetableForm.id) {
      updateMutation.mutate({ id: timetableForm.id, payload: timetableForm });
    } else {
      handleCreateTimetable();
    }
  }, [timetableForm, updateMutation, handleCreateTimetable]);

  const handleDeleteTimetable = useCallback(
    (id: string) => {
      deleteMutation.mutate(id);
    },
    [deleteMutation]
  );

  const handleAddEntry = useCallback(() => {
    if (!selectedTimetable) return;
    setEntryForm({ day_of_week: 0 });
    setEntryDialogOpen(true);
  }, [selectedTimetable]);

  const handleEditEntry = useCallback((entry: TimetableEntry) => {
    setEntryForm(entry);
    setEntryDialogOpen(true);
  }, []);

  const handleSaveEntry = useCallback(() => {
    if (!selectedTimetable) return;

    if (entryForm.id) {
      updateEntryMutation.mutate({
        timetableId: selectedTimetable,
        entryId: entryForm.id,
        payload: entryForm,
      });
    } else {
      addEntryMutation.mutate({
        timetableId: selectedTimetable,
        payload: entryForm as CreateTimetableEntryPayload,
      });
    }
  }, [selectedTimetable, entryForm, updateEntryMutation, addEntryMutation]);

  const handleDeleteEntry = useCallback(
    (entryId: string) => {
      if (!selectedTimetable) return;
      deleteEntryMutation.mutate({ timetableId: selectedTimetable, entryId });
    },
    [selectedTimetable, deleteEntryMutation]
  );

  const handlePublishTimetable = useCallback(
    (id: string) => {
      publishMutation.mutate(id);
    },
    [publishMutation]
  );

  const handleCheckClashes = useCallback(
    (id: string) => {
      checkClashesMutation.mutate(id);
    },
    [checkClashesMutation]
  );

  // Timetable columns
  const timetableColumns: GridColDef<Timetable>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'academic_year', headerName: 'Academic Year', width: 150 },
    { field: 'term', headerName: 'Term', width: 100 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => <Chip label={p.value} size="small" color={statusColors[p.value]} />,
    },
    {
      field: 'actions',
      headerName: '',
      width: 200,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Button
            size="small"
            onClick={() => setSelectedTimetable(p.row.id)}
            disabled={selectedTimetable === p.row.id}
          >
            View
          </Button>
          <Button size="small" onClick={() => handleUpdateTimetable(p.row)}>
            Edit
          </Button>
          <Button
            size="small"
            onClick={() => handleCheckClashes(p.row.id)}
            disabled={p.row.status === 'published'}
          >
            Check Clashes
          </Button>
          <Button
            size="small"
            color="primary"
            onClick={() => handlePublishTimetable(p.row.id)}
            disabled={p.row.status === 'published'}
          >
            Publish
          </Button>
          <Button size="small" color="error" onClick={() => handleDeleteTimetable(p.row.id)}>
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  // Entry columns
  const entryColumns: GridColDef<TimetableEntry>[] = [
    { field: 'staff_id', headerName: 'Staff ID', width: 150 },
    { field: 'class_id', headerName: 'Class ID', width: 150 },
    { field: 'subject_id', headerName: 'Subject ID', width: 150 },
    {
      field: 'day_of_week',
      headerName: 'Day',
      width: 120,
      renderCell: (p) => DAY_NAMES[p.value],
    },
    { field: 'start_time', headerName: 'Start Time', width: 120 },
    { field: 'end_time', headerName: 'End Time', width: 120 },
    { field: 'room', headerName: 'Room', width: 100 },
    {
      field: 'actions',
      headerName: '',
      width: 150,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Button size="small" onClick={() => handleEditEntry(p.row)}>
            Edit
          </Button>
          <Button size="small" color="error" onClick={() => handleDeleteEntry(p.row.id)}>
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <>
      <Toolbar sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Staff Timetables</Typography>
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
            setTimetableForm({});
            setTimetableDialogOpen(true);
          }}
        >
          Create Timetable
        </Button>
      </Toolbar>

      {clashes.length > 0 && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          <WarningIcon sx={{ mr: 1 }} />
          {clashes.length} clash{clashes.length > 1 ? 'es' : ''} detected in timetable
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Timetables
            </Typography>
            <DataGrid
              rows={timetables?.items ?? []}
              columns={timetableColumns}
              loading={timetablesLoading}
              rowSelection={false}
              disableRowSelectionOnClick
              autoHeight
              slots={{ noRowsOverlay: () => <DataEmptyState title="No timetables found" message="There are no timetables to display at this time." /> }}
            />
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <Paper sx={{ p: 2 }}>
            <Box
              sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}
            >
              <Typography variant="h6">
                {selectedTimetable ? 'Timetable Entries' : 'Select a timetable to view entries'}
              </Typography>
              {selectedTimetable && (
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                  <ToggleButtonGroup
                    value={view}
                    exclusive
                    onChange={(_, v) => v && setView(v)}
                    size="small"
                  >
                    <ToggleButton value="list">List</ToggleButton>
                    <ToggleButton value="grid">Grid</ToggleButton>
                  </ToggleButtonGroup>
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={handleAddEntry}
                    sx={{
                      borderRadius: 2,
                      px: 3,
                      py: 1,
                      fontWeight: 600,
                      boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)',
                      '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' },
                    }}
                  >
                    Add Entry
                  </Button>
                </Box>
              )}
            </Box>
            {view === 'grid' ? (
              <TimetableGrid
                entries={entries ?? []}
                timetableId={selectedTimetable!}
                isLoading={entriesLoading}
                onAddEntry={(day) => {
                  setEntryForm({ day_of_week: day ?? 1 });
                  setEntryDialogOpen(true);
                }}
                onEditEntry={(entry) => {
                  setEntryForm(entry);
                  setEntryDialogOpen(true);
                }}
              />
            ) : (
              <DataGrid
                rows={entries ?? []}
                columns={entryColumns}
                loading={entriesLoading}
                rowSelection={false}
                disableRowSelectionOnClick
                autoHeight
                slots={{ noRowsOverlay: () => <DataEmptyState title="No entries found" message="There are no timetable entries to display at this time." /> }}
              />
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Timetable Dialog */}
      <Dialog open={timetableDialogOpen} onClose={() => setTimetableDialogOpen(false)}>
        <DialogTitle>{timetableForm.id ? 'Edit Timetable' : 'Create Timetable'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Name"
            value={timetableForm.name || ''}
            onChange={(e) => setTimetableForm({ ...timetableForm, name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Academic Year"
            value={timetableForm.academic_year || ''}
            onChange={(e) => setTimetableForm({ ...timetableForm, academic_year: e.target.value })}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Term</InputLabel>
            <Select
              value={timetableForm.term || ''}
              label="Term"
              onChange={(e) => setTimetableForm({ ...timetableForm, term: e.target.value })}
            >
              <MenuItem value="first">First Term</MenuItem>
              <MenuItem value="second">Second Term</MenuItem>
              <MenuItem value="third">Third Term</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTimetableDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSaveTimetable}
            disabled={!timetableForm.name || !timetableForm.academic_year || !timetableForm.term}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Entry Dialog */}
      <Dialog open={entryDialogOpen} onClose={() => setEntryDialogOpen(false)}>
        <DialogTitle>{entryForm.id ? 'Edit Entry' : 'Add Entry'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Staff ID"
            value={entryForm.staff_id || ''}
            onChange={(e) => setEntryForm({ ...entryForm, staff_id: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Class ID"
            value={entryForm.class_id || ''}
            onChange={(e) => setEntryForm({ ...entryForm, class_id: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Subject ID"
            value={entryForm.subject_id || ''}
            onChange={(e) => setEntryForm({ ...entryForm, subject_id: e.target.value })}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Day of Week</InputLabel>
            <Select
              value={entryForm.day_of_week || 0}
              label="Day of Week"
              onChange={(e) => setEntryForm({ ...entryForm, day_of_week: e.target.value })}
            >
              {DAY_NAMES.map((day, index) => (
                <MenuItem key={day} value={index}>
                  {day}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="Start Time"
            type="time"
            value={entryForm.start_time || ''}
            onChange={(e) => setEntryForm({ ...entryForm, start_time: e.target.value })}
            sx={{ mb: 2 }}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            label="End Time"
            type="time"
            value={entryForm.end_time || ''}
            onChange={(e) => setEntryForm({ ...entryForm, end_time: e.target.value })}
            sx={{ mb: 2 }}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            fullWidth
            label="Room"
            value={entryForm.room || ''}
            onChange={(e) => setEntryForm({ ...entryForm, room: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEntryDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSaveEntry}
            disabled={
              !entryForm.staff_id ||
              !entryForm.class_id ||
              !entryForm.subject_id ||
              !entryForm.start_time ||
              !entryForm.end_time
            }
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
