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
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getClubs, createClub, type Club, type CreateClubPayload } from './api';

export function ClubsPage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateClubPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['clubs'], queryFn: () => getClubs() });

  const create = useMutation({
    mutationFn: (p: CreateClubPayload) => createClub(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clubs'] });
      setOpen(false);
      setForm({});
    },
  });

  const columns: GridColDef<Club>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'category', headerName: 'Category', width: 140 },
    { field: 'advisor_name', headerName: 'Advisor', width: 180 },
    { field: 'member_count', headerName: 'Members', width: 100 },
    { field: 'meeting_day', headerName: 'Meeting Day', width: 130 },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value ? 'Active' : 'Inactive'}
          size="small"
          color={p.value ? 'success' : 'default'}
        />
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
          Clubs
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
            onClick={() => setOpen(true)}
          >
            New Club
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
          rows={data ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(r) => r.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[10, 25, 50]}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Club</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Name"
            value={form.name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Category</InputLabel>
            <Select
              value={form.category ?? ''}
              label="Category"
              onChange={(e) => setForm((f) => ({ ...f, category: e.target.value }))}
            >
              <MenuItem value="academic">Academic</MenuItem>
              <MenuItem value="sports">Sports</MenuItem>
              <MenuItem value="arts">Arts</MenuItem>
              <MenuItem value="science">Science</MenuItem>
              <MenuItem value="cultural">Cultural</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Advisor Name"
            value={form.advisor_name ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, advisor_name: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Meeting Day</InputLabel>
            <Select
              value={form.meeting_day ?? ''}
              label="Meeting Day"
              onChange={(e) => setForm((f) => ({ ...f, meeting_day: e.target.value }))}
            >
              <MenuItem value="monday">Monday</MenuItem>
              <MenuItem value="tuesday">Tuesday</MenuItem>
              <MenuItem value="wednesday">Wednesday</MenuItem>
              <MenuItem value="thursday">Thursday</MenuItem>
              <MenuItem value="friday">Friday</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateClubPayload)}
            variant="contained"
            disabled={create.isPending}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
