import { apiClient } from '../../shared/api/client';

export interface OTPRequestPayload {
  phone: string;
}

export interface OTPVerifyPayload {
  phone: string;
  otp_code: string;
}

export interface OTPRequestResponse {
  message: string;
  data: {
    phone: string;
    sent_via: string;
    expires_in: number;
  };
}

export interface ChildSummary {
  student_id: string;
  first_name: string;
  last_name: string;
  admission_number: string;
  class_name: string | null;
  status: string;
}

export interface AttendanceSummary {
  total_days: number;
  present_days: number;
  absent_days: number;
  late_days: number;
  excused_days: number;
  attendance_rate: number;
}

export interface FinanceSummary {
  student_id: string;
  total_charges: number;
  total_payments: number;
  total_waivers: number;
  balance: number;
  last_payment_date?: string;
}

export interface ParentNotification {
  id: string;
  notification_type: string;
  title: string;
  message: string;
  channel: string;
  priority: string;
  status: string;
  notification_metadata: Record<string, unknown> | null;
  sent_at: string | null;
  delivered_at: string | null;
  read_at: string | null;
  created_at: string;
}

export interface ParentNotificationsListResponse {
  items: ParentNotification[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface ParentAuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  guardian_id: string;
  guardian_name: string;
  children: ChildSummary[];
}

export interface FeedbackPayload {
  feedback_type: 'complaint' | 'suggestion' | 'praise' | 'question';
  subject: string;
  message: string;
  is_anonymous: boolean;
}

export interface FeedbackResponse {
  id: string;
  guardian_id: string;
  school_id: string;
  feedback_type: string;
  subject: string;
  message: string;
  is_anonymous: boolean;
  status: string;
  response: string | null;
  responded_at: string | null;
  created_at: string;
  updated_at: string;
}

export async function requestOTP(payload: OTPRequestPayload): Promise<OTPRequestResponse> {
  const { data } = await apiClient.post<OTPRequestResponse>('/parent/auth/request-otp', payload);
  return data;
}

export async function verifyOTP(payload: OTPVerifyPayload): Promise<ParentAuthResponse> {
  const { data } = await apiClient.post<ParentAuthResponse>('/parent/auth/verify-otp', payload);
  return data;
}

export async function getChildren(): Promise<ChildSummary[]> {
  const { data } = await apiClient.get<ChildSummary[]>('/parent/children');
  return data;
}

export async function getChildAttendance(childId: string): Promise<AttendanceSummary> {
  const { data } = await apiClient.get<AttendanceSummary>(`/parent/children/${childId}/attendance`);
  return data;
}

export async function getChildFinance(childId: string): Promise<FinanceSummary> {
  const { data } = await apiClient.get<FinanceSummary>(`/parent/children/${childId}/finance`);
  return data;
}

export async function getNotifications(): Promise<ParentNotification[]> {
  const { data } = await apiClient.get<ParentNotificationsListResponse | ParentNotification[]>(
    '/parent/notifications'
  );
  return Array.isArray(data) ? data : data.items;
}

export async function submitFeedback(payload: FeedbackPayload): Promise<FeedbackResponse> {
  const { data } = await apiClient.post<FeedbackResponse>('/parent/feedback', payload);
  return data;
}

export async function markNotificationRead(id: string): Promise<ParentNotification> {
  const { data } = await apiClient.patch<ParentNotification>(`/parent/notifications/${id}/read`);
  return data;
}

export interface ExcusalPayload {
  student_id: string;
  absence_date: string;
  reason: string;
  details?: string;
}

export interface AbsenceExcusalResponse {
  id: string;
  student_id: string;
  guardian_id: string;
  absence_date: string;
  reason: string;
  details: string | null;
  status: string;
  reviewed_by: string | null;
  reviewed_at: string | null;
  review_notes: string | null;
  created_at: string;
  updated_at: string;
}

export async function submitExcusal(payload: ExcusalPayload): Promise<AbsenceExcusalResponse> {
  const { data } = await apiClient.post<AbsenceExcusalResponse>(
    '/parent/children/' + payload.student_id + '/excusal',
    payload
  );
  return data;
}

export interface PaymentInitiatePayload {
  student_id: string;
  amount: number;
  fee_category?: string;
}

export interface PaymentInitiateResponse {
  payment_url: string;
  reference: string;
  gateway: string;
  amount: number;
  status: string;
}

export async function initiateOnlinePayment(
  studentId: string,
  payload: PaymentInitiatePayload
): Promise<PaymentInitiateResponse> {
  const { data } = await apiClient.post<PaymentInitiateResponse>(
    `/parent/children/${studentId}/payment/initiate`,
    payload
  );
  return data;
}

export async function downloadReportCard(studentId: string, termId?: string): Promise<Blob> {
  const { data } = await apiClient.get<Blob>(`/parent/children/${studentId}/report-card/download`, {
    params: { term_id: termId },
    responseType: 'blob',
  });
  return data;
}

export interface DirectMessagePayload {
  recipient_role: string;
  recipient_id?: string;
  subject: string;
  message: string;
}

export async function sendDirectMessage(payload: DirectMessagePayload): Promise<void> {
  await apiClient.post<void>('/parent/messages', payload);
}
