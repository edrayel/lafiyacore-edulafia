import { useState, useEffect } from 'react';
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
  Card,
  CardContent,
  Autocomplete,
} from '@mui/material';
import {
  Add as AddIcon,
  Warning,
  CloudSync as SyncIcon,
  WifiOff as OfflineIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getSickBayVisits,
  createSickBayVisit,
  getReferrals,
  createReferral,
  updateReferral,
  getVaccinations,
  createVaccination,
  getSentinelAlerts,
  acknowledgeAlert,
  getHealthProfile,
  getPendingScreenings,
  syncPendingScreenings,
  type SickBayVisit,
  type Referral,
  type SentinelAlert,
  type Vaccination,
  type HealthProfile,
  type CreateSickBayVisitPayload,
  type CreateReferralPayload,
  type CreateVaccinationPayload,
} from './api';
import { VaccinationsDialog } from './VaccinationsDialog';
import { HealthProfileForm } from './HealthProfileForm';
import { BatchScreeningsDialog } from './BatchScreeningsDialog';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { useTabState } from '@/shared/hooks/useTabState';
import { DataErrorAlert } from '@/shared/components/DataErrorAlert';

const OUTCOMES = ['returned_to_class', 'sent_home', 'referred', 'hospitalized'];
const PRIORITIES = ['urgent', 'normal', 'follow_up'];
const REFERRAL_STATUSES = ['pending', 'sent', 'acknowledged', 'attended', 'completed'];
const SYMPTOMS = [
  'fever',
  'cough',
  'runny_nose',
  'headache',
  'vomiting',
  'diarrhea',
  'rash',
  'sore_throat',
  'fatigue',
  'abdominal_pain',
  'difficulty_breathing',
  'body_ache',
  'conjunctivitis',
  'other',
];

const fmtDate = (d: string) => new Date(d).toLocaleDateString();

export function HealthPage() {
  const [tab, setTab] = useTabState('tab');
  const queryClient = useQueryClient();
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [pendingCount, setPendingCount] = useState(0);
  const [vaccStudentId, setVaccStudentId] = useState('');
  const [profileStudentId, setProfileStudentId] = useState('');

  useEffect(() => {
    const handleOnline = async () => {
      setIsOffline(false);
      // Let the auto-sync listener in api.ts handle it, then refresh queries
      setTimeout(async () => {
        const pending = await getPendingScreenings();
        setPendingCount(pending.length);
        queryClient.invalidateQueries({ queryKey: ['screenings'] });
      }, 1000);
    };
    const handleOffline = () => setIsOffline(true);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial check
    getPendingScreenings().then((pending) => setPendingCount(pending.length));

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [queryClient]);

  // Sick Bay state
  const [visitDialogOpen, setVisitDialogOpen] = useState(false);
  const [visitForm, setVisitForm] = useState<Partial<CreateSickBayVisitPayload>>({
    presenting_complaint_codes: [],
    outcome: 'returned_to_class',
  });

  // Referral state
  const [referralDialogOpen, setReferralDialogOpen] = useState(false);
  const [referralForm, setReferralForm] = useState<Partial<CreateReferralPayload>>({
    priority: 'normal',
  });

  // Vaccination state
  const [vaccDialogOpen, setVaccDialogOpen] = useState(false);
  const [vaccForm, setVaccForm] = useState<Partial<CreateVaccinationPayload>>({ dose_number: 1 });

  // Profiles state
  const [profileDialogOpen, setProfileDialogOpen] = useState(false);

  // Screenings state
  const [batchScreeningDialogOpen, setBatchScreeningDialogOpen] = useState(false);

  // Queries
  const {
    data: visitsData,
    isLoading: visitsLoading,
    isError: visitsError,
    refetch: refetchVisits,
  } = useQuery({
    queryKey: ['sickBayVisits'],
    queryFn: () => getSickBayVisits(),
  });
  const {
    data: referrals,
    isLoading: referralsLoading,
    isError: referralsError,
    refetch: refetchReferrals,
  } = useQuery({
    queryKey: ['referrals'],
    queryFn: () => getReferrals(),
  });
  const {
    data: alerts,
    isLoading: alertsLoading,
    isError: alertsError,
    refetch: refetchAlerts,
  } = useQuery({
    queryKey: ['sentinelAlerts'],
    queryFn: () => getSentinelAlerts({ status: 'active' }),
  });
  const {
    data: vaccinations,
    isLoading: vaccinationsLoading,
    isError: vaccinationsError,
    refetch: refetchVaccinations,
  } = useQuery({
    queryKey: ['vaccinations', vaccStudentId],
    queryFn: () => getVaccinations(vaccStudentId),
    enabled: !!vaccStudentId,
  });
  const {
    data: profile,
    isLoading: profileLoading,
    isError: profileError,
    refetch: refetchProfile,
  } = useQuery({
    queryKey: ['healthProfile', profileStudentId],
    queryFn: () => getHealthProfile(profileStudentId),
    enabled: !!profileStudentId,
  });

  // Mutations
  const createVisit = useMutation({
    mutationFn: createSickBayVisit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sickBayVisits'] });
      setVisitDialogOpen(false);
      setVisitForm({ presenting_complaint_codes: [], outcome: 'returned_to_class' });
    },
  });
  const createRef = useMutation({
    mutationFn: createReferral,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['referrals'] });
      setReferralDialogOpen(false);
      setReferralForm({ priority: 'normal' });
    },
  });
  const updateRef = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: { status: string } }) =>
      updateReferral(id, payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['referrals'] }),
  });
  const createVacc = useMutation({
    mutationFn: createVaccination,
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['vaccinations', variables.student_id] });
      setVaccDialogOpen(false);
      setVaccForm({ dose_number: 1 });
    },
  });
  const ackAlert = useMutation({
    mutationFn: acknowledgeAlert,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['sentinelAlerts'] }),
  });

  const visitColumns: GridColDef<SickBayVisit>[] = [
    { field: 'student_id', headerName: 'Student ID', width: 220 },
    { field: 'visit_date', headerName: 'Date', width: 120, valueGetter: (v: string) => fmtDate(v) },
    {
      field: 'presenting_complaint_codes',
      headerName: 'Complaints',
      width: 200,
      valueGetter: (v: string[]) => v?.join(', '),
    },
    { field: 'temperature', headerName: 'Temp (°C)', width: 100 },
    { field: 'outcome', headerName: 'Outcome', width: 140 },
    {
      field: 'is_sentinel_relevant',
      headerName: 'Sentinel',
      width: 100,
      renderCell: (p) =>
        p.value ? (
          <Chip label="Alert" color="error" size="small" />
        ) : (
          <Chip label="Normal" size="small" />
        ),
    },
  ];

  const referralColumns: GridColDef<Referral>[] = [
    { field: 'student_id', headerName: 'Student ID', width: 220 },
    { field: 'destination_facility', headerName: 'Facility', width: 200 },
    {
      field: 'priority',
      headerName: 'Priority',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value}
          color={p.value === 'urgent' ? 'error' : p.value === 'follow_up' ? 'warning' : 'default'}
          size="small"
        />
      ),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => <Chip label={p.value} size="small" />,
    },
    {
      field: 'follow_up_due_date',
      headerName: 'Follow-up',
      width: 130,
      valueGetter: (v: string) => fmtDate(v),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) => (
        <FormControl size="small" sx={{ minWidth: 100 }}>
          <Select
            value={p.row.status}
            onChange={(e) =>
              updateRef.mutate({ id: p.row.id, payload: { status: e.target.value } })
            }
          >
            {REFERRAL_STATUSES.map((s) => (
              <MenuItem key={s} value={s}>
                {s}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      ),
    },
  ];

  const alertColumns: GridColDef<SentinelAlert>[] = [
    {
      field: 'alert_tier',
      headerName: 'Tier',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value}
          color={p.value === 'state' ? 'error' : p.value === 'lga' ? 'warning' : 'info'}
          size="small"
        />
      ),
    },
    { field: 'students_affected', headerName: 'Affected', width: 100 },
    {
      field: 'symptom_profile',
      headerName: 'Symptoms',
      width: 250,
      valueGetter: (v: Record<string, number>) =>
        Object.entries(v ?? {})
          .map(([k, v]) => `${k}: ${v}`)
          .join(', '),
    },
    {
      field: 'date_generated',
      headerName: 'Date',
      width: 130,
      valueGetter: (v: string) => fmtDate(v),
    },
    { field: 'status', headerName: 'Status', width: 120 },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) =>
        p.row.status === 'active' && (
          <Button size="small" onClick={() => ackAlert.mutate(p.row.id)}>
            Acknowledge
          </Button>
        ),
    },
  ];

  const vaccColumns: GridColDef<Vaccination>[] = [
    { field: 'vaccine_name', headerName: 'Vaccine', width: 200 },
    {
      field: 'administration_date',
      headerName: 'Administration Date',
      width: 160,
      valueGetter: (v: string) => fmtDate(v),
    },
    { field: 'dose_number', headerName: 'Dose', width: 100 },
    { field: 'administering_facility', headerName: 'Facility', width: 220 },
    { field: 'lot_number', headerName: 'Lot Number', width: 140 },
    { field: 'vaccine_code', headerName: 'Vaccine Code', width: 140 },
  ];

  const profileColumns: GridColDef<HealthProfile>[] = [
    { field: 'student_id', headerName: 'Student ID', width: 220 },
    { field: 'blood_group', headerName: 'Blood Group', width: 120 },
    { field: 'genotype', headerName: 'Genotype', width: 100 },
    {
      field: 'allergies',
      headerName: 'Allergies',
      width: 200,
      valueGetter: (v: string[]) => v?.join(', ') || 'None',
    },
    {
      field: 'chronic_conditions',
      headerName: 'Conditions',
      width: 200,
      valueGetter: (v: string[]) => v?.join(', ') || 'None',
    },
    {
      field: 'current_medications',
      headerName: 'Medications',
      width: 220,
      valueGetter: (v: string[]) => v?.join(', ') || 'None',
    },
    { field: 'parental_consent_given', headerName: 'Consent', width: 100 },
  ];

  return (
    <>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Health & Sentinel
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {isOffline && (
            <Chip icon={<OfflineIcon />} label="Offline Mode" color="warning" variant="outlined" />
          )}
          {pendingCount > 0 && (
            <Chip
              icon={<SyncIcon />}
              label={`${pendingCount} Pending Sync`}
              color="info"
              onClick={async () => {
                await syncPendingScreenings();
                const pending = await getPendingScreenings();
                setPendingCount(pending.length);
                queryClient.invalidateQueries({ queryKey: ['screenings'] });
              }}
            />
          )}
        </Box>
      </Box>

      {alerts?.items && alerts.items.length > 0 && (
        <Card sx={{ mb: 3, bgcolor: 'warning.light', color: 'warning.contrastText' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Warning />
              <Typography variant="h6">
                {alerts.items.length} Active Sentinel Alert{alerts.items.length > 1 ? 's' : ''}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}

      <Paper sx={{ mb: 2 }}>
          <Tabs
            value={tab}
            onChange={(_, v) => setTab(v)}
            variant="scrollable"
            scrollButtons="auto"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
          <Tab label="Sick Bay" />
          <Tab label="Referrals" />
          <Tab label="Vaccinations" />
          <Tab label="Health Profiles" />
          <Tab label="Screenings" />
          <Tab label="Sentinel Alerts" />
        </Tabs>
      </Paper>

      {tab === 0 && (
        <>
          {visitsError && <DataErrorAlert onRetry={() => refetchVisits()} />}
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
                onClick={() => setVisitDialogOpen(true)}
              >
                Log Sick Bay Visit
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
              rows={visitsData?.items ?? []}
              columns={visitColumns}
              loading={visitsLoading}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No sick bay visits found" message="There are no sick bay visits to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {tab === 1 && (
        <>
          {referralsError && <DataErrorAlert onRetry={() => refetchReferrals()} />}
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
                onClick={() => setReferralDialogOpen(true)}
              >
                Create Referral
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
              rows={referrals ?? []}
              columns={referralColumns}
              loading={referralsLoading}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No referrals found" message="There are no referrals to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {tab === 2 && (
        <>
          {vaccinationsError && <DataErrorAlert onRetry={() => refetchVaccinations()} />}
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
              <TextField
                label="Student ID"
                value={vaccStudentId}
                onChange={(e) => setVaccStudentId(e.target.value)}
                size="small"
                sx={{ width: 360 }}
              />
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
                  setVaccForm((f) => ({ ...f, student_id: f.student_id || vaccStudentId }));
                  setVaccDialogOpen(true);
                }}
              >
                Add Vaccination Record
              </Button>
            </Toolbar>
          </Paper>
          {vaccStudentId ? (
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
                rows={vaccinations ?? []}
                columns={vaccColumns}
                loading={vaccinationsLoading}
                getRowId={(r) => r.id}
                initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
                pageSizeOptions={[10, 25, 50]}
                slots={{ noRowsOverlay: () => <DataEmptyState title="No vaccination records found" message="There are no vaccination records to display at this time." /> }}
              />
            </Paper>
          ) : (
            <Typography color="text.secondary">Enter a student ID to view vaccination records.</Typography>
          )}
        </>
      )}

      {tab === 3 && (
        <>
          {profileError && <DataErrorAlert onRetry={() => refetchProfile()} />}
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
              <TextField
                label="Student ID"
                value={profileStudentId}
                onChange={(e) => setProfileStudentId(e.target.value)}
                size="small"
                sx={{ width: 360 }}
              />
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
                onClick={() => setProfileDialogOpen(true)}
              >
                Add Health Profile
              </Button>
            </Toolbar>
          </Paper>
          {!profileStudentId ? (
            <Typography color="text.secondary">Enter a student ID to view a health profile.</Typography>
          ) : profileLoading ? (
            <Typography color="text.secondary">Loading health profile…</Typography>
          ) : profile ? (
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
                rows={[profile]}
                columns={profileColumns}
                loading={profileLoading}
                getRowId={(r) => r.id}
                initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
                pageSizeOptions={[10, 25, 50]}
                slots={{ noRowsOverlay: () => <DataEmptyState title="No health profile found" message="There is no health profile to display at this time." /> }}
              />
            </Paper>
          ) : (
            <Typography color="text.secondary">No health profile found for this student.</Typography>
          )}
        </>
      )}

      {tab === 4 && (
        <>
          <Typography color="text.secondary" sx={{ mb: 2 }}>
            Backend currently supports recording screenings (single and bulk) but does not provide a list endpoint.
          </Typography>
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
                onClick={() => setBatchScreeningDialogOpen(true)}
              >
                Log Screening (Batch Mode)
              </Button>
            </Toolbar>
          </Paper>
          {pendingCount > 0 && (
            <Typography color="text.secondary">
              {pendingCount} screening record{pendingCount > 1 ? 's' : ''} pending sync.
            </Typography>
          )}
        </>
      )}

      {tab === 5 && (
        <>
          {alertsError && <DataErrorAlert onRetry={() => refetchAlerts()} />}
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
              rows={alerts?.items ?? []}
              columns={alertColumns}
              loading={alertsLoading}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No active alerts found" message="There are no sentinel alerts to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {/* Sick Bay Visit Dialog */}
      <Dialog
        open={visitDialogOpen}
        onClose={() => setVisitDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Log Sick Bay Visit</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={visitForm.student_id ?? ''}
            onChange={(e) => setVisitForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <Autocomplete
            multiple
            options={SYMPTOMS}
            value={visitForm.presenting_complaint_codes ?? []}
            onChange={(_, v) => setVisitForm((f) => ({ ...f, presenting_complaint_codes: v }))}
            renderInput={(params) => <TextField {...params} label="Symptoms" />}
            fullWidth
          />
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              label="Temperature (°C)"
              type="number"
              value={visitForm.temperature ?? ''}
              onChange={(e) =>
                setVisitForm((f) => ({
                  ...f,
                  temperature: e.target.value ? +e.target.value : undefined,
                }))
              }
              fullWidth
            />
            <TextField
              label="Pulse Rate"
              type="number"
              value={visitForm.pulse_rate ?? ''}
              onChange={(e) =>
                setVisitForm((f) => ({
                  ...f,
                  pulse_rate: e.target.value ? +e.target.value : undefined,
                }))
              }
              fullWidth
            />
          </Box>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              label="BP Systolic"
              type="number"
              value={visitForm.blood_pressure_systolic ?? ''}
              onChange={(e) =>
                setVisitForm((f) => ({
                  ...f,
                  blood_pressure_systolic: e.target.value ? +e.target.value : undefined,
                }))
              }
              fullWidth
            />
            <TextField
              label="BP Diastolic"
              type="number"
              value={visitForm.blood_pressure_diastolic ?? ''}
              onChange={(e) =>
                setVisitForm((f) => ({
                  ...f,
                  blood_pressure_diastolic: e.target.value ? +e.target.value : undefined,
                }))
              }
              fullWidth
            />
          </Box>
          <TextField
            label="Complaint Notes"
            value={visitForm.presenting_complaint_notes ?? ''}
            onChange={(e) =>
              setVisitForm((f) => ({ ...f, presenting_complaint_notes: e.target.value }))
            }
            fullWidth
            multiline
            rows={2}
          />
          <TextField
            label="Treatment Given"
            value={visitForm.treatment_given ?? ''}
            onChange={(e) => setVisitForm((f) => ({ ...f, treatment_given: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <FormControl fullWidth>
            <InputLabel>Outcome</InputLabel>
            <Select
              value={visitForm.outcome ?? 'returned_to_class'}
              label="Outcome"
              onChange={(e) => setVisitForm((f) => ({ ...f, outcome: e.target.value }))}
            >
              {OUTCOMES.map((o) => (
                <MenuItem key={o} value={o}>
                  {o.replace(/_/g, ' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setVisitDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => createVisit.mutate(visitForm as CreateSickBayVisitPayload)}
            variant="contained"
            disabled={createVisit.isPending}
          >
            Log Visit
          </Button>
        </DialogActions>
      </Dialog>

      {/* Referral Dialog */}
      <Dialog
        open={referralDialogOpen}
        onClose={() => setReferralDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create Referral</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={referralForm.student_id ?? ''}
            onChange={(e) => setReferralForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Destination Facility"
            value={referralForm.destination_facility ?? ''}
            onChange={(e) =>
              setReferralForm((f) => ({ ...f, destination_facility: e.target.value }))
            }
            fullWidth
          />
          <TextField
            label="Reason"
            value={referralForm.reason ?? ''}
            onChange={(e) => setReferralForm((f) => ({ ...f, reason: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
          <FormControl fullWidth>
            <InputLabel>Priority</InputLabel>
            <Select
              value={referralForm.priority ?? 'medium'}
              label="Priority"
              onChange={(e) => setReferralForm((f) => ({ ...f, priority: e.target.value }))}
            >
              {PRIORITIES.map((p) => (
                <MenuItem key={p} value={p}>
                  {p}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            label="Follow-up Due Date"
            type="date"
            value={referralForm.follow_up_due_date ?? ''}
            onChange={(e) => setReferralForm((f) => ({ ...f, follow_up_due_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReferralDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => createRef.mutate(referralForm as CreateReferralPayload)}
            variant="contained"
            disabled={createRef.isPending}
          >
            Create Referral
          </Button>
        </DialogActions>
      </Dialog>

      <VaccinationsDialog
        open={vaccDialogOpen}
        onClose={() => setVaccDialogOpen(false)}
        vaccForm={vaccForm}
        setVaccForm={setVaccForm}
        onSubmit={() => createVacc.mutate(vaccForm as CreateVaccinationPayload)}
        isPending={createVacc.isPending}
      />

      <HealthProfileForm open={profileDialogOpen} onClose={() => setProfileDialogOpen(false)} />

      <BatchScreeningsDialog
        open={batchScreeningDialogOpen}
        onClose={async () => {
          setBatchScreeningDialogOpen(false);
          const pending = await getPendingScreenings();
          setPendingCount(pending.length);
        }}
      />
    </>
  );
}
