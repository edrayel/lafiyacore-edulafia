import { useState } from 'react';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Tabs,
  Tab,
  Paper,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  TrendingUp,
  School,
  People,
  EventNote,
  AttachMoney,
  Warning,
  Verified as VerifiedIcon,
  Add as AddIcon,
  Download,
  AutoAwesome,
  Sync as SyncIcon,
  Storage as DataIcon,
} from '@mui/icons-material';
import ErrorIcon from '@mui/icons-material/Error';

import type { ReportGenerationPayload, DataPortalRequestPayload } from './api';
import {
  getIllnessHeatmap,
  syncEMISData,
  requestAnonymisedData,
  getSchoolDashboard,
  getSentinelDashboard,
  getReports,
  generateReport,
} from './api';
import { LGADashboard } from './LGADashboard';
import { VerificationPage } from './VerificationPage';
import { useToastStore } from '@/shared/stores/toastStore';

const severityConfig: Record<
  string,
  { color: 'success' | 'info' | 'warning' | 'error'; icon: typeof Warning }
> = {
  low: { color: 'info', icon: Warning },
  medium: { color: 'warning', icon: Warning },
  high: { color: 'error', icon: ErrorIcon },
  critical: { color: 'error', icon: ErrorIcon },
};

const reportStatusConfig: Record<string, 'default' | 'warning' | 'success' | 'error'> = {
  pending: 'default',
  generating: 'warning',
  completed: 'success',
  failed: 'error',
};

export function IntelligencePage() {
  const [tab, setTab] = useState(0);
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [reportForm, setReportForm] = useState<ReportGenerationPayload>({
    type: '',
    title: '',
  });

  const [dataPortalOpen, setDataPortalOpen] = useState(false);
  const [dataPortalForm, setDataPortalForm] = useState<Partial<DataPortalRequestPayload>>({
    dataset_type: 'health_sentinel',
    purpose: 'research',
  });

  const queryClient = useQueryClient();

  const { data: heatmapData, isLoading: heatmapLoading } = useQuery({
    queryKey: ['illness-heatmap'],
    queryFn: getIllnessHeatmap,
  });

  const syncMutation = useMutation({
    mutationFn: syncEMISData,
    onSuccess: () => {
      useToastStore.getState().addToast('EMIS sync initiated successfully.', 'success');
    },
  });

  const dataPortalMutation = useMutation({
    mutationFn: requestAnonymisedData,
    onSuccess: () => {
      useToastStore.getState().addToast('Anonymised data request submitted successfully.', 'success');
      setDataPortalOpen(false);
    },
  });

  const { data: dashboard, isLoading: dashboardLoading } = useQuery({
    queryKey: ['intelligence-dashboard'],
    queryFn: getSchoolDashboard,
  });

  const { data: sentinel, isLoading: sentinelLoading } = useQuery({
    queryKey: ['sentinel-dashboard'],
    queryFn: getSentinelDashboard,
  });

  const { data: reports, isLoading: reportsLoading } = useQuery({
    queryKey: ['intelligence-reports'],
    queryFn: getReports,
  });

  const generateMutation = useMutation({
    mutationFn: (payload: ReportGenerationPayload) => generateReport(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['intelligence-reports'] });
      setReportDialogOpen(false);
      setReportForm({ type: '', title: '' });
    },
  });

  const handleGenerateReport = () => {
    if (reportForm.type && reportForm.title) {
      generateMutation.mutate(reportForm);
    }
  };

  return (
    <>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box sx={{ mb: 4 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
          >
            Intelligence
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<DataIcon />}
            onClick={() => setDataPortalOpen(true)}
          >
            Data Portal Request
          </Button>
          <Button
            variant="outlined"
            color="info"
            startIcon={<SyncIcon />}
            onClick={() => syncMutation.mutate('attendance')}
            disabled={syncMutation.isPending}
          >
            {syncMutation.isPending ? 'Syncing...' : 'Sync EMIS'}
          </Button>
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
            onClick={() => setReportDialogOpen(true)}
          >
            Generate Report
          </Button>
        </Box>
      </Box>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab icon={<TrendingUp />} label="Dashboard" iconPosition="start" />
        <Tab icon={<TrendingUp />} label="LGA / State" iconPosition="start" />
        <Tab
          icon={
            sentinel?.summary.critical ? (
              <Chip label={sentinel.summary.critical} color="error" size="small" />
            ) : (
              <Warning />
            )
          }
          label="Alerts"
          iconPosition="start"
        />
        <Tab icon={<AutoAwesome />} label="Reports" iconPosition="start" />
        <Tab icon={<VerifiedIcon />} label="Verify Cert" iconPosition="start" />
      </Tabs>

      {tab === 0 && (
        <>
          {dashboardLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : dashboard ? (
            <>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 6, sm: 4, md: 2 }}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <School color="primary" />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          Students
                        </Typography>
                        <Typography variant="h6">{dashboard.kpis.total_students}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 4, md: 2 }}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <People color="primary" />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          Staff
                        </Typography>
                        <Typography variant="h6">{dashboard.kpis.total_staff}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 4, md: 2 }}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <EventNote color="success" />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          Attendance
                        </Typography>
                        <Typography variant="h6">{dashboard.kpis.attendance_rate}%</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 4, md: 3 }}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <AttachMoney color="success" />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          Revenue
                        </Typography>
                        <Typography variant="h6">
                          ₦{dashboard.kpis.revenue_collected.toLocaleString()}
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 4, md: 3 }}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <TrendingUp color="info" />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          Avg Score
                        </Typography>
                        <Typography variant="h6">{dashboard.kpis.average_score}%</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              {dashboard.trends.length > 0 && (
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Trends
                  </Typography>
                  <Box sx={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                      <thead>
                        <tr>
                          <th style={{ textAlign: 'left', padding: 8 }}>Period</th>
                          <th style={{ textAlign: 'right', padding: 8 }}>Students</th>
                          <th style={{ textAlign: 'right', padding: 8 }}>Attendance</th>
                          <th style={{ textAlign: 'right', padding: 8 }}>Revenue</th>
                        </tr>
                      </thead>
                      <tbody>
                        {dashboard.trends.map((t) => (
                          <tr key={t.period}>
                            <td style={{ padding: 8 }}>{t.period}</td>
                            <td style={{ textAlign: 'right', padding: 8 }}>{t.students}</td>
                            <td style={{ textAlign: 'right', padding: 8 }}>{t.attendance}%</td>
                            <td style={{ textAlign: 'right', padding: 8 }}>
                              ₦{t.revenue.toLocaleString()}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </Box>
                </Paper>
              )}
            </>
          ) : null}
        </>
      )}

      {tab === 1 && <LGADashboard />}

      {tab === 2 && (
        <>
          {sentinelLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : sentinel ? (
            <>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 6, sm: 3 }}>
                  <Card sx={{ bgcolor: 'error.light' }}>
                    <CardContent>
                      <Typography variant="caption">Critical</Typography>
                      <Typography variant="h4">{sentinel.summary.critical}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 3 }}>
                  <Card sx={{ bgcolor: 'error.main', color: 'white' }}>
                    <CardContent>
                      <Typography variant="caption">High</Typography>
                      <Typography variant="h4">{sentinel.summary.high}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 3 }}>
                  <Card sx={{ bgcolor: 'warning.light' }}>
                    <CardContent>
                      <Typography variant="caption">Medium</Typography>
                      <Typography variant="h4">{sentinel.summary.medium}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 6, sm: 3 }}>
                  <Card sx={{ bgcolor: 'info.light' }}>
                    <CardContent>
                      <Typography variant="caption">Low</Typography>
                      <Typography variant="h4">{sentinel.summary.low}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>

              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Paper sx={{ p: 2, height: '100%' }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>
                      Illness Hotspots
                    </Typography>
                    {heatmapLoading ? (
                      <CircularProgress />
                    ) : heatmapData && heatmapData.length > 0 ? (
                      <List>
                        {heatmapData.map((spot, i) => (
                          <ListItem key={i} divider>
                            <Box
                              sx={{ display: 'flex', width: '100%', alignItems: 'center', gap: 2 }}
                            >
                              <Box
                                sx={{
                                  width: 24,
                                  height: 24,
                                  borderRadius: '50%',
                                  bgcolor: `rgba(211, 47, 47, ${spot.intensity})`,
                                  flexShrink: 0,
                                }}
                              />
                              <ListItemText
                                primary={spot.pattern}
                                secondary={`Lat: ${spot.lat}, Lng: ${spot.lng} (Intensity: ${spot.intensity * 100}%)`}
                              />
                            </Box>
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography color="textSecondary">No hotspots detected</Typography>
                    )}
                  </Paper>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Paper sx={{ p: 2, height: '100%' }}>
                    <Typography variant="h6" sx={{ mb: 2 }}>
                      Active Alerts
                    </Typography>
                    <List>
                      {sentinel.alerts.length === 0 ? (
                        <Typography color="textSecondary" sx={{ p: 4, textAlign: 'center' }}>
                          No alerts
                        </Typography>
                      ) : (
                        sentinel.alerts.map((alert) => {
                          const config = severityConfig[alert.severity] || severityConfig.low;
                          const Icon = config.icon;
                          return (
                            <ListItem
                              key={alert.id}
                              divider
                              sx={{
                                bgcolor: alert.resolved ? 'transparent' : 'action.hover',
                              }}
                            >
                              <Box
                                sx={{
                                  display: 'flex',
                                  gap: 2,
                                  width: '100%',
                                  alignItems: 'flex-start',
                                }}
                              >
                                <Icon color={config.color} />
                                <ListItemText
                                  primary={
                                    <Box
                                      sx={{
                                        display: 'flex',
                                        gap: 1,
                                        alignItems: 'center',
                                      }}
                                    >
                                      {alert.title}
                                      <Chip
                                        label={alert.severity}
                                        color={config.color}
                                        size="small"
                                      />
                                      {alert.resolved && (
                                        <Chip label="Resolved" color="success" size="small" />
                                      )}
                                    </Box>
                                  }
                                  secondary={
                                    <>
                                      {alert.description}
                                      <br />
                                      <Typography
                                        component="span"
                                        variant="caption"
                                        color="textSecondary"
                                      >
                                        {new Date(alert.created_at).toLocaleString()}
                                      </Typography>
                                    </>
                                  }
                                />
                              </Box>
                            </ListItem>
                          );
                        })
                      )}
                    </List>
                  </Paper>
                </Grid>
              </Grid>
            </>
          ) : null}
        </>
      )}

      {tab === 3 && (
        <Paper>
          {reportsLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : reports && reports.length > 0 ? (
            <List>
              {reports.map((report) => (
                <ListItem key={report.id} divider>
                  <Box
                    sx={{
                      display: 'flex',
                      gap: 2,
                      width: '100%',
                      alignItems: 'center',
                    }}
                  >
                    <ListItemText
                      primary={report.title}
                      secondary={`${report.type} • ${new Date(report.created_at).toLocaleDateString()}`}
                    />
                    <Chip
                      label={report.status}
                      color={reportStatusConfig[report.status]}
                      size="small"
                    />
                    {report.status === 'completed' && report.download_url && (
                      <Button size="small" startIcon={<Download />} href={report.download_url}>
                        Download
                      </Button>
                    )}
                  </Box>
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography color="textSecondary" sx={{ p: 4, textAlign: 'center' }}>
              No reports generated yet
            </Typography>
          )}
        </Paper>
      )}

      {tab === 4 && <VerificationPage />}

      <Dialog
        open={reportDialogOpen}
        onClose={() => setReportDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Generate Report</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Report Title"
            value={reportForm.title}
            onChange={(e) => setReportForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Report Type</InputLabel>
            <Select
              value={reportForm.type}
              label="Report Type"
              onChange={(e) => setReportForm((f) => ({ ...f, type: e.target.value }))}
            >
              <MenuItem value="attendance">Attendance Report</MenuItem>
              <MenuItem value="finance">Finance Report</MenuItem>
              <MenuItem value="academic">Academic Report</MenuItem>
              <MenuItem value="enrollment">Enrollment Report</MenuItem>
              <MenuItem value="sentinel">Sentinel Summary</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReportDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleGenerateReport}
            variant="contained"
            disabled={generateMutation.isPending || !reportForm.type || !reportForm.title}
          >
            {generateMutation.isPending ? <CircularProgress size={24} /> : 'Generate'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={dataPortalOpen}
        onClose={() => setDataPortalOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Anonymised Data Portal Request</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Request anonymised datasets for donor reporting or epidemiological research. Data will
            have all PII stripped.
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Dataset Type</InputLabel>
            <Select
              value={dataPortalForm.dataset_type ?? 'health_sentinel'}
              label="Dataset Type"
              onChange={(e) => setDataPortalForm((f) => ({ ...f, dataset_type: e.target.value }))}
            >
              <MenuItem value="health_sentinel">Health & Sentinel</MenuItem>
              <MenuItem value="attendance_patterns">Attendance Patterns</MenuItem>
              <MenuItem value="academic_trends">Academic Trends</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Purpose</InputLabel>
            <Select
              value={dataPortalForm.purpose ?? 'research'}
              label="Purpose"
              onChange={(e) => setDataPortalForm((f) => ({ ...f, purpose: e.target.value }))}
            >
              <MenuItem value="research">Epidemiological Research</MenuItem>
              <MenuItem value="donor_reporting">Donor Reporting</MenuItem>
              <MenuItem value="policy_planning">Policy Planning</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              label="Start Date"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              onChange={(e) =>
                setDataPortalForm((f) => ({
                  ...f,
                  date_range: { ...f.date_range, start: e.target.value } as { start: string; end: string },
                }))
              }
            />
            <TextField
              label="End Date"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              onChange={(e) =>
                setDataPortalForm((f) => ({
                  ...f,
                  date_range: { ...f.date_range, end: e.target.value } as { start: string; end: string },
                }))
              }
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDataPortalOpen(false)}>Cancel</Button>
          <Button
            onClick={() => dataPortalMutation.mutate(dataPortalForm as DataPortalRequestPayload)}
            variant="contained"
            disabled={
              !dataPortalForm.dataset_type ||
              !dataPortalForm.purpose ||
              dataPortalMutation.isPending
            }
          >
            {dataPortalMutation.isPending ? 'Submitting...' : 'Submit Request'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
