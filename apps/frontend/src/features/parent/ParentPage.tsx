import { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Paper,
  Typography,
  Avatar,
  Badge,
  Tab,
  Tabs,
  TextField,
  Button,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  CheckCircle,
  Error as ErrorIcon,
  School,
  AttachMoney,
  Person,
  EventBusy,
  Feedback as FeedbackIcon,
  TrendingUp,
  CreditCard as PayOnlineIcon,
  Download as DownloadIcon,
  Message as MessageIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getChildren,
  getChildAttendance,
  getChildFinance,
  getNotifications,
  markNotificationRead,
  submitExcusal,
  submitFeedback,
  initiateOnlinePayment,
  downloadReportCard,
  sendDirectMessage,
  type ChildSummary,
  type ExcusalPayload,
  type FeedbackPayload,
  type DirectMessagePayload,
  type ParentNotification,
} from './api';
import { ExcusalDialog } from './ExcusalDialog';
import { FeedbackDialog } from './FeedbackDialog';

const notificationTypeConfig: Record<
  string,
  { icon: typeof NotificationsIcon; color: 'info' | 'warning' | 'error' | 'success' }
> = {
  attendance: { icon: School, color: 'info' },
  finance: { icon: AttachMoney, color: 'warning' },
  academic: { icon: TrendingUp, color: 'success' },
  alert: { icon: ErrorIcon, color: 'error' },
  general: { icon: NotificationsIcon, color: 'info' },
};

function ChildCard({ child }: { child: ChildSummary }) {
  const { data: attendance, isLoading: attendanceLoading } = useQuery({
    queryKey: ['parent-attendance', child.student_id],
    queryFn: () => getChildAttendance(child.student_id),
  });

  const { data: finance, isLoading: financeLoading } = useQuery({
    queryKey: ['parent-finance', child.student_id],
    queryFn: () => getChildFinance(child.student_id),
  });

  const presentCount = attendance?.present_days ?? 0;
  const totalCount = attendance?.total_days ?? 0;
  const effectiveRate = totalCount > 0 ? Math.round((presentCount / totalCount) * 100) : 0;

  const outstandingBalance = finance?.balance ?? 0;

  const pendingCount = outstandingBalance > 0 ? 1 : 0;
  const overdueCount = 0; // Not available in summary

  return (
    <Card>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: 'primary.main' }} alt={`${child.first_name} ${child.last_name}`}>
            {child.first_name[0]}
            {child.last_name[0]}
          </Avatar>
        }
        title={`${child.first_name} ${child.last_name}`}
        subheader={`${child.class_name ?? '—'} • ${child.admission_number}`}
      />
      <Divider />
      <CardContent>
        <Grid container spacing={2}>
          <Grid size={{ xs: 6 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <TrendingUp color="success" />
              <Box>
                <Typography variant="caption" color="textSecondary">
                  Attendance
                </Typography>
                <Typography variant="h6">
                  {attendanceLoading ? <CircularProgress size={16} /> : `${effectiveRate}%`}
                </Typography>
              </Box>
            </Box>
          </Grid>
          <Grid size={{ xs: 6 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AttachMoney
                color={overdueCount > 0 ? 'error' : pendingCount > 0 ? 'warning' : 'success'}
              />
              <Box>
                <Typography variant="caption" color="textSecondary">
                  Balance
                </Typography>
                <Typography variant="h6">
                  {financeLoading ? (
                    <CircularProgress size={16} />
                  ) : (
                    `₦${outstandingBalance.toLocaleString()}`
                  )}
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>
        {finance && outstandingBalance > 0 && (
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {pendingCount > 0 && (
              <Chip
                label={`${pendingCount} Pending`}
                color="warning"
                size="small"
                variant="outlined"
              />
            )}
            {overdueCount > 0 && (
              <Chip
                label={`${overdueCount} Overdue`}
                color="error"
                size="small"
                variant="outlined"
              />
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

function NotificationsPanel({
  notifications,
  isLoading,
}: {
  notifications: ParentNotification[];
  isLoading: boolean;
}) {
  const queryClient = useQueryClient();

  const markReadMutation = useMutation({
    mutationFn: markNotificationRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parent-notifications'] });
    },
  });

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!notifications.length) {
    return (
      <Typography color="textSecondary" sx={{ p: 4, textAlign: 'center' }}>
        No notifications
      </Typography>
    );
  }

  return (
    <List>
      {notifications.map((notification) => {
        const metadata = notification.notification_metadata;
        const studentName =
          metadata && typeof metadata.student_name === 'string' ? metadata.student_name : undefined;

        const isRead = notification.status === 'read' || Boolean(notification.read_at);
        const config =
          notificationTypeConfig[notification.notification_type] || notificationTypeConfig.general;
        const Icon = config.icon;

        return (
          <ListItem
            key={notification.id}
            secondaryAction={
              !isRead && (
                <IconButton
                  edge="end"
                  size="small"
                  aria-label="Mark as read"
                  onClick={() => markReadMutation.mutate(notification.id)}
                >
                  <CheckCircle color="success" fontSize="small" />
                </IconButton>
              )
            }
            sx={{
              bgcolor: isRead ? 'transparent' : 'action.hover',
              borderRadius: 1,
              mb: 0.5,
            }}
          >
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: `${config.color}.main` }}>
                <Icon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {notification.title}
                  {studentName && (
                    <Chip label={studentName} size="small" variant="outlined" />
                  )}
                </Box>
              }
              secondary={
                <>
                  {notification.message}
                  <br />
                  <Typography component="span" variant="caption" color="textSecondary">
                    {new Date(notification.created_at).toLocaleDateString()}
                  </Typography>
                </>
              }
            />
          </ListItem>
        );
      })}
    </List>
  );
}

export function ParentPage() {
  const [tab, setTab] = useState(0);
  const queryClient = useQueryClient();
  const [excusalOpen, setExcusalOpen] = useState(false);
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [selectedChild, setSelectedChild] = useState<ChildSummary | null>(null);
  const [excusalForm, setExcusalForm] = useState<Partial<ExcusalPayload>>({});
  const [feedbackForm, setFeedbackForm] = useState<Partial<FeedbackPayload>>({
    feedback_type: 'complaint',
    is_anonymous: false,
  });

  const [paymentOpen, setPaymentOpen] = useState(false);
  const [paymentAmount, setPaymentAmount] = useState<number | ''>('');

  const [messageOpen, setMessageOpen] = useState(false);
  const [messageForm, setMessageForm] = useState<Partial<DirectMessagePayload>>({
    recipient_role: 'teacher',
  });

  const { data: children, isLoading: childrenLoading } = useQuery({
    queryKey: ['parent-children'],
    queryFn: getChildren,
  });

  const { data: notifications, isLoading: notificationsLoading } = useQuery({
    queryKey: ['parent-notifications'],
    queryFn: getNotifications,
  });

  const unreadCount =
    notifications?.filter((n) => n.status !== 'read' && !n.read_at).length ?? 0;

  const excusalMutation = useMutation({
    mutationFn: submitExcusal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parent-children'] });
      setExcusalOpen(false);
      setExcusalForm({});
    },
  });

  const feedbackMutation = useMutation({
    mutationFn: submitFeedback,
    onSuccess: () => {
      setFeedbackOpen(false);
      setFeedbackForm({ feedback_type: 'complaint', is_anonymous: false });
    },
  });

  const paymentMutation = useMutation({
    mutationFn: ({ studentId, amount }: { studentId: string; amount: number }) =>
      initiateOnlinePayment(studentId, { student_id: studentId, amount }),
    onSuccess: (data) => {
      setPaymentOpen(false);
      setPaymentAmount('');
      if (data?.payment_url) {
        window.open(data.payment_url, '_blank');
      }
    },
  });

  const downloadReportMutation = useMutation({
    mutationFn: (studentId: string) => downloadReportCard(studentId),
    onSuccess: (data) => {
      const url = URL.createObjectURL(data);
      window.open(url, '_blank');
      window.setTimeout(() => URL.revokeObjectURL(url), 10_000);
    },
  });

  const messageMutation = useMutation({
    mutationFn: sendDirectMessage,
    onSuccess: () => {
      setMessageOpen(false);
      setMessageForm({ recipient_role: 'teacher' });
    },
  });

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Parent Portal
        </Typography>
      </Box>

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab icon={<Person />} label="Children" iconPosition="start" />
        <Tab
          icon={
            <Badge badgeContent={unreadCount} color="error">
              <NotificationsIcon />
            </Badge>
          }
          label="Notifications"
          iconPosition="start"
        />
        <Tab icon={<EventBusy />} label="Excusals" iconPosition="start" />
        <Tab icon={<FeedbackIcon />} label="Feedback" iconPosition="start" />
      </Tabs>

      {tab === 0 && (
        <>
          {childrenLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : children && children.length > 0 ? (
            <Grid container spacing={3}>
              {children.map((child) => (
                <Grid size={{ xs: 12, md: 6 }} key={child.student_id}>
                  <ChildCard child={child} />
                  <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Button
                      variant="outlined"
                      startIcon={<EventBusy />}
                      onClick={() => {
                        setSelectedChild(child);
                        setExcusalForm({ student_id: child.student_id });
                        setExcusalOpen(true);
                      }}
                    >
                      Absence
                    </Button>
                    <Button
                      variant="outlined"
                      color="warning"
                      startIcon={<PayOnlineIcon />}
                      onClick={() => {
                        setSelectedChild(child);
                        setPaymentOpen(true);
                      }}
                    >
                      Pay Fees
                    </Button>
                    <Button
                      variant="outlined"
                      color="success"
                      startIcon={<DownloadIcon />}
                      onClick={() => downloadReportMutation.mutate(child.student_id)}
                      disabled={downloadReportMutation.isPending}
                    >
                      Report Card
                    </Button>
                    <Button
                      variant="outlined"
                      color="info"
                      startIcon={<MessageIcon />}
                      onClick={() => {
                        setSelectedChild(child);
                        setMessageOpen(true);
                      }}
                    >
                      Message Staff
                    </Button>
                  </Box>
                </Grid>
              ))}
            </Grid>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography color="textSecondary">No children linked to your account</Typography>
            </Paper>
          )}
        </>
      )}

      {tab === 1 && (
        <Paper>
          <NotificationsPanel
            notifications={notifications ?? []}
            isLoading={notificationsLoading}
          />
        </Paper>
      )}

      {tab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Submit Absence Excusal
          </Typography>
          <Button variant="contained" onClick={() => setExcusalOpen(true)}>
            Open Excusal Form
          </Button>
        </Paper>
      )}

      {tab === 3 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Submit Feedback
          </Typography>
          <Button variant="contained" color="warning" onClick={() => setFeedbackOpen(true)}>
            Open Feedback Form
          </Button>
        </Paper>
      )}

      <ExcusalDialog
        open={excusalOpen}
        onClose={() => setExcusalOpen(false)}
        excusalForm={excusalForm}
        setExcusalForm={setExcusalForm}
        onSubmit={() => {
          if (!excusalForm.student_id || !excusalForm.reason || !excusalForm.absence_date) return;
          excusalMutation.mutate({
            student_id: excusalForm.student_id,
            reason: excusalForm.reason,
            absence_date: excusalForm.absence_date,
            details: excusalForm.details,
          });
        }}
        isPending={excusalMutation.isPending}
      />

      <FeedbackDialog
        open={feedbackOpen}
        onClose={() => setFeedbackOpen(false)}
        feedbackForm={feedbackForm}
        setFeedbackForm={setFeedbackForm}
        onSubmit={() => {
          if (!feedbackForm.feedback_type || !feedbackForm.subject || !feedbackForm.message) return;
          feedbackMutation.mutate({
            feedback_type: feedbackForm.feedback_type,
            subject: feedbackForm.subject,
            message: feedbackForm.message,
            is_anonymous: Boolean(feedbackForm.is_anonymous),
          });
        }}
        isPending={feedbackMutation.isPending}
      />

      <Dialog open={paymentOpen} onClose={() => setPaymentOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Pay Fees for {selectedChild?.first_name}</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Enter the amount you wish to pay online via our secure payment gateway.
          </Typography>
          <TextField
            label="Amount (₦)"
            type="number"
            fullWidth
            value={paymentAmount}
            onChange={(e) => setPaymentAmount(e.target.value ? Number(e.target.value) : '')}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPaymentOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            disabled={!paymentAmount || paymentMutation.isPending || !selectedChild}
            onClick={() => {
              if (!selectedChild) return;
              paymentMutation.mutate({
                studentId: selectedChild.student_id,
                amount: paymentAmount as number,
              });
            }}
          >
            {paymentMutation.isPending ? 'Processing...' : 'Pay Online'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={messageOpen} onClose={() => setMessageOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Message Staff regarding {selectedChild?.first_name}</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Send a direct message to a teacher or administrator.
          </Typography>
          <FormControl fullWidth>
            <InputLabel>Recipient Role</InputLabel>
            <Select
              value={messageForm.recipient_role ?? 'teacher'}
              label="Recipient Role"
              onChange={(e) => setMessageForm((f) => ({ ...f, recipient_role: e.target.value }))}
            >
              <MenuItem value="teacher">Form Teacher</MenuItem>
              <MenuItem value="admin">School Administrator</MenuItem>
              <MenuItem value="nurse">School Nurse</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="Subject"
            fullWidth
            value={messageForm.subject ?? ''}
            onChange={(e) => setMessageForm((f) => ({ ...f, subject: e.target.value }))}
          />
          <TextField
            label="Message"
            fullWidth
            multiline
            rows={4}
            value={messageForm.message ?? ''}
            onChange={(e) => setMessageForm((f) => ({ ...f, message: e.target.value }))}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setMessageOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            disabled={!messageForm.subject || !messageForm.message || messageMutation.isPending}
            onClick={() => messageMutation.mutate(messageForm as DirectMessagePayload)}
          >
            {messageMutation.isPending ? 'Sending...' : 'Send Message'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
