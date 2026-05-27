import { apiClient } from '../../shared/api/client';
import type { ListResponse } from '../../shared/types';

export interface FeeSchedule {
  id: string;
  school_id: string;
  class_id: string;
  term_id?: string;
  fee_type: string;
  amount: number;
  due_date: string;
  is_mandatory: boolean;
  is_locked: boolean;
  created_at: string;
}

export interface Payment {
  id: string;
  student_id: string;
  student_name: string;
  fee_schedule_id: string;
  fee_type: string;
  amount_paid: number;
  payment_method: string;
  receipt_number: string;
  status: string;
  payment_date: string;
  recorded_by: string;
}

export interface Scholarship {
  id: string;
  name: string;
  description?: string;
  discount_type: string;
  discount_value: number;
  is_active: boolean;
}

export interface StudentBalance {
  student_id: string;
  student_name: string;
  total_charges: number;
  total_payments: number;
  total_waivers: number;
  balance: number;
}

export interface FinancialDashboard {
  total_expected: number;
  total_collected: number;
  total_outstanding: number;
  collection_rate: number;
}

export interface CreateFeeSchedulePayload {
  class_id: string;
  term_id?: string;
  fee_type: string;
  amount: number;
  due_date: string;
  is_mandatory: boolean;
}

export interface RecordPaymentPayload {
  student_id: string;
  fee_schedule_id: string;
  amount_paid: number;
  payment_method: string;
  notes?: string;
}

export interface CreateScholarshipPayload {
  name: string;
  description?: string;
  discount_type: string;
  discount_value: number;
  is_active: boolean;
}

export async function getFeeSchedules(params?: {
  class_id?: string;
  term_id?: string;
}): Promise<FeeSchedule[]> {
  const { data } = await apiClient.get('/finance/fee-schedules', { params });
  return data;
}

export async function createFeeSchedule(payload: CreateFeeSchedulePayload): Promise<FeeSchedule> {
  const { data } = await apiClient.post('/finance/fee-schedules', payload);
  return data;
}

export async function lockFeeSchedule(id: string): Promise<void> {
  await apiClient.post(`/finance/fee-schedules/${id}/lock`);
}

export async function copyFeeSchedule(
  id: string,
  payload: { term_id: string }
): Promise<FeeSchedule> {
  const { data } = await apiClient.post(`/finance/fee-schedules/copy`, {
    fee_schedule_id: id,
    ...payload,
  });
  return data;
}

export async function getPayments(params?: {
  student_id?: string;
  page?: number;
  per_page?: number;
}): Promise<ListResponse<Payment>> {
  const { data } = await apiClient.get('/finance/payments', { params });
  return data;
}

export async function recordPayment(payload: RecordPaymentPayload): Promise<Payment> {
  const { data } = await apiClient.post('/finance/payments', payload);
  return data;
}

export async function initiateOnlinePayment(payload: RecordPaymentPayload): Promise<{ payment_url: string; reference: string }> {
  const { data } = await apiClient.post('/finance/payments/initiate', payload);
  return data.data;
}

export async function reversePayment(id: string, reason: string): Promise<void> {
  await apiClient.post(`/finance/payments/${id}/reverse`, { reason });
}

export async function getReceipt(receiptNumber: string): Promise<Payment> {
  const { data } = await apiClient.get(`/finance/receipts/${receiptNumber}`);
  return data;
}

export async function getStudentBalance(studentId: string): Promise<StudentBalance> {
  const { data } = await apiClient.get(`/finance/students/${studentId}/balance`);
  return data;
}

export async function getFinancialDashboard(params?: {
  class_id?: string;
  term_id?: string;
}): Promise<FinancialDashboard> {
  const { data } = await apiClient.get('/finance/dashboard', { params });
  return data;
}

export async function getScholarships(): Promise<Scholarship[]> {
  const { data } = await apiClient.get('/finance/scholarships');
  return data;
}

export async function createScholarship(payload: CreateScholarshipPayload): Promise<Scholarship> {
  const { data } = await apiClient.post('/finance/scholarships', payload);
  return data;
}

export async function awardScholarship(scholarshipId: string, studentId: string): Promise<void> {
  await apiClient.post(`/finance/scholarships/${scholarshipId}/award`, { student_id: studentId });
}

export async function exportDebtReport(classId?: string): Promise<{ download_url: string; total_debt: number; student_count: number }> {
  const { data } = await apiClient.get('/finance/export/debt-report', {
    params: { class_id: classId },
  });
  return data.data;
}
