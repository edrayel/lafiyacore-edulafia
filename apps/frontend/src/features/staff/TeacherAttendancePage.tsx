import { useState, useCallback, useEffect } from 'react';
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  TextField,
  Toolbar,
  Typography,
  Grid,
  Card,
  CardContent,
  Alert,
} from '@mui/material';
import {
  CheckCircle as CheckInIcon,
  Cancel as CheckOutIcon,
  Search as SearchIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { format } from 'date-fns';
import { ListResponse } from '@/shared/types';
import {
  getStaffAttendance,
  checkIn,
  checkOut,
  type StaffAttendance,
  type CheckInPayload,
  type CheckOutPayload,
} from './api';
import type { StaffMember } from './api';

const statusColors: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  present: 'success',
  late: 'warning',
  absent: 'error',
  on_leave: 'default',
};

export function TeacherAttendancePage() {
  const queryClient = useQueryClient();
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [staffFilter, setStaffFilter] = useState<string>('');
  const [checkInDialogOpen, setCheckInDialogOpen] = useState(false);
  const [checkOutDialogOpen, setCheckOutDialogOpen] = useState(false);
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(null);

  const dateStr = selectedDate ? format(selectedDate, 'yyyy-MM-dd') : '';

  // Get current location
  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        (error) => console.error('Error getting location:', error)
      );
    }
  }, []);

  // Queries
  const { data: attendanceRecords, isLoading: attendanceLoading } = useQuery<
    ListResponse<StaffAttendance>
  >({
    queryKey: ['staff-attendance', staffFilter, dateStr],
    queryFn: () =>
      getStaffAttendance({
        staff_id: staffFilter || undefined,
        date: dateStr || undefined,
      }),
    enabled: !!dateStr,
  });

  // Mutations
  const checkInMutation = useMutation({
    mutationFn: (payload: CheckInPayload) => checkIn(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff-attendance'] });
      setCheckInDialogOpen(false);
    },
  });

  const checkOutMutation = useMutation({
    mutationFn: (payload: CheckOutPayload) => checkOut(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff-attendance'] });
      setCheckOutDialogOpen(false);
    },
  });

  // Handlers
  const handleCheckIn = useCallback(() => {
    const payload: CheckInPayload = location
      ? {
          latitude: location.lat,
          longitude: location.lng,
        }
      : {};
    checkInMutation.mutate(payload);
  }, [location, checkInMutation]);

  const handleCheckOut = useCallback(() => {
    const payload: CheckOutPayload = location
      ? {
          latitude: location.lat,
          longitude: location.lng,
        }
      : {};
    checkOutMutation.mutate(payload);
  }, [location, checkOutMutation]);

  // Columns
  const columns: GridColDef<StaffAttendance & { staff?: StaffMember }>[] = [
    {
      field: 'staff_id',
      headerName: 'Staff ID',
      width: 150,
      renderCell: (p) =>
        p.row.staff ? `${p.row.staff.first_name} ${p.row.staff.last_name}` : p.row.staff_id,
    },
    {
      field: 'check_in',
      headerName: 'Check In',
      width: 150,
      renderCell: (p) => (p.row.check_in ? format(new Date(p.row.check_in), 'HH:mm') : '--'),
    },
    {
      field: 'check_out',
      headerName: 'Check Out',
      width: 150,
      renderCell: (p) => (p.row.check_out ? format(new Date(p.row.check_out), 'HH:mm') : '--'),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => <Chip label={p.value} size="small" color={statusColors[p.value]} />,
    },
    {
      field: 'created_at',
      headerName: 'Date',
      width: 120,
      renderCell: (p) => format(new Date(p.row.created_at), 'MM/dd/yyyy'),
    },
  ];

  // Calculate attendance stats
  const calculateStats = () => {
    if (!attendanceRecords?.items) return { present: 0, late: 0, absent: 0, onLeave: 0 };

    const stats = { present: 0, late: 0, absent: 0, onLeave: 0 };
    attendanceRecords.items.forEach((record: StaffAttendance) => {
      if (record.status === 'present') stats.present++;
      else if (record.status === 'late') stats.late++;
      else if (record.status === 'absent') stats.absent++;
      else if (record.status === 'on_leave') stats.onLeave++;
    });

    return stats;
  };

  const stats = calculateStats();

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Toolbar sx={{ justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">Staff Attendance</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<CheckInIcon />}
            onClick={() => setCheckInDialogOpen(true)}
          >
            Check In
          </Button>
          <Button
            variant="contained"
            startIcon={<CheckOutIcon />}
            onClick={() => setCheckOutDialogOpen(true)}
          >
            Check Out
          </Button>
        </Box>
      </Toolbar>

      {!location && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          <LocationIcon sx={{ mr: 1 }} />
          Location services not available. Check-in/check-out will proceed without location data.
        </Alert>
      )}

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Present
              </Typography>
              <Typography variant="h4" sx={{ mt: 1, fontWeight: 700, color: 'success.main' }}>
                {stats.present}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Late
              </Typography>
              <Typography variant="h4" sx={{ mt: 1, fontWeight: 700, color: 'warning.main' }}>
                {stats.late}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                Absent
              </Typography>
              <Typography variant="h4" sx={{ mt: 1, fontWeight: 700, color: 'error.main' }}>
                {stats.absent}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                On Leave
              </Typography>
              <Typography variant="h4" sx={{ mt: 1, fontWeight: 700, color: 'text.secondary' }}>
                {stats.onLeave}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
        <DatePicker
          label="Select Date"
          value={selectedDate}
          onChange={(newValue) => setSelectedDate(newValue)}
          sx={{ minWidth: 200 }}
        />
        <TextField
          label="Staff ID"
          placeholder="Search by staff ID"
          value={staffFilter}
          onChange={(e) => setStaffFilter(e.target.value)}
          InputProps={{ startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} /> }}
          sx={{ minWidth: 200 }}
        />
      </Box>

      <Paper sx={{ p: 2 }}>
        <DataGrid
          rows={attendanceRecords?.items ?? []}
          columns={columns}
          loading={attendanceLoading}
          rowSelection={false}
          disableRowSelectionOnClick
          autoHeight
        />
      </Paper>

      {/* Check In Dialog */}
      <Dialog open={checkInDialogOpen} onClose={() => setCheckInDialogOpen(false)}>
        <DialogTitle>Check In</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography>
              You are about to check in. This will record your attendance for today.
            </Typography>
            {location && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocationIcon color="action" />
                <Typography variant="body2" color="text.secondary">
                  Location: Lat {location.lat.toFixed(4)}, Lng {location.lng.toFixed(4)}
                </Typography>
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCheckInDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleCheckIn}
            disabled={checkInMutation.isPending}
          >
            Check In
          </Button>
        </DialogActions>
      </Dialog>

      {/* Check Out Dialog */}
      <Dialog open={checkOutDialogOpen} onClose={() => setCheckOutDialogOpen(false)}>
        <DialogTitle>Check Out</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography>
              You are about to check out. This will complete your attendance record for today.
            </Typography>
            {location && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LocationIcon color="action" />
                <Typography variant="body2" color="text.secondary">
                  Location: Lat {location.lat.toFixed(4)}, Lng {location.lng.toFixed(4)}
                </Typography>
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCheckOutDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleCheckOut}
            disabled={checkOutMutation.isPending}
          >
            Check Out
          </Button>
        </DialogActions>
      </Dialog>
    </LocalizationProvider>
  );
}
