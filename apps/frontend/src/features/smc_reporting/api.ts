import { apiClient } from '../../shared/api/client';

export interface SMCReport {
  id: string;
  report_date: string;
  attendance_count: number;
  financial_summary: string;
  challenges: string;
  resolutions: string;
  created_by: string;
  created_at: string;
}

export interface CreateSMCReportPayload {
  report_date: string;
  attendance_count: number;
  financial_summary: string;
  challenges: string;
  resolutions: string;
}

export async function getSMCReports(): Promise<SMCReport[]> {
  const { data } = await apiClient.get('/smc/reports');
  return data;
}

export async function createSMCReport(payload: CreateSMCReportPayload): Promise<SMCReport> {
  const { data } = await apiClient.post('/smc/reports', payload);
  return data;
}
