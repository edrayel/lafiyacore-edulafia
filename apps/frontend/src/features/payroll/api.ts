import { apiClient } from '../../shared/api/client';

export interface PayrollRun {
  id: string;
  month: number;
  year: number;
  total_gross: number;
  total_deductions: number;
  total_net: number;
  status: string;
  processed_at: string;
}

export interface Payslip {
  id: string;
  payroll_run_id: string;
  staff_id: string;
  staff_name: string;
  basic_salary: number;
  allowances: number;
  deductions: number;
  net_pay: number;
}

export interface CreatePayrollPayload {
  month: number;
  year: number;
}

export async function getPayrollRuns(params?: { year?: number }): Promise<PayrollRun[]> {
  const { data } = await apiClient.get('/payroll/runs', { params });
  return data;
}

export async function createPayrollRun(payload: CreatePayrollPayload): Promise<PayrollRun> {
  const { data } = await apiClient.post('/payroll/runs', payload);
  return data;
}

export async function processPayrollRun(id: string): Promise<void> {
  await apiClient.post(`/payroll/runs/${id}/process`);
}

export async function getPayslips(runId: string): Promise<Payslip[]> {
  const { data } = await apiClient.get(`/payroll/runs/${runId}/payslips`);
  return data;
}
