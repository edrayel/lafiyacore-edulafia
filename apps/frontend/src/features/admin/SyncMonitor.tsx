import { Box, Typography, Paper, Card, CardContent } from '@mui/material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';
import { Grid } from '@mui/material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery } from '@tanstack/react-query';
import { getSyncDashboard, getSyncHistory } from './api';

export function SyncMonitor() {
  const { data: dashboard, isLoading: dashLoading } = useQuery({
    queryKey: ['admin-sync-dashboard'],
    queryFn: getSyncDashboard,
  });

  const { data: history, isLoading: histLoading } = useQuery({
    queryKey: ['admin-sync-history'],
    queryFn: getSyncHistory,
  });

  const columns: GridColDef[] = [
    { field: 'school_id', headerName: 'School ID', width: 250 },
    { field: 'device_id', headerName: 'Device ID', width: 150 },
    { field: 'sync_type', headerName: 'Sync Type', width: 120 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'records_synced', headerName: 'Records', width: 120 },
    {
      field: 'started_at',
      headerName: 'Start Time',
      width: 180,
      valueGetter: (v: string) => (v ? new Date(v).toLocaleString() : ''),
    },
  ];

  if (dashLoading) return <SkeletonPage rows={5} cardCount={4} />;

  return (
    <PageTransition isLoading={dashLoading}>
      <Box sx={{ p: 2 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        Sync Monitoring Dashboard
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Active Syncs
              </Typography>
              <Typography variant="h4">{dashboard?.active_syncs || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Pending Data (MB)
              </Typography>
              <Typography variant="h4">{dashboard?.pending_megabytes || 0}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Failed Syncs (24h)
              </Typography>
              <Typography variant="h4" color="error">
                {dashboard?.failed_syncs_24h || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Last Global Sync
              </Typography>
              <Typography variant="h5">Recently</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h6" sx={{ mb: 2 }}>
        Detailed Sync Logs
      </Typography>
      <Paper
        sx={{
          height: 400,
          width: '100%',
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 2,
        }}
      >
        <DataGrid
          rows={history?.items || []}
          columns={columns}
          loading={histLoading}
          disableRowSelectionOnClick
        />
      </Paper>
    </Box>
    </PageTransition>
  );
}
