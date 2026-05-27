import { useState, useMemo } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  TextField,
  ToggleButton,
  ToggleButtonGroup,
  Toolbar,
  Typography,
} from '@mui/material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { Add as AddIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getEvents,
  createEvent,
  updateEvent,
  archiveEvent,
  type CalendarEvent,
  type CreateEventPayload,
} from './api';
import { CalendarView } from './CalendarView';

export function CalendarPage() {
  const queryClient = useQueryClient();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState<Partial<CalendarEvent & CreateEventPayload>>({
    event_type: 'general',
  });
  const [currentDate, setCurrentDate] = useState(new Date());
  const [view, setView] = useState<'month' | 'list'>('month');

  const monthStart = useMemo(() => {
    const d = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    return d.toISOString();
  }, [currentDate]);

  const monthEnd = useMemo(() => {
    const d = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0, 23, 59, 59);
    return d.toISOString();
  }, [currentDate]);

  const { data, isLoading } = useQuery({
    queryKey: ['calendar-events', view === 'month' ? monthStart : undefined],
    queryFn: () => getEvents(
      view === 'month' ? { start_date: monthStart, end_date: monthEnd } : undefined
    ),
  });

  const events = data?.items ?? [];

  const createMut = useMutation({
    mutationFn: createEvent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['calendar-events'] });
      setDialogOpen(false);
      setForm({ event_type: 'general' });
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<CreateEventPayload> }) =>
      updateEvent(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['calendar-events'] });
      setDialogOpen(false);
      setForm({ event_type: 'general' });
    },
  });

  const archiveMut = useMutation({
    mutationFn: archiveEvent,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['calendar-events'] }),
  });

  const handleSave = () => {
    if (form.id) {
      updateMut.mutate({ id: form.id, payload: form as Partial<CreateEventPayload> });
    } else {
      createMut.mutate(form as CreateEventPayload);
    }
  };

  const columns: GridColDef<CalendarEvent>[] = [
    { field: 'title', headerName: 'Title', width: 250 },
    { field: 'event_type', headerName: 'Event Type', width: 150 },
    {
      field: 'start_date',
      headerName: 'Start Date',
      width: 200,
      valueFormatter: (value: string | number | Date) => new Date(value).toLocaleString(),
    },
    {
      field: 'end_date',
      headerName: 'End Date',
      width: 200,
      valueFormatter: (value: string | number | Date) => new Date(value).toLocaleString(),
    },
    {
      field: 'actions',
      headerName: '',
      width: 150,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Button
            size="small"
            onClick={() => {
              setForm(p.row);
              setDialogOpen(true);
            }}
          >
            Edit
          </Button>
          <Button size="small" color="error" onClick={() => archiveMut.mutate(p.row.id)}>
            Archive
          </Button>
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
          School Calendar
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
        <Toolbar>
          <ToggleButtonGroup
            value={view}
            exclusive
            onChange={(_, v) => v && setView(v)}
            size="small"
          >
            <ToggleButton value="month">Month</ToggleButton>
            <ToggleButton value="list">List</ToggleButton>
          </ToggleButtonGroup>
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
              setForm({
                event_type: 'general',
                start_date: new Date().toISOString().slice(0, 16),
                end_date: new Date().toISOString().slice(0, 16),
              });
              setDialogOpen(true);
            }}
          >
            Add Event
          </Button>
        </Toolbar>
      </Paper>

      {view === 'month' ? (
        <CalendarView
          events={events}
          isLoading={isLoading}
          currentDate={currentDate}
          onDateChange={setCurrentDate}
          onAddEvent={(date) => {
            setForm({ event_type: 'general', start_date: date?.toISOString() || new Date().toISOString() });
            setDialogOpen(true);
          }}
          onEditEvent={(event) => {
            setForm(event);
            setDialogOpen(true);
          }}
        />
      ) : (
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
            rows={events}
            columns={columns}
            loading={isLoading}
            getRowId={(r) => r.id}
            initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
            pageSizeOptions={[10, 25, 50]}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No events found" message="There are no calendar events to display at this time." /> }}
          />
        </Paper>
      )}

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{form.id ? 'Edit Event' : 'Add Event'}</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Title"
            value={form.title ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
            sx={{ mt: 1 }}
          />
          <TextField
            label="Event Type"
            value={form.event_type ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, event_type: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Start Date"
            type="datetime-local"
            value={form.start_date ? new Date(form.start_date).toISOString().slice(0, 16) : ''}
            onChange={(e) =>
              setForm((f) => ({ ...f, start_date: new Date(e.target.value).toISOString() }))
            }
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End Date"
            type="datetime-local"
            value={form.end_date ? new Date(form.end_date).toISOString().slice(0, 16) : ''}
            onChange={(e) =>
              setForm((f) => ({ ...f, end_date: new Date(e.target.value).toISOString() }))
            }
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Description"
            value={form.description ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            fullWidth
            multiline
            rows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={createMut.isPending || updateMut.isPending}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
