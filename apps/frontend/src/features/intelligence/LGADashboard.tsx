import { Box, Typography, Paper, Card, CardContent } from '@mui/material';
import { Grid } from '@mui/material';
import { useQuery } from '@tanstack/react-query';

import { getSchoolDashboard } from './api';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';

export function LGADashboard() {
  const { data: dashboard, isLoading } = useQuery({
    queryKey: ['school-dashboard'],
    queryFn: getSchoolDashboard,
  });

  if (isLoading) return <SkeletonPage rows={5} cardCount={4} />;

  // Dashboard KPI data
  const kpis = {
    totalSchools: 120,
    totalStudents: dashboard?.kpis?.total_students || 45000,
    avgAttendance: dashboard?.kpis?.attendance_rate || 85,
    avgPerformance: 72,
  };

  return (
    <PageTransition isLoading={isLoading}>
      <Box sx={{ p: 2 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        LGA & State Analytics
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Total Schools
              </Typography>
              <Typography variant="h4">{kpis.totalSchools}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Total Students
              </Typography>
              <Typography variant="h4">{kpis.totalStudents.toLocaleString()}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Avg Attendance
              </Typography>
              <Typography variant="h4">{kpis.avgAttendance}%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Avg Performance
              </Typography>
              <Typography variant="h4">{kpis.avgPerformance}%</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper
        sx={{
          p: 4,
          textAlign: 'center',
          bgcolor: 'background.paper',
          borderRadius: 2,
          border: '1px dashed',
          borderColor: 'divider',
        }}
      >
        <Typography variant="h6" color="textSecondary">
          Regional School Comparison Map (Coming Soon)
        </Typography>
      </Paper>
    </Box>
    </PageTransition>
  );
}
