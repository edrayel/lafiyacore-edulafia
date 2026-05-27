import { useState } from 'react';
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
  Typography,
} from '@mui/material';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { Add as AddIcon, Check as CheckIcon, Close as CloseIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getLeaveRequests,
  createLeaveRequest,
  approveLeave,
  rejectLeave,
  type LeaveRequest,
  type CreateLeavePayload,
} from './api';

const statusColor: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
  approved: 'success',
  pending: 'warning',
  rejected: 'error',
};

export function LeavePage() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<CreateLeavePayload>>({ leave_type: 'annual' });
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['leaveRequests'],
    queryFn: () => getLeaveRequests(),
  });

  const create = useMutation({
    mutationFn: (p: CreateLeavePayload) => createLeaveRequest(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leaveRequests'] });
      setOpen(false);
      setForm({ leave_type: 'annual' });
    },
  });
  const approve = useMutation({
    mutationFn: approveLeave,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leaveRequests'] }),
  });
  const reject = useMutation({
    mutationFn: (id: string) => rejectLeave(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leaveRequests'] }),
  });

  const columns: GridColDef<LeaveRequest>[] = [
    { field: 'staff_name', headerName: 'Staff', width: 180 },
    { field: 'leave_type', headerName: 'Type', width: 120 },
    {
      field: 'start_date',
      headerName: 'Start',
      width: 120,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'end_date',
      headerName: 'End',
      width: 120,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value} size="small" color={statusColor[p.value] ?? 'default'} />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 120,
      sortable: false,
      renderCell: (p) =>
        p.row.status === 'pending' ? (
          <Box sx={{ display: 'flex', gap: 0.5 }}>
            <Button aria-label="Approve" size="small" onClick={() => approve.mutate(p.row.id)}>
              <CheckIcon fontSize="small" />
            </Button>
            <Button
              aria-label="Reject"
              size="small"
              color="error"
              onClick={() => reject.mutate(p.row.id)}
            >
              <CloseIcon fontSize="small" />
            </Button>
          </Box>
        ) : null,
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Leave Management
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
            onClick={() => setOpen(true)}
          >
            New Request
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
          rows={data ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(r) => r.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[10, 25, 50]}
          slots={{ noRowsOverlay: () => <DataEmptyState title="No leave requests found" message="There are no leave requests to display at this time." /> }}
        />
      </Paper>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>New Leave Request</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Staff ID"
            value={form.staff_id ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, staff_id: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Leave Type</InputLabel>
            <Select
              value={form.leave_type ?? 'annual'}
              label="Leave Type"
              onChange={(e) => setForm((f) => ({ ...f, leave_type: e.target.value }))}
            >
              <MenuItem value="annual">Annual</MenuItem>
              <MenuItem value="sick">Sick</MenuItem>
              <MenuItem value="maternity">Maternity</MenuItem>
              <MenuItem value="emergency">Emergency</MenuItem>
              <MenuItem value="unpaid">Unpaid</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Start Date"
            type="date"
            value={form.start_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, start_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End Date"
            type="date"
            value={form.end_date ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, end_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Reason"
            value={form.reason ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, reason: e.target.value }))}
            fullWidth
            multiline
            rows={2}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(form as CreateLeavePayload)}
            variant="contained"
            disabled={create.isPending}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
