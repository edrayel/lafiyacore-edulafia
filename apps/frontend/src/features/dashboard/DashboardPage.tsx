import {
  Typography,
  Grid,
  Card,
  CardContent,
  Alert,
  Box,
  Divider,
  Paper,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getSchoolDashboard } from './api';
import { useAuthStore } from '@/shared/stores/authStore';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { PageTransition } from '@/shared/components/PageTransition';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  School as SchoolIcon,
  People as PeopleIcon,
  Class as ClassIcon,
  NotificationsActive as AlertIcon,
} from '@mui/icons-material';

export function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const schoolId = user?.school_id || null;

  const {
    data: dashboardData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['schoolDashboard', schoolId],
    queryFn: () => (schoolId ? getSchoolDashboard(schoolId) : Promise.resolve(null)),
    enabled: !!schoolId,
  });

  if (isLoading) return <SkeletonPage rows={5} cardCount={4} />;

  if (error) {
    return (
      <Alert
        severity="error"
        sx={{ borderRadius: 2, boxShadow: '0 4px 12px rgba(220, 38, 38, 0.1)' }}
      >
        Failed to load dashboard data. Please try again later.
      </Alert>
    );
  }

  if (!dashboardData) {
    return (
      <Alert
        severity="info"
        sx={{ borderRadius: 2, boxShadow: '0 4px 12px rgba(59, 130, 246, 0.1)' }}
      >
        No school selected. Please select a school to view the dashboard.
      </Alert>
    );
  }

  const renderTrendIcon = (trend: string | null) => {
    if (trend === 'up') return <TrendingUp fontSize="small" sx={{ color: '#10b981', ml: 0.5 }} />;
    if (trend === 'down')
      return <TrendingDown fontSize="small" sx={{ color: '#ef4444', ml: 0.5 }} />;
    return <TrendingFlat fontSize="small" sx={{ color: '#94a3b8', ml: 0.5 }} />;
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'critical':
        return '#ef4444';
      case 'warning':
        return '#f59e0b';
      case 'normal':
        return '#10b981';
      default:
        return '#64748b';
    }
  };

  return (
    <PageTransition isLoading={isLoading}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      {/* Header Area */}
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          flexWrap: 'wrap',
          gap: 2,
        }}
      >
        <Box>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
          >
            School Overview
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', mt: 0.5 }}>
            Here is what's happening today at your institution.
          </Typography>
        </Box>
        <Typography
          variant="caption"
          sx={{
            color: 'text.primary',
            fontWeight: 500,
            bgcolor: 'background.paper',
            px: 2,
            py: 1,
            borderRadius: 2,
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          }}
        >
          Last Updated: {new Date(dashboardData.last_updated).toLocaleString()}
        </Typography>
      </Box>

      {/* Quick Stats Row */}
      <Grid container spacing={3}>
        {[
          {
            label: 'Total Students',
            value: dashboardData.quick_stats.total_students,
            icon: <SchoolIcon sx={{ color: '#3b82f6' }} />,
            bg: 'rgba(59, 130, 246, 0.1)',
          },
          {
            label: 'Total Teachers',
            value: dashboardData.quick_stats.total_teachers,
            icon: <PeopleIcon sx={{ color: '#8b5cf6' }} />,
            bg: 'rgba(139, 92, 246, 0.1)',
          },
          {
            label: 'Active Classes',
            value: dashboardData.quick_stats.total_classes,
            icon: <ClassIcon sx={{ color: '#10b981' }} />,
            bg: 'rgba(16, 185, 129, 0.1)',
          },
          {
            label: 'Active Alerts',
            value: dashboardData.quick_stats.active_alerts,
            icon: <AlertIcon sx={{ color: '#ef4444' }} />,
            bg: 'rgba(239, 68, 68, 0.1)',
          },
        ].map((stat, idx) => (
          <Grid size={{ xs: 12, sm: 6, md: 3 }} key={idx}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                border: '1px solid',
                borderColor: 'divider',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.02)',
              }}
            >
              <Box sx={{ p: 1.5, borderRadius: 2, bgcolor: stat.bg, display: 'flex' }}>
                {stat.icon}
              </Box>
              <Box>
                <Typography
                  variant="h5"
                  sx={{ fontWeight: 700, lineHeight: 1.2, color: 'text.primary' }}
                >
                  {stat.value.toLocaleString()}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 500 }}>
                  {stat.label}
                </Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Divider sx={{ my: 1 }} />

      {/* KPIs Section */}
      <Box>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2, color: 'text.primary' }}>
          Key Performance Indicators
        </Typography>
        {dashboardData.kpis.length === 0 ? (
          <Paper
            elevation={0}
            sx={{
              p: 4,
              textAlign: 'center',
              border: '1px dashed',
              borderColor: 'divider',
              bgcolor: 'transparent',
            }}
          >
            <Typography variant="body1" color="text.secondary">
              No KPIs recorded for this period.
            </Typography>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {dashboardData.kpis.map((kpi) => (
              <Grid size={{ xs: 12, sm: 6, lg: 4 }} key={kpi.code}>
                <Card
                  sx={{
                    boxShadow:
                      '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05)',
                    borderTop: `4px solid ${getStatusColor(kpi.status)}`,
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateY(-2px)' },
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Box
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'flex-start',
                        mb: 2,
                      }}
                    >
                      <Typography
                        variant="subtitle2"
                        sx={{
                          fontWeight: 600,
                          color: 'text.secondary',
                          textTransform: 'uppercase',
                          letterSpacing: '0.5px',
                        }}
                      >
                        {kpi.name}
                      </Typography>
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          bgcolor: 'background.default',
                          px: 1,
                          py: 0.5,
                          borderRadius: 1,
                        }}
                      >
                        <Typography
                          variant="caption"
                          sx={{
                            fontWeight: 600,
                            color: 'text.secondary',
                            textTransform: 'capitalize',
                          }}
                        >
                          {kpi.trend || 'stable'}
                        </Typography>
                        {renderTrendIcon(kpi.trend)}
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5 }}>
                      <Typography
                        variant="h3"
                        sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-1px' }}
                      >
                        {kpi.value.toLocaleString()}
                      </Typography>
                      <Typography
                        variant="subtitle1"
                        sx={{ fontWeight: 600, color: 'text.secondary' }}
                      >
                        {kpi.unit}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      {/* Alerts Section */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2, color: 'text.primary' }}>
          Active Sentinel Alerts
        </Typography>
        <Card sx={{ boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.02)' }}>
          <CardContent sx={{ p: 0 }}>
            {dashboardData.alerts.length === 0 ? (
              <Box sx={{ p: 4, textAlign: 'center' }}>
                <AlertIcon sx={{ fontSize: 40, color: '#e2e8f0', mb: 1 }} />
                <Typography variant="body1" color="text.secondary">
                  All clear. No active alerts at this time.
                </Typography>
              </Box>
            ) : (
              <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                {dashboardData.alerts.map((alert, index) => {
                  let bgCol = 'rgba(0,0,0,0.02)';

                  switch (alert.severity.toLowerCase()) {
                    case 'low':
                      bgCol = 'rgba(59, 130, 246, 0.05)';
                      break;
                    case 'medium':
                      bgCol = 'rgba(245, 158, 11, 0.05)';
                      break;
                    case 'high':
                    case 'critical':
                      bgCol = 'rgba(239, 68, 68, 0.05)';
                      break;
                    default:
                      bgCol = 'rgba(239, 68, 68, 0.05)';
                  }

                  return (
                    <Box key={alert.id}>
                      <Box
                        sx={{
                          p: 3,
                          bgcolor: bgCol,
                          display: 'flex',
                          gap: 2,
                          alignItems: 'flex-start',
                        }}
                      >
                        <AlertIcon sx={{ color: getStatusColor(alert.severity), mt: 0.5 }} />
                        <Box sx={{ flexGrow: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                            <Typography
                              variant="subtitle1"
                              sx={{ fontWeight: 700, color: 'text.primary' }}
                            >
                              {alert.title}
                            </Typography>
                            <Typography
                              variant="caption"
                              sx={{ color: 'text.primary', fontWeight: 500 }}
                            >
                              {new Date(alert.created_at).toLocaleDateString()}
                            </Typography>
                          </Box>
                          <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                            {alert.message}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Typography
                              variant="caption"
                              sx={{
                                px: 1,
                                py: 0.5,
                                bgcolor: 'rgba(128,128,128,0.1)',
                                color: 'text.primary',
                                borderRadius: 1,
                                fontWeight: 600,
                                textTransform: 'uppercase',
                              }}
                            >
                              {alert.alert_type.replace('_', ' ')}
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                      {index < dashboardData.alerts.length - 1 && <Divider />}
                    </Box>
                  );
                })}
              </Box>
            )}
          </CardContent>
        </Card>
      </Box>
    </Box>
    </PageTransition>
  );
}
