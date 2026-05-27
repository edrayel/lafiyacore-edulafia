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
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getGuardians, updateGuardian, archiveGuardian } from './api';
import type { Guardian } from '@/shared/types';
import { DataEmptyState }
import { SkeletonPage } from "@/shared/components/SkeletonPage"; from '@/shared/components/DataEmptyState';
import { useDebounce } from '@/shared/hooks/useDebounce';

export function GuardiansPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 300);
  const [selectedGuardian, setSelectedGuardian] = useState<Guardian | null>(null);
  const [editOpen, setEditOpen] = useState(false);
  const [archiveConfirmOpen, setArchiveConfirmOpen] = useState(false);
  const [editForm, setEditForm] = useState<Partial<Guardian>>({});

  const { data, isLoading } = useQuery({
    queryKey: ['guardians', { search: debouncedSearch }],
    queryFn: () => getGuardians({ search: debouncedSearch || undefined }),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<Guardian> }) =>
      updateGuardian(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['guardians'] });
      setEditOpen(false);
    },
  });

  const archiveMutation = useMutation({
    mutationFn: (id: string) => archiveGuardian(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['guardians'] });
      setArchiveConfirmOpen(false);
    },
  });

  const handleEdit = useCallback((guardian: Guardian) => {
    setSelectedGuardian(guardian);
    setEditForm({
      first_name: guardian.first_name,
      last_name: guardian.last_name,
      phone_number: guardian.phone_number,
      relationship_type: guardian.relationship_type,
      email: guardian.email,
      whatsapp_number: guardian.whatsapp_number,
      occupation: guardian.occupation,
      address: guardian.address,
    });
    setEditOpen(true);
  }, []);

  const handleArchive = useCallback((guardian: Guardian) => {
    setSelectedGuardian(guardian);
    setArchiveConfirmOpen(true);
  }, []);

  const handleSaveEdit = useCallback(() => {
    if (selectedGuardian) {
      updateMutation.mutate({ id: selectedGuardian.id, payload: editForm });
    }
  }, [selectedGuardian, editForm, updateMutation]);

  const handleConfirmArchive = useCallback(() => {
    if (selectedGuardian) {
      archiveMutation.mutate(selectedGuardian.id);
    }
  }, [selectedGuardian, archiveMutation]);

  const columns: GridColDef<Guardian>[] = [
    {
      field: 'name',
      headerName: 'Name',
      width: 220,
      valueGetter: (_, row: Guardian) => `${row.first_name} ${row.last_name}`,
    },
    { field: 'phone_number', headerName: 'Phone', width: 160 },
    { field: 'email', headerName: 'Email', width: 200 },
    {
      field: 'relationship_type',
      headerName: 'Relationship',
      width: 140,
      renderCell: (params) => <Chip label={params.value} size="small" variant="outlined" />,
    },
    {
      field: 'portal_access',
      headerName: 'Portal Access',
      width: 130,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Enabled' : 'Disabled'}
          color={params.value ? 'success' : 'default'}
          size="small"
        />
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
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Guardians
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
            placeholder="Search guardians..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{ startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} /> }}
            sx={{ minWidth: 250 }}
          />
          <Box sx={{ flexGrow: 1 }} />
          <Tooltip title="Guardian registration requires SMS/WhatsApp provider configuration. Use a parent's detail page to manage existing guardians.">
            <span>
              <Button variant="contained" startIcon={<AddIcon />} disabled>
                Add Guardian
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
        <DataGrid
          rows={data?.items ?? []}
          columns={columns}
          loading={isLoading}
          rowCount={data?.total ?? 0}
          pageSizeOptions={[10, 25, 50]}
          paginationMode="server"
          getRowId={(row) => row.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          slots={{ noRowsOverlay: () => <DataEmptyState title="No guardians found" message="There are no guardians to display at this time." /> }}
        />
      </Paper>

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
          <FormControl fullWidth>
            <InputLabel>Relationship</InputLabel>
            <Select
              value={editForm.relationship_type ?? ''}
              label="Relationship"
              onChange={(e) => setEditForm((f) => ({ ...f, relationship_type: e.target.value }))}
            >
              <MenuItem value="father">Father</MenuItem>
              <MenuItem value="mother">Mother</MenuItem>
              <MenuItem value="guardian">Guardian</MenuItem>
              <MenuItem value="sibling">Sibling</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
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
            Are you sure you want to archive {selectedGuardian?.first_name}{' '}
            {selectedGuardian?.last_name}?
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
    </>
  );
}
