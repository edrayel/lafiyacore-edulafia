import { Box, Typography, Paper, Card, CardContent } from '@mui/material';
import { Grid } from '@mui/material';

export function AnalyticsPage() {
  const stats = {
    totalRevenue: '₦ 1.2B',
    activeUsers: 14500,
    platformUptime: '99.98%',
    activeSchools: 120,
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
        Platform Analytics
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Total Revenue Processed
              </Typography>
              <Typography variant="h4">{stats.totalRevenue}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Active Users
              </Typography>
              <Typography variant="h4">{stats.activeUsers.toLocaleString()}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Platform Uptime
              </Typography>
              <Typography variant="h4" color="success.main">
                {stats.platformUptime}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" variant="subtitle2">
                Active Schools
              </Typography>
              <Typography variant="h4">{stats.activeSchools}</Typography>
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
          Detailed Analytics Charts Coming Soon
        </Typography>
      </Paper>
    </Box>
  );
}
