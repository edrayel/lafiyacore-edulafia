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
  Tab,
  Tabs,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  School as SchoolIcon,
  People,
  Warning,
  Sync as SyncIcon,
  Update as UpdateIcon,
  MenuBook as TrainingIcon,
  BarChart as AnalyticsIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getProvisioningSchools, getUsers, getSentinelThresholds, createThreshold } from './api';
import { SyncMonitor } from './SyncMonitor';
import { SystemUpdates } from './SystemUpdates';
import { TrainingManager } from './TrainingManager';
import { AnalyticsPage } from './AnalyticsPage';
import type { ProvisioningSchool, AdminUser, SentinelThreshold, CreateThresholdPayload } from './api';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { useTabState } from '@/shared/hooks/useTabState';
import { DataErrorAlert } from '@/shared/components/DataErrorAlert';

const provisioningStatusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  completed: 'success',
  active: 'success',
  pending: 'warning',
  in_progress: 'warning',
  failed: 'error',
  error: 'error',
};

const userActiveColors: Record<string, 'success' | 'warning'> = {
  active: 'success',
  inactive: 'warning',
};

export function AdminPage() {
  const [tab, setTab] = useTabState('tab');

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Admin
        </Typography>
      </Box>

      <Tabs
        value={tab}
        onChange={(_, v) => setTab(v)}
        sx={{ mb: 3 }}
        variant="scrollable"
        scrollButtons="auto"
      >
        <Tab icon={<SchoolIcon />} label="Schools" iconPosition="start" />
        <Tab icon={<People />} label="Users" iconPosition="start" />
        <Tab icon={<Warning />} label="Sentinel Thresholds" iconPosition="start" />
        <Tab icon={<SyncIcon />} label="Sync Monitor" iconPosition="start" />
        <Tab icon={<UpdateIcon />} label="System Updates" iconPosition="start" />
        <Tab icon={<TrainingIcon />} label="Training" iconPosition="start" />
        <Tab icon={<AnalyticsIcon />} label="Analytics" iconPosition="start" />
      </Tabs>

      {tab === 0 && <SchoolsPanel />}
      {tab === 1 && <UsersPanel />}
      {tab === 2 && <SentinelThresholdsPanel />}
      {tab === 3 && <SyncMonitor />}
      {tab === 4 && <SystemUpdates />}
      {tab === 5 && <TrainingManager />}
      {tab === 6 && <AnalyticsPage />}
    </>
  );
}

function SchoolsPanel() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['admin-schools', { search, status: statusFilter }],
    queryFn: () =>
      getProvisioningSchools({
        status: statusFilter || undefined,
      }),
  });

  const rows =
    search.trim().length > 0
      ? (data?.items ?? []).filter(
          (row) =>
            row.school_id.toLowerCase().includes(search.trim().toLowerCase()) ||
            row.status.toLowerCase().includes(search.trim().toLowerCase())
        )
      : data?.items ?? [];

  const columns: GridColDef<ProvisioningSchool>[] = [
    { field: 'school_id', headerName: 'School ID', width: 280 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={provisioningStatusColors[params.value] || 'default'}
          size="small"
        />
      ),
    },
    {
      field: 'snapshot_date',
      headerName: 'Snapshot Date',
      width: 140,
      valueGetter: (value: string) => new Date(value).toLocaleDateString(),
    },
  ];

  return (
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
        <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
          <TextField
            size="small"
            placeholder="Search schools..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />,
            }}
            sx={{ minWidth: 250 }}
          />
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={statusFilter}
              label="Status"
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="inactive">Inactive</MenuItem>
              <MenuItem value="suspended">Suspended</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ flexGrow: 1 }} />
          <Tooltip title="Coming soon — requires Paystack, SMS, and email configuration. Contact support for setup assistance.">
            <span>
              <Button variant="contained" startIcon={<AddIcon />} disabled>
                Provision School
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
            message={
              error instanceof Error ? error.message : 'Failed to load provisioning schools list.'
            }
            onRetry={refetch}
          />
        )}
        {!isError && (
          <DataGrid
            rows={rows}
            columns={columns}
            loading={isLoading}
            pageSizeOptions={[10, 25, 50]}
            paginationMode="client"
            getRowId={(row) => row.school_id}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No schools found" message="There are no provisioning schools to display at this time." /> }}
          />
        )}
      </Paper>
    </>
  );
}

function UsersPanel() {
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 25 });

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['admin-users', { search, role: roleFilter, page: paginationModel.page, pageSize: paginationModel.pageSize }],
    queryFn: () =>
      getUsers({
        search: search || undefined,
        role: roleFilter || undefined,
        page: paginationModel.page + 1,
        per_page: paginationModel.pageSize,
      }),
  });

  const columns: GridColDef<AdminUser>[] = [
    {
      field: 'name',
      headerName: 'Name',
      width: 200,
      valueGetter: (_, row: AdminUser) => `${row.first_name} ${row.last_name}`,
    },
    { field: 'email', headerName: 'Email', width: 220 },
    {
      field: 'role',
      headerName: 'Role',
      width: 140,
      renderCell: (params) => <Chip label={params.value} size="small" variant="outlined" />,
    },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Active' : 'Inactive'}
          color={params.value ? userActiveColors.active : userActiveColors.inactive}
          size="small"
        />
      ),
    },
    {
      field: 'last_login_at',
      headerName: 'Last Login',
      width: 160,
      valueGetter: (value: string) => (value ? new Date(value).toLocaleDateString() : 'Never'),
    },
  ];

  return (
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
        <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
          <TextField
            size="small"
            placeholder="Search users..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />,
            }}
            sx={{ minWidth: 250 }}
          />
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Role</InputLabel>
            <Select value={roleFilter} label="Role" onChange={(e) => setRoleFilter(e.target.value)}>
              <MenuItem value="">All</MenuItem>
              <MenuItem value="super_admin">Super Admin</MenuItem>
              <MenuItem value="school_admin">School Admin</MenuItem>
              <MenuItem value="teacher">Teacher</MenuItem>
              <MenuItem value="nurse">Nurse</MenuItem>
              <MenuItem value="bursar">Bursar</MenuItem>
              <MenuItem value="accountant">Accountant</MenuItem>
              <MenuItem value="librarian">Librarian</MenuItem>
              <MenuItem value="parent">Parent</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ flexGrow: 1 }} />
          <Tooltip title="User creation requires SMTP configuration. Configure email settings in production to enable this feature.">
            <span>
              <Button variant="contained" startIcon={<AddIcon />} disabled>
                Create User
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
            message={error instanceof Error ? error.message : 'Failed to load users list.'}
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
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            getRowId={(row) => row.id}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No users found" message="There are no users to display at this time." /> }}
          />
        )}
      </Paper>
    </>
  );
}

function SentinelThresholdsPanel() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [thresholdForm, setThresholdForm] = useState<CreateThresholdPayload>({
    symptom_category: '',
    time_window_hours: 48,
    cluster_threshold: 3,
    school_threshold_percent: 10,
    change_reason: '',
  });

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['sentinel-thresholds'],
    queryFn: getSentinelThresholds,
  });

  const createMutation = useMutation({
    mutationFn: (payload: CreateThresholdPayload) => createThreshold(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sentinel-thresholds'] });
      setDialogOpen(false);
      setThresholdForm({
        symptom_category: '',
        time_window_hours: 48,
        cluster_threshold: 3,
        school_threshold_percent: 10,
        change_reason: '',
      });
    },
  });

  const queryClient = useQueryClient();

  const handleCreate = useCallback(() => {
    if (thresholdForm.symptom_category && thresholdForm.change_reason) {
      createMutation.mutate(thresholdForm);
    }
  }, [thresholdForm, createMutation]);

  const columns: GridColDef<SentinelThreshold>[] = [
    {
      field: 'symptom_category',
      headerName: 'Symptom Category',
      width: 200,
      renderCell: (params) => <Chip label={params.value} size="small" variant="outlined" />,
    },
    {
      field: 'school_threshold_percent',
      headerName: 'School Threshold',
      width: 160,
      renderCell: (params) => <Chip label={`${params.value}%`} color="warning" size="small" />,
    },
    { field: 'cluster_threshold', headerName: 'Cluster Threshold', width: 140 },
    { field: 'time_window_hours', headerName: 'Window (hrs)', width: 130 },
    { field: 'state', headerName: 'State', width: 120 },
    { field: 'lga', headerName: 'LGA', width: 120 },
    {
      field: 'is_active',
      headerName: 'Active',
      width: 100,
      renderCell: (params) => (
        <Chip label={params.value ? 'Yes' : 'No'} size="small" color={params.value ? 'success' : 'default'} />
      ),
    },
    {
      field: 'effective_from',
      headerName: 'Effective From',
      width: 140,
      valueGetter: (value: string) => new Date(value).toLocaleDateString(),
    },
  ];

  return (
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
        <Toolbar sx={{ gap: 2 }}>
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
            onClick={() => setDialogOpen(true)}
          >
            Add Threshold
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
        {isError && (
          <DataErrorAlert
            message={
              error instanceof Error ? error.message : 'Failed to load sentinel thresholds configuration.'
            }
            onRetry={refetch}
          />
        )}
        {!isError && (
          <DataGrid
            rows={data ?? []}
            columns={columns}
            loading={isLoading}
            pageSizeOptions={[10, 25, 50]}
            getRowId={(row) => row.id}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            slots={{ noRowsOverlay: () => <DataEmptyState title="No thresholds found" message="There are no sentinel thresholds to display at this time." /> }}
          />
        )}
      </Paper>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Sentinel Threshold</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Symptom Category"
            value={thresholdForm.symptom_category}
            onChange={(e) => setThresholdForm((f) => ({ ...f, symptom_category: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Time Window (hours)"
            type="number"
            value={thresholdForm.time_window_hours ?? 48}
            onChange={(e) =>
              setThresholdForm((f) => ({
                ...f,
                time_window_hours: Number(e.target.value),
              }))
            }
            fullWidth
          />
          <TextField
            label="Cluster Threshold"
            type="number"
            value={thresholdForm.cluster_threshold ?? 3}
            onChange={(e) =>
              setThresholdForm((f) => ({
                ...f,
                cluster_threshold: Number(e.target.value),
              }))
            }
            fullWidth
          />
          <TextField
            label="School Threshold (%)"
            type="number"
            value={thresholdForm.school_threshold_percent ?? 10}
            onChange={(e) =>
              setThresholdForm((f) => ({
                ...f,
                school_threshold_percent: Number(e.target.value),
              }))
            }
            fullWidth
          />
          <TextField
            label="Change Reason"
            value={thresholdForm.change_reason}
            onChange={(e) => setThresholdForm((f) => ({ ...f, change_reason: e.target.value }))}
            fullWidth
            multiline
            minRows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreate}
            variant="contained"
            disabled={createMutation.isPending || !thresholdForm.symptom_category || !thresholdForm.change_reason}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
