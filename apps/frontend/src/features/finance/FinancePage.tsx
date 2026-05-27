import { useState } from 'react';
import {
  Box,
  Button,
  Chip,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Tab,
  Tabs,
  Toolbar,
  Typography,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import {
  Add as AddIcon,
  Lock as LockIcon,
  ContentCopy as CopyIcon,
  Receipt as ReceiptIcon,
  School as SchoolIcon,
  AttachMoney as MoneyIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  Undo as ReversalIcon,
  CreditCard as PayOnlineIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getFeeSchedules,
  lockFeeSchedule,
  copyFeeSchedule,
  getPayments,
  getFinancialDashboard,
  getScholarships,
  exportDebtReport,
  type FeeSchedule,
  type Payment,
  type Scholarship,
} from './api';

import { ReceiptView } from './ReceiptView';
import { CreateFeeScheduleDialog } from './components/CreateFeeScheduleDialog';
import { RecordPaymentDialog } from './components/RecordPaymentDialog';
import { InitiateOnlinePaymentDialog } from './components/InitiateOnlinePaymentDialog';
import { ReversePaymentDialog } from './components/ReversePaymentDialog';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { useTabState } from '@/shared/hooks/useTabState';
import { AddScholarshipDialog } from './components/AddScholarshipDialog';

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

export function FinancePage() {
  const [tab, setTab] = useTabState('tab');
  const queryClient = useQueryClient();
  const [classFilter, setClassFilter] = useState('');
  const [feeDialogOpen, setFeeDialogOpen] = useState(false);
  const [paymentDialogOpen, setPaymentDialogOpen] = useState(false);
  const [selectedPayment, setSelectedPayment] = useState<Payment | null>(null);
  const [receiptDialogOpen, setReceiptDialogOpen] = useState(false);
  const [scholarshipDialogOpen, setScholarshipDialogOpen] = useState(false);
  const [reversalDialogOpen, setReversalDialogOpen] = useState(false);
  const [onlinePaymentDialogOpen, setOnlinePaymentDialogOpen] = useState(false);
  const [paymentsPaginationModel, setPaymentsPaginationModel] = useState({ page: 0, pageSize: 25 });

  const { data: feeSchedules, isLoading: feesLoading } = useQuery({
    queryKey: ['feeSchedules', classFilter],
    queryFn: () => getFeeSchedules({ class_id: classFilter || undefined }),
  });

  const { data: payments, isLoading: paymentsLoading } = useQuery({
    queryKey: [
      'payments',
      { page: paymentsPaginationModel.page, per_page: paymentsPaginationModel.pageSize },
    ],
    queryFn: () =>
      getPayments({
        page: paymentsPaginationModel.page + 1,
        per_page: paymentsPaginationModel.pageSize,
      }),
  });

  const { data: dashboard } = useQuery({
    queryKey: ['financialDashboard', classFilter],
    queryFn: () => getFinancialDashboard({ class_id: classFilter || undefined }),
  });

  const { data: scholarships } = useQuery({
    queryKey: ['scholarships'],
    queryFn: getScholarships,
  });

  const lockFee = useMutation({
    mutationFn: lockFeeSchedule,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['feeSchedules'] }),
  });

  const copyFee = useMutation({
    mutationFn: (id: string) => copyFeeSchedule(id, { term_id: 'next' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['feeSchedules'] }),
  });

  const exportDebtMutation = useMutation({
    mutationFn: () => exportDebtReport(classFilter || undefined),
    onSuccess: (data) => {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `debt_report_${classFilter || 'all'}_${new Date().getTime()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    },
  });

  const feeColumns: GridColDef<FeeSchedule>[] = [
    { field: 'fee_type', headerName: 'Fee Type', width: 180 },
    { field: 'class_id', headerName: 'Class', width: 100 },
    { field: 'amount', headerName: 'Amount', width: 140, valueGetter: (v: number) => fmt(v) },
    {
      field: 'due_date',
      headerName: 'Due Date',
      width: 130,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'is_mandatory',
      headerName: 'Mandatory',
      width: 110,
      renderCell: (p) => (
        <Chip label={p.value ? 'Yes' : 'No'} size="small" color={p.value ? 'success' : 'default'} />
      ),
    },
    {
      field: 'is_locked',
      headerName: 'Status',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value ? 'Locked' : 'Open'}
          size="small"
          color={p.value ? 'error' : 'success'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 160,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          {!p.row.is_locked && (
            <Button aria-label="Lock" size="small" onClick={() => lockFee.mutate(p.row.id)}>
              <LockIcon fontSize="small" />
            </Button>
          )}
          {!p.row.is_locked && (
            <Button aria-label="Copy" size="small" onClick={() => copyFee.mutate(p.row.id)}>
              <CopyIcon fontSize="small" />
            </Button>
          )}
        </Box>
      ),
    },
  ];

  const paymentColumns: GridColDef<Payment>[] = [
    { field: 'student_name', headerName: 'Student', width: 200 },
    { field: 'fee_type', headerName: 'Fee Type', width: 140 },
    { field: 'amount_paid', headerName: 'Amount', width: 140, valueGetter: (v: number) => fmt(v) },
    { field: 'payment_method', headerName: 'Method', width: 110 },
    { field: 'receipt_number', headerName: 'Receipt #', width: 160 },
    {
      field: 'payment_date',
      headerName: 'Date',
      width: 130,
      valueGetter: (v: string) => new Date(v).toLocaleDateString(),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 110,
      renderCell: (p) => (
        <Chip
          label={p.value}
          size="small"
          color={p.value === 'confirmed' ? 'success' : 'warning'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 180,
      sortable: false,
      renderCell: (p) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            size="small"
            onClick={() => {
              setSelectedPayment(p.row);
              setReceiptDialogOpen(true);
            }}
          >
            Receipt
          </Button>
          {p.row.status === 'confirmed' && (
            <Button
              size="small"
              color="error"
              onClick={() => {
                setSelectedPayment(p.row);
                setReversalDialogOpen(true);
              }}
            >
              <ReversalIcon fontSize="small" />
            </Button>
          )}
        </Box>
      ),
    },
  ];

  const scholarshipColumns: GridColDef<Scholarship>[] = [
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'description', headerName: 'Description', width: 250 },
    { field: 'discount_type', headerName: 'Type', width: 120 },
    {
      field: 'discount_value',
      headerName: 'Value',
      width: 100,
      valueGetter: (v: number) => `${v}%`,
    },
    {
      field: 'is_active',
      headerName: 'Status',
      width: 100,
      renderCell: (p) => (
        <Chip
          label={p.value ? 'Active' : 'Inactive'}
          size="small"
          color={p.value ? 'success' : 'default'}
        />
      ),
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Finance
        </Typography>
      </Box>

      {dashboard && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <StatCard
              title="Total Expected"
              value={fmt(dashboard.total_expected)}
              icon={<SchoolIcon />}
              color="primary.main"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <StatCard
              title="Total Collected"
              value={fmt(dashboard.total_collected)}
              icon={<MoneyIcon />}
              color="success.main"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <StatCard
              title="Outstanding"
              value={fmt(dashboard.total_outstanding)}
              icon={<WarningIcon />}
              color="error.main"
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6, md: 3 }}>
            <StatCard
              title="Collection Rate"
              value={`${dashboard.collection_rate}%`}
              icon={<TrendingUpIcon />}
              color="info.main"
            />
            <Button
              fullWidth
              variant="outlined"
              startIcon={<DownloadIcon />}
              sx={{ mt: 2 }}
              onClick={() => exportDebtMutation.mutate()}
              disabled={exportDebtMutation.isPending}
            >
              {exportDebtMutation.isPending ? 'Exporting...' : 'Export Debt Report'}
            </Button>
          </Grid>
        </Grid>
      )}

      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Fee Schedules" />
          <Tab label="Payments" />
          <Tab label="Scholarships" />
        </Tabs>
      </Paper>

      {tab === 0 && (
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
              <FormControl size="small" sx={{ minWidth: 180 }}>
                <InputLabel>Class</InputLabel>
                <Select
                  value={classFilter}
                  label="Class"
                  onChange={(e) => setClassFilter(e.target.value)}
                >
                  <MenuItem value="">All Classes</MenuItem>
                  <MenuItem value="jss1">JSS 1</MenuItem>
                  <MenuItem value="jss2">JSS 2</MenuItem>
                  <MenuItem value="jss3">JSS 3</MenuItem>
                  <MenuItem value="ss1">SS 1</MenuItem>
                  <MenuItem value="ss2">SS 2</MenuItem>
                  <MenuItem value="ss3">SS 3</MenuItem>
                </Select>
              </FormControl>
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
                onClick={() => setFeeDialogOpen(true)}
              >
                Add Fee Schedule
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
              rows={feeSchedules ?? []}
              columns={feeColumns}
              loading={feesLoading}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No fee schedules found" message="There are no fee schedules to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {tab === 1 && (
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
            <Toolbar>
              <Box sx={{ flexGrow: 1 }} />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="outlined"
                  startIcon={<PayOnlineIcon />}
                  onClick={() => setOnlinePaymentDialogOpen(true)}
                >
                  Pay Online
                </Button>
                <Button
                  variant="contained"
                  startIcon={<ReceiptIcon />}
                  onClick={() => setPaymentDialogOpen(true)}
                >
                  Record Payment
                </Button>
              </Box>
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
              rows={payments?.items ?? []}
              columns={paymentColumns}
              loading={paymentsLoading}
              rowCount={payments?.total ?? 0}
              paginationMode="server"
              paginationModel={paymentsPaginationModel}
              onPaginationModelChange={setPaymentsPaginationModel}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No payments found" message="There are no payments to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {tab === 2 && (
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
                onClick={() => setScholarshipDialogOpen(true)}
              >
                Add Scholarship
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
              rows={scholarships ?? []}
              columns={scholarshipColumns}
              getRowId={(r) => r.id}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              pageSizeOptions={[10, 25, 50]}
              slots={{ noRowsOverlay: () => <DataEmptyState title="No scholarships found" message="There are no scholarships to display at this time." /> }}
            />
          </Paper>
        </>
      )}

      {/* Dialogs extracted */}
      <CreateFeeScheduleDialog open={feeDialogOpen} onClose={() => setFeeDialogOpen(false)} />
      <RecordPaymentDialog open={paymentDialogOpen} onClose={() => setPaymentDialogOpen(false)} />
      <InitiateOnlinePaymentDialog
        open={onlinePaymentDialogOpen}
        onClose={() => setOnlinePaymentDialogOpen(false)}
      />
      <ReversePaymentDialog
        open={reversalDialogOpen}
        onClose={() => setReversalDialogOpen(false)}
        payment={selectedPayment}
      />
      <AddScholarshipDialog
        open={scholarshipDialogOpen}
        onClose={() => setScholarshipDialogOpen(false)}
      />

      <ReceiptView
        open={receiptDialogOpen}
        onClose={() => setReceiptDialogOpen(false)}
        payment={selectedPayment}
      />
    </>
  );
}
