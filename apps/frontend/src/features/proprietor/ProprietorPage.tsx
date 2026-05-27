import { Box, Card, CardContent, Grid, Typography } from '@mui/material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';
import {
  School as SchoolIcon,
  AttachMoney as MoneyIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  People as PeopleIcon,
  Percent as PercentIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getProprietorDashboard } from './api';

function StatCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: string;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
            <Typography variant="h4" sx={{ mt: 1, fontWeight: 700 }}>
              {value}
            </Typography>
          </Box>
          <Box sx={{ color, fontSize: 40 }}>{icon}</Box>
        </Box>
      </CardContent>
    </Card>
  );
}

const fmt = (n: number) => `₦${n.toLocaleString()}`;

export function ProprietorPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['proprietorDashboard'],
    queryFn: getProprietorDashboard,
  });

  if (isLoading) return <SkeletonPage rows={5} cardCount={4} />;
  if (!data) return null;

  return (
    <PageTransition isLoading={isLoading}>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Proprietor Dashboard
        </Typography>
      </Box>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Total Students"
            value={data.total_students.toLocaleString()}
            icon={<SchoolIcon />}
            color="primary.main"
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Total Revenue"
            value={fmt(data.total_revenue)}
            icon={<MoneyIcon />}
            color="success.main"
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Attendance Rate"
            value={`${data.attendance_rate}%`}
            icon={<PercentIcon />}
            color="info.main"
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Active Alerts"
            value={data.active_alerts.toString()}
            icon={<WarningIcon />}
            color="error.main"
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Total Staff"
            value={data.total_staff.toLocaleString()}
            icon={<PeopleIcon />}
            color="secondary.main"
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <StatCard
            title="Collection Rate"
            value={`${data.collection_rate}%`}
            icon={<TrendingUpIcon />}
            color="warning.main"
          />
        </Grid>
      </Grid>
    </PageTransition>
  );
}
